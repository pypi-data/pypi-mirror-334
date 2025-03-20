from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_config_set_validate( self ):
		with self.assertRaises( Error ) as e:
			self.config_set( '', '' )

		self.assertEqual( e.exception.error_message, 'Invalid config setting' )

		with self.assertRaises( Error ) as e:
			self.config_set( 'some_invalid_key', '' )

		self.assertEqual( e.exception.error_message, 'Invalid config setting \'some_invalid_key\'' )

		with self.assertRaises( Error ) as e:
			self.config_set( 'diff', [] )

		self.assertEqual( e.exception.error_message, 'Setting value cannot be blank' )

		with self.assertRaises( Error ) as e:
			self.config_set( 'editor', [] )

		self.assertEqual( e.exception.error_message, 'Setting value cannot be blank' )

	def test_config_set( self ):
		self.config_set( 'editor', [ '/usr/bin/vim' ] )
		self.assertIn( 'editor: [\'/usr/bin/vim\']', self.config_list() )

	def test_config_delete_validate( self ):
		with self.assertRaises( Error ) as e:
			self.config_delete( '' )

		self.assertEqual( e.exception.error_message, 'Invalid config setting' )

		with self.assertRaises( Error ) as e:
			self.config_delete( 'some_invalid_key' )

		self.assertEqual( e.exception.error_message, 'Invalid config setting \'some_invalid_key\'' )

	def test_config_delete( self ):
		self.config_delete( 'editor' )
		self.assertIn( 'editor: <Not Set>', self.config_list() )

	def test_config_list( self ):
		self.assertIn( 'diff: <Not Set>',	self.config_list() )
		self.assertIn( 'editor: <Not Set>', self.config_list() )
