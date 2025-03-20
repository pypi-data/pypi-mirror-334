"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2024 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-METADATA-LOCALCONFIG-
Next Error Code: 4
"""

import typing

from mmt.exceptions import Error
from mmt.metadata.config import ConfigMetadataFile


class LocalConfigMetadataFile( ConfigMetadataFile ):
	def __init__( self, metadata_directory: str ):
		super().__init__( metadata_directory )

		self._version						= 2
		self._remote_key					= ''
		self._branch_id						= 0
		self._branch_name					= ''
		self._branch_key					= ''
		self._branch_tags					= []
		self._ignore_unsynced_templates		= False
		self._ignore_unsynced_properties	= False
		self._include_hidden_settings		= False

	def _serialize( self ) -> dict:
		data									= {}
		data[ 'version' ]						= self._version
		data[ 'remote_key' ]					= self.remote_key
		data[ 'ignore_unsynced_templates' ]		= self.ignore_unsynced_templates
		data[ 'ignore_unsynced_properties' ]	= self.ignore_unsynced_properties
		data[ 'include_hidden_settings' ]		= self.include_hidden_settings
		data[ 'branch_id' ]						= self.branch_id
		data[ 'branch_name' ]					= self.branch_name
		data[ 'branch_key' ]					= self.branch_key
		data[ 'branch_tags' ]					= self.branch_tags

		return data

	def _deserialize( self, data: dict ):
		version = data.get( 'version' )

		if version == 1:
			try:
				self.remote_key					= data[ 'remote_key' ]
				self.ignore_unsynced_templates	= data[ 'ignore_unsynced_templates' ]
				self.ignore_unsynced_properties	= data[ 'ignore_unsynced_properties' ]
				self.include_hidden_settings	= True
				self.branch_id					= data[ 'branch_id' ]
				self.branch_name				= data[ 'branch_name' ]
				self.branch_key					= data[ 'branch_key' ]
				self.branch_tags				= data[ 'branch_tags' ]
			except KeyError as e:
				raise Error( 'MMT-METADATA-LOCALCONFIG-00001', f'Invalid configuration file: Missing {str( e )}' )
			else:
				return
		elif version == 2:
			try:
				self.remote_key					= data[ 'remote_key' ]
				self.ignore_unsynced_templates	= data[ 'ignore_unsynced_templates' ]
				self.ignore_unsynced_properties	= data[ 'ignore_unsynced_properties' ]
				self.include_hidden_settings	= data[ 'include_hidden_settings' ]
				self.branch_id					= data[ 'branch_id' ]
				self.branch_name				= data[ 'branch_name' ]
				self.branch_key					= data[ 'branch_key' ]
				self.branch_tags				= data[ 'branch_tags' ]
			except KeyError as e:
				raise Error( 'MMT-METADATA-LOCALCONFIG-00003', f'Invalid configuration file: Missing {str( e )}' )
			else:
				return

		raise Error( 'MMT-METADATA-LOCALCONFIG-00002', 'Unknown file version' )

	@property
	def remote_key( self ) -> str:
		return self._get._remote_key

	@property
	def ignore_unsynced_templates( self ) -> bool:
		return self._get._ignore_unsynced_templates

	@property
	def ignore_unsynced_properties( self ) -> bool:
		return self._get._ignore_unsynced_properties

	@property
	def include_hidden_settings( self ) -> bool:
		return self._get._include_hidden_settings

	@property
	def branch_id( self ) -> int:
		return self._get._branch_id

	@property
	def branch_name( self ) -> str:
		return self._get._branch_name

	@property
	def branch_key( self ) -> str:
		return self._get._branch_key

	@property
	def branch_tags( self ) -> typing.List[ str ]:
		return self._get._branch_tags

	@remote_key.setter
	def remote_key( self, remote_key: str ):
		self._set._remote_key = remote_key

	@ignore_unsynced_templates.setter
	def ignore_unsynced_templates( self, ignore_unsynced_templates: bool ):
		self._set._ignore_unsynced_templates = ignore_unsynced_templates

	@ignore_unsynced_properties.setter
	def ignore_unsynced_properties( self, ignore_unsynced_properties: bool ):
		self._set._ignore_unsynced_properties = ignore_unsynced_properties

	@include_hidden_settings.setter
	def include_hidden_settings( self, include_hidden_settings: bool ):
		self._set._include_hidden_settings = include_hidden_settings

	@branch_id.setter
	def branch_id( self, branch_id: int ):
		self._set._branch_id = branch_id

	@branch_name.setter
	def branch_name( self, branch_name: str ):
		self._set._branch_name = branch_name

	@branch_key.setter
	def branch_key( self, branch_key: str ):
		self._set._branch_key = branch_key

	@branch_tags.setter
	def branch_tags( self, branch_tags: [ str ] ):
		self._set._branch_tags = branch_tags
