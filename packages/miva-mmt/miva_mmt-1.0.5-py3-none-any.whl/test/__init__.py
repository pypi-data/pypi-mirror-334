import os
import sys
import json
import base64
import shutil
import typing
import hashlib
import tempfile
import unittest

import requests
import requests.models

import merchantapi.client
import merchantapi.model
import merchantapi.request
import merchantapi.response

from mmt.commands import Command
from mmt.commands.branch import BranchListCommand, BranchCreateCommand, BranchDeleteCommand
from mmt.commands.checkout import CheckoutCommand
from mmt.commands.config import ConfigListCommand, ConfigSetCommand, ConfigDeleteCommand
from mmt.commands.credential import CredentialListCommand, CredentialAddCommand, CredentialUpdateCommand, CredentialDeleteCommand
from mmt.commands.diff import DiffCommand
from mmt.commands.info import InfoCommand
from mmt.commands.log import LogCommand
from mmt.commands.pull import PullCommand
from mmt.commands.push import PushCommand
from mmt.commands.remote import RemoteListCommand, RemoteAddCommand, RemoteUpdateCommand, RemoteDeleteCommand
from mmt.commands.revert import RevertCommand
from mmt.commands.status import StatusCommand
from mmt.commands.switch import SwitchCommand
from mmt.commands.tag import TagListCommand, TagAddCommand, TagSetCommand, TagDeleteCommand


class MMTOutputBuffer:
	def __init__( self ):
		self._data = ''

	def __enter__( self ):
		self._stdout	= sys.stdout
		sys.stdout		= self

		return self

	def __exit__( self, _type, value, trace ):
		sys.stdout = self._stdout

	def write( self, data: str ):
		self._data += data

	@property
	def data( self ) -> str:
		return self._data


class MMTTest( unittest.TestCase ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		self.maxDiff					= None

		self._global_config_file		= os.path.join( os.path.expanduser( '~' ), '.mmt', 'config.json' )
		self._global_config_file_bak	= f'{self._global_config_file}.bak'
		self._base_directory			= os.path.dirname( __file__ )
		self._checkout_directories		= []

		with open( os.path.join( self._base_directory, 'config.json' ) ) as fh:
			self._config = json.load( fh )

	def setUp( self ):
		try:
			os.rename( self._global_config_file, self._global_config_file_bak )
		except FileNotFoundError:
			pass

	def tearDown( self ):
		try:
			os.rename( self._global_config_file_bak, self._global_config_file )
		except FileNotFoundError:
			pass

		for checkout_directory in self._checkout_directories:
			for root, dirs, files in os.walk( checkout_directory, topdown = False ):
				for name in files:
					os.remove( os.path.join( root, name ) )

				for name in dirs:
					os.rmdir( os.path.join( root, name ) )

			os.rmdir( checkout_directory )

	def merchantapi_client( self ) -> merchantapi.client.Client:
		return merchantapi.client.Client( self._config.get( 'api_url' ), self._config.get( 'api_token' ), self._config.get( 'api_signing_key' ), { 'default_store_code': self._config.get( 'store_code' ) } )

	def generate_random( self ) -> str:
		return hashlib.md5( os.urandom( 64 ) ).hexdigest()[ : 16 ]

	def checkout_path( self ):
		self._checkout_directories.append( tempfile.mkdtemp() )

		return self._checkout_directories[ -1 ]

	def checkout_args( self, remote_key: typing.Optional[ str ] = None, c: int = 0, ignore_unsynced_templates: bool = True, ignore_unsynced_properties: bool = True, include_hidden_settings: bool = False, reinitialize: bool = False, path: typing.Optional[ str ] = None ):
		if remote_key is None:
			remote_key		= self.generate_random()
			credential_key	= self.generate_random()

			self.credential_add( credential_key )
			self.remote_add( remote_key, credential_key = credential_key )

		if path is None:
			path = self.checkout_path()

		args									= {}
		args[ 'remote-key' ]					= remote_key
		args[ 'path' ]							= path
		args[ 'c' ]								= c
		args[ 'ignore_unsynced_templates' ]		= ignore_unsynced_templates
		args[ 'ignore_unsynced_properties' ]	= ignore_unsynced_properties
		args[ 'include_hidden_settings' ]		= include_hidden_settings
		args[ 'reinitialize' ]					= reinitialize

		return args

	def import_domain_provisioning_file( self, *args, **kwargs ) -> merchantapi.response.ProvisionDomain:
		return self._import_provisioning_file_lowlevel( merchantapi.request.ProvisionDomain(), *args, **kwargs )

	def import_store_provisioning_file( self, *args, **kwargs ) -> merchantapi.response.ProvisionStore:
		return self._import_provisioning_file_lowlevel( merchantapi.request.ProvisionStore(), *args, **kwargs )

	def _import_provisioning_file_lowlevel( self, request: typing.Union[ merchantapi.request.ProvisionDomain, merchantapi.request.ProvisionStore ], filepath: str, searchreplace_list: typing.Optional[ typing.List [ typing.Tuple[ str, str ] ] ] = None ) -> typing.Union[ merchantapi.response.ProvisionDomain, merchantapi.response.ProvisionStore ]:
		with open( os.path.join( self._base_directory, 'provisioning_files', filepath ), 'r' ) as fh:
			data = fh.read()

		if searchreplace_list is not None:
			for search, replace in searchreplace_list:
				data = data.replace( search, replace )

		request.set_client( self.merchantapi_client() )
		request.set_xml( data )

		return request.send()

	def delete_directory( self, directory: str ):
		shutil.rmtree( directory )

	@property
	def config( self ) -> dict:
		return self._config

	# Helper Functions

	def latest_changeset_id( self ) -> int:
		return self.changeset_load_latest().get_id()

	def set_diff_tool( self ):
		with open( 'diff.sh', 'w' ) as fh:
			fh.write( '#!/bin/bash\n' )
			fh.write( 'cat $1 > diff.old && cat $2 > diff.new' )

		os.chmod( 'diff.sh', 0o755 )

		self.config_set( 'diff', [ os.path.join( os.getcwd(), 'diff.sh' ) ] )

	def changeset_load_latest( self ) -> merchantapi.model.Changeset:
		request = merchantapi.request.ChangesetListLoadQuery( self.merchantapi_client() )
		request.set_branch_name( self.config.get( 'branch_name' ) )
		request.set_sort( 'id', request.SORT_DESCENDING )
		request.set_count( 1 )

		response = request.send()
		self.assertTrue( response.is_success(), f'ChangesetList_Load_Query failed: {response.get_error_code()}: {response.get_error_message()}' )
		self.assertEqual( len( response.get_changesets() ), 1, 'Failed to load latest changeset' )

		return response.get_changesets()[ 0 ]

	def upload_js_file_from_data( self, filename: str, data: str, params: typing.Optional[ dict ] = None, file_overwrite: bool = True ) -> requests.models.Response:
		if params is None:
			params = {}

		return self.upload_file_from_data( 'JavaScriptResource_Upload', 'Script', filename, data, params, file_overwrite )

	def upload_css_file_from_data( self, filename: str, data: str, params: typing.Optional[ dict ] = None, file_overwrite: bool = True ) -> requests.models.Response:
		if params is None:
			params = {}

		return self.upload_file_from_data( 'CSSResource_Upload', 'Script', filename, data, params, file_overwrite )

	def upload_file_from_data( self, function: str, fieldname: str, filename: str, data: str, params: typing.Optional[ dict ] = None, file_overwrite: bool = True ) -> requests.models.Response:
		if params is None:
			params = {}

		params[ 'Username' ]					= self.config.get( 'admin_username' )
		params[ 'Password' ]					= self.config.get( 'admin_password' )
		params[ 'Session_Type' ]				= 'admin'
		params[ 'Function' ]					= function
		params[ 'TemporarySession' ]			= 1
		params[ 'Store_Code' ]					= self.config.get( 'store_code' )

		if file_overwrite:
			params[ 'FileUpload_Overwrite' ]	= 1

		return requests.post( self.config.get( 'api_url' ), data = params, files = { fieldname: ( filename, data ) } )

	def branch_load_api( self, name: str ) -> merchantapi.model.Branch:
		request = merchantapi.request.BranchListLoadQuery( self.merchantapi_client() )
		request.set_count( 1 )
		request.set_filters( request.filter_expression().equal( 'name', name ) )

		response = request.send()
		self.assertTrue( response.is_success(), f'BranchList_Load_Query failed: {response.get_error_code()}: {response.get_error_message()}' )
		self.assertEqual( len( response.get_branches() ), 1, 'Branch does not exist' )

		return response.get_branches()[ 0 ]

	def branch_create_api( self, name: str, parent_branch_id: int = 1, color: typing.Optional[ str ] = None, tags: typing.Optional[ str ] = None ) -> merchantapi.model.Branch:
		request = merchantapi.request.BranchCreate( self.merchantapi_client() )
		request.set_name( name )
		request.set_parent_branch_id( parent_branch_id )
		request.set_tags( tags )
		request.set_color( color )

		response = request.send()
		self.assertTrue( response.is_success(), f'Branch_Create failed: {response.get_error_code()}: {response.get_error_message()}' )

		return response.get_branch()

	def branch_delete_all_api( self ):
		request = merchantapi.request.BranchListLoadQuery( self.merchantapi_client() )

		response = request.send()
		self.assertTrue( response.is_success(), f'BranchList_Load_Query failed: {response.get_error_code()}: {response.get_error_message()}' )

		request = merchantapi.request.BranchListDelete( self.merchantapi_client() )

		for branch in response.get_branches():
			if not branch.get_is_primary():
				request.add_branch( branch )

		request.send()

	def load_runtime_screen( self, screen: str, store_code: typing.Optional[ str ] = None, additional_parameters: typing.Optional[ dict ] = None ) -> str:
		if additional_parameters is None:
			additional_parameters = {}

		additional_parameters[ 'Store_Code' ]	= store_code or self._config.get( 'store_code' )
		additional_parameters[ 'Screen' ]		= screen

		return requests.get( self._config.get( 'api_url' ).replace( 'json.mvc', 'merchant.mvc' ), params = additional_parameters ).text

	def json_loads( self, data: typing.AnyStr ) -> typing.Any:
		return json.loads( data )

	def json_dumps( self, data: typing.Any ) -> str:
		return json.dumps( data, indent = 4 )

	def base64_encode( self, data: bytes ) -> bytes:
		return base64.b64encode( data )

	def other_data_path( self, filename: str ) -> str:
		return os.path.join( self._base_directory, 'other_data', filename )

	def other_data_open( self, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.other_data_path( filename ), mode )

	def template_path( self, filename: str ) -> str:
		return os.path.join( 'templates', filename )

	def template_open( self, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.template_path( filename ), mode )

	def property_path( self, _type: str, filename: str ) -> str:
		return os.path.join( 'properties', _type, filename )

	def property_open( self, _type: str, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.property_path( _type, filename ), mode )

	def property_product_path( self, _type: str, filename: str ) -> str:
		return os.path.join( 'properties', 'product', _type, filename )

	def property_product_open( self, _type: str, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.property_product_path( _type, filename ), mode )

	def property_category_path( self, _type: str, filename: str ) -> str:
		return os.path.join( 'properties', 'category', _type, filename )

	def property_category_open( self, _type: str, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.property_category_path( _type, filename ), mode )

	def jsresource_path( self, filename: str ) -> str:
		return os.path.join( 'js', filename )

	def jsresource_open( self, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.jsresource_path( filename ), mode )

	def cssresource_path( self, filename: str ) -> str:
		return os.path.join( 'css', filename )

	def cssresource_open( self, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.cssresource_path( filename ), mode )

	def resourcegroup_path( self, filename: str ) -> str:
		return os.path.join( 'resourcegroups', filename )

	def resourcegroup_open( self, filename: str, mode: str = 'r' ) -> typing.TextIO:
		return open( self.resourcegroup_path( filename ), mode )

	def load_expected_results( self, filename: str ) -> dict:
		with open( os.path.join( self._base_directory, 'expected_results', filename ) ) as fh:
			return self.json_loads( fh.read() )

	def load_state_file( self ) -> dict:
		with open( os.path.join( '.mmt', 'state.json' ) ) as fh:
			return self.json_loads( fh.read() )

	def load_global_config( self ) -> dict:
		with open( self._global_config_file ) as fh:
			return self.json_loads( fh.read() )

	def assertSettingsEqual( self, settings: str, expected_settings: dict, settings_sub_section: typing.Optional[ str ] = None ):
		settings = self.json_loads( settings )

		if settings_sub_section is not None:
			settings = settings.get( settings_sub_section )

		for key in expected_settings:
			self.assertIn( key, settings )
			self.assertEqual( expected_settings[ key ], settings[ key ] )

	def assertFileModified( self, data: str, action: str, filepath: str ):
		modifications	= list( map( lambda x: x.strip(), data.strip().split( '\n' ) ) )
		search			= f'{action}: {filepath}'

		self.assertTrue( search in modifications, f'"{search}" not found in { modifications }' )

	def assertFileExists( self, filepath: str ):
		self.assertTrue( os.path.exists( filepath ) )

	def assertFileNotExists( self, filepath: str ):
		self.assertFalse( os.path.exists( filepath ) )

	# Command wrappers

	def _run_command( self, command: Command ) -> str:
		with MMTOutputBuffer() as buf:
			command.validate()
			command.initialize()
			command.run()

		return buf.data.strip()

	def checkout( self, *args, **kwargs ) -> str:
		try:
			arguments = kwargs[ 'args' ]
		except KeyError:
			arguments = self.checkout_args( *args, **kwargs )

		retval = self._run_command( CheckoutCommand( arguments ) )
		os.chdir( arguments.get( 'path' ) )

		return retval

	def pull( self, c: int = 0, filepaths: typing.Optional[ typing.List[ str ] ] = None, force: bool = False ) -> str:
		if filepaths is None:
			filepaths = []

		return self._run_command( PullCommand( { 'c': c, 'filepaths': filepaths, 'force': force } ) )

	def push( self, notes: str or None, filepaths: typing.Optional[ typing.List[ str ] ] = None ) -> str:
		if filepaths is None:
			filepaths = []

		return self._run_command( PushCommand( { 'notes': notes, 'filepaths': filepaths } ) )

	def status( self ) -> str:
		return self._run_command( StatusCommand( {} ) )

	def revert( self, _all: bool = True, filepaths: typing.Optional[ typing.List[ str ] ] = None ) -> str:
		if filepaths is None:
			filepaths = []

		return self._run_command( RevertCommand( { 'all': _all, 'filepaths': filepaths } ) )

	def diff( self, filepaths: typing.Optional[ typing.List[ str ] ] = None ) -> str:
		if filepaths is None:
			filepaths = []

		return self._run_command( DiffCommand( { 'filepaths': filepaths } ) )

	def credential_list( self ) -> str:
		return self._run_command( CredentialListCommand( {} ) )

	def credential_add( self, key: str, url: typing.Optional[ str ] = None, token: typing.Optional[ str ] = None, signing_key: typing.Optional[ str ] = None, ssh_username: typing.Optional[ str ] = None, ssh_private_key: typing.Optional[ str ] = None, http_basic_auth_username: typing.Optional[ str ] = None, http_basic_auth_password: typing.Optional[ str ] = None ) -> str:
		if url is None:
			url = self._config.get( 'api_url' )

		params = { 'credential_command': 'add', 'key': key, 'url': url, 'http_basic_auth_username': http_basic_auth_username, 'http_basic_auth_password': http_basic_auth_password }

		if ssh_username is not None or ssh_private_key is not None:
			if ssh_username is None:
				ssh_username = self.config.get( 'admin_username' )

			params[ 'ssh_username' ]	= ssh_username
			params[ 'ssh_private_key' ]	= ssh_private_key
		else:
			if token is None:
				token = self._config.get( 'api_token' )

			if signing_key is None:
				signing_key = self._config.get( 'api_signing_key' )

			params[ 'token' ]		= token
			params[ 'signing_key' ]	= signing_key

		return self._run_command( CredentialAddCommand( params ) )

	def credential_update( self, key: str, new_key: typing.Optional[ str ] = None, url: typing.Optional[ str ] = None, token: typing.Optional[ str ] = None, signing_key: typing.Optional[ str ] = None, ssh_username: typing.Optional[ str ] = None, ssh_private_key: typing.Optional[ str ] = None, http_basic_auth_username: typing.Optional[ str ] = None, http_basic_auth_password: typing.Optional[ str ] = None ) -> str:
		return self._run_command( CredentialUpdateCommand( { 'credential_command': 'update', 'key': key, 'credential_key': new_key, 'url': url, 'token': token, 'signing_key': signing_key, 'ssh_username': ssh_username, 'ssh_private_key': ssh_private_key, 'http_basic_auth_username': http_basic_auth_username, 'http_basic_auth_password': http_basic_auth_password } ) )

	def credential_delete( self, key: str ) -> str:
		return self._run_command( CredentialDeleteCommand( { 'key': key } ) )

	def remote_list( self ) -> str:
		return self._run_command( RemoteListCommand( {} ) )

	def remote_add( self, key: str, credential_key: typing.Optional[ str ] = None, store_code: typing.Optional[ str ] = None, branch_name: typing.Optional[ str ] = None ) -> str:
		if credential_key is None:
			credential_key = self.generate_random()
			self.credential_add( credential_key )

		if store_code is None:
			store_code = self.config.get( 'store_code' )

		if branch_name is None:
			branch_name = self.config.get( 'branch_name' )

		return self._run_command( RemoteAddCommand( { 'key': key, 'credential_key': credential_key, 'store_code': store_code, 'branch_name': branch_name } ) )

	def remote_update( self, key: str, new_key: typing.Optional[ str ] = None, credential_key: typing.Optional[ str ] = None, store_code: typing.Optional[ str ] = None, branch_name: typing.Optional[ str ] = None ) -> str:
		return self._run_command( RemoteUpdateCommand( { 'key': key, 'remote_key': new_key, 'credential_key': credential_key, 'store_code': store_code, 'branch_name': branch_name } ) )

	def remote_delete( self, key: typing.List[ str ] ) -> str:
		return self._run_command( RemoteDeleteCommand( { 'key': key } ) )

	def switch( self, remote_key: str ) -> str:
		return self._run_command( SwitchCommand( { 'remote-key': remote_key } ) )

	def tag_list( self ) -> str:
		return self._run_command( TagListCommand( {} ) )

	def tag_add( self, tags: typing.List[ str ] ) -> str:
		return self._run_command( TagAddCommand( { 'tags': tags } ) )

	def tag_set( self, tags: typing.List[ str ] ) -> str:
		return self._run_command( TagSetCommand( { 'tags': tags } ) )

	def tag_delete( self, tags: typing.List[ str ] ) -> str:
		return self._run_command( TagDeleteCommand( { 'tags': tags, 'all': False } ) )

	def tag_delete_all( self ) -> str:
		return self._run_command( TagDeleteCommand( { 'tags': [], 'all': True } ) )

	def info( self ) -> str:
		return self._run_command( InfoCommand( {} ) )

	def config_list( self ) -> str:
		return self._run_command( ConfigListCommand( {} ) )

	def config_set( self, key: str, value: typing.Any ) -> str:
		return self._run_command( ConfigSetCommand( { 'key': key, 'value': value } ) )

	def config_delete( self, key: str ) -> str:
		return self._run_command( ConfigDeleteCommand( { 'key': key } ) )

	def log( self, **kwargs ):
		return self._run_command( LogCommand( kwargs ) )

	def branch_list( self, credential_key: typing.Optional[ str ] = None, store_code: typing.Optional[ str ] = None ) -> str:
		if credential_key is None:
			credential_key = self.generate_random()
			self.credential_add( credential_key )

		if store_code is None:
			store_code = self.config.get( 'store_code' )

		return self._run_command( BranchListCommand( { 'credential_key': credential_key, 'store_code': store_code } ) )

	def branch_create( self, name: str, remote_key: typing.Optional[ str ] = None, credential_key: typing.Optional[ str ] = None, _from: typing.Optional[ str ] = None, store_code: typing.Optional[ str ] = None, color: typing.Optional[ str ] = None ) -> str:
		args			= {}
		args[ 'name' ]	= name

		if color is not None:
			args[ 'color' ]	= color

		if remote_key is not None:
			args[ 'remote_key' ] = remote_key
		else:
			if credential_key is not None:
				args[ 'credential_key' ] = credential_key
			else:
				credential_key = self.generate_random()
				self.credential_add( credential_key )

				args[ 'credential_key' ] = credential_key

			if _from is not None:
				args[ 'from' ] = _from
			else:
				args[ 'from' ] = self.config.get( 'branch_name' )

			if store_code is not None:
				args[ 'store_code' ] = store_code
			else:
				args[ 'store_code' ] = self.config.get( 'store_code' )

		return self._run_command( BranchCreateCommand( args ) )

	def branch_delete( self, name: str, credential_key: typing.Optional[ str ] = None, store_code: typing.Optional[ str ] = None, raise_exception: bool = False ) -> str:
		if credential_key is None:
			credential_key = self.generate_random()
			self.credential_add( credential_key )

		if store_code is None:
			store_code = self.config.get( 'store_code' )

		try:
			return self._run_command( BranchDeleteCommand( { 'credential_key': credential_key, 'name': name, 'store_code': store_code } ) )
		except Exception:
			if raise_exception:
				raise

			return ''
