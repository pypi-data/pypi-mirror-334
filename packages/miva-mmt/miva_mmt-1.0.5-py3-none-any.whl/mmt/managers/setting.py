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

Prefix         : MMT-MANAGERS-SETTING-
Next Error Code: 1
"""

import typing


class Setting:
	def __init__( self, key: str, value: typing.Any ):
		self._key	= key
		self._value	= value

	@property
	def key( self ) -> str:
		return self._key

	@property
	def value( self ) -> typing.Any:
		return self._value


class SettingManager:
	def __init__( self ):
		self._settings = {}

	def set( self, key: str, value: typing.Any ) -> Setting:
		self._settings[ key ] = Setting( key, value )

		return self._settings[ key ]

	def delete( self, key: str ):
		try:
			del self._settings[ key ]
		except KeyError:
			pass

	def lookup( self, key: str ) -> typing.Optional[ Setting ]:
		return self._settings.get( key )

	@property
	def settings( self ) -> typing.List[ Setting ]:
		return [ setting for setting in self._settings.values() ]
