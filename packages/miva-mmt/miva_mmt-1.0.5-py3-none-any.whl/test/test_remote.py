import typing

from mmt.exceptions import Error
from test import MMTTest


class TestRemoteList( MMTTest ):
	def test_remote_list( self ):
		self.assertEqual( self.remote_list(), '' )

		self.credential_add( 'test_remote_list_credential_key' )
		self.remote_add( 'test_remote_list', 'test_remote_list_credential_key', 'test_remote_list_store_code', 'test_remote_list_branch_name' )

		data = self.remote_list()

		self.assertIn( 'test_remote_list',									data )
		self.assertIn( 'Credential Key: test_remote_list_credential_key',	data )
		self.assertIn( 'Store Code: test_remote_list_store_code',			data )
		self.assertIn( 'Branch Name: test_remote_list_branch_name',			data )


class TestRemoteAdd( MMTTest ):
	def test_remote_add_validate( self ):
		self.credential_add( 'test_remote_add_validate_credential_key' )
		self.remote_add( 'test_remote_add_validate', 'test_remote_add_validate_credential_key',  )

		with self.assertRaises( Error ) as e:
			self.remote_add( 'test_remote_add_validate', 'test_remote_add_validate_credential_key' )

		self.assertEqual( e.exception.error_message, 'Remote key \'test_remote_add_validate\' already exists' )

		with self.assertRaises( Error ) as e:
			self.remote_add( 'test_remote_add_validate_invalid', 'invalid_credential_key' )

		self.assertEqual( e.exception.error_message, 'Credential key \'invalid_credential_key\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.remote_add( 'test_remote_add_validate_invalid', store_code = '' )

		self.assertEqual( e.exception.error_message, 'A Store Code value is required' )

		with self.assertRaises( Error ) as e:
			self.remote_add( 'test_remote_add_validate_invalid', branch_name = '' )

		self.assertEqual( e.exception.error_message, 'A Branch Name value is required' )

	def test_remote_add( self ):
		def validate( key: str, credential_key: str, store_code: str, branch_name: str ):
			data = self.remote_list()

			self.assertIn( key,									data )
			self.assertIn( f'Credential Key: {credential_key}',	data )
			self.assertIn( f'Store Code: {store_code}',			data )
			self.assertIn( f'Branch Name: {branch_name}',		data )

		self.credential_add( 'test_remote_add_credential_key' )
		self.remote_add( 'test_remote_add_1', 'test_remote_add_credential_key', 'test_remote_add_1_store_code_', 'test_remote_add_1_branch_name_' )
		self.remote_add( 'test_remote_add_2', 'test_remote_add_credential_key', 'test_remote_add_1_store_code_', 'test_remote_add_1_branch_name_' )

		validate( 'test_remote_add_1', 'test_remote_add_credential_key', 'test_remote_add_1_store_code_', 'test_remote_add_1_branch_name_' )
		validate( 'test_remote_add_2', 'test_remote_add_credential_key', 'test_remote_add_1_store_code_', 'test_remote_add_1_branch_name_' )

class TestRemoteUpdate( MMTTest ):
	def test_remote_update_validate( self ):
		self.credential_add( 'test_remote_update_validate_credential_key' )

		self.remote_add( 'test_remote_update_validate_1', 'test_remote_update_validate_credential_key' )
		self.remote_add( 'test_remote_update_validate_2', 'test_remote_update_validate_credential_key' )

		with self.assertRaises( Error ) as e:
			self.remote_update( 'test_remote_update_validate_invalid' )

		self.assertEqual( e.exception.error_message, 'Remote key \'test_remote_update_validate_invalid\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.remote_update( 'test_remote_update_validate_1', 'test_remote_update_validate_2' )

		self.assertEqual( e.exception.error_message, 'Remote key \'test_remote_update_validate_2\' already exists' )

		with self.assertRaises( Error ) as e:
			self.remote_update( 'test_remote_update_validate_1', credential_key = 'test_remote_update_validate_invalid' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_remote_update_validate_invalid\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.remote_update( 'test_remote_update_validate_1', new_key = '' )

		self.assertEqual( e.exception.error_message, 'Remote key cannot be blank' )

		with self.assertRaises( Error ) as e:
			self.remote_update( 'test_remote_update_validate_1', store_code = '' )

		self.assertEqual( e.exception.error_message, 'Store code cannot be blank' )

		with self.assertRaises( Error ) as e:
			self.remote_update( 'test_remote_update_validate_1', branch_name = '' )

		self.assertEqual( e.exception.error_message, 'Branch name cannot be blank' )

	def test_remote_update( self ):
		def validate( key: str, credential_key: str, store_code: str, branch_name: str ):
			data = self.remote_list()

			self.assertEqual( data.count( 'Store Code:' ), 1, 'Expected exactly 1 remote entry' )

			self.assertIn( key,									data )
			self.assertIn( f'Credential Key: {credential_key}',	data )
			self.assertIn( f'Store Code: {store_code}',			data )
			self.assertIn( f'Branch Name: {branch_name}',		data )

		self.credential_add( 'test_remote_update_credential_key_1' )
		self.credential_add( 'test_remote_update_credential_key_2' )
		self.remote_add( 'test_remote_update', 'test_remote_update_credential_key_1', 'test_remote_update_store_code', 'test_remote_update_branch_name' )

		# Don't update anything
		self.remote_update( 'test_remote_update' )
		validate( 'test_remote_update', 'test_remote_update_credential_key_1', 'test_remote_update_store_code', 'test_remote_update_branch_name' )

		# Update only the remote key
		self.remote_update( 'test_remote_update', new_key = 'test_remote_update_modified' )
		validate( 'test_remote_update_modified', 'test_remote_update_credential_key_1', 'test_remote_update_store_code', 'test_remote_update_branch_name' )

		# Update only the credential key
		self.remote_update( 'test_remote_update_modified', credential_key = 'test_remote_update_credential_key_2' )
		validate( 'test_remote_update_modified', 'test_remote_update_credential_key_2', 'test_remote_update_store_code', 'test_remote_update_branch_name' )

		# Update only the store code
		self.remote_update( 'test_remote_update_modified', store_code = 'test_remote_update_store_code_modified' )
		validate( 'test_remote_update_modified', 'test_remote_update_credential_key_2', 'test_remote_update_store_code_modified', 'test_remote_update_branch_name' )

		# Update only the store code
		self.remote_update( 'test_remote_update_modified', branch_name = 'test_remote_update_branch_name_modified' )
		validate( 'test_remote_update_modified', 'test_remote_update_credential_key_2', 'test_remote_update_store_code_modified', 'test_remote_update_branch_name_modified' )

		# Update everything
		self.remote_update( 'test_remote_update_modified', new_key = 'test_remote_update', credential_key = 'test_remote_update_credential_key_1', store_code = 'test_remote_update_store_code', branch_name = 'test_remote_update_branch_name' )
		validate( 'test_remote_update', 'test_remote_update_credential_key_1', 'test_remote_update_store_code', 'test_remote_update_branch_name' )


class TestRemoteDelete( MMTTest ):
	def test_remote_delete( self ):
		def validate_in( key: str, credential_key: str, store_code: str, branch_name: str ):
			return validate( key, credential_key, store_code, branch_name, self.assertIn )

		def validate_notin( key: str, credential_key: str, store_code: str, branch_name: str ):
			return validate( key, credential_key, store_code, branch_name, self.assertNotIn )

		def validate( key: str, credential_key: str, store_code: str, branch_name: str, assert_callback: typing.Callable ):
			data = self.remote_list()

			assert_callback( key,									data )
			assert_callback( f'Credential Key: {credential_key}',	data )
			assert_callback( f'Store Code: {store_code}',			data )
			assert_callback( f'Branch Name: {branch_name}',			data )

		self.credential_add( 'test_remote_delete_credential_key_1' )
		self.credential_add( 'test_remote_delete_credential_key_2' )
		self.credential_add( 'test_remote_delete_credential_key_3' )
		self.remote_add( 'test_remote_delete_1', 'test_remote_delete_credential_key_1', 'store_code_1', 'branch_name_1' )
		self.remote_add( 'test_remote_delete_2', 'test_remote_delete_credential_key_2', 'store_code_2', 'branch_name_2' )
		self.remote_add( 'test_remote_delete_3', 'test_remote_delete_credential_key_3', 'store_code_3', 'branch_name_3' )

		self.remote_delete( [ 'test_remote_delete_invalid' ] )
		validate_in( 'test_remote_delete_1', 'test_remote_delete_credential_key_1', 'store_code_1', 'branch_name_1' )
		validate_in( 'test_remote_delete_2', 'test_remote_delete_credential_key_2', 'store_code_2', 'branch_name_2' )
		validate_in( 'test_remote_delete_3', 'test_remote_delete_credential_key_3', 'store_code_3', 'branch_name_3' )

		self.remote_delete( [ 'test_remote_delete_2' ] )
		validate_in( 'test_remote_delete_1', 'test_remote_delete_credential_key_1', 'store_code_1', 'branch_name_1' )
		validate_in( 'test_remote_delete_3', 'test_remote_delete_credential_key_3', 'store_code_3', 'branch_name_3' )
		validate_notin( 'test_remote_delete_2', 'test_remote_delete_credential_key_2', 'store_code_2', 'branch_name_2' )

		self.remote_delete( [ 'test_remote_delete_3', 'test_remote_delete_1' ] )
		validate_notin( 'test_remote_delete_1', 'test_remote_delete_credential_key_1', 'store_code_1', 'branch_name_1' )
		validate_notin( 'test_remote_delete_3', 'test_remote_delete_credential_key_3', 'store_code_3', 'branch_name_3' )
