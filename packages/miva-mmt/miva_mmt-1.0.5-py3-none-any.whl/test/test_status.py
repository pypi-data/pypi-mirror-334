from test import MMTTest


class Test( MMTTest ):
	def test_no_modified_files( self ):
		self.checkout()
		self.assertEqual( 'No files modified', self.status() )

	def test_modified_files( self ):
		self.import_store_provisioning_file( 'test_status.xml' )
		self.checkout()

		with self.template_open( 'test_status_1.mvt', 'w' ) as fh:
			fh.write( 'test_status_1 modified' )

		modified_files = self.status()

		self.assertIn( self.template_path( 'test_status_1.mvt' ),		modified_files )
		self.assertNotIn( self.template_path( 'test_status_2.mvt' ),	modified_files )
