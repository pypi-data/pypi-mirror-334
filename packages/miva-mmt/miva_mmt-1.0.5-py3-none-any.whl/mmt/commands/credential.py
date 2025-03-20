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

Prefix         : MMT-COMMAND-CREDENTIALS-
Next Error Code: 22
"""

import os
import getpass

from mmt.exceptions import Error
from mmt.commands import Command


def _prompt_for_http_basic_auth_password() -> str:
	password = ''

	try:
		password = getpass.getpass( 'Please enter the HTTP Basic Authentication Password: ' )
	except KeyboardInterrupt:
		print( '' )
		quit()

	return password


class CredentialListCommand( Command ):
	def run( self ):
		for i, credential in enumerate( self.configmanager.credentials ):
			if i > 0:
				print( '' )

			print( credential.key )
			print( f'\tMethod: {credential.method}' )
			print( f'\tURL: {credential.url}' )

			if credential.is_token():
				print( f'\tToken: {credential.token}' )
			elif credential.is_ssh():
				print( f'\tUsername: {credential.username}' )
				print( f'\tFilepath: {credential.filepath}' )

			if credential.http_basic_auth_username is not None and credential.http_basic_auth_password is not None:
				print( f'\tHTTP Basic Authentication Username: {credential.http_basic_auth_username}' )
				print( f'\tHTTP Basic Authentication Password: **********' )


class CredentialAddCommand( Command ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		self._is_token	= False
		self._is_ssh	= False

	def validate( self ):
		if self.configmanager.credential_lookup( self.args.get( 'key' ) ) is not None:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00001', f'Credential key \'{self.args.get( "key" )}\' already exists' )

		if len( self.args.get( 'url' ) ) == 0:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00002', 'A URL value is required' )

		token			= self.args.get( 'token' )
		signing_key		= self.args.get( 'signing_key' )
		ssh_username	= self.args.get( 'ssh_username' )
		ssh_private_key	= self.args.get( 'ssh_private_key' )

		self._is_token	= token is not None or signing_key is not None
		self._is_ssh	= ssh_username is not None or ssh_private_key is not None

		if not self._is_token and not self._is_ssh:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00012', 'One of token authentication or SSH authentication is required' )
		elif self._is_token and self._is_ssh:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00013', 'Only one of token authentication or SSH authentication is allowed' )

		if self._is_token:
			if token is None or len( token ) == 0:
				raise Error( 'MMT-COMMAND-CREDENTIALS-00003', 'An API Token value is required' )

			if signing_key is None or len( signing_key ) == 0:
				raise Error( 'MMT-COMMAND-CREDENTIALS-00004', 'An API Signing Key value is required' )

		if self._is_ssh:
			if ssh_username is None or len( ssh_username ) == 0:
				raise Error( 'MMT-COMMAND-CREDENTIALS-00014', 'An SSH Username value is required' )

			if ssh_private_key is None or len( ssh_private_key ) == 0:
				raise Error( 'MMT-COMMAND-CREDENTIALS-00015', 'An SSH Private Key value is required' )
			elif not os.path.exists( os.path.expanduser( ssh_private_key ) ):
				raise Error( 'MMT-COMMAND-CREDENTIALS-00016', 'SSH Private Key does not exist' )

		if self.args.get( 'http_basic_auth_username' ) is not None and len( self.args.get( 'http_basic_auth_username' ) ) != 0:
			if self.args.get( 'http_basic_auth_password' ) is None:
				self.args[ 'http_basic_auth_password' ] = _prompt_for_http_basic_auth_password()

	def run( self ):
		if self._is_token:
			self.configmanager.credential_add_token( self.args.get( 'key' ), self.args.get( 'url' ), self.args.get( 'token' ), self.args.get( 'signing_key' ), self.args.get( 'http_basic_auth_username' ), self.args.get( 'http_basic_auth_password' ) )
			self.configmanager.save()
		elif self._is_ssh:
			self.configmanager.credential_add_ssh( self.args.get( 'key' ), self.args.get( 'url' ), self.args.get( 'ssh_username' ), os.path.abspath( os.path.expanduser( self.args.get( 'ssh_private_key' ) ) ), self.args.get( 'http_basic_auth_username' ), self.args.get( 'http_basic_auth_password' ) )
			self.configmanager.save()


class CredentialUpdateCommand( Command ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		self._is_token	= False
		self._is_ssh	= False

	def validate( self ):
		credential = self.configmanager.credential_lookup( self.args.get( 'key' ) )

		if credential is None:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00005', f'Credential key \'{self.args.get( "key" )}\' does not exist' )

		if self.args.get( 'credential_key' ) is not None and self.args.get( 'credential_key' ) != self.args.get( 'key' ):
			if self.configmanager.credential_lookup( self.args.get( 'credential_key' ) ) is not None:
				raise Error( 'MMT-COMMAND-CREDENTIALS-00011', f'Credential key \'{self.args.get( "credential_key" )}\' already exists' )

		if self.args.get( 'url' ) is not None:
			if len( self.args.get( 'url' ) ) == 0:
				raise Error( 'MMT-COMMAND-CREDENTIALS-00006', 'A URL value is required' )

		token			= self.args.get( 'token' )
		signing_key		= self.args.get( 'signing_key' )
		ssh_username	= self.args.get( 'ssh_username' )
		ssh_private_key	= self.args.get( 'ssh_private_key' )

		self._is_token	= token is not None or signing_key is not None
		self._is_ssh	= ssh_username is not None or ssh_private_key is not None

		if self._is_token and self._is_ssh:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00017', 'Only one of token authentication or SSH authentication is allowed' )

		if ( self._is_token and not credential.is_token() ) or ( self._is_ssh and not credential.is_ssh() ):
			raise Error( 'MMT-COMMAND-CREDENTIALS-00018', 'Cannot switch a credential between token and SSH authentication' )

		if self._is_token:
			if token is not None:
				if len( token ) == 0:
					raise Error( 'MMT-COMMAND-CREDENTIALS-00007', 'An API Token value is required' )

			if signing_key is not None:
				if len( signing_key ) == 0:
					raise Error( 'MMT-COMMAND-CREDENTIALS-00008', 'An API Signing Key value is required' )

		if self._is_ssh:
			if ssh_username is not None:
				if len( ssh_username ) == 0:
					raise Error( 'MMT-COMMAND-CREDENTIALS-00019', 'An SSH Username value is required' )

			if ssh_private_key is not None:
				if len( ssh_private_key ) == 0:
					raise Error( 'MMT-COMMAND-CREDENTIALS-00020', 'An SSH Private Key value is required' )
				elif not os.path.exists( os.path.expanduser( ssh_private_key ) ):
					raise Error( 'MMT-COMMAND-CREDENTIALS-00021', 'SSH Private Key does not exist' )

		if self.args.get( 'http_basic_auth_username' ) is not None and len( self.args.get( 'http_basic_auth_username' ) ) != 0:
			if self.args.get( 'http_basic_auth_password' ) is None:
				self.args[ 'http_basic_auth_password' ] = _prompt_for_http_basic_auth_password()

	def run( self ):
		credential = self.configmanager.credential_lookup( self.args.get( 'key' ) )

		if credential.is_token():
			self.configmanager.credential_update_token( credential, self.args.get( 'credential_key' ), self.args.get( 'url' ), self.args.get( 'token' ), self.args.get( 'signing_key' ), self.args.get( 'http_basic_auth_username' ), self.args.get( 'http_basic_auth_password' ) )
			self.configmanager.save()
		elif credential.is_ssh():
			ssh_private_key = self.args.get( 'ssh_private_key' )

			if ssh_private_key is not None:
				ssh_private_key = os.path.abspath( os.path.expanduser( self.args.get( 'ssh_private_key' ) ) )

			self.configmanager.credential_update_ssh( credential, self.args.get( 'credential_key' ), self.args.get( 'url' ), self.args.get( 'ssh_username' ), ssh_private_key, self.args.get( 'http_basic_auth_username' ), self.args.get( 'http_basic_auth_password' ) )
			self.configmanager.save()

class CredentialDeleteCommand( Command ):
	def validate( self ):
		if self.configmanager.credential_lookup( self.args.get( 'key' ) ) is None:
			raise Error( 'MMT-COMMAND-CREDENTIALS-00009', f'Credential key \'{self.args.get( "key" ) }\' does not exist' )

	def run( self ):
		self.configmanager.credential_delete( self.args.get( 'key' ) )
		self.configmanager.save()
