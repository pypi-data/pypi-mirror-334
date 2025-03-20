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

Prefix         : MMT-COMMAND-
Next Error Code: 16
"""

import os
import abc
import json
import base64
import typing
import getpass
import hashlib

import merchantapi.abstract
import merchantapi.authenticator
import merchantapi.client
import merchantapi.model
import merchantapi.logging
import merchantapi.listquery

from mmt.version import __version__ as version
from mmt.exceptions import Error, APIRequestError, APIResponseError
from mmt.file import File, BinaryFile
from mmt.managers.config import ConfigManager
from mmt.managers.remote import Remote
from mmt.managers.credential import CredentialToken, CredentialSSH
from mmt.metadata.state import StateMetadataFile, StateMetadataEntryFile, StateMetadataBaseTemplateFile, StateMetadataBasePropertyFile, StateMetadataBaseJSResourceFile, StateMetadataBaseCSSResourceFile, StateMetadataBaseResourceGroupFile


class Command( abc.ABC ):
	def __init__( self, args: dict ):
		if args.get( 'path' ) is None:
			args[ 'path' ]					= '.'

		for key, value in args.items():
			if type( value ) is str:
				args[ key ]					= value.strip()

		self._args							= args

		self._root_directory				= os.path.normpath( args.get( 'path' ) )
		self._templates_directory			= os.path.join( self._root_directory, 'templates' )
		self._properties_directory			= os.path.join( self._root_directory, 'properties' )
		self._js_directory					= os.path.join( self._root_directory, 'js' )
		self._css_directory					= os.path.join( self._root_directory, 'css' )
		self._resourcegroups_directory		= os.path.join( self._root_directory, 'resourcegroups' )

		self._global_metadata_directory		= os.path.join( os.path.expanduser( '~' ), '.mmt' )
		self._local_metadata_directory		= os.path.join( self._root_directory, '.mmt' )

		self._state							= StateMetadataFile( self._root_directory, self._local_metadata_directory )

		self._configmanager					= ConfigManager( self._global_metadata_directory, self._local_metadata_directory )

		self._cached_client					= None
		self._cached_remote					= None
		self._cached_credential				= None

		self._request_logger				= None

		if args.get( 'debug' ):
			self._request_logger			= merchantapi.logging.ConsoleLogger( 'stdout' )

	def validate( self ):
		pass

	def initialize( self ):
		pass

	@abc.abstractmethod
	def run( self ):
		raise NotImplementedError

	@property
	def args( self ) -> dict:
		return self._args

	@property
	def root_directory( self ) -> str:
		return self._root_directory

	@property
	def local_metadata_directory( self ) -> str:
		return self._local_metadata_directory

	@property
	def templates_directory( self ) -> str:
		return self._templates_directory

	@property
	def properties_directory( self ) -> str:
		return self._properties_directory

	@property
	def js_directory( self ) -> str:
		return self._js_directory

	@property
	def css_directory( self ) -> str:
		return self._css_directory

	@property
	def resourcegroups_directory( self ) -> str:
		return self._resourcegroups_directory

	@property
	def configmanager( self ) -> ConfigManager:
		return self._configmanager

	@property
	def state( self ) -> StateMetadataFile:
		return self._state

	# Helper Functions

	def filter_expression( self ):
		return MMTFilterExpression()

	def load_remote( self, remote_key: str ) -> Remote:
		if self._cached_remote is not None and self._cached_remote.key == remote_key:
			return self._cached_remote

		remote = self.configmanager.remote_lookup( remote_key )

		if remote is None:
			raise Error( 'MMT-COMMAND-00010', f'Remote key \'{self.configmanager.remote_key}\' does not exist' )

		self._cached_remote = remote

		return self._cached_remote

	def load_credential( self, credential_key: str ) -> typing.Union[ CredentialToken, CredentialSSH ]:
		if self._cached_credential is not None and self._cached_credential.key == credential_key:
			return self._cached_credential

		credential = self.configmanager.credential_lookup( credential_key )

		if credential is None:
			raise Error( 'MMT-COMMAND-00011', f'Credential key \'{credential_key}\' does not exist' )

		self._cached_credential = credential

		return self._cached_credential

	def _build_request_client( self, credential: typing.Union[ CredentialToken, CredentialSSH ] ) -> typing.Union[ merchantapi.client.Client, merchantapi.client.SSHClient ]:
		if self._cached_client is not None:
			return self._cached_client

		if credential.is_token():
			self._cached_client = merchantapi.client.Client( credential.url, credential.token, credential.signing_key )

			return self._cached_client

		if credential.is_ssh():
			# Attempt to create an SSHClient without supplying a password
			try:
				self._cached_client = merchantapi.client.SSHClient( credential.url, credential.username, credential.filepath )
			except FileNotFoundError:
				raise Error( 'MMT-COMMAND-00014', f'SSH private key \'{credential.filepath}\' does not exist' )
			except merchantapi.authenticator.SSHPrivateKeyPasswordError:
				# The private key requires a password so prompt the user for the password
				for attempt in range( 3 ):
					password = None

					try:
						password = getpass.getpass()
					except KeyboardInterrupt:
						print( '' )
						quit()

					try:
						self._cached_client = merchantapi.client.SSHClient( credential.url, credential.username, credential.filepath, password )
					except merchantapi.authenticator.SSHPrivateKeyPasswordError:
						print( 'Sorry, try again.' )
						continue
					else:
						return self._cached_client

				raise Error( 'MMT-COMMAND-00008', 'Incorrect private key password' )
			else:
				return self._cached_client

		raise Error( 'MMT-COMMAND-00009', 'Unknown credential' )

	def send_request( self, request: merchantapi.abstract.Request ) -> merchantapi.abstract.Response:
		remote = self.load_remote( self.configmanager.remote_key )

		return self.send_request_lowlevel( request, remote.credential_key, remote.store_code )

	def send_request_lowlevel( self, request: merchantapi.abstract.Request, credential_key: str, store_code: str ) -> merchantapi.abstract.Response:
		credential	= self.load_credential( credential_key )
		client		= self._build_request_client( credential )
		client.set_option( 'default_store_code', store_code )
		client.set_global_header( 'User-Agent', f'MMT/{version}' )
		client.set_logger( self._request_logger )

		if credential.http_basic_auth_username is not None and credential.http_basic_auth_password is not None:
			encoded = self.base64_encode( f'{credential.http_basic_auth_username}:{credential.http_basic_auth_password}'.encode( 'utf-8' ) ).decode( 'ascii' )

			client.set_global_header( 'Authorization', f'Basic {encoded}' )

		request.set_client( client )

		try:
			response = request.send()
		except merchantapi.client.ClientHttpAuthenticationError:
			if client.has_global_header( 'Authorization' ):
				error_message = 'Invalid HTTP Basic Authentication credentials'
			else:
				error_message = 'Missing HTTP Basic Authentication credentials'

			raise Error( 'MMT-COMMAND-00015', error_message )
		except merchantapi.client.ClientException as e:
			raise APIRequestError( request.get_function(), 'MMT-COMMAND-00002', str( e ) )
		except KeyboardInterrupt:
			quit()

		if response.is_error():
			raise APIResponseError( response )

		return response

	def send_request_base64( self, request: merchantapi.abstract.Request ) -> merchantapi.abstract.Response:
		request.set_binary_encoding( request.BINARY_ENCODING_BASE64 )

		return self.send_request( request )

	def base64_decode( self, data: typing.AnyStr ) -> bytes:
		return base64.b64decode( data )

	def base64_encode( self, data: bytes ) -> bytes:
		return base64.b64encode( data )

	def json_dumps( self, data: typing.Any ) -> str:
		return json.dumps( data, indent = 4 )

	def json_dumps_exclude_hidden_keys( self, data: typing.AnyStr ) -> str:
		def delete_hidden_keys( data: typing.AnyStr ):
			if isinstance( data, list ):
				for value in data:
					delete_hidden_keys( value )
			elif isinstance( data, dict ):
				for key in data.copy():
					if key.startswith( '.' ):
						del data[ key ]
					else:
						delete_hidden_keys( data[ key ] )

		delete_hidden_keys( data )

		return self.json_dumps( data )

	def json_loads( self, data: typing.AnyStr ) -> typing.Any:
		return json.loads( data )

	def calculate_sha256( self, data: typing.AnyStr, encoding: str = 'utf-8' ) -> str:
		if isinstance( data, str ):
			data = data.encode( encoding )

		return hashlib.sha256( data ).hexdigest()

	def is_json_empty( self, data: typing.Any ) -> bool:
		return isinstance( data, str ) and len( data ) == 0 # JSON is considered empty only if the object is a string and the string length is 0

	def build_branch_tags( self ) -> str:
		return ' '.join( [ f'#{branch_tag}' for branch_tag in self.configmanager.branch_tags ] )

	def ensure_toplevel_directories_exist( self ):
		self.ensure_path_exists( self.templates_directory )
		self.ensure_path_exists( self.properties_directory )
		self.ensure_path_exists( self.js_directory )
		self.ensure_path_exists( self.css_directory )
		self.ensure_path_exists( self.resourcegroups_directory )

	def ensure_path_exists( self, path: str ):
		try:
			os.makedirs( path, exist_ok = True )
		except Exception as e:
			raise Error( 'MMT-COMMAND-00003', f'Failed to create directory \'{path}\': {e}' )

	def ensure_property_path_exists( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ):
		self.ensure_path_exists( os.path.join( os.path.abspath( self._root_directory ), self._build_property_path( branchpropertyversion ) ) )

	def load_modified_files( self, filtered_filepaths: typing.Optional[ typing.Set[ str ] ] = None ) -> typing.List[ typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ] ]:
		if filtered_filepaths is None:
			filtered_filepaths = []

		modified_files			= []
		apply_filepath_filter	= len( filtered_filepaths ) > 0

		for state_file in self.state.filemanager.files:
			if apply_filepath_filter:
				if state_file.filepath not in filtered_filepaths:
					continue

			if state_file.sha256_hash == state_file.file.sha256_hash:
				continue

			modified_files.append( ( state_file, state_file.file ) )

		return modified_files

	def group_modified_template_files( self, modified_files: typing.List[ typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ] ] ) -> typing.List[ typing.Tuple[ StateMetadataBaseTemplateFile, typing.Union[ File, BinaryFile ] ] ]:
		return list( filter( lambda modified_file: modified_file[ 0 ].is_template(), modified_files ) )

	def group_modified_property_files( self, modified_files: typing.List[ typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ] ] ) -> typing.List[ typing.Tuple[ StateMetadataBasePropertyFile, typing.Union[ File, BinaryFile ] ] ]:
		return list( filter( lambda modified_file: modified_file[ 0 ].is_property(), modified_files ) )

	def group_modified_jsresource_files( self, modified_files: typing.List[ typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ] ] ) -> typing.List[ typing.Tuple[ StateMetadataBaseJSResourceFile, typing.Union[ File, BinaryFile ] ] ]:
		return list( filter( lambda modified_file: modified_file[ 0 ].is_jsresource(), modified_files ) )

	def group_modified_cssresource_files( self, modified_files: typing.List[ typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ] ] ) -> typing.List[ typing.Tuple[ StateMetadataBaseCSSResourceFile, typing.Union[ File, BinaryFile ] ] ]:
		return list( filter( lambda modified_file: modified_file[ 0 ].is_cssresource(), modified_files ) )

	def group_modified_resourcegroup_files( self, modified_files: typing.List[ typing.Tuple[ StateMetadataEntryFile, typing.Union[ File, BinaryFile ] ] ] ) -> typing.List[ typing.Tuple[ StateMetadataBaseResourceGroupFile, typing.Union[ File, BinaryFile ] ] ]:
		return list( filter( lambda modified_file: modified_file[ 0 ].is_resourcegroup(), modified_files ) )

	def get_branchtemplateversion_filename( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> str:
		return branchtemplateversion.get_filename()

	def get_branchtemplateversion_template_data( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> bytes:
		return self.base64_decode( branchtemplateversion.get_source() )

	def get_branchtemplateversion_template_settings_data( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> str:
		if not self.configmanager.include_hidden_settings:
			return self.json_dumps_exclude_hidden_keys( branchtemplateversion.get_settings().get_data() )
		else:
			return self.json_dumps( branchtemplateversion.get_settings().get_data() )

	def is_branchtemplateversion_template_settings_empty( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> bool:
		return self.is_json_empty( branchtemplateversion.get_settings().get_data() )

	def get_branchpropertyversion_template_data( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> bytes:
		return self.base64_decode( branchpropertyversion.get_source() )

	def get_branchpropertyversion_settings_data( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		if not self.configmanager.include_hidden_settings:
			return self.json_dumps_exclude_hidden_keys( branchpropertyversion.get_settings().get_data() )
		else:
			return self.json_dumps( branchpropertyversion.get_settings().get_data() )

	def is_branchpropertyversion_settings_empty( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> bool:
		return self.is_json_empty( branchpropertyversion.get_settings().get_data() )

	def get_branchpropertyversion_group( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		if len( branchpropertyversion.get_code() ):
			return ''
		elif branchpropertyversion.get_product_id():
			return 'product'
		elif branchpropertyversion.get_category_id():
			return 'category'

		raise Error( 'MMT-COMMAND-00013', 'Failed to determine property group' )

	def get_branchpropertyversion_type( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		return branchpropertyversion.get_type()

	def get_branchpropertyversion_code( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		if len( branchpropertyversion.get_code() ):
			return branchpropertyversion.get_code()
		elif branchpropertyversion.get_product_id():
			return branchpropertyversion.get_product().get( 'code' )
		elif branchpropertyversion.get_category_id():
			return branchpropertyversion.get_category().get( 'code' )

		raise Error( 'MMT-COMMAND-00004', 'Failed to determine property code' )

	def get_branchjavascriptresourceversion_code( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> str:
		return branchjavascriptresourceversion.get_code()

	def get_branchjavascriptresourceversion_type( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> str:
		return branchjavascriptresourceversion.get_type()

	def get_branchjavascriptresourceversion_settings_data( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> str:
		return self.json_dumps( self.build_jsresource_settings( branchjavascriptresourceversion ) )

	def get_branchjavascriptresourceversion_inline_data( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> bytes:
		if self.get_branchjavascriptresourceversion_type( branchjavascriptresourceversion ) != 'I':
			return b''

		return self.base64_decode( branchjavascriptresourceversion.get_source() )

	def get_branchjavascriptresourceversion_local_data( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> bytes:
		if self.get_branchjavascriptresourceversion_type( branchjavascriptresourceversion ) != 'L':
			return b''

		return self.base64_decode( branchjavascriptresourceversion.get_source() )

	def get_branchcssresourceversion_code( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ):
		return branchcssresourceversion.get_code()

	def get_branchcssresourceversion_type( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> str:
		return branchcssresourceversion.get_type()

	def get_branchcssresourceversion_settings_data( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> str:
		return self.json_dumps( self.build_cssresource_settings( branchcssresourceversion ) )

	def get_branchcssresourceversion_inline_data( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> bytes:
		if self.get_branchcssresourceversion_type( branchcssresourceversion ) != 'I':
			return b''

		return self.base64_decode( branchcssresourceversion.get_source() )

	def get_branchcssresourceversion_local_data( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> bytes:
		if self.get_branchcssresourceversion_type( branchcssresourceversion ) != 'L':
			return b''

		return self.base64_decode( branchcssresourceversion.get_source() )

	def get_resourcegroup_code( self, resourcegroup: merchantapi.model.ResourceGroup ) -> str:
		return resourcegroup.get_code()

	def get_resourcegroup_settings_data( self, resourcegroup: merchantapi.model.ResourceGroup ) -> str:
		return self.json_dumps( self.build_resourcegroup_settings( resourcegroup ) )

	# Compare state file to an object

	def template_equals_branchtemplateversion( self, state_file: StateMetadataBaseTemplateFile, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> bool:
		return state_file.template_filename == self.get_branchtemplateversion_filename( branchtemplateversion )

	def property_equals_branchpropertyversion( self, state_file: StateMetadataBasePropertyFile, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> bool:
		return state_file.property_group == self.get_branchpropertyversion_group( branchpropertyversion ) and state_file.property_type == self.get_branchpropertyversion_type( branchpropertyversion ) and state_file.property_code == self.get_branchpropertyversion_code( branchpropertyversion )

	def jsresource_equals_branchjavascriptresourceversion( self, state_file: StateMetadataBaseJSResourceFile, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> bool:
		return state_file.jsresource_code == self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )

	def cssresource_equals_branchcssresourceversion( self, state_file: StateMetadataBaseCSSResourceFile, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> bool:
		return state_file.cssresource_code == self.get_branchcssresourceversion_code( branchcssresourceversion )

	def resourcegroup_equals_resourcegroup( self, state_file: StateMetadataBaseResourceGroupFile, resourcegroup: merchantapi.model.ResourceGroup ) -> bool:
		return state_file.resourcegroup_code == self.get_resourcegroup_code( resourcegroup )

	# Filepath helper functions

	def build_template_filepath( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> str:
		return self._build_template_filepath_lowlevel( branchtemplateversion, '.mvt' )

	def build_template_settings_filepath( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> str:
		return self._build_template_filepath_lowlevel( branchtemplateversion, '.json' )

	def build_property_template_filepath( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		return self._build_property_filepath_lowlevel( branchpropertyversion, '.mvt' )

	def build_property_settings_filepath( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		return self._build_property_filepath_lowlevel( branchpropertyversion, '.json' )

	def build_jsresource_settings_filepath( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> str:
		return self._build_jsresource_filepath_lowlevel( branchjavascriptresourceversion, '.json' )

	def build_jsresource_local_filepath( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> str:
		return self._build_jsresource_filepath_lowlevel( branchjavascriptresourceversion, '.js' )

	def build_jsresource_inline_filepath( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> str:
		return self._build_jsresource_filepath_lowlevel( branchjavascriptresourceversion, '.mvt' )

	def build_cssresource_settings_filepath( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> str:
		return self._build_cssresource_filepath_lowlevel( branchcssresourceversion, '.json' )

	def build_cssresource_local_filepath( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> str:
		return self._build_cssresource_filepath_lowlevel( branchcssresourceversion, '.css' )

	def build_cssresource_inline_filepath( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> str:
		return self._build_cssresource_filepath_lowlevel( branchcssresourceversion, '.mvt' )

	def build_resourcegroup_settings_filepath( self, resourcegroup: merchantapi.model.ResourceGroup ) -> str:
		return self._build_resourcegroup_filepath_lowlevel( resourcegroup, '.json' )

	def _build_template_filepath_lowlevel( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion, suffix: str ) -> str:
		return self._build_filepath_lowlevel( 'templates', os.path.splitext( self.get_branchtemplateversion_filename( branchtemplateversion ) )[ 0 ], suffix )

	def _build_jsresource_filepath_lowlevel( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion, suffix: str ) -> str:
		return self._build_filepath_lowlevel( 'js', self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion ), suffix )

	def _build_cssresource_filepath_lowlevel( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion, suffix: str ) -> str:
		return self._build_filepath_lowlevel( 'css', self.get_branchcssresourceversion_code( branchcssresourceversion ), suffix )

	def _build_property_filepath_lowlevel( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion, suffix: str ) -> str:
		return self._build_filepath_lowlevel( self._build_property_path( branchpropertyversion ), self.get_branchpropertyversion_code( branchpropertyversion ), suffix )

	def _build_resourcegroup_filepath_lowlevel( self, resourcegroup: merchantapi.model.ResourceGroup, suffix: str ) -> str:
		return self._build_filepath_lowlevel( 'resourcegroups', self.get_resourcegroup_code( resourcegroup ), suffix )

	def _build_property_path( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> str:
		if len( branchpropertyversion.get_code() ):
			directories = [ branchpropertyversion.get_type() ]
		elif branchpropertyversion.get_product_id():
			directories = [ 'product', branchpropertyversion.get_type() ]
		elif branchpropertyversion.get_category_id():
			directories = [ 'category', branchpropertyversion.get_type() ]
		else:
			raise Error( 'MMT-COMMAND-00005', 'Failed to determine property code' )

		return os.path.join( 'properties', os.sep.join( directories ) )

	def _build_filepath_lowlevel( self, parent_directory: str, filename_no_ext: str, suffix: str ) -> str:
		return os.path.join( parent_directory, f'{self._os_safe_filename_no_ext( filename_no_ext )}{suffix}' )

	def _os_safe_filename_no_ext( self, filename_no_ext: str ) -> str:
		for character in filename_no_ext:
			if not character.isalnum() and not character in [ '-', '_', ' ' ]:
				return hashlib.md5( filename_no_ext.encode( 'utf-8' ) ).hexdigest()

		return filename_no_ext

	# JS resource file helper functions

	def build_jsresource_settings( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> dict:
		data									= {}
		data[ 'code' ]							= branchjavascriptresourceversion.get_code()
		data[ 'type' ]							= branchjavascriptresourceversion.get_type()

		# Only include the filepath member when the file type
		# is either external or local file
		if branchjavascriptresourceversion.get_type() == 'E':
			data[ 'filepath' ]					= branchjavascriptresourceversion.get_file()
		elif branchjavascriptresourceversion.get_type() == 'L':
			if branchjavascriptresourceversion.get_branchless_file() is None:
				data[ 'filepath' ]				= branchjavascriptresourceversion.get_file()
			else:
				data[ 'branchless_filepath' ]	= branchjavascriptresourceversion.get_branchless_file()

		data[ 'is_global' ]						= branchjavascriptresourceversion.get_is_global()
		data[ 'active' ]						= branchjavascriptresourceversion.get_active()
		data[ 'attributes' ]					= []

		for attribute in branchjavascriptresourceversion.get_attributes():
			entry								= {}
			entry[ 'name' ]						= attribute.get_name()
			entry[ 'value' ]					= attribute.get_value()

			data[ 'attributes' ].append( entry )

		# Only build the linked_pages member when dealing with
		# a non-global resource
		if not branchjavascriptresourceversion.get_is_global():
			data[ 'linked_pages' ]				= [ linked_page.get_code() for linked_page in branchjavascriptresourceversion.get_linked_pages() ]

		# Only build the linked_resources member when dealing with
		# a combined resource
		if branchjavascriptresourceversion.get_type() == 'C':
			data[ 'linked_resources' ]			= [ linked_resource.get_code() for linked_resource in branchjavascriptresourceversion.get_linked_resources() ]

		return data

	# CSS resource file helper functions

	def build_cssresource_settings( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> dict:
		data							= {}
		data[ 'code' ]					= branchcssresourceversion.get_code()
		data[ 'type' ]					= branchcssresourceversion.get_type()

		# Only include the filepath member when the file type
		# is either external or local file
		if branchcssresourceversion.get_type() == 'E':
			data[ 'filepath' ]					= branchcssresourceversion.get_file()
		elif branchcssresourceversion.get_type() == 'L':
			if branchcssresourceversion.get_branchless_file() is None:
				data[ 'filepath' ]				= branchcssresourceversion.get_file()
			else:
				data[ 'branchless_filepath' ]	= branchcssresourceversion.get_branchless_file()

		data[ 'is_global' ]						= branchcssresourceversion.get_is_global()
		data[ 'active' ]						= branchcssresourceversion.get_active()
		data[ 'attributes' ]					= []

		for attribute in branchcssresourceversion.get_attributes():
			entry								= {}
			entry[ 'name' ]						= attribute.get_name()
			entry[ 'value' ]					= attribute.get_value()

			data[ 'attributes' ].append( entry )

		# Only build the linked_pages member when dealing with
		# a non-global resource
		if not branchcssresourceversion.get_is_global():
			data[ 'linked_pages' ]				= [ linked_page.get_code() for linked_page in branchcssresourceversion.get_linked_pages() ]

		# Only build the linked_resources member when dealing with
		# a combined resource
		if branchcssresourceversion.get_type() == 'C':
			data[ 'linked_resources' ]			= [ linked_resource.get_code() for linked_resource in branchcssresourceversion.get_linked_resources() ]

		return data

	# Resource Group file helper functions

	def build_resourcegroup_settings( self, resourcegroup: merchantapi.model.ResourceGroup ) -> dict:
		data							= {}
		data[ 'code' ]					= resourcegroup.get_code()
		data[ 'linked_js_resources' ]	= [ linked_js_resource.get_code() for linked_js_resource in resourcegroup.get_linked_java_script_resources() ]
		data[ 'linked_css_resources' ]	= [ linked_css_resource.get_code() for linked_css_resource in resourcegroup.get_linked_css_resources() ]

		return data


class ConfiguredCommand( Command, abc.ABC ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		try:
			self._state.read()
		except FileNotFoundError:
			raise Error( 'MMT-COMMAND-00001', f'MMT has not been configured for path \'{self.root_directory}\'' )

	@abc.abstractmethod
	def run( self ):
		raise NotImplementedError


class MMTFilterExpression( merchantapi.listquery.FilterExpression ):
	def to_list( self ) -> list:
		def lowlevel():
			filters = []

			for e in self.expressions:
				if isinstance( e[  'entry' ], MMTFilterExpression) and ( e[ 'type' ] in MMTFilterExpression.VALID_FILTERS ):
					entry = {
						'field':	e[ 'type' ],
						'operator':	MMTFilterExpression.OPERATOR_SUBWHERE,
						'value':	e[ 'entry' ].to_list()
					}
				else:
					entry = {
						'field':	e[ 'entry' ].get_left(),
						'operator':	e[ 'entry' ].get_operator(),
						'value':	e[ 'entry' ].get_right_joined()
					}

				filters.append(entry)

			return filters

		if self.is_child():
			return lowlevel()

		return [
			{
				'name': MMTFilterExpression.FILTER_SEARCH,
				'value': lowlevel()
			}
		]
