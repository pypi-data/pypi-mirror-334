import os
import typing
import tempfile

from mmt.exceptions import Error
from mmt.commands.credential import CredentialAddCommand, CredentialUpdateCommand
from test import MMTTest


class TestCredentialList( MMTTest ):
	def test_credential_list( self ):
		self.assertEqual( self.credential_list(), '' )

		self.credential_add( key = 'test_credential_list_1', token = 'test_credential_add_token', signing_key = 'test_credential_add_token_signing_key' )
		self.credential_add( key = 'test_credential_list_2', ssh_username = 'Administrator', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )
		self.credential_add( key = 'test_credential_list_3', http_basic_auth_username = 'test_credential_list_username', http_basic_auth_password = 'test_credential_list_password' )

		data = self.credential_list()

		self.assertIn( 'Method: Token',							data )
		self.assertIn( f'URL: {self.config.get( "api_url" )}',	data )
		self.assertIn( 'Token: test_credential_add_token',		data )

		self.assertIn( 'Method: SSH',										data )
		self.assertIn( f'URL: {self.config.get( "api_url" )}',				data )
		self.assertIn( 'Username: Administrator',							data )
		self.assertIn( f'Filepath: {self.other_data_path( "id_rsa_pem" )}', data )

		self.assertIn( 'HTTP Basic Authentication Username: test_credential_list_username',	data )
		self.assertIn( 'HTTP Basic Authentication Password: **********',					data )


class TestCredentialAdd( MMTTest ):
	def test_credential_add_validate( self ):
		# Generic Validation
		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate', url = '' )

		self.assertEqual( e.exception.error_message, 'A URL value is required' )

		self.credential_add( key = 'test_credential_add_validate' )

		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_credential_add_validate\' already exists' )

		# Token Validation
		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate_token', token = '' )

		self.assertEqual( e.exception.error_message, 'An API Token value is required' )

		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate_token', signing_key = '' )

		self.assertEqual( e.exception.error_message, 'An API Signing Key value is required' )

		# SSH Validation
		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate_ssh', ssh_username = '' )

		self.assertEqual( e.exception.error_message, 'An SSH Username value is required' )

		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate_ssh', ssh_private_key = '' )

		self.assertEqual( e.exception.error_message, 'An SSH Private Key value is required' )

		with self.assertRaises( Error ) as e:
			self.credential_add( key = 'test_credential_add_validate_ssh', ssh_private_key = 'invalid_file_path' )

		self.assertEqual( e.exception.error_message, 'SSH Private Key does not exist' )

		# Token and SSH Validation
		with self.assertRaises( Error ) as e:
			self._run_command( CredentialAddCommand( { 'key': 'test_credential_add_validate_both', 'url': 'http://localhost' } ) )

		self.assertEqual( e.exception.error_message, 'One of token authentication or SSH authentication is required' )

		with self.assertRaises( Error ) as e:
			self._run_command( CredentialAddCommand( { 'key': 'test_credential_add_validate_both', 'url': 'http://localhost', 'token': 'some_token', 'ssh_username': 'some_username' } ) )

		self.assertEqual( e.exception.error_message, 'Only one of token authentication or SSH authentication is allowed' )

	def test_credential_add_token( self ):
		self.credential_add( key = 'test_credential_add', token = 'test_credential_add_token', signing_key = 'test_credential_add_token_signing_key' )

		data = self.credential_list()

		self.assertIn( 'Method: Token',							data )
		self.assertIn( f'URL: {self.config.get( "api_url" )}',	data )
		self.assertIn( 'Token: test_credential_add_token',		data )

	def test_credential_add_ssh( self ):
		self.credential_add( key = 'test_credential_add_ssh', ssh_username = 'Administrator', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )

		data = self.credential_list()

		self.assertIn( 'Method: SSH',										data )
		self.assertIn( f'URL: {self.config.get( "api_url" )}',				data )
		self.assertIn( 'Username: Administrator',							data )
		self.assertIn( f'Filepath: {self.other_data_path( "id_rsa_pem" )}', data )

	def test_credential_add_http_basic_auth( self ):
		self.credential_add( key = 'test_credential_add_http_basic_auth', http_basic_auth_username = 'test_credential_add_http_basic_auth_username', http_basic_auth_password = 'test_credential_add_http_basic_auth_password' )

		data = self.credential_list()

		self.assertIn( 'HTTP Basic Authentication Username: test_credential_add_http_basic_auth_username',	data )
		self.assertIn( 'HTTP Basic Authentication Password: **********',									data )

class TestCredentialUpdate( MMTTest ):
	def test_credential_update_validate( self ):
		# Does not exist
		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_credential_update_validate\' does not exist' )

		# Already exists
		self.credential_add( 'test_credential_update_validate_already_exists_1' )
		self.credential_add( 'test_credential_update_validate_already_exists_2' )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_already_exists_2', new_key = 'test_credential_update_validate_already_exists_1' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_credential_update_validate_already_exists_1\' already exists' )

		# Empty URL
		self.credential_add( 'test_credential_update_validate_empty_URL' )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_empty_URL', url = '' )

		self.assertEqual( e.exception.error_message, 'A URL value is required' )

		# Token and SSH authentication
		self.credential_add( 'test_credential_update_validate_token_and_ssh' )

		with self.assertRaises( Error ) as e:
			self._run_command( CredentialUpdateCommand( { 'key': 'test_credential_update_validate_token_and_ssh', 'token': 'invalid', 'ssh_username': 'invalid' } ) )

		self.assertEqual( e.exception.error_message, 'Only one of token authentication or SSH authentication is allowed' )

		# Cannot switch token authentication to SSH authentication
		self.credential_add( 'test_credential_update_validate_token_to_ssh' )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_token_to_ssh', ssh_username = 'invalid' )

		self.assertEqual( e.exception.error_message, 'Cannot switch a credential between token and SSH authentication' )

		# Cannot switch SSH authentication to token authentication
		self.credential_add( 'test_credential_update_validate_ssh_to_token', ssh_username = 'test', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_ssh_to_token', token = 'invalid' )

		self.assertEqual( e.exception.error_message, 'Cannot switch a credential between token and SSH authentication' )

		# Empty token
		self.credential_add( 'test_credential_update_validate_empty_token' )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_empty_token', token = '' )

		self.assertEqual( e.exception.error_message, 'An API Token value is required' )

		# Empty signing key
		self.credential_add( 'test_credential_update_validate_empty_signing_key' )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_empty_signing_key', signing_key = '' )

		self.assertEqual( e.exception.error_message, 'An API Signing Key value is required' )

		# Empty SSH username
		self.credential_add( 'test_credential_update_validate_empty_ssh_username', ssh_username = 'test', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_empty_ssh_username', ssh_username = '' )

		self.assertEqual( e.exception.error_message, 'An SSH Username value is required' )

		# Empty SSH private key
		self.credential_add( 'test_credential_update_validate_empty_ssh_private_key', ssh_username = 'test', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_empty_ssh_private_key', ssh_private_key = '' )

		self.assertEqual( e.exception.error_message, 'An SSH Private Key value is required' )

		# Empty SSH private key
		self.credential_add( 'test_credential_update_validate_invalid_ssh_private_key', ssh_username = 'test', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )

		with self.assertRaises( Error ) as e:
			self.credential_update( 'test_credential_update_validate_invalid_ssh_private_key', ssh_private_key = 'invalid' )

		self.assertEqual( e.exception.error_message, 'SSH Private Key does not exist' )

	def test_credential_update_token( self ):
		def verify( url: str, token: str ):
			data = self.credential_list()

			self.assertIn( 'Method: Token',		data )
			self.assertIn( f'URL: {url}',		data )
			self.assertIn( f'Token: {token}',	data )

		self.credential_add( 'test_credential_update_token', url = self.config.get( 'api_url' ), token = self.config.get( 'api_token' ) )

		# Do not modify anything
		self.credential_update( 'test_credential_update_token' )
		verify( self.config.get( 'api_url' ), self.config.get( 'api_token' ) )

		# Change just the URL and verify everything else stays the same
		self.credential_update( key = 'test_credential_update_token', url = 'http://miva.com/mm5/json.mvc' )
		verify( 'http://miva.com/mm5/json.mvc', self.config.get( 'api_token' ) )

		# Change just the token and verify everything else stays the same
		self.credential_update( key = 'test_credential_update_token', token = 'updated token' )
		verify( 'http://miva.com/mm5/json.mvc', 'updated token' )

		# Change everything and verify it works as expected
		self.credential_update( key = 'test_credential_update_token', url = 'http://localhost/mm5/json.mvc', token = 'red white blue' )
		verify( 'http://localhost/mm5/json.mvc', 'red white blue' )

	def test_credential_update_ssh( self ):
		def verify( url: str, ssh_username: str, ssh_private_key: str ):
			data = self.credential_list()

			self.assertIn( 'Method: SSH',					data )
			self.assertIn( f'URL: {url}',					data )
			self.assertIn( f'Username: {ssh_username}',		data )
			self.assertIn( f'Filepath: {ssh_private_key}',	data )

		self.credential_add( 'test_credential_update_ssh', url = self.config.get( 'api_url' ), ssh_username = self.config.get( 'admin_username' ), ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )

		# Do not modify anything
		self.credential_update( 'test_credential_update_ssh' )
		verify( self.config.get( 'api_url' ), self.config.get( 'admin_username' ), self.other_data_path( 'id_rsa_pem' ) )

		# Change just the URL and verify everything else stays the same
		self.credential_update( key = 'test_credential_update_ssh', url = 'http://miva.com/mm5/json.mvc' )
		verify( 'http://miva.com/mm5/json.mvc', self.config.get( 'admin_username' ), self.other_data_path( 'id_rsa_pem' ) )

		# Change just the SSH username and verify everything else stays the same
		self.credential_update( key = 'test_credential_update_ssh', ssh_username = 'updated username' )
		verify( 'http://miva.com/mm5/json.mvc', 'updated username', self.other_data_path( 'id_rsa_pem' ) )

		# Change just the SSH private key and verify everything else stays the same
		self.credential_update( key = 'test_credential_update_ssh', ssh_private_key = self.other_data_path( 'id_rsa_openssh' ) )
		verify( 'http://miva.com/mm5/json.mvc', 'updated username', self.other_data_path( 'id_rsa_openssh' ) )

		# Change everything and verify it works as expected
		self.credential_update( key = 'test_credential_update_ssh', url = 'http://localhost/mm5/json.mvc', ssh_username = 'random username', ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )
		verify( 'http://localhost/mm5/json.mvc', 'random username', self.other_data_path( 'id_rsa_pem' ) )

	def test_credential_update_http_basic_auth( self ):
		def verify( http_basic_auth_username: typing.Optional[ str ], http_basic_auth_password: typing.Optional[ str ] ):
			data	= self.credential_list()
			config	= self.load_global_config()

			if http_basic_auth_username is None and http_basic_auth_password is None:
				self.assertNotIn( 'HTTP Basic Authentication Username', data )
				self.assertNotIn( 'HTTP Basic Authentication Password', data )
			else:
				self.assertIn( f'HTTP Basic Authentication Username: {http_basic_auth_username}', data )
				self.assertIn( f'HTTP Basic Authentication Password: **********', data )

			self.assertEqual( config.get( 'credentials' ).get( 'test_credential_update_http_basic_auth' ).get( 'http_basic_auth_username' ), http_basic_auth_username )
			self.assertEqual( config.get( 'credentials' ).get( 'test_credential_update_http_basic_auth' ).get( 'http_basic_auth_password' ), http_basic_auth_password )

		self.credential_add( 'test_credential_update_http_basic_auth', http_basic_auth_username = 'test_credential_update_http_basic_auth_username', http_basic_auth_password = 'test_credential_update_http_basic_auth_password' )

		# Do not modify anything
		self.credential_update( key = 'test_credential_update_http_basic_auth' )
		verify( 'test_credential_update_http_basic_auth_username', 'test_credential_update_http_basic_auth_password' )

		# Change just the password
		self.credential_update( key = 'test_credential_update_http_basic_auth', http_basic_auth_password = 'test_credential_update_http_basic_auth_password_updated' )
		verify( 'test_credential_update_http_basic_auth_username', 'test_credential_update_http_basic_auth_password_updated' )

		# You cannot change just the username because if the username is
		# specified and the password is omitted, the user is prompted for
		# the password
		self.credential_update( key = 'test_credential_update_http_basic_auth', http_basic_auth_username = 'test_credential_update_http_basic_auth_username_updated', http_basic_auth_password = 'test_credential_update_http_basic_auth_password_updated' )
		verify( 'test_credential_update_http_basic_auth_username_updated', 'test_credential_update_http_basic_auth_password_updated' )

		# Remove the username and password
		self.credential_update( key = 'test_credential_update_http_basic_auth', http_basic_auth_username = '', http_basic_auth_password = '' )
		verify( None, None )


class TestCredentialDelete( MMTTest ):
	def test_credential_delete_validate( self ):
		with self.assertRaises( Error ) as e:
			self.credential_delete( 'test_credential_delete_validate' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_credential_delete_validate\' does not exist' )

	def test_credential_delete( self ):
		self.credential_add( 'test_credential_delete' )
		self.credential_delete( 'test_credential_delete' )

		with self.assertRaises( Error ) as e:
			self.credential_delete( 'test_credential_delete' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_credential_delete\' does not exist' )


class Regressions( MMTTest ):
	""" SSH Private Key credentials should have their absolute path stored """
	def test_regression_MMT_47( self ):
		with tempfile.TemporaryDirectory() as directory:
			os.chdir( directory )

			private_key_filename = 'id_rsa_pem'

			with open( self.other_data_path( private_key_filename ), 'rb' ) as fh_read:
				with open( private_key_filename, 'wb' ) as fh_write:
					fh_write.write( fh_read.read() )

			self.credential_add( 'test_regression_MMT_47', ssh_private_key = private_key_filename )
			self.assertIn( f'Filepath: {os.path.join( os.getcwd(), private_key_filename )}', self.credential_list() )

			self.credential_update( 'test_regression_MMT_47', ssh_private_key = private_key_filename )
			self.assertIn( f'Filepath: {os.path.join( os.getcwd(), private_key_filename )}', self.credential_list() )
