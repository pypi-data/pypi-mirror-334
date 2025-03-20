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

Prefix         : MMT-MANAGERS-CONFIG-
Next Error Code: 1
"""

from mmt.metadata.globalconfig import GlobalConfigMetadataFile
from mmt.metadata.localconfig import LocalConfigMetadataFile


class ConfigManager:
	def __init__( self, global_metadata_directory: str, local_metadata_directory: str ):
		self.__dict__[ '_globalconfig' ]	= GlobalConfigMetadataFile( global_metadata_directory )
		self.__dict__[ '_localconfig' ]		= LocalConfigMetadataFile( local_metadata_directory )

	def __getattr__( self, name ):
		if hasattr( self._globalconfig, name ):
			return getattr( self._globalconfig, name )

		if hasattr( self._localconfig, name ):
			return getattr( self._localconfig, name )

		raise AttributeError( f'Attribute \'{name}\' is not a global or local configuration setting' )

	def __setattr__( self, name, value ):
		if hasattr( self._globalconfig, name ):
			return setattr( self._globalconfig, name, value )

		if hasattr( self._localconfig, name ):
			return setattr( self._localconfig, name, value )

		raise AttributeError( f'Attribute \'{name}\' is not a global or local configuration setting' )

	def save( self ):
		self._globalconfig.save()
		self._localconfig.save()
