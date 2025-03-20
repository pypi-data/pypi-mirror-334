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

Prefix         : MMT-COMMAND-CHECKOUT-
Next Error Code: 16
"""

import os
import typing

import merchantapi.client
import merchantapi.request
import merchantapi.model

from mmt.exceptions import Error
from mmt.commands import Command
from mmt.file import File, BinaryFile
from mmt.metadata.state import StateMetadataEntryFile


class CheckoutCommand( Command ):
	def validate( self ):
		if os.path.exists( self.root_directory ):
			if not os.path.isdir( self.root_directory ):
				raise Error( 'MMT-COMMAND-CHECKOUT-00012', f'\'{self.root_directory}\' is not a directory' )

		remote = self.configmanager.remote_lookup( self.args.get( 'remote-key' ) )

		if remote is None:
			raise Error( 'MMT-COMMAND-CHECKOUT-00014', f'Remote key \'{self.args.get( "remote-key" )}\' does not exist' )

		if self.configmanager.credential_lookup( remote.credential_key ) is None:
			raise Error( 'MMT-COMMAND-CHECKOUT-00015', f'Credential key \'{remote.credential_key}\' associated with remote key \'{self.args.get( "remote-key" )}\' does not exist' )

		if len( self.args.get( 'path' ) ) == 0:
			raise Error( 'MMT-COMMAND-CHECKOUT-00006', 'A Path value is required' )

	def initialize( self ):
		self.ensure_path_exists( self.root_directory )
		self.ensure_path_exists( self.local_metadata_directory )

		self.ensure_toplevel_directories_exist()

		self.state.filemanager.delete_all()

	def run( self ):
		remote											= self.configmanager.remote_lookup( self.args.get( 'remote-key' ) )

		self.configmanager.remote_key					= remote.key
		self.configmanager.ignore_unsynced_templates	= self.args.get( 'ignore_unsynced_templates' )
		self.configmanager.ignore_unsynced_properties	= self.args.get( 'ignore_unsynced_properties' )
		self.configmanager.include_hidden_settings		= self.args.get( 'include_hidden_settings' )

		branch											= self._load_branch( remote.branch_name )
		changeset										= self._load_changeset( self.args.get( 'c' ), branch )
		branchtemplateversions							= self._listload_branchtemplateversions( branch, changeset )
		branchpropertyversions							= self._listload_branchpropertyversions( branch, changeset )
		branchjavascriptresourceversions				= self._listload_branchjavascriptresourceversions( branch, changeset )
		branchcssresourceversions						= self._listload_branchcssresourceversions( branch, changeset )
		resourcegroups									= self._listload_resourcegroups( branch, changeset )

		self.configmanager.branch_id					= branch.get_id()
		self.configmanager.branch_name					= branch.get_name()
		self.configmanager.branch_key					= branch.get_branch_key()
		self.configmanager.branch_tags					= changeset.get_tags()

		self.state.changeset.id							= changeset.get_id()
		self.state.changeset.username					= changeset.get_user_name()
		self.state.changeset.notes						= changeset.get_notes()

		for branchtemplateversion in branchtemplateversions:
			self._process_branchtemplateversion( branchtemplateversion )

		for branchpropertyversion in branchpropertyversions:
			self._process_branchpropertyversion( branchpropertyversion )

		for branchjavascriptresourceversion in branchjavascriptresourceversions:
			self._process_branchjavascriptresourceversion( branchjavascriptresourceversion )

		for branchcssresourceversion in branchcssresourceversions:
			self._process_branchcssresourceversion( branchcssresourceversion )

		for resourcegroup in resourcegroups:
			self._process_resourcegroup( resourcegroup )

		self.configmanager.save()
		self.state.save()

	def _load_branch( self, branch_name: str ) -> merchantapi.model.Branch:
		request	= merchantapi.request.BranchListLoadQuery()
		request.set_count( 1 )
		request.set_filters( request.filter_expression().equal( 'name', branch_name ) )

		response = self.send_request( request )

		if len( response.get_branches() ) != 1:
			raise Error( 'MMT-COMMAND-CHECKOUT-00009', f'Branch \'{branch_name}\' does not exist' )

		return response.get_branches()[ 0 ]

	def _load_changeset( self, changeset_id: int, branch: merchantapi.model.Branch ) -> merchantapi.model.Changeset:
		request = merchantapi.request.ChangesetListLoadQuery()
		request.set_branch_id( branch.get_id() )

		if changeset_id > 0:
			request.set_filters( request.filter_expression().equal( 'id', changeset_id ) )
		else:
			request.set_count( 1 )
			request.set_sort( 'id', request.SORT_DESCENDING )

		response = self.send_request( request )

		if len( response.get_changesets() ) != 1:
			if changeset_id > 0:
				raise Error( 'MMT-COMMAND-CHECKOUT-00010', f'Changeset {changeset_id} does not exist' )
			else:
				raise Error( 'MMT-COMMAND-CHECKOUT-00011', 'No changesets exist' )

		return response.get_changesets()[ 0 ]

	def _listload_branchtemplateversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchTemplateVersion ]:
		request = merchantapi.request.BranchTemplateVersionListLoadQuery()
		filters = request.filter_expression()
		filters.equal( 'prop_id', 0 )

		if self.configmanager.ignore_unsynced_templates:
			filters.and_is_true( 'sync' )

		request.set_filters( filters )
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( branch.get_id() )
		request.set_on_demand_columns( [ 'source', 'settings' ] )

		return self.send_request_base64( request ).get_branch_template_versions()

	def _listload_branchpropertyversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchPropertyVersion ]:
		request = merchantapi.request.BranchPropertyVersionListLoadQuery()
		filters = request.filter_expression()

		if self.configmanager.ignore_unsynced_properties:
			filters.is_true( 'sync' )

		request.set_filters( filters )
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( branch.get_id() )
		request.set_on_demand_columns( [ 'source', 'settings', 'category', 'product' ] )

		return self.send_request_base64( request ).get_branch_property_versions()

	def _listload_branchjavascriptresourceversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchJavaScriptResourceVersion ]:
		request = merchantapi.request.BranchJavaScriptResourceVersionListLoadQuery()
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( branch.get_id() )
		request.set_on_demand_columns( [ 'linkedpages', 'linkedresources', 'source' ] )

		return self.send_request_base64( request ).get_branch_java_script_resource_versions()

	def _listload_branchcssresourceversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchCSSResourceVersion ]:
		request = merchantapi.request.BranchCSSResourceVersionListLoadQuery()
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( branch.get_id() )
		request.set_on_demand_columns( [ 'linkedpages', 'linkedresources', 'source' ] )

		return self.send_request_base64( request ).get_branch_css_resource_versions()

	def _listload_resourcegroups( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.ResourceGroup ]:
		request = merchantapi.request.ResourceGroupListLoadQuery()
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( branch.get_id() )
		request.set_on_demand_columns( [ 'linkedjavascriptresources', 'linkedcssresources' ] )

		return self.send_request( request ).get_resource_groups()

	def _process_branchtemplateversion( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ):
		# Always create a page template
		template_data		= self.get_branchtemplateversion_template_data( branchtemplateversion )
		template_filepath	= self.build_template_filepath( branchtemplateversion )
		template_filename	= self.get_branchtemplateversion_filename( branchtemplateversion )

		state_file, file	= self.state.filemanager.add_template( template_filepath, template_filename )

		self._process_lowlevel( state_file, file, template_data )

		# Page templates have a parent_id of 0 whereas item templates have a parent_id
		# referencing the page template id.  Only create the settings file when dealing
		# with a page template as that encompasses both the page and item settings
		if branchtemplateversion.get_parent_id() == 0:
			template_settings_data		= self.get_branchtemplateversion_template_settings_data( branchtemplateversion )
			template_settings_filepath	= self.build_template_settings_filepath( branchtemplateversion )
			template_settings_filename	= self.get_branchtemplateversion_filename( branchtemplateversion )

			state_file, file			= self.state.filemanager.add_template( template_settings_filepath, template_settings_filename )

			if not self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ):
				self._process_lowlevel( state_file, file, template_settings_data )

	def _process_branchpropertyversion( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ):
		self.ensure_property_path_exists( branchpropertyversion )

		# If the property is not associated with a template, do not create it
		if branchpropertyversion.get_template_id():
			property_template_data		= self.get_branchpropertyversion_template_data( branchpropertyversion )
			property_template_filepath	= self.build_property_template_filepath( branchpropertyversion )
			property_group				= self.get_branchpropertyversion_group( branchpropertyversion )
			property_type				= self.get_branchpropertyversion_type( branchpropertyversion )
			property_code				= self.get_branchpropertyversion_code( branchpropertyversion )

			state_file, file			= self.state.filemanager.add_property( property_template_filepath, property_group, property_type, property_code )

			self._process_lowlevel( state_file, file, property_template_data )

		# If the property is not associated with settings, do not create it
		if branchpropertyversion.get_version_id():
			property_settings_data		= self.get_branchpropertyversion_settings_data( branchpropertyversion )
			property_settings_filepath	= self.build_property_settings_filepath( branchpropertyversion )
			property_group				= self.get_branchpropertyversion_group( branchpropertyversion )
			property_type				= self.get_branchpropertyversion_type( branchpropertyversion )
			property_code				= self.get_branchpropertyversion_code( branchpropertyversion )

			state_file, file			= self.state.filemanager.add_property( property_settings_filepath, property_group, property_type, property_code )

			if not self.is_branchpropertyversion_settings_empty( branchpropertyversion ):
				self._process_lowlevel( state_file, file, property_settings_data )

	def _process_branchjavascriptresourceversion( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ):
		jsresource_settings_data		= self.get_branchjavascriptresourceversion_settings_data( branchjavascriptresourceversion )
		jsresource_settings_filepath	= self.build_jsresource_settings_filepath( branchjavascriptresourceversion )
		jsresource_code					= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )

		state_file, file				= self.state.filemanager.add_jsresource( jsresource_settings_filepath, jsresource_code )

		self._process_lowlevel( state_file, file, jsresource_settings_data )

		if branchjavascriptresourceversion.get_type() == 'I':
			jsresource_inline_data		= self.get_branchjavascriptresourceversion_inline_data( branchjavascriptresourceversion )
			jsresource_inline_filepath	= self.build_jsresource_inline_filepath( branchjavascriptresourceversion )
			jsresource_code				= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )

			state_file, file			= self.state.filemanager.add_jsresource( jsresource_inline_filepath, jsresource_code )

			self._process_lowlevel( state_file, file, jsresource_inline_data )

		if branchjavascriptresourceversion.get_type() == 'L':
			jsresource_local_data		= self.get_branchjavascriptresourceversion_local_data( branchjavascriptresourceversion )
			jsresource_local_filepath	= self.build_jsresource_local_filepath( branchjavascriptresourceversion )
			jsresource_code				= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )

			state_file, file			= self.state.filemanager.add_jsresource( jsresource_local_filepath, jsresource_code )

			self._process_lowlevel( state_file, file, jsresource_local_data )

	def _process_branchcssresourceversion( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ):
		cssresource_settings_data		= self.get_branchcssresourceversion_settings_data( branchcssresourceversion )
		cssresource_settings_filepath	= self.build_cssresource_settings_filepath( branchcssresourceversion )
		cssresource_code				= self.get_branchcssresourceversion_code( branchcssresourceversion )

		state_file, file				= self.state.filemanager.add_cssresource( cssresource_settings_filepath, cssresource_code )

		self._process_lowlevel( state_file, file, cssresource_settings_data )

		if branchcssresourceversion.get_type() == 'I':
			cssresource_inline_data		= self.get_branchcssresourceversion_inline_data( branchcssresourceversion )
			cssresource_inline_filepath	= self.build_cssresource_inline_filepath( branchcssresourceversion )
			cssresource_code			= self.get_branchcssresourceversion_code( branchcssresourceversion )

			state_file, file			= self.state.filemanager.add_cssresource( cssresource_inline_filepath, cssresource_code )

			self._process_lowlevel( state_file, file, cssresource_inline_data )

		if branchcssresourceversion.get_type() == 'L':
			cssresource_local_data		= self.get_branchcssresourceversion_local_data( branchcssresourceversion )
			cssresource_local_filepath	= self.build_cssresource_local_filepath( branchcssresourceversion )
			cssresource_code			= self.get_branchcssresourceversion_code( branchcssresourceversion )

			state_file, file			= self.state.filemanager.add_cssresource( cssresource_local_filepath, cssresource_code )

			self._process_lowlevel( state_file, file, cssresource_local_data )

	def _process_resourcegroup( self, resourcegroup: merchantapi.model.ResourceGroup ):
		resourcegroup_settings_data		= self.get_resourcegroup_settings_data( resourcegroup )
		resourcegroup_settings_filepath	= self.build_resourcegroup_settings_filepath( resourcegroup )
		resourcegroup_code				= self.get_resourcegroup_code( resourcegroup )

		state_file, file				= self.state.filemanager.add_resourcegroup( resourcegroup_settings_filepath, resourcegroup_code )

		self._process_lowlevel( state_file, file, resourcegroup_settings_data )

	def _process_lowlevel( self, state_file: StateMetadataEntryFile, file: typing.Union[ File, BinaryFile ], data: typing.AnyStr ):
		def checkout():
			file.write( data )
			state_file.sha256_hash = file.sha256_hash

		def reinitialize():
			state_file.sha256_hash = self.calculate_sha256( data )

		# Normal checkout
		if not self.args.get( 'reinitialize' ):
			return checkout()

		# Reinitialize, but the file does not exist on disk so
		# treat it as a normal checkout
		if not file.exists():
			return checkout()

		# Reinitialize, but the file does exist on disk so it
		# should not be overwritten, instead update the state file's
		# sha256 hash
		return reinitialize()
