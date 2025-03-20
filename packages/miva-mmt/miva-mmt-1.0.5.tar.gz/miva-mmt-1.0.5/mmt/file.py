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

Prefix         : MMT-MANAGERS-FILE
Next Error Code: 1
"""

import os
import typing
import hashlib


class File:
	def __init__( self, filepath: str ):
		self._filepath		= filepath
		self._sha256_hash	= None

	def exists( self ) -> bool:
		return os.path.exists( self._filepath )

	def read( self ) -> str:
		try:
			with open( self._filepath, 'r', newline = '' ) as fh:
				return fh.read()
		except FileNotFoundError:
			return ''

	def write( self, data: str, encoding = 'utf-8' ):
		self._sha256_hash = hashlib.sha256( data.encode( encoding ) ).hexdigest()

		with open( self._filepath, 'w', newline = '', encoding = encoding ) as fh:
			fh.write( data )

	def delete( self ):
		try:
			os.remove( self._filepath )
			self._sha256_hash = None
		except FileNotFoundError:
			pass

	@property
	def sha256_hash( self ) -> typing.Optional[ str ]:
		if self._sha256_hash is None:
			sha256 = hashlib.sha256()

			try:
				with open( self._filepath, 'rb' ) as fh:
					for block in iter( lambda: fh.read( 4096 ), b'' ):
						sha256.update( block )
			except FileNotFoundError:
				return None

			self._sha256_hash = sha256.hexdigest()

		return self._sha256_hash

	@property
	def filepath( self ) -> str:
		return self._filepath


class BinaryFile( File ):
	def read( self ) -> bytes:
		try:
			with open( self._filepath, 'rb' ) as fh:
				return fh.read()
		except FileNotFoundError:
			return b''

	def write( self, data: bytes ):
		self._sha256_hash = hashlib.sha256( data ).hexdigest()

		with open( self._filepath, 'wb' ) as fh:
			fh.write( data )
