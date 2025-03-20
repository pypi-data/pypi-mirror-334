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

Prefix         : MMT-MANAGERS-REMOTE-
Next Error Code: 1
"""

import typing


class Remote:
	def __init__( self, key: str, credential_key: str, store_code: str, branch_name: str ):
		self._key				= key
		self._credential_key	= credential_key
		self._store_code		= store_code
		self._branch_name		= branch_name

	@property
	def key( self ) -> str:
		return self._key

	@property
	def credential_key( self ) -> str:
		return self._credential_key

	@property
	def store_code( self ) -> str:
		return self._store_code

	@property
	def branch_name( self ) -> str:
		return self._branch_name

	@key.setter
	def key( self, key: str ):
		self._key = key

	@credential_key.setter
	def credential_key( self, credential_key: str ):
		self._credential_key = credential_key

	@store_code.setter
	def store_code( self, store_code: str ):
		self._store_code = store_code

	@branch_name.setter
	def branch_name( self, branch_name: str ):
		self._branch_name = branch_name


class RemoteManager:
	def __init__( self ):
		self._remotes = {}

	def add( self, key: str, credential_key: str, store_code: str, branch_name: str ) -> Remote:
		self._remotes[ key ] = Remote( key, credential_key, store_code, branch_name )

		return self._remotes[ key ]

	def update( self, remote: Remote, key: typing.Optional[ str ] = None, credential_key: typing.Optional[ str ] = None, store_code: typing.Optional[ str ] = None, branch_name: typing.Optional[ str ] = None ) -> Remote:
		original_key = remote.key

		if key is not None:
			remote.key = key

		if credential_key is not None:
			remote.credential_key = credential_key

		if store_code is not None:
			remote.store_code = store_code

		if branch_name is not None:
			remote.branch_name = branch_name

		if original_key != remote.key:
			del self._remotes[ original_key ]
			self._remotes[ remote.key ] = remote

		return remote

	def delete( self, key: str ):
		try:
			del self._remotes[ key ]
		except KeyError:
			pass

	def lookup( self, key: str ) -> typing.Optional[ Remote ]:
		return self._remotes.get( key )

	@property
	def remotes( self ) -> typing.List[ Remote ]:
		return [ remote for remote in self._remotes.values() ]
