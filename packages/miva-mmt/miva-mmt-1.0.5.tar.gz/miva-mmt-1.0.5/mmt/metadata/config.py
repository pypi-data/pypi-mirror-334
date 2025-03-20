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

Prefix         : MMT-METADATA-CONFIG-
Next Error Code: 4
"""

import os
import abc

from mmt.exceptions import Error
from mmt.metadata import MetadataFile


class ConfigMetadataFile( MetadataFile, abc.ABC ):
	def __init__( self, metadata_directory: str ):
		self._loaded	= False
		self._modified	= False

		super().__init__( metadata_directory, 'config.json' )

	def save( self ):
		if self._modified:
			super().save()

	@property
	def _get( self ):
		if self._loaded:
			return self

		self._loaded = True

		try:
			self.read()
		except FileNotFoundError:
			pass
		except Exception as e:
			raise Error( 'MMT-METADATA-CONFIG-00001', f'Configuration error: Failed to read metadata file: {str( e )}' )

		return self

	@property
	def _set( self ):
		if self._modified:
			return self

		self._modified = True

		try:
			os.mkdir( self.directory )
		except FileExistsError:
			pass
		except Exception as e:
			raise Error( 'MMT-METADATA-CONFIG-00002', f'Configuration error: Failed to create metadata directory: {str( e )}' )

		if not self._loaded:
			self._loaded = True

			try:
				self.read()
			except FileNotFoundError:
				pass
			except Exception as e:
				raise Error( 'MMT-METADATA-CONFIG-00003', f'Configuration error: Failed to read metadata file: {str( e )}' )

		return self
