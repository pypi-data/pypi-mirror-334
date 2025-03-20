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

Prefix         : MMT-METADATA-STATE-
Next Error Code: 11
"""

import os
import abc
import typing

from mmt.exceptions import Error
from mmt.metadata import MetadataFile
from mmt.file import File, BinaryFile


class StateMetadataChangeset:
	def __init__( self, _id: int, username: str, notes: str ):
		self._id		= _id
		self._username	= username
		self._notes		= notes

	@property
	def id( self ) -> int:
		return self._id

	@property
	def username( self ) -> str:
		return self._username

	@property
	def notes( self ) -> str:
		return self._notes

	@id.setter
	def id( self, _id: int ):
		self._id = _id

	@username.setter
	def username( self, username: str ):
		self._username = username

	@notes.setter
	def notes( self, notes: str ):
		self._notes = notes


class StateMetadataEntryFile( abc.ABC ):
	def __init__( self, root_directory: str, filepath: str, sha256_hash: typing.Optional[ str ] = None ):
		self._filepath		= filepath
		self._sha256_hash	= sha256_hash
		self._file			= self.file_type()( os.path.join( root_directory, filepath ) )

	@abc.abstractmethod
	def file_type( self ):
		raise NotImplementedError

	@property
	def filepath( self ):
		return self._filepath

	@property
	def sha256_hash( self ) -> typing.Optional[ str ]:
		return self._sha256_hash

	@sha256_hash.setter
	def sha256_hash( self, sha256_hash ):
		self._sha256_hash = sha256_hash

	@property
	def file( self ) -> File:
		return self._file

	def is_template( self ) -> bool:
		return isinstance( self, StateMetadataBaseTemplateFile )

	def is_template_file( self ) -> bool:
		return isinstance( self, StateMetadataTemplateFile )

	def is_template_settings_file( self ) -> bool:
		return isinstance( self, StateMetadataTemplateSettingsFile )

	def is_property( self ) -> bool:
		return isinstance( self, StateMetadataBasePropertyFile )

	def is_property_template_file( self ) -> bool:
		return isinstance( self, StateMetadataPropertyTemplateFile )

	def is_property_settings_file( self ) -> bool:
		return isinstance( self, StateMetadataPropertySettingsFile )

	def is_jsresource( self ) -> bool:
		return isinstance( self, StateMetadataBaseJSResourceFile )

	def is_jsresource_settings_file( self ) -> bool:
		return isinstance( self, StateMetadataJSResourceSettingsFile )

	def is_jsresource_js_file( self ) -> bool:
		return isinstance( self, StateMetadataJSResourceJSFile )

	def is_jsresource_template_file( self ) -> bool:
		return isinstance( self, StateMetadataJSResourceTemplateFile )

	def is_cssresource( self ) -> bool:
		return isinstance( self, StateMetadataBaseCSSResourceFile )

	def is_cssresource_settings_file( self ) -> bool:
		return isinstance( self, StateMetadataCSSResourceSettingsFile )

	def is_cssresource_css_file( self ) -> bool:
		return isinstance( self, StateMetadataCSSResourceCSSFile )

	def is_cssresource_template_file( self ) -> bool:
		return isinstance( self, StateMetadataCSSResourceTemplateFile )

	def is_resourcegroup( self ) -> bool:
		return isinstance( self, StateMetadataBaseResourceGroupFile )

	def is_resourcegroup_settings_file( self ) -> bool:
		return isinstance( self, StateMetadataResourceGroupSettingsFile )


class StateMetadataBaseTemplateFile( StateMetadataEntryFile, abc.ABC ):
	def __init__( self, root_directory: str, filepath: str, template_filename: str, sha256_hash: typing.Optional[ str ] = None ):
		super().__init__( root_directory, filepath, sha256_hash )

		self._template_filename = template_filename

	@property
	def template_filename( self ) -> str:
		return self._template_filename


class StateMetadataTemplateFile( StateMetadataBaseTemplateFile ):
	def file_type( self ) -> typing.Type[ BinaryFile ]:
		return BinaryFile


class StateMetadataTemplateSettingsFile( StateMetadataBaseTemplateFile ):
	def file_type( self ) -> typing.Type[ File ]:
		return File


class StateMetadataBasePropertyFile( StateMetadataEntryFile, abc.ABC ):
	def __init__( self, root_directory: str, filepath: str, property_group: str, property_type: str, property_code: str, sha256_hash: typing.Optional[ str ] = None ):
		super().__init__( root_directory, filepath, sha256_hash )

		self._property_group	= property_group
		self._property_type		= property_type
		self._property_code		= property_code

	@property
	def property_group( self ):
		return self._property_group

	@property
	def property_type( self ) -> str:
		return self._property_type

	@property
	def property_code( self ) -> str:
		return self._property_code


class StateMetadataPropertyTemplateFile( StateMetadataBasePropertyFile ):
	def file_type( self ) -> typing.Type[ BinaryFile ]:
		return BinaryFile


class StateMetadataPropertySettingsFile( StateMetadataBasePropertyFile ):
	def file_type( self ) -> typing.Type[ File ]:
		return File


class StateMetadataBaseJSResourceFile( StateMetadataEntryFile, abc.ABC ):
	def __init__( self, root_directory: str, filepath: str, jsresource_code: str, sha256_hash: typing.Optional[ str ] = None ):
		super().__init__( root_directory, filepath, sha256_hash )

		self._jsresource_code = jsresource_code

	@property
	def jsresource_code( self ) -> str:
		return self._jsresource_code


class StateMetadataJSResourceJSFile( StateMetadataBaseJSResourceFile ):
	def file_type( self ) -> typing.Type[ BinaryFile ]:
		return BinaryFile


class StateMetadataJSResourceTemplateFile( StateMetadataBaseJSResourceFile ):
	def file_type( self ) -> typing.Type[ BinaryFile ]:
		return BinaryFile


class StateMetadataJSResourceSettingsFile( StateMetadataBaseJSResourceFile ):
	def file_type( self ) -> typing.Type[ File ]:
		return File


class StateMetadataBaseCSSResourceFile( StateMetadataEntryFile, abc.ABC ):
	def __init__( self, root_directory: str, filepath: str, cssresource_code: str, sha256_hash: typing.Optional[ str ] = None ):
		super().__init__( root_directory, filepath, sha256_hash )

		self._cssresource_code = cssresource_code

	@property
	def cssresource_code( self ) -> str:
		return self._cssresource_code


class StateMetadataCSSResourceCSSFile( StateMetadataBaseCSSResourceFile ):
	def file_type( self ) -> typing.Type[ BinaryFile ]:
		return BinaryFile


class StateMetadataCSSResourceTemplateFile( StateMetadataBaseCSSResourceFile ):
	def file_type( self ) -> typing.Type[ BinaryFile ]:
		return BinaryFile


class StateMetadataCSSResourceSettingsFile( StateMetadataBaseCSSResourceFile ):
	def file_type( self ) -> typing.Type[ File ]:
		return File


class StateMetadataBaseResourceGroupFile( StateMetadataEntryFile, abc.ABC ):
	def __init__( self, root_directory: str, filepath: str, resourcegroup_code: str, sha256_hash: typing.Optional[ str ] = None ):
		super().__init__( root_directory, filepath, sha256_hash )

		self._resourcegroup_code = resourcegroup_code

	@property
	def resourcegroup_code( self ) -> str:
		return self._resourcegroup_code


class StateMetadataResourceGroupSettingsFile( StateMetadataBaseResourceGroupFile ):
	def file_type( self ) -> typing.Type[ File ]:
		return File


class StateMetadataFileManager:
	def __init__( self, root_directory: str ):
		self._root_directory	= root_directory
		self._files				= []
		self._files_lookup		= {}

	def add_template( self, filepath: str, template_filename: str, sha256_hash: typing.Optional[ str ] = None ) -> typing.Tuple[ StateMetadataBaseTemplateFile, typing.Union[ File, BinaryFile ] ]:
		if filepath.endswith( '.json' ):
			state_file = StateMetadataTemplateSettingsFile
		elif filepath.endswith( '.mvt' ):
			state_file = StateMetadataTemplateFile
		else:
			raise Error( 'MMT-METADATA-STATE-00004', f'Unexpected template file: {filepath}' )

		return self._add( state_file( self._root_directory, filepath, template_filename, sha256_hash ) )

	def add_property( self, filepath: str, property_group: str, property_type: str, property_code: str, sha256_hash: typing.Optional[ str ] = None ) -> typing.Tuple[ StateMetadataBasePropertyFile, typing.Union[ File, BinaryFile ] ]:
		if filepath.endswith( '.json' ):
			state_file = StateMetadataPropertySettingsFile
		elif filepath.endswith( '.mvt' ):
			state_file = StateMetadataPropertyTemplateFile
		else:
			raise Error( 'MMT-METADATA-STATE-00005', f'Unexpected property file: {filepath}' )

		return self._add( state_file( self._root_directory, filepath, property_group, property_type, property_code, sha256_hash ) )

	def add_jsresource( self, filepath: str, jsresource_code: str, sha256_hash: typing.Optional[ str ] = None ) -> typing.Tuple[ StateMetadataBaseJSResourceFile, typing.Union[ File, BinaryFile ] ]:
		if filepath.endswith( '.json' ):
			state_file = StateMetadataJSResourceSettingsFile
		elif filepath.endswith( '.js' ):
			state_file = StateMetadataJSResourceJSFile
		elif filepath.endswith( '.mvt' ):
			state_file = StateMetadataJSResourceTemplateFile
		else:
			raise Error( 'MMT-METADATA-STATE-00006', f'Unexpected JS resource file: {filepath}' )

		return self._add( state_file( self._root_directory, filepath, jsresource_code, sha256_hash ) )

	def add_cssresource( self, filepath: str, cssresource_code: str, sha256_hash: typing.Optional[ str ] = None ) -> typing.Tuple[ StateMetadataBaseCSSResourceFile, typing.Union[ File, BinaryFile ] ]:
		if filepath.endswith( '.json' ):
			state_file = StateMetadataCSSResourceSettingsFile
		elif filepath.endswith( '.css' ):
			state_file = StateMetadataCSSResourceCSSFile
		elif filepath.endswith( '.mvt' ):
			state_file = StateMetadataCSSResourceTemplateFile
		else:
			raise Error( 'MMT-METADATA-STATE-00007', f'Unexpected CSS resource file: {filepath}' )

		return self._add( state_file( self._root_directory, filepath, cssresource_code, sha256_hash ) )

	def add_resourcegroup( self, filepath: str, resourcegroup_code: str, sha256_hash: typing.Optional[ str ] = None ) -> typing.Tuple[ StateMetadataBaseResourceGroupFile, File ]:
		if filepath.endswith( '.json' ):
			state_file = StateMetadataResourceGroupSettingsFile
		else:
			raise Error( 'MMT-METADATA-STATE-00010', f'Unexpected resource group file: {filepath}' )

		return self._add( state_file( self._root_directory, filepath, resourcegroup_code, sha256_hash ) )

	def _add( self, state_file: StateMetadataEntryFile ) -> typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ]:
		self._files.append( state_file )
		self._files_lookup[ state_file.filepath ] = state_file

		return state_file, state_file.file

	def lookup( self, filepath: str ) -> typing.Optional[ typing.Union[ StateMetadataTemplateFile, StateMetadataTemplateSettingsFile, StateMetadataPropertyTemplateFile, StateMetadataPropertySettingsFile, StateMetadataJSResourceJSFile, StateMetadataJSResourceTemplateFile, StateMetadataJSResourceSettingsFile, StateMetadataCSSResourceCSSFile, StateMetadataCSSResourceTemplateFile, StateMetadataCSSResourceSettingsFile, StateMetadataResourceGroupSettingsFile ] ]:
		return self._files_lookup.get( filepath )

	def delete( self, state_file: StateMetadataEntryFile ):
		for index, file in enumerate( self.files ):
			if state_file == file:
				del self._files[ index ]
				break

		del self._files_lookup[ state_file.filepath ]

		state_file.file.delete()

	def delete_all( self ):
		self._files			= []
		self._files_lookup	= {}

	@property
	def files( self ) -> typing.List[ typing.Union[ StateMetadataTemplateFile, StateMetadataTemplateSettingsFile, StateMetadataPropertyTemplateFile, StateMetadataPropertySettingsFile, StateMetadataJSResourceJSFile, StateMetadataJSResourceTemplateFile, StateMetadataJSResourceSettingsFile, StateMetadataCSSResourceCSSFile, StateMetadataCSSResourceTemplateFile, StateMetadataCSSResourceSettingsFile, StateMetadataResourceGroupSettingsFile ] ]:
		return self._files


class StateMetadataFile( MetadataFile ):
	def __init__( self, root_directory: str, metadata_directory: str ):
		super().__init__( metadata_directory, 'state.json' )

		self._version			= 1

		self._changeset			= StateMetadataChangeset( 0, '', '' )
		self._filemanager		= StateMetadataFileManager( root_directory )

	def _serialize( self ) -> dict:
		data									= {}
		data[ 'version' ]						= self._version
		data[ 'changeset' ]						= {}
		data[ 'changeset' ][ 'id' ]				= self._changeset.id
		data[ 'changeset' ][ 'username' ]		= self._changeset.username
		data[ 'changeset' ][ 'notes' ]			= self._changeset.notes
		data[ 'files' ]							= {}

		for file in self.filemanager.files:
			if file.is_template():
				entry							= {}
				entry[ 'template_filename' ]	= file.template_filename
				entry[ 'hash' ]					= file.sha256_hash
			elif file.is_property():
				entry							= {}
				entry[ 'property_group' ]		= file.property_group
				entry[ 'property_type' ]		= file.property_type
				entry[ 'property_code' ]		= file.property_code
				entry[ 'hash' ]					= file.sha256_hash
			elif file.is_jsresource():
				entry							= {}
				entry[ 'jsresource_code' ]		= file.jsresource_code
				entry[ 'hash' ]					= file.sha256_hash
			elif file.is_cssresource():
				entry							= {}
				entry[ 'cssresource_code' ]		= file.cssresource_code
				entry[ 'hash' ]					= file.sha256_hash
			elif file.is_resourcegroup():
				entry							= {}
				entry[ 'resourcegroup_code' ]	= file.resourcegroup_code
				entry[ 'hash' ]					= file.sha256_hash
			else:
				raise Error( 'MMT-METADATA-STATE-00008', f'Unrecognized file type' )

			data[ 'files' ][ file.filepath ]	= entry

		return data

	def _deserialize( self, data: dict ):
		version = data.get( 'version', 0 )

		if version == 1:
			try:
				changeset_id		= data[ 'changeset' ][ 'id' ]
				changeset_username	= data[ 'changeset' ][ 'username' ]
				changeset_notes		= data[ 'changeset' ][ 'notes' ]
				files				= data[ 'files' ]
			except KeyError as e:
				raise Error( 'MMT-METADATA-STATE-00001', f'Invalid state file: Missing \'{str( e )}\'' )

			self._changeset.id			= changeset_id
			self._changeset.username	= changeset_username
			self._changeset.notes		= changeset_notes

			for path, value in files.items():
				try:
					if value.get( 'template_filename' ) is not None:
						template_filename	= value[ 'template_filename' ]
						sha256_hash			= value[ 'hash' ]

						self.filemanager.add_template( path, template_filename, sha256_hash )
					elif value.get( 'property_group' ) is not None and value.get( 'property_type' ) is not None and value.get( 'property_code' ) is not None:
						property_group		= value[ 'property_group' ]
						property_type		= value[ 'property_type' ]
						property_code		= value[ 'property_code' ]
						sha256_hash			= value[ 'hash' ]

						self.filemanager.add_property( path, property_group, property_type, property_code, sha256_hash )
					elif value.get( 'jsresource_code' ) is not None:
						jsresource_code		= value[ 'jsresource_code' ]
						sha256_hash			= value[ 'hash' ]

						self.filemanager.add_jsresource( path, jsresource_code, sha256_hash )
					elif value.get( 'cssresource_code' ) is not None:
						cssresource_code	= value[ 'cssresource_code' ]
						sha256_hash			= value[ 'hash' ]

						self.filemanager.add_cssresource( path, cssresource_code, sha256_hash )
					elif value.get( 'resourcegroup_code' ) is not None:
						resourcegroup_code	= value[ 'resourcegroup_code' ]
						sha256_hash			= value[ 'hash' ]

						self.filemanager.add_resourcegroup( path, resourcegroup_code, sha256_hash )
					else:
						raise Error( 'MMT-METADATA-STATE-00009', 'Unrecognized file type' )
				except KeyError as e:
					raise Error( 'MMT-METADATA-STATE-00002', f'Invalid state file: Files entry \'{path}\' is missing \'{str( e )}\'' )
		else:
			raise Error( 'MMT-METADATA-STATE-00003', 'Unknown file version' )

	@property
	def filemanager( self ) -> StateMetadataFileManager:
		return self._filemanager

	@property
	def changeset( self ) -> StateMetadataChangeset:
		return self._changeset

	@changeset.setter
	def changeset( self, changeset: StateMetadataChangeset ):
		self._changeset = changeset
