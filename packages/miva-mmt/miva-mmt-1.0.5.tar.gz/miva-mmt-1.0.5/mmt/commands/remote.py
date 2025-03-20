"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2020 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-COMMAND-REMOTE-
Next Error Code: 12
"""

from mmt.exceptions import Error
from mmt.commands import Command


class RemoteListCommand( Command ):
	def run( self ):
		for i, remote in enumerate( self.configmanager.remotes ):
			if i > 0:
				print( '' )

			print( remote.key )
			print( f'\tCredential Key: {remote.credential_key}' )
			print( f'\tStore Code: {remote.store_code}' )
			print( f'\tBranch Name: { remote.branch_name}' )


class RemoteAddCommand( Command ):
	def validate( self ):
		if self.configmanager.remote_lookup( self.args.get( 'key' ) ) is not None:
			raise Error( 'MMT-COMMAND-REMOTE-00001', f'Remote key \'{self.args.get( "key" )}\' already exists' )

		if self.configmanager.credential_lookup( self.args.get( 'credential_key' ) ) is None:
			raise Error( 'MMT-COMMAND-REMOTE-00002', f'Credential key \'{self.args.get( "credential_key" )}\' does not exist' )

		if len( self.args.get( 'store_code' ) ) == 0:
			raise Error( 'MMT-COMMAND-REMOTE-00003', 'A Store Code value is required' )

		if len( self.args.get( 'branch_name' ) ) == 0:
			raise Error( 'MMT-COMMAND-REMOTE-00004', 'A Branch Name value is required' )

	def run( self ):
		self.configmanager.remote_add( self.args.get( 'key' ), self.args.get( 'credential_key' ), self.args.get( 'store_code' ), self.args.get( 'branch_name' ) )
		self.configmanager.save()


class RemoteUpdateCommand( Command ):
	def validate( self ):
		if self.configmanager.remote_lookup( self.args.get( 'key' ) ) is None:
			raise Error( 'MMT-COMMAND-REMOTE-00005', f'Remote key \'{self.args.get( "key" )}\' does not exist' )

		if self.args.get( 'remote_key' ) is not None and self.args.get( 'remote_key' ) != self.args.get( 'key' ):
			if self.configmanager.remote_lookup( self.args.get( 'remote_key' ) ) is not None:
				raise Error( 'MMT-COMMAND-REMOTE-00006', f'Remote key \'{self.args.get( "remote_key" )}\' already exists' )

		if self.args.get( 'credential_key' ) is not None:
			if self.configmanager.credential_lookup( self.args.get( 'credential_key' ) ) is None:
				raise Error( 'MMT-COMMAND-REMOTE-00007', f'Credential key \'{self.args.get( "credential_key" )}\' does not exist' )

		if self.args.get( 'remote_key', '' ) is not None and len( self.args.get( 'remote_key' ) ) == 0:
			raise Error( 'MMT-COMMAND-REMOTE-00008', 'Remote key cannot be blank' )

		if self.args.get( 'store_code' ) is not None and len( self.args.get( 'store_code' ) ) == 0:
			raise Error( 'MMT-COMMAND-REMOTE-00009', 'Store code cannot be blank' )

		if self.args.get( 'branch_name' ) is not None and len( self.args.get( 'branch_name' ) ) == 0:
			raise Error( 'MMT-COMMAND-REMOTE-00010', 'Branch name cannot be blank' )

	def run( self ):
		remote = self.configmanager.remote_lookup( self.args.get( 'key' ) )

		self.configmanager.remote_update( remote, self.args.get( 'remote_key' ), self.args.get( 'credential_key' ), self.args.get( 'store_code' ), self.args.get( 'branch_name' ) )
		self.configmanager.save()

class RemoteDeleteCommand( Command ):
	def run( self ):
		for key in self.args.get( 'key' ):
			self.configmanager.remote_delete( key )

		self.configmanager.save()
