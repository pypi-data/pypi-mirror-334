"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2025 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-COMMAND-BRANCH-
Next Error Code: 14
"""

import merchantapi.request
import merchantapi.model

from mmt.exceptions import Error
from mmt.commands import Command


class BranchListCommand( Command ):
	def validate( self ):
		if self.configmanager.credential_lookup( self.args.get( 'credential_key' ) ) is None:
			raise Error( 'MMT-COMMAND-BRANCH-00001', f'Credential key \'{self.args.get( "credential_key" )}\' does not exist' )

		if self.args.get( 'store_code' ) is None or len( self.args.get( 'store_code' ) ) == 0:
			raise Error( 'MMT-COMMAND-BRANCH-00002', 'A Store Code is required' )

	def run( self ):
		request = merchantapi.request.BranchListLoadQuery()
		request.set_sort( 'name' )

		response = self.send_request_lowlevel( request, self.args.get( 'credential_key' ), self.args.get( 'store_code' ) )

		for i, branch in enumerate( response.get_branches() ):
			if i > 0:
				print( '' )

			print( f'Branch: {branch.get_name()}' )
			print( f'\tIs Primary: {branch.get_is_primary()}' )
			print( f'\tIs Working: {branch.get_is_working()}' )
			print( f'\tPreview URL: {branch.get_preview_url()}' )


class BranchCreateCommand( Command ):
	def validate( self ):
		if self.args.get( 'remote_key' ) is not None:
			if len( self.args.get( 'remote_key' ) ) == 0:
				raise Error( 'MMT-COMMAND-BRANCH-00012', 'A Remote Key is required' )

			if self.configmanager.remote_lookup( self.args.get( 'remote_key' ) ) is None:
				raise Error( 'MMT-COMMAND-BRANCH-00005', f'Remote key \'{self.args.get( "remote_key" )}\' does not exist' )
		else:
			if self.args.get( 'credential_key' ) is None or len( self.args.get( 'credential_key' ) ) == 0:
				raise Error( 'MMT-COMMAND-BRANCH-00006', f'A Credential Key is required' )

			if self.configmanager.credential_lookup( self.args.get( 'credential_key' ) ) is None:
				raise Error( 'MMT-COMMAND-BRANCH-00007', f'Credential key \'{self.args.get( "credential_key" )}\' does not exist' )

			if self.args.get( 'store_code' ) is None or len( self.args.get( 'store_code' ) ) == 0:
				raise Error( 'MMT-COMMAND-BRANCH-00008', 'A Store Code is required' )

			if self.args.get( 'from' ) is None or len( self.args.get( 'from' ) ) == 0:
				raise Error( 'MMT-COMMAND-BRANCH-00009', 'A From value is required' )

	def run( self ):
		if self.args.get( 'remote_key' ) is None:
			parent_branch_name	= self.args.get( 'from' )
			credential_key		= self.args.get( 'credential_key' )
			store_code			= self.args.get( 'store_code' )
		else:
			remote				= self.configmanager.remote_lookup( self.args.get( 'remote_key' ) )
			parent_branch_name	= remote.branch_name
			credential_key		= remote.credential_key
			store_code			= remote.store_code

		parent_branch_id = self._load_branch( parent_branch_name, credential_key, store_code ).get_id()

		request = merchantapi.request.BranchCreate()
		request.set_parent_branch_id( parent_branch_id )
		request.set_name( self.args.get( 'name' ) )
		request.set_color( self.args.get( 'color' ) )

		while True:
			response = self.send_request_lowlevel( request, credential_key = credential_key, store_code = store_code )

			# Account for Merchant version less than 10.10 by checking for
			# the presence of completed in the response

			if 'completed' not in response.data or response.get_completed():
				branch = response.get_branch()
				break

			if len( response.get_branch_create_session_id() ) == 0:
				raise Error( 'MMT-COMMAND-BRANCH-00014', 'Expected a valid session id' )

			request.set_branch_create_session_id( response.get_branch_create_session_id() )

		print( f'Branch \'{branch.get_name()}\' created' )

	def _load_branch( self, branch_name: str, credential_key: str, store_code: str ) -> merchantapi.model.Branch:
		request	= merchantapi.request.BranchListLoadQuery()
		request.set_count( 1 )
		request.set_filters( request.filter_expression().equal( 'name', branch_name ) )

		response = self.send_request_lowlevel( request, credential_key, store_code )
		branches = response.get_branches()

		if len( branches ) != 1:
			raise Error( 'MMT-COMMAND-BRANCH-00003', f'Branch \'{branch_name}\' does not exist' )

		return branches[ 0 ]


class BranchDeleteCommand( Command ):
	def validate( self ):
		if self.configmanager.credential_lookup( self.args.get( 'credential_key' ) ) is None:
			raise Error( 'MMT-COMMAND-BRANCH-00010', f'Credential key \'{self.args.get( "credential_key" )}\' does not exist' )

		if self.args.get( 'store_code' ) is None or len( self.args.get( 'store_code' ) ) == 0:
			raise Error( 'MMT-COMMAND-BRANCH-00011', 'A Store Code is required' )

	def run( self ):
		request = merchantapi.request.BranchDelete()
		request.set_branch_name( self.args.get( 'name' ) )

		self.send_request_lowlevel( request, self.args.get( 'credential_key' ), self.args.get( 'store_code' ) )

		print( f'Branch \'{self.args.get( "name" )}\' deleted' )
