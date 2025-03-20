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

Prefix         : MMT-COMMAND-PUSH-
Next Error Code: 18
"""

import os
import typing
import tempfile
import subprocess

import merchantapi.model
import merchantapi.request

from mmt.file import File, BinaryFile
from mmt.commands import ConfiguredCommand
from mmt.exceptions import Error
from mmt.metadata.state import StateMetadataEntryFile, StateMetadataBaseTemplateFile, StateMetadataBasePropertyFile, StateMetadataBaseJSResourceFile, StateMetadataBaseCSSResourceFile, StateMetadataBaseResourceGroupFile


class PushCommand( ConfiguredCommand ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		self._template_changes_lookup		= {}
		self._property_changes_lookup		= {}
		self._jsresource_changes_lookup		= {}
		self._cssresource_changes_lookup	= {}
		self._resourcegroup_changes_lookup	= {}
		self._files_to_delete				= []

	def validate( self ):
		if self.args.get( 'notes' ) is None and self.configmanager.setting_lookup( 'editor' ) is None:
			raise Error( 'MMT-COMMAND-PUSH-00001', 'Either the --notes parameter must be specified or the \'editor\' configuration setting must be set' )
		elif self.args.get( 'notes' ) is not None and len( self.args.get( 'notes' ) ) == 0:
			raise Error( 'MMT-COMMAND-PUSH-00002', 'Notes cannot be blank' )

	def run( self ):
		filepaths		= set( filepath for filepath in self.args.get( 'filepaths' ) )
		modified_files	= self.load_modified_files( filtered_filepaths = filepaths )

		if len( modified_files ) == 0:
			print( 'No files to commit' )
			return

		for state_file, file in self.group_modified_template_files( modified_files ):
			self._build_template_changes( state_file, file )

		for state_file, file in self.group_modified_property_files( modified_files ):
			self._build_property_changes( state_file, file )

		for state_file, file in self.group_modified_jsresource_files( modified_files ):
			self._build_jsresource_changes( state_file, file )

		for state_file, file in self.group_modified_cssresource_files( modified_files ):
			self._build_cssresource_changes( state_file, file )

		for state_file, file in self.group_modified_resourcegroup_files( modified_files ):
			self._build_resourcegroup_changes( state_file, file )

		commit_notes = self._generate_commit_notes( modified_files )

		if len( commit_notes ) == 0:
			print( 'Aborting commit due to empty commit notes' )
			return

		request = merchantapi.request.ChangesetCreate()
		request.set_branch_id( self.configmanager.branch_id )
		request.set_notes( commit_notes )
		request.set_tags( ' '.join( self.configmanager.branch_tags ) )

		for template_change in self._template_changes_lookup.values():
			request.add_template_change( template_change )

		for property_change in self._property_changes_lookup.values():
			request.add_property_change( property_change )

		for jsresource_change in self._jsresource_changes_lookup.values():
			request.add_java_script_resource_change( jsresource_change )

		for cssresource_change in self._cssresource_changes_lookup.values():
			request.add_css_resource_change( cssresource_change )

		for resourcegroup_change in self._resourcegroup_changes_lookup.values():
			request.add_resource_group_change( resourcegroup_change )

		changeset = self.send_request_base64( request ).get_changeset()

		self.state.changeset.id			= changeset.get_id()
		self.state.changeset.username	= changeset.get_user_name()
		self.state.changeset.notes		= changeset.get_notes()

		# This save saves the updated changeset as well as all of
		# the state files that had their sha256 hashes updated
		self.state.save()

		print( 'Committed the following files:' )

		for state_file, file in modified_files:
			print( f'\t{state_file.filepath}' )

		for file in self._files_to_delete:
			file.delete()

	def _build_template_changes( self, state_file: StateMetadataBaseTemplateFile, file: typing.Union[ File, BinaryFile ] ):
		# Build a template changes lookup dictionary
		# Modified files that share the same template id
		# need to be grouped together in a single changeset

		if state_file.template_filename in self._template_changes_lookup:
			template_change = self._template_changes_lookup[ state_file.template_filename ]
		else:
			template_change = merchantapi.model.TemplateChange()
			template_change.set_template_filename( state_file.template_filename )

			self._template_changes_lookup[ state_file.template_filename ] = template_change

		if state_file.is_template_file():
			data			= file.read()
			data_len		= len( data )

			template_change.set_source( self.base64_encode( data ).decode( 'ascii' ) )
		elif state_file.is_template_settings_file():
			data			= file.read()
			data_len		= len( data )

			if data_len == 0:
				self._files_to_delete.append( file )
			else:
				try:
					data = self.json_loads( data )
				except Exception as e:
					raise Error( 'MMT-COMMAND-PUSH-00003', f'Failed to parse JSON in \'{state_file.filepath}\': {e}' )

			template_change.set_settings( data )
		else:
			raise Error( 'MMT-COMMAND-PUSH-00006', 'Unexpected modified file' )

		# Template files are never deleted (even if they are empty)
		# so the sha256 hash is always loaded.  Settings files
		# are deleted if they are empty so their sha256 hash is
		# conditionally loaded

		if state_file.is_template_file():
			state_file.sha256_hash = file.sha256_hash
		elif state_file.is_template_settings_file():
			if data_len == 0:
				state_file.sha256_hash = None
			else:
				state_file.sha256_hash = file.sha256_hash

	def _build_property_changes( self, state_file: StateMetadataBasePropertyFile, file: typing.Union[ File, BinaryFile ] ):
		# Build a property changes lookup dictionary
		# Modified files that share the same property id
		# need to be grouped together in a single changeset

		if ( state_file.property_group, state_file.property_type, state_file.property_code ) in self._property_changes_lookup:
			property_change = self._property_changes_lookup[ ( state_file.property_group, state_file.property_type, state_file.property_code ) ]
		else:
			property_change = merchantapi.model.PropertyChange()
			property_change.set_property_type( state_file.property_type )

			if state_file.property_group == 'product':
				property_change.set_product_code( state_file.property_code )
			elif state_file.property_group == 'category':
				property_change.set_category_code( state_file.property_code )
			elif state_file.property_group == '':
				property_change.set_property_code( state_file.property_code )
			else:
				raise Error( 'MMT-COMMAND-PUSH-00017', 'Unexpected property group' )

			self._property_changes_lookup[ ( state_file.property_group, state_file.property_type, state_file.property_code ) ] = property_change

		if state_file.is_property_template_file():
			data		= file.read()
			data_len	= len( data )

			property_change.set_source( self.base64_encode( data ).decode( 'ascii' ) )
		elif state_file.is_property_settings_file():
			data		= file.read()
			data_len	= len( data )

			if data_len == 0:
				self._files_to_delete.append( file )
			else:
				try:
					data = self.json_loads( data )
				except Exception as e:
					raise Error( 'MMT-COMMAND-PUSH-00003', f'Failed to parse JSON in \'{state_file.filepath}\': {e}' )

			property_change.set_settings( data )
		else:
			raise Error( 'MMT-COMMAND-PUSH-00007', 'Unexpected modified file' )

		# Template files are never deleted (even if they are empty)
		# so the sha256 hash is always loaded.  Settings files
		# are deleted if they are empty so their sha256 hash is
		# conditionally loaded

		if state_file.is_property_template_file():
			state_file.sha256_hash = file.sha256_hash
		elif state_file.is_property_settings_file():
			if data_len == 0:
				state_file.sha256_hash = None
			else:
				state_file.sha256_hash = file.sha256_hash

	def _build_jsresource_changes( self, state_file: StateMetadataBaseJSResourceFile, file: typing.Union[ File, BinaryFile ] ):
		# Build a JS resource changes lookup dictionary
		# Modified files that share the same JS resource id
		# need to be grouped together in a single changeset

		if state_file.jsresource_code in self._jsresource_changes_lookup:
			jsresource_change = self._jsresource_changes_lookup[ state_file.jsresource_code ]
		else:
			jsresource_change = merchantapi.model.JavaScriptResourceChange()
			jsresource_change.set_java_script_resource_code( state_file.jsresource_code )

			self._jsresource_changes_lookup[ state_file.jsresource_code ] = jsresource_change

		if state_file.is_jsresource_js_file():
			jsresource_change.set_source( self.base64_encode( file.read() ).decode( 'ascii' ) )
		elif state_file.is_jsresource_template_file():
			jsresource_change.set_source( self.base64_encode( file.read() ).decode( 'ascii' ) )
		elif state_file.is_jsresource_settings_file():
			try:
				data = self.json_loads( file.read() )
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00008', f'Failed to parse JSON in \'{state_file.filepath}\': {e}' )

			try:
				jsresource_change.set_is_global( data[ 'is_global' ] )
				jsresource_change.set_active( data[ 'active' ] )

				for attribute in data[ 'attributes' ]:
					jsresource_attribute = merchantapi.model.JavaScriptResourceVersionAttribute()
					jsresource_attribute.set_name( attribute[ 'name' ] )
					jsresource_attribute.set_value( attribute[ 'value' ] )

					jsresource_change.add_attribute( jsresource_attribute )

				if data[ 'type' ] == 'C':
					jsresource_change.set_linked_resources( data[ 'linked_resources' ] )
				elif data[ 'type' ] == 'E':
					jsresource_change.set_file_path( data[ 'filepath' ] )
				elif data[ 'type' ] == 'L':
					if 'filepath' in data:
						jsresource_change.set_file_path( data[ 'filepath' ] )
					elif 'branchless_filepath' in data:
						jsresource_change.set_branchless_file_path( data[ 'branchless_filepath' ] )

				if not data[ 'is_global' ]:
					jsresource_change.set_linked_pages( data[ 'linked_pages' ] )
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00009', f'Failed building JS resource changeset for \'{state_file.filepath}\': {e}' )
		else:
			raise Error( 'MMT-COMMAND-PUSH-00010', 'Unexpected modified file' )

		state_file.sha256_hash = file.sha256_hash

	def _build_cssresource_changes( self, state_file: StateMetadataBaseCSSResourceFile, file: typing.Union[ File, BinaryFile ] ):
		# Build a CSS resource changes lookup dictionary
		# Modified files that share the same CSS resource id
		# need to be grouped together in a single changeset

		if state_file.cssresource_code in self._cssresource_changes_lookup:
			cssresource_change = self._cssresource_changes_lookup[ state_file.cssresource_code ]
		else:
			cssresource_change = merchantapi.model.CSSResourceChange()
			cssresource_change.set_css_resource_code( state_file.cssresource_code )

			self._cssresource_changes_lookup[ state_file.cssresource_code ] = cssresource_change

		if state_file.is_cssresource_css_file():
			cssresource_change.set_source( self.base64_encode( file.read() ).decode( 'ascii' ) )
		elif state_file.is_cssresource_template_file():
			cssresource_change.set_source( self.base64_encode( file.read() ).decode( 'ascii' ) )
		elif state_file.is_cssresource_settings_file():
			try:
				data = self.json_loads( file.read() )
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00011', f'Failed to parse JSON in \'{state_file.filepath}\': {e}' )

			try:
				cssresource_change.set_is_global( data[ 'is_global' ] )
				cssresource_change.set_active( data[ 'active' ] )

				for attribute in data[ 'attributes' ]:
					cssresource_attribute = merchantapi.model.CSSResourceVersionAttribute()
					cssresource_attribute.set_name( attribute[ 'name' ] )
					cssresource_attribute.set_value( attribute[ 'value' ] )

					cssresource_change.add_attribute( cssresource_attribute )

				if data[ 'type' ] == 'C':
					cssresource_change.set_linked_resources( data[ 'linked_resources' ] )
				elif data[ 'type' ] == 'E':
					cssresource_change.set_file_path( data[ 'filepath' ] )
				elif data[ 'type' ] == 'L':
					if 'filepath' in data:
						cssresource_change.set_file_path( data[ 'filepath' ] )
					elif 'branchless_filepath' in data:
						cssresource_change.set_branchless_file_path( data[ 'branchless_filepath' ] )

				if not data[ 'is_global' ]:
					cssresource_change.set_linked_pages( data[ 'linked_pages' ] )
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00012', f'Failed building CSS resource changeset for \'{state_file.filepath}\': {e}' )
		else:
			raise Error( 'MMT-COMMAND-PUSH-00013', 'Unexpected modified file' )

		state_file.sha256_hash = file.sha256_hash

	def _build_resourcegroup_changes( self, state_file: StateMetadataBaseResourceGroupFile, file: typing.Union[ File, BinaryFile ] ):
		# Build a resource group changes lookup dictionary
		# Modified files that share the same resource group id
		# need to be grouped together in a single changeset

		if state_file.resourcegroup_code in self._resourcegroup_changes_lookup:
			resourcegroup_change = self._resourcegroup_changes_lookup[ state_file.resourcegroup_code ]
		else:
			resourcegroup_change = merchantapi.model.ResourceGroupChange()
			resourcegroup_change.set_resource_group_code( state_file.resourcegroup_code )

			self._resourcegroup_changes_lookup[ state_file.resourcegroup_code ] = resourcegroup_change

		if state_file.is_resourcegroup_settings_file():
			try:
				data = self.json_loads( file.read() )
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00014', f'Failed to parse JSON in \'{state_file.filepath}\': {e}' )

			try:
				resourcegroup_change.set_linked_css_resources( data[ 'linked_css_resources' ] )
				resourcegroup_change.set_linked_java_script_resources( data[ 'linked_js_resources' ] )
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00015', f'Failed building Resource Group changeset for \'{state_file.filepath}\': {e}' )
		else:
			raise Error( 'MMT-COMMAND-PUSH-00016', 'Unexpected modified file' )

		state_file.sha256_hash = file.sha256_hash

	def _generate_commit_notes( self, modified_files: [ ( StateMetadataEntryFile, File ) ] ) -> str:
		if self.args.get( 'notes' ) is not None:
			return self.args.get( 'notes' )

		tags			= '<None>' if len( self.configmanager.branch_tags ) == 0 else self.build_branch_tags()
		default_notes	= "\n" \
						  "# Please enter the commit notes for your changes. Lines starting\n" \
						  "# with '#' will be ignored, and an empty note aborts the commit.\n" \
						  "#\n" \
						  f"# Tags: {tags}\n" \
						  "#\n" \
						  "# Changes to be committed:\n"

		for state_file, file in modified_files:
			default_notes += f'#\t{state_file.filepath}\n'

		default_notes += '#'

		try:
			temp = tempfile.NamedTemporaryFile( mode = 'w+', prefix = 'mmt_', suffix = '.tmp', delete = False )
		except Exception as e:
			raise Error( 'MMT-COMMAND-PUSH-00005', f'Failed to create temporary file: {str( e ) }' )

		try:
			temp.write( default_notes )
			temp.close()

			editor_args = self.configmanager.setting_lookup( 'editor' ).value
			editor_args.append( temp.name )

			try:
				subprocess.run( editor_args ).check_returncode()
			except Exception as e:
				raise Error( 'MMT-COMMAND-PUSH-00004', f'Failed to open external editor \'{editor_args[ 0 ]}\': {str( e )}' )

			with open( temp.name ) as fh:
				commit_notes = ''

				for line in fh:
					if not line.startswith( '#' ):
						commit_notes += line.strip()
		finally:
			os.unlink( temp.name )

		return commit_notes.strip()
