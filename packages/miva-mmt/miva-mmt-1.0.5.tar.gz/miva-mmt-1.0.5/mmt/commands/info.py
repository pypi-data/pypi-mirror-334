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

Prefix         : MMT-COMMAND-INFO-
Next Error Code: 1
"""

from mmt.commands import ConfiguredCommand


class InfoCommand( ConfiguredCommand ):
	def run( self ):
		remote				= self.load_remote( self.configmanager.remote_key )
		credential			= self.load_credential( remote.credential_key )
		changeset			= self.state.changeset
		branch_tags			= self.build_branch_tags() if len( self.configmanager.branch_tags ) > 0 else '<None>'

		print( 'Remote' )
		print( f'\tKey: {remote.key}' )
		print( f'\tStore Code: {remote.store_code}' )
		print( f'\tBranch Name: {remote.branch_name}' )
		print( '' )

		print( 'Credential' )
		print( f'\tKey: {remote.credential_key}' )
		print( f'\tURL: {credential.url}' )
		print( f'\tMethod: {credential.method}' )

		if credential.is_token():
			print( f'\tToken: {credential.token}' )
		elif credential.is_ssh():
			print( f'\tUsername: {credential.username}' )
			print( f'\tFilepath: {credential.filepath}' )

		print( '' )

		print( 'Branch' )
		print( f'\tName: {remote.branch_name}' )
		print( f'\tKey: {self.configmanager.branch_key}' )
		print( f'\tTags: {branch_tags}' )
		print( '' )

		print( 'Changeset' )
		print( f'\tID: {changeset.id}' )
		print( f'\tUsername: {changeset.username}' )
		print( f'\tNotes: {changeset.notes}' )
