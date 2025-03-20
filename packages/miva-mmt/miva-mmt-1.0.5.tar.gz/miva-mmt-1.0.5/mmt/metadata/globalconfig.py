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

Prefix         : MMT-METADATA-GLOBALCONFIG-
Next Error Code: 4
"""

import typing

from mmt.exceptions import Error
from mmt.metadata.config import ConfigMetadataFile
from mmt.managers.remote import Remote, RemoteManager
from mmt.managers.credential import CredentialToken, CredentialSSH, CredentialManager
from mmt.managers.setting import Setting, SettingManager


class GlobalConfigMetadataFile( ConfigMetadataFile ):
	def __init__( self, metadata_directory: str ):
		super().__init__( metadata_directory )

		self._version			= 2
		self._settingsmanager	= SettingManager()
		self._credentialmanager	= CredentialManager()
		self._remotemanager		= RemoteManager()

	def _serialize( self ) -> dict:
		data					= {}
		data[ 'version' ]		= self._version
		data[ 'settings' ]		= {}
		data[ 'credentials' ]	= {}
		data[ 'remotes' ]		= {}

		for setting in self._settingsmanager.settings:
			data[ 'settings' ][ setting.key ] = setting.value

		for credential in self._credentialmanager.credentials:
			if credential.is_token():
				entry								= {}
				entry[ 'url' ]						= credential.url
				entry[ 'token' ]					= credential.token
				entry[ 'signing_key' ]				= credential.signing_key
				entry[ 'http_basic_auth_username' ]	= credential.http_basic_auth_username
				entry[ 'http_basic_auth_password' ]	= credential.http_basic_auth_password
			elif credential.is_ssh():
				entry								= {}
				entry[ 'url' ]						= credential.url
				entry[ 'username' ]					= credential.username
				entry[ 'filepath' ]					= credential.filepath
				entry[ 'http_basic_auth_username' ]	= credential.http_basic_auth_username
				entry[ 'http_basic_auth_password' ]	= credential.http_basic_auth_password
			else:
				continue

			data[ 'credentials' ][ credential.key ]	= entry

		for remote in self._remotemanager.remotes:
			entry							= {}
			entry[ 'credential_key' ]		= remote.credential_key
			entry[ 'store_code' ]			= remote.store_code
			entry[ 'branch_name' ]			= remote.branch_name

			data[ 'remotes' ][ remote.key ]	= entry

		return data

	def _deserialize( self, data: dict ):
		version = data.get( 'version' )

		if version == 1:
			try:
				for key, value in data.get( 'settings', {} ).items():
					self._settingsmanager.set( key, value )

				for key, value in data.get( 'credentials', {} ).items():
					if value.get( 'token' ) is not None:
						self._credentialmanager.add_token( key, value[ 'url' ], value[ 'token' ], value[ 'signing_key' ], None, None )
					elif value.get( 'username' ) is not None:
						self._credentialmanager.add_ssh( key, value[ 'url' ], value[ 'username' ], value[ 'filepath' ], None, None )

				for key, value in data.get( 'remotes', {} ).items():
					self._remotemanager.add( key, value[ 'credential_key' ], value[ 'store_code' ], value[ 'branch_name' ] )
			except KeyError as e:
				raise Error( 'MMT-METADATA-GLOBALCONFIG-00001', f'Invalid configuration file: Missing {str( e )}' )
			else:
				return
		elif version == 2:
			try:
				for key, value in data.get( 'settings', {} ).items():
					self._settingsmanager.set( key, value )

				for key, value in data.get( 'credentials', {} ).items():
					if value.get( 'token' ) is not None:
						self._credentialmanager.add_token( key, value[ 'url' ], value[ 'token' ], value[ 'signing_key' ], value[ 'http_basic_auth_username' ], value[ 'http_basic_auth_password' ] )
					elif value.get( 'username' ) is not None:
						self._credentialmanager.add_ssh( key, value[ 'url' ], value[ 'username' ], value[ 'filepath' ], value[ 'http_basic_auth_username' ], value[ 'http_basic_auth_password' ] )

				for key, value in data.get( 'remotes', {} ).items():
					self._remotemanager.add( key, value[ 'credential_key' ], value[ 'store_code' ], value[ 'branch_name' ] )
			except KeyError as e:
				raise Error( 'MMT-METADATA-GLOBALCONFIG-00003', f'Invalid configuration file: Missing {str( e )}' )
			else:
				return

		raise Error( 'MMT-METADATA-GLOBALCONFIG-00002', 'Unknown file version' )

	def setting_lookup( self, *args, **kwargs ) -> typing.Optional[ Setting ]:
		return self._get._settingsmanager.lookup( *args, **kwargs )

	def setting_set( self, *args, **kwargs ) -> Setting:
		return self._set._settingsmanager.set( *args, **kwargs )

	def setting_delete( self, *args, **kwargs ):
		return self._set._settingsmanager.delete( *args, **kwargs )

	def credential_lookup( self, *args, **kwargs ) -> typing.Optional[ typing.Union[ CredentialToken, CredentialSSH ] ]:
		return self._get._credentialmanager.lookup( *args, **kwargs )

	def credential_add_token( self, *args, **kwargs ) -> CredentialToken:
		return self._set._credentialmanager.add_token( *args, **kwargs )

	def credential_add_ssh( self, *args, **kwargs ) -> CredentialSSH:
		return self._set._credentialmanager.add_ssh( *args, **kwargs )

	def credential_update_token( self, *args, **kwargs ) -> CredentialToken:
		return self._set._credentialmanager.update_token( *args, **kwargs )

	def credential_update_ssh( self, *args, **kwargs ) -> CredentialSSH:
		return self._set._credentialmanager.update_ssh( *args, **kwargs )

	def credential_delete( self, *args, **kwargs ):
		return self._set._credentialmanager.delete( *args, **kwargs )

	def remote_lookup( self, *args, **kwargs ) -> typing.Optional[ Remote ]:
		return self._get._remotemanager.lookup( *args, **kwargs )

	def remote_add( self, *args, **kwargs ) -> Remote:
		return self._set._remotemanager.add( *args, **kwargs )

	def remote_update( self, *args, **kwargs ) -> Remote:
		return self._set._remotemanager.update( *args, **kwargs )

	def remote_delete( self, *args, **kwargs ):
		return self._set._remotemanager.delete( *args, **kwargs )

	@property
	def credentials( self ) -> typing.List[ typing.Union[ CredentialToken, CredentialSSH ] ]:
		return self._get._credentialmanager.credentials

	@property
	def remotes( self ) -> typing.List[ Remote ]:
		return self._get._remotemanager.remotes
