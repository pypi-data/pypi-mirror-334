from mmt.exceptions import Error
from test import MMTTest


class TestBranchList( MMTTest ):
	def test_branch_list_validate( self ):
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', credential_key = 'invalid_credential_key' )

		self.assertEqual( e.exception.error_message, 'Credential key \'invalid_credential_key\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', store_code = '' )

		self.assertEqual( e.exception.error_message, 'A Store Code is required' )

	def test_branch_list( self ):
		self.branch_delete( 'test_branch_list_1' )
		self.branch_delete( 'test_branch_list_2' )

		self.branch_create( 'test_branch_list_1', color = '#FFFFFF' )
		self.branch_create( 'test_branch_list_2', color = '#000000' )

		data = self.branch_list()

		# Verify specific data
		self.assertIn( 'Branch: test_branch_list_1',	data )
		self.assertIn( 'Branch: test_branch_list_2',	data )

		# Verify generic data
		self.assertIn( 'Is Primary: False', 			data )
		self.assertIn( 'Is Primary: True',				data )
		self.assertIn( 'Is Working: False',				data )
		self.assertIn( 'Is Working: True',				data )
		self.assertIn( 'Preview URL: http',				data )

		branch = self.branch_load_api( 'test_branch_list_1' )
		self.assertEqual( branch.get_color(), '#FFFFFF' )

		branch = self.branch_load_api( 'test_branch_list_2' )
		self.assertEqual( branch.get_color(), '#000000' )


class TestBranchCreate( MMTTest ):
	def test_branch_add_validate( self ):
		# Credential Key
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', credential_key = '' )

		self.assertEqual( e.exception.error_message, 'A Credential Key is required' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', credential_key = 'invalid_credential_key' )

		self.assertEqual( e.exception.error_message, 'Credential key \'invalid_credential_key\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', store_code = '' )

		self.assertEqual( e.exception.error_message, 'A Store Code is required' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', _from = '' )

		self.assertEqual( e.exception.error_message, 'A From value is required' )

		# Remote Key
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', remote_key = '' )

		self.assertEqual( e.exception.error_message, 'A Remote Key is required' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', remote_key = 'invalid_remote_key' )

		self.assertEqual( e.exception.error_message, 'Remote key \'invalid_remote_key\' does not exist' )

	def test_branch_add_credential_key( self ):
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_add_credential_key', _from = 'invalid' )

		self.assertEqual( e.exception.error_message, 'Branch \'invalid\' does not exist' )

		self.credential_add( 'test_branch_add_credential_key' )

		self.branch_delete( 'test_branch_add_credential_key', credential_key = 'test_branch_add_credential_key' )
		self.branch_create( 'test_branch_add_credential_key', credential_key = 'test_branch_add_credential_key' )
		self.assertIn( 'Branch: test_branch_add_credential_key', self.branch_list() )

	def test_branch_add_remote_key( self ):
		self.credential_add( 'test_branch_add_remote_key' )
		self.remote_add( 'test_branch_add_remote_key', credential_key = 'test_branch_add_remote_key' )

		self.branch_delete( 'test_branch_add_remote_key', credential_key = 'test_branch_add_remote_key' )
		self.branch_create( 'test_branch_add_remote_key', remote_key = 'test_branch_add_remote_key' )
		self.assertIn( 'test_branch_add_remote_key', self.branch_list() )


class TestBranchDelete( MMTTest ):
	def test_branch_delete_validate( self ):
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', credential_key = 'invalid_credential_key' )

		self.assertEqual( e.exception.error_message, 'Credential key \'invalid_credential_key\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', store_code = '' )

		self.assertEqual( e.exception.error_message, 'A Store Code is required' )

	def test_branch_delete( self ):
		self.branch_delete( 'test_branch_delete' )

		self.branch_create( 'test_branch_delete' )
		self.assertIn( 'Branch: test_branch_delete', self.branch_list() )

		self.branch_delete( 'test_branch_delete' )
		self.assertNotIn( 'Branch: test_branch_delete', self.branch_list() )
