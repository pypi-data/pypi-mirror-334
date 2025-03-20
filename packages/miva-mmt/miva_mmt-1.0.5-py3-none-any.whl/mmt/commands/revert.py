"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2023 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-COMMAND-REVERT-
Next Error Code: 7
"""

import typing

import merchantapi.model
import merchantapi.request

from mmt.exceptions import Error
from mmt.file import File, BinaryFile
from mmt.commands import ConfiguredCommand
from mmt.metadata.state import StateMetadataEntryFile, StateMetadataTemplateFile, StateMetadataTemplateSettingsFile, StateMetadataPropertyTemplateFile, StateMetadataPropertySettingsFile, StateMetadataJSResourceJSFile, StateMetadataJSResourceTemplateFile, StateMetadataJSResourceSettingsFile, StateMetadataCSSResourceCSSFile, StateMetadataCSSResourceTemplateFile, StateMetadataCSSResourceSettingsFile, StateMetadataResourceGroupSettingsFile


class RevertCommand( ConfiguredCommand ):
	def validate( self ):
		if len( self.args.get( 'filepaths' ) ) == 0 and self.args.get( 'all' ) is False:
			raise Error( 'MMT-COMMAND-REVERT-00001', 'Either the --all parameter or individual filepaths must be specified' )

	def initialize( self ):
		self.ensure_toplevel_directories_exist()

	def run( self ):
		filepaths		= set( filepath for filepath in self.args.get( 'filepaths' ) )
		modified_files	= self.load_modified_files( filtered_filepaths = filepaths )

		if len( modified_files ) == 0:
			return

		modified_template_files			= self.group_modified_template_files( modified_files )
		modified_property_files			= self.group_modified_property_files( modified_files )
		modified_jsresource_files		= self.group_modified_jsresource_files( modified_files )
		modified_cssresource_files		= self.group_modified_cssresource_files( modified_files )
		modified_resourcegroup_files	= self.group_modified_resourcegroup_files( modified_files )

		if len( modified_template_files ) > 0:
			template_filenames		= [ state_file.template_filename for state_file, file in modified_template_files ]
			branchtemplateversions	= self._listload_branchtemplateversions( template_filenames )

			for state_file, file in modified_template_files:
				for branchtemplateversion in branchtemplateversions:
					if self.template_equals_branchtemplateversion( state_file, branchtemplateversion ):
						self._process_branchtemplateversion( branchtemplateversion, state_file, file )

						break

		if len( modified_property_files ) > 0:
			property_types_codes	= [ ( state_file.property_group, state_file.property_type, state_file.property_code ) for state_file, file in modified_property_files ]
			branchpropertyversions	= self._listload_branchpropertyversions( property_types_codes )

			for state_file, file in modified_property_files:
				for branchpropertyversion in branchpropertyversions:
					if self.property_equals_branchpropertyversion( state_file, branchpropertyversion ):
						self._process_branchpropertyversion( branchpropertyversion, state_file, file )

						break

		if len( modified_jsresource_files ) > 0:
			jsresource_codes					= [ state_file.jsresource_code for state_file, file in modified_jsresource_files ]
			branchjavascriptresourceversions	= self._listload_branchjavascriptresourceversions( jsresource_codes )

			for state_file, file in modified_jsresource_files:
				for branchjavascriptresourceversion in branchjavascriptresourceversions:
					if self.jsresource_equals_branchjavascriptresourceversion( state_file, branchjavascriptresourceversion ):
						self._process_branchjavascriptresourceversion( branchjavascriptresourceversion, state_file, file )

						break

		if len( modified_cssresource_files ) > 0:
			cssresource_codes			= [ state_file.cssresource_code for state_file, file in modified_cssresource_files ]
			branchcssresourceversions	= self._listload_branchcssresourceversions( cssresource_codes )

			for state_file, file in modified_cssresource_files:
				for branchcssresourceversion in branchcssresourceversions:
					if self.cssresource_equals_branchcssresourceversion( state_file, branchcssresourceversion ):
						self._process_branchcssresourceversion( branchcssresourceversion, state_file, file )

						break

		if len( modified_resourcegroup_files ) > 0:
			resourcegroup_codes	= [ state_file.resourcegroup_code for state_file, file in modified_resourcegroup_files ]
			resourcegroups		= self._listload_resourcegroups( resourcegroup_codes )

			for state_file, file, in modified_resourcegroup_files:
				for resourcegroup in resourcegroups:
					if self.resourcegroup_equals_resourcegroup( state_file, resourcegroup ):
						self._process_resourcegroup( resourcegroup, state_file, file )

						break

		self.state.save()

		print( 'Reverted the following files:' )

		for state_file, file in modified_files:
			print( f'\t{state_file.filepath}' )

	def _listload_branchtemplateversions( self, template_filenames: typing.List[ str ] ) -> typing.List[ merchantapi.model.BranchTemplateVersion ]:
		request = merchantapi.request.BranchTemplateVersionListLoadQuery()
		request.set_filters( request.filter_expression().is_in( 'filename', template_filenames ) )
		request.set_changeset_id( self.state.changeset.id )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'source', 'settings' ] )

		return self.send_request_base64( request ).get_branch_template_versions()

	def _listload_branchpropertyversions( self, property_groups_types_codes: typing.List[ typing.Tuple[ str, str, str ] ] ) -> typing.List[ merchantapi.model.BranchPropertyVersion ]:
		request = merchantapi.request.BranchPropertyVersionListLoadQuery()
		filters = self.filter_expression()

		for property_group, property_type, property_code in property_groups_types_codes:
			filter_expression = self.filter_expression().equal( 'type', property_type )

			if property_group in [ 'product', 'category' ]:
				filter_expression.is_null( 'code' )
			else:
				filter_expression.equal( 'code', property_code )

			filters.or_x( filter_expression )

		request.set_filters( filters )
		request.set_changeset_id( self.state.changeset.id )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'source', 'settings', 'category', 'product' ] )

		return self.send_request_base64( request ).get_branch_property_versions()

	def _listload_branchjavascriptresourceversions( self, jsresource_codes: typing.List[ str ] ) -> typing.List[ merchantapi.model.BranchJavaScriptResourceVersion ]:
		request = merchantapi.request.BranchJavaScriptResourceVersionListLoadQuery()
		request.set_filters( request.filter_expression().is_in( 'code', jsresource_codes ) )
		request.set_changeset_id( self.state.changeset.id )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'linkedpages', 'linkedresources', 'source' ] )

		return self.send_request_base64( request ).get_branch_java_script_resource_versions()

	def _listload_branchcssresourceversions( self, cssresource_codes: typing.List[ str ] ) -> typing.List[ merchantapi.model.BranchCSSResourceVersion ]:
		request = merchantapi.request.BranchCSSResourceVersionListLoadQuery()
		request.set_filters( request.filter_expression().is_in( 'code', cssresource_codes ) )
		request.set_changeset_id( self.state.changeset.id )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'linkedpages', 'linkedresources', 'source' ] )

		return self.send_request_base64( request ).get_branch_css_resource_versions()

	def _listload_resourcegroups( self, resourcegroup_codes: typing.List[ str ] ) -> typing.List[ merchantapi.model.ResourceGroup ]:
		request = merchantapi.request.ResourceGroupListLoadQuery()
		request.set_filters( request.filter_expression().is_in( 'code', resourcegroup_codes ) )
		request.set_changeset_id( self.state.changeset.id )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'linkedjavascriptresources', 'linkedcssresources' ] )

		return self.send_request( request ).get_resource_groups()

	def _process_branchtemplateversion( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion, state_file: typing.Union[ StateMetadataTemplateFile, StateMetadataTemplateSettingsFile ], file: typing.Union[ File, BinaryFile ] ):
		if state_file.is_template_file():
			self._process_lowlevel( state_file, file, self.get_branchtemplateversion_template_data( branchtemplateversion ) )
		elif state_file.is_template_settings_file():
			if self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ):
				self._process_lowlevel_delete( state_file, file )
			else:
				self._process_lowlevel( state_file, file, self.get_branchtemplateversion_template_settings_data( branchtemplateversion ) )
		else:
			raise Error( 'MMT-COMMAND-REVERT-00002', 'Unexpected template' )

	def _process_branchpropertyversion( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion, state_file: typing.Union[ StateMetadataPropertyTemplateFile, StateMetadataPropertySettingsFile ], file: typing.Union[ File, BinaryFile ] ):
		self.ensure_property_path_exists( branchpropertyversion )

		if state_file.is_property_template_file():
			self._process_lowlevel( state_file, file, self.get_branchpropertyversion_template_data( branchpropertyversion ) )
		elif state_file.is_property_settings_file():
			if self.is_branchpropertyversion_settings_empty( branchpropertyversion ):
				self._process_lowlevel_delete( state_file, file )
			else:
				self._process_lowlevel( state_file, file, self.get_branchpropertyversion_settings_data( branchpropertyversion ) )
		else:
			raise Error( 'MMT-COMMAND-REVERT-00003', 'Unexpected property' )

	def _process_branchjavascriptresourceversion( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion, state_file: typing.Union[ StateMetadataJSResourceJSFile, StateMetadataJSResourceTemplateFile, StateMetadataJSResourceSettingsFile ], file: typing.Union[ File, BinaryFile ] ):
		if state_file.is_jsresource_settings_file():
			self._process_lowlevel( state_file, file, self.get_branchjavascriptresourceversion_settings_data( branchjavascriptresourceversion ) )
		elif state_file.is_jsresource_js_file():
			self._process_lowlevel( state_file, file, self.get_branchjavascriptresourceversion_local_data( branchjavascriptresourceversion ) )
		elif state_file.is_jsresource_template_file():
			self._process_lowlevel( state_file, file, self.get_branchjavascriptresourceversion_inline_data( branchjavascriptresourceversion ) )
		else:
			raise Error( 'MMT-COMMAND-REVERT-00004', 'Unexpected JS resource' )

	def _process_branchcssresourceversion( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion, state_file: typing.Union[ StateMetadataCSSResourceCSSFile, StateMetadataCSSResourceTemplateFile, StateMetadataCSSResourceSettingsFile ], file: typing.Union[ File, BinaryFile ] ):
		if state_file.is_cssresource_settings_file():
			self._process_lowlevel( state_file, file, self.get_branchcssresourceversion_settings_data( branchcssresourceversion ) )
		elif state_file.is_cssresource_css_file():
			self._process_lowlevel( state_file, file, self.get_branchcssresourceversion_local_data( branchcssresourceversion ) )
		elif state_file.is_cssresource_template_file():
			self._process_lowlevel( state_file, file, self.get_branchcssresourceversion_inline_data( branchcssresourceversion ) )
		else:
			raise Error( 'MMT-COMMAND-REVERT-00005', 'Unexpected CSS resource' )

	def _process_resourcegroup( self, resourcegroup: merchantapi.model.ResourceGroup, state_file: StateMetadataResourceGroupSettingsFile, file: File ):
		if state_file.is_resourcegroup_settings_file():
			self._process_lowlevel( state_file, file, self.get_resourcegroup_settings_data( resourcegroup ) )
		else:
			raise Error( 'MMT-COMMAND-REVERT-00006', 'Unexpected resource group' )

	def _process_lowlevel( self, state_file: StateMetadataEntryFile, file: typing.Union[ File, BinaryFile ], data: typing.AnyStr ):
		file.write( data )
		state_file.sha256_hash = file.sha256_hash

	def _process_lowlevel_delete( self, state_file: StateMetadataEntryFile, file: typing.Union[ File, BinaryFile ] ):
		file.delete()
		state_file.sha256_hash = None
