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

Prefix         : MMT-METADATA-
Next Error Code: 2
"""

import os
import abc
import json

from mmt.exceptions import Error


class MetadataFile( abc.ABC ):
	def __init__( self, directory: str, filename: str ):
		self._directory	= directory
		self._filepath	= os.path.join( directory, filename )

	def read( self ):
		with open( self._filepath, 'r' ) as fh:
			try:
				self._deserialize( json.load( fh ) )
			except json.decoder.JSONDecodeError as e:
				raise Error( 'MMT-METADATA-00001', f'Failed to parse \'{self._filepath}\': {e}' )

	def save( self ):
		with open( self._filepath, 'w' ) as fh:
			json.dump( self._serialize(), fh, indent = 4 )

	@abc.abstractmethod
	def _serialize( self ) -> dict:
		raise NotImplementedError

	@abc.abstractmethod
	def _deserialize( self, data: dict ):
		raise NotImplementedError

	@property
	def directory( self ) -> str:
		return self._directory

	@property
	def filepath( self ) -> str:
		return self._filepath
