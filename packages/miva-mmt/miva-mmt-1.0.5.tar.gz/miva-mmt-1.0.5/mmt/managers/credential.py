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

Prefix         : MMT-MANAGERS-CREDENTIAL-
Next Error Code: 1
"""

import abc
import typing


class Credential( abc.ABC ):
	def __init__( self, key: str, url: str, http_basic_auth_username: typing.Optional[ str ], http_basic_auth_password: typing.Optional[ str ] ):
		self._key						= key
		self._url						= url
		self._http_basic_auth_username	= http_basic_auth_username
		self._http_basic_auth_password	= http_basic_auth_password

	@property
	@abc.abstractmethod
	def method( self ) -> str:
		raise NotImplementedError

	@property
	def key( self ) -> str:
		return self._key

	@property
	def url( self ) -> str:
		return self._url

	@property
	def http_basic_auth_username( self ) -> typing.Optional[ str ]:
		return self._http_basic_auth_username

	@property
	def http_basic_auth_password( self ) -> typing.Optional[ str ]:
		return self._http_basic_auth_password

	@key.setter
	def key( self, key: str ):
		self._key = key

	@url.setter
	def url( self, url: str ):
		self._url = url

	@http_basic_auth_username.setter
	def http_basic_auth_username( self, http_basic_auth_username: typing.Optional[ str ] ):
		self._http_basic_auth_username = http_basic_auth_username

	@http_basic_auth_password.setter
	def http_basic_auth_password( self, http_basic_auth_password: typing.Optional[ str ] ):
		self._http_basic_auth_password = http_basic_auth_password

	def is_token( self ) -> bool:
		return isinstance( self, CredentialToken )

	def is_ssh( self ) -> bool:
		return isinstance( self, CredentialSSH )


class CredentialToken( Credential ):
	def __init__( self, key: str, url: str, token: str, signing_key: str, http_basic_auth_username: typing.Optional[ str ], http_basic_auth_password: typing.Optional[ str ] ):
		super().__init__( key, url, http_basic_auth_username, http_basic_auth_password )

		self._token			= token
		self._signing_key	= signing_key

	@property
	def method( self ) -> str:
		return 'Token'

	@property
	def token( self ) -> str:
		return self._token

	@property
	def signing_key( self ) -> str:
		return self._signing_key

	@token.setter
	def token( self, token: str ):
		self._token = token

	@signing_key.setter
	def signing_key( self, signing_key: str ):
		self._signing_key = signing_key


class CredentialSSH( Credential ):
	def __init__( self, key: str, url: str, username: str, filepath: str, http_basic_auth_username: typing.Optional[ str ], http_basic_auth_password: typing.Optional[ str ] ):
		super().__init__( key, url, http_basic_auth_username, http_basic_auth_password )

		self._username = username
		self._filepath = filepath

	@property
	def method( self ) -> str:
		return 'SSH'

	@property
	def username( self ) -> str:
		return self._username

	@property
	def filepath( self ) -> str:
		return self._filepath

	@username.setter
	def username( self, username: str ):
		self._username = username

	@filepath.setter
	def filepath( self, filepath: str ):
		self._filepath = filepath


class CredentialManager:
	def __init__( self ):
		self._credentials = {}

	def add_token( self, key: str, url: str, token: str, signing_key: str, http_basic_auth_username: typing.Optional[ str ], http_basic_auth_password: typing.Optional[ str ] ) -> CredentialToken:
		self._credentials[ key ] = CredentialToken( key, url, token, signing_key, http_basic_auth_username, http_basic_auth_password )

		return self._credentials[ key ]

	def add_ssh( self, key: str, url: str, username: str, filepath: str, http_basic_auth_username: typing.Optional[ str ], http_basic_auth_password: typing.Optional[ str ] ) -> CredentialSSH:
		self._credentials[ key ] = CredentialSSH( key, url, username, filepath, http_basic_auth_username, http_basic_auth_password )

		return self._credentials[ key ]

	def update_token( self, credential: CredentialToken, key: typing.Optional[ str ] = None, url: typing.Optional[ str ] = None, token: typing.Optional[ str ] = None, signing_key: typing.Optional[ str ] = None, http_basic_auth_username: typing.Optional[ str ] = None, http_basic_auth_password: typing.Optional[ str ] = None ) -> CredentialToken:
		original_key = credential.key

		if key is not None:
			credential.key = key

		if url is not None:
			credential.url = url

		if token is not None:
			credential.token = token

		if signing_key is not None:
			credential.signing_key = signing_key

		if original_key != credential.key:
			del self._credentials[ original_key ]
			self._credentials[ credential.key ] = credential

		if http_basic_auth_username is not None:
			if len( http_basic_auth_username ) == 0:
				credential.http_basic_auth_username = None
			else:
				credential.http_basic_auth_username = http_basic_auth_username

		if http_basic_auth_password is not None:
			if len( http_basic_auth_password ) == 0:
				credential.http_basic_auth_password = None
			else:
				credential.http_basic_auth_password = http_basic_auth_password

		return credential

	def update_ssh( self, credential: CredentialSSH, key: typing.Optional[ str ] = None, url: typing.Optional[ str ] = None, username: typing.Optional[ str ] = None, filepath: typing.Optional[ str ] = None, http_basic_auth_username: typing.Optional[ str ] = None, http_basic_auth_password: typing.Optional[ str ] = None ) -> CredentialSSH:
		original_key = credential.key

		if key is not None:
			credential.key = key

		if url is not None:
			credential.url = url

		if username is not None:
			credential.username = username

		if filepath is not None:
			credential.filepath = filepath

		if original_key != credential.key:
			del self._credentials[ original_key ]
			self._credentials[ credential.key ] = credential

		if http_basic_auth_username is not None:
			if len( http_basic_auth_username ) == 0:
				credential.http_basic_auth_username = None
			else:
				credential.http_basic_auth_username = http_basic_auth_username

		if http_basic_auth_password is not None:
			if len( http_basic_auth_password ) == 0:
				credential.http_basic_auth_password = None
			else:
				credential.http_basic_auth_password = http_basic_auth_password

		return credential

	def delete( self, key: str ):
		try:
			del self._credentials[ key ]
		except KeyError:
			pass

	def lookup( self, key: str ) -> typing.Optional[ typing.Union[ CredentialToken, CredentialSSH ] ]:
		return self._credentials.get( key )

	@property
	def credentials( self ) -> typing.List[ typing.Union[ CredentialToken, CredentialSSH ] ]:
		return [ credential for credential in self._credentials.values() ]
