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

Prefix         : MMT-COMMAND-SWITCH-
Next Error Code: 4
"""

import typing

import merchantapi.request
import merchantapi.model

from mmt.exceptions import Error
from mmt.commands import ConfiguredCommand


class SwitchCommand( ConfiguredCommand ):
	def validate( self ):
		if self.configmanager.remote_lookup( self.args.get( 'remote-key' ) ) is None:
			raise Error( 'MMT-COMMAND-SWITCH-00001', f'Remote key \'{self.args.get( "remote-key" )}\' does not exist' )

	def initialize( self ):
		self.state.filemanager.delete_all()

	def run( self ):
		remote								= self.configmanager.remote_lookup( self.args.get( 'remote-key' ) )

		branch								= self._load_branch( remote.branch_name )
		changeset							= self._load_changeset( branch )
		branchtemplateversions				= self._listload_branchtemplateversions( branch, changeset )
		branchpropertyversions				= self._listload_branchpropertyversions( branch, changeset )
		branchjavascriptresourceversions	= self._listload_branchjavascriptresourceversions( branch, changeset )
		branchcssresourceversions			= self._listload_branchcssresourceversions( branch, changeset )
		resourcegroups						= self._listload_resourcegroups( branch, changeset )

		self.configmanager.remote_key		= remote.key
		self.configmanager.branch_id		= branch.get_id()
		self.configmanager.branch_name		= branch.get_name()
		self.configmanager.branch_key		= branch.get_branch_key()
		self.configmanager.branch_tags		= changeset.get_tags()

		self.state.changeset.id				= changeset.get_id()
		self.state.changeset.username		= changeset.get_user_name()
		self.state.changeset.notes			= changeset.get_notes()

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
			raise Error( 'MMT-COMMAND-SWITCH-00002', f'Branch \'{branch_name}\' does not exist' )

		return response.get_branches()[ 0 ]

	def _load_changeset( self, branch: merchantapi.model.Branch ) -> merchantapi.model.Changeset:
		request = merchantapi.request.ChangesetListLoadQuery()
		request.set_branch_id( branch.get_id() )
		request.set_count( 1 )
		request.set_sort( 'id', request.SORT_DESCENDING )

		response = self.send_request( request )

		if len( response.get_changesets() ) != 1:
			raise Error( 'MMT-COMMAND-SWITCH-00003', 'No changesets exist' )

		return response.get_changesets()[ 0 ]

	def _listload_branchtemplateversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchTemplateVersion ]:
		request = merchantapi.request.BranchTemplateVersionListLoadQuery()
		filters = request.filter_expression()
		filters.equal( 'prop_id', 0 )

		if self.configmanager.ignore_unsynced_templates:
			filters.and_is_true( 'sync' )

		request.set_filters( filters )
		request.set_branch_id( branch.get_id() )
		request.set_changeset_id( changeset.get_id() )
		request.set_on_demand_columns( [ 'source', 'settings' ] )

		return self.send_request_base64( request ).get_branch_template_versions()

	def _listload_branchpropertyversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchPropertyVersion ]:
		request = merchantapi.request.BranchPropertyVersionListLoadQuery()
		filters = request.filter_expression()

		if self.configmanager.ignore_unsynced_properties:
			filters.and_is_true( 'sync' )

		request.set_filters( filters )
		request.set_branch_id( branch.get_id() )
		request.set_changeset_id( changeset.get_id() )
		request.set_on_demand_columns( [ 'source', 'settings', 'category', 'product' ] )

		return self.send_request_base64( request ).get_branch_property_versions()

	def _listload_branchjavascriptresourceversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchJavaScriptResourceVersion ]:
		request = merchantapi.request.BranchJavaScriptResourceVersionListLoadQuery()
		request.set_branch_id( branch.get_id() )
		request.set_changeset_id( changeset.get_id() )
		request.set_on_demand_columns( [ 'linkedpages', 'linkedresources', 'source' ] )

		return self.send_request_base64( request ).get_branch_java_script_resource_versions()

	def _listload_branchcssresourceversions( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.BranchCSSResourceVersion ]:
		request = merchantapi.request.BranchCSSResourceVersionListLoadQuery()
		request.set_branch_id( branch.get_id() )
		request.set_changeset_id( changeset.get_id() )
		request.set_on_demand_columns( [ 'linkedpages', 'linkedresources', 'source' ] )

		return self.send_request_base64( request ).get_branch_css_resource_versions()

	def _listload_resourcegroups( self, branch: merchantapi.model.Branch, changeset: merchantapi.model.Changeset ) -> typing.List[ merchantapi.model.ResourceGroup ]:
		request = merchantapi.request.ResourceGroupListLoadQuery()
		request.set_branch_id( branch.get_id() )
		request.set_changeset_id( changeset.get_id() )
		request.set_on_demand_columns( [ 'linkedjavascriptresources', 'linkedcssresources' ] )

		return self.send_request( request ).get_resource_groups()

	def _process_branchtemplateversion( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ):
		# Always create a page template

		template_filepath	= self.build_template_filepath( branchtemplateversion )
		template_filename	= self.get_branchtemplateversion_filename( branchtemplateversion )
		template_sha256		= self.calculate_sha256( self.get_branchtemplateversion_template_data( branchtemplateversion ) )

		self.state.filemanager.add_template( template_filepath, template_filename, template_sha256 )

		# Page templates have a parent_id of 0 whereas item templates have a parent_id
		# referencing the page template id.  Only create the settings file when dealing
		# with a page template as that encompasses both the page and item settings

		if branchtemplateversion.get_parent_id() == 0:
			template_settings_filepath		= self.build_template_settings_filepath( branchtemplateversion )
			template_settings_filename		= self.get_branchtemplateversion_filename( branchtemplateversion )
			template_settings_sha256		= None if self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ) else self.calculate_sha256( self.get_branchtemplateversion_template_settings_data( branchtemplateversion ) )

			self.state.filemanager.add_template( template_settings_filepath, template_settings_filename, template_settings_sha256 )

	def _process_branchpropertyversion( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ):
		# If the property is associated with a template, create a state file entry
		if branchpropertyversion.get_template_id():
			property_template_filepath	= self.build_property_template_filepath( branchpropertyversion )
			property_template_group		= self.get_branchpropertyversion_group( branchpropertyversion )
			property_template_type		= self.get_branchpropertyversion_type( branchpropertyversion )
			property_template_code		= self.get_branchpropertyversion_code( branchpropertyversion )
			property_template_sha256	= self.calculate_sha256( self.get_branchpropertyversion_template_data( branchpropertyversion ) )

			self.state.filemanager.add_property( property_template_filepath, property_template_group, property_template_type, property_template_code, property_template_sha256 )

		# If the property is associated with settings, create a state file entry
		if branchpropertyversion.get_version_id():
			property_settings_filepath	= self.build_property_settings_filepath( branchpropertyversion )
			property_settings_group		= self.get_branchpropertyversion_group( branchpropertyversion )
			property_settings_type		= self.get_branchpropertyversion_type( branchpropertyversion )
			property_settings_code		= self.get_branchpropertyversion_code( branchpropertyversion )
			property_settings_sha256	= None if self.is_branchpropertyversion_settings_empty( branchpropertyversion ) else self.calculate_sha256( self.get_branchpropertyversion_settings_data( branchpropertyversion ) )

			self.state.filemanager.add_property( property_settings_filepath, property_settings_group, property_settings_type, property_settings_code, property_settings_sha256 )

	def _process_branchjavascriptresourceversion( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ):
		jsresource_settings_filepath	= self.build_jsresource_settings_filepath( branchjavascriptresourceversion )
		jsresource_settings_code		= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )
		jsresource_settings_sha256		= self.calculate_sha256( self.get_branchjavascriptresourceversion_settings_data( branchjavascriptresourceversion ) )

		self.state.filemanager.add_jsresource( jsresource_settings_filepath, jsresource_settings_code, jsresource_settings_sha256 )

		if branchjavascriptresourceversion.get_type() == 'I':
			jsresource_inline_filepath	= self.build_jsresource_inline_filepath( branchjavascriptresourceversion )
			jsresource_inline_code		= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )
			jsresource_inline_sha256	= self.calculate_sha256( self.get_branchjavascriptresourceversion_inline_data( branchjavascriptresourceversion ) )

			self.state.filemanager.add_jsresource( jsresource_inline_filepath, jsresource_inline_code, jsresource_inline_sha256 )

		if branchjavascriptresourceversion.get_type() == 'L':
			jsresource_local_filepath	= self.build_jsresource_local_filepath( branchjavascriptresourceversion )
			jsresource_local_code		= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )
			jsresource_local_sha256		= self.calculate_sha256( self.get_branchjavascriptresourceversion_local_data( branchjavascriptresourceversion ) )

			self.state.filemanager.add_jsresource( jsresource_local_filepath, jsresource_local_code, jsresource_local_sha256 )

	def _process_branchcssresourceversion( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ):
		cssresource_settings_filepath	= self.build_cssresource_settings_filepath( branchcssresourceversion )
		cssresource_settings_code		= self.get_branchcssresourceversion_code( branchcssresourceversion )
		cssresource_settings_sha256		= self.calculate_sha256( self.get_branchcssresourceversion_settings_data( branchcssresourceversion ) )

		self.state.filemanager.add_cssresource( cssresource_settings_filepath, cssresource_settings_code, cssresource_settings_sha256 )

		if branchcssresourceversion.get_type() == 'I':
			cssresource_inline_filepath	= self.build_cssresource_inline_filepath( branchcssresourceversion )
			cssresource_inline_code		= self.get_branchcssresourceversion_code( branchcssresourceversion )
			cssresource_inline_sha256	= self.calculate_sha256( self.get_branchcssresourceversion_inline_data( branchcssresourceversion ) )

			self.state.filemanager.add_cssresource( cssresource_inline_filepath, cssresource_inline_code, cssresource_inline_sha256 )

		if branchcssresourceversion.get_type() == 'L':
			cssresource_local_filepath	= self.build_cssresource_local_filepath( branchcssresourceversion )
			cssresource_local_code		= self.get_branchcssresourceversion_code( branchcssresourceversion )
			cssresource_local_sha256	= self.calculate_sha256( self.get_branchcssresourceversion_local_data( branchcssresourceversion ) )

			self.state.filemanager.add_cssresource( cssresource_local_filepath, cssresource_local_code, cssresource_local_sha256 )

	def _process_resourcegroup( self, resourcegroup: merchantapi.model.ResourceGroup ):
		resourcegroup_settings_filepath	= self.build_resourcegroup_settings_filepath( resourcegroup )
		resourcegroup_settings_code		= self.get_resourcegroup_code( resourcegroup )
		resourcegroup_settings_sha256	= self.calculate_sha256( self.get_resourcegroup_settings_data( resourcegroup ) )

		self.state.filemanager.add_resourcegroup( resourcegroup_settings_filepath, resourcegroup_settings_code, resourcegroup_settings_sha256 )
