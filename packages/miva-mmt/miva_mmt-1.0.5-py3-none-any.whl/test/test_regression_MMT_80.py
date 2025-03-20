from mmt.exceptions import ErrorList
from test import MMTTest


class Test( MMTTest ):
	def test( self ):
		js_upload_filepath	= self.upload_js_file_from_data( 'regression_MMT-80_local.js', 'regression_MMT-80_local.js' ).json().get( 'data' ).get( 'file_path' )
		css_upload_filepath = self.upload_css_file_from_data( 'regression_MMT-80_local.css', 'regression_MMT-80_local.css' ).json().get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'regression_MMT-80.xml', [ ( '%regression_MMT-80_local.js%', js_upload_filepath ), ( '%regression_MMT-80_local.css%', css_upload_filepath ) ] )
		self.checkout()

		# Verify the resource types
		with self.jsresource_open( 'regression_MMT-80_inline.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'I' } )

		with self.jsresource_open( 'regression_MMT-80_local.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'L' } )

		with self.cssresource_open( 'regression_MMT-80_inline.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'I' } )

		with self.cssresource_open( 'regression_MMT-80_local.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'L' } )

		# Modify the source data files locally
		with self.jsresource_open( 'regression_MMT-80_inline.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.jsresource_open( 'regression_MMT-80_local.js', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.cssresource_open( 'regression_MMT-80_inline.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.cssresource_open( 'regression_MMT-80_local.css', 'w' ) as fh:
			fh.write( self.generate_random() )

		# Manually modify the resource types
		self.load_runtime_screen( 'regression_MMT-80' )

		# Verify we get the expected out-of-sync errors
		with self.assertRaises( ErrorList ) as e:
			self.pull()

		self.assertIn( self.jsresource_path( 'regression_MMT-80_inline.mvt' ),	e.exception.error_message )
		self.assertIn( self.jsresource_path( 'regression_MMT-80_local.js' ),	e.exception.error_message )
		self.assertIn( self.cssresource_path( 'regression_MMT-80_inline.mvt' ),	e.exception.error_message )
		self.assertIn( self.cssresource_path( 'regression_MMT-80_local.css' ),	e.exception.error_message )

		# Revert the files
		self.revert()

		# Pull the latest version
		updated_files = self.pull()

		# Verify only the settings files were updated
		self.assertFileModified( updated_files, 'Updated', self.jsresource_path( 'regression_MMT-80_inline.json' ) )
		self.assertFileModified( updated_files, 'Updated', self.jsresource_path( 'regression_MMT-80_local.json' ) )
		self.assertFileModified( updated_files, 'Updated', self.cssresource_path( 'regression_MMT-80_inline.json' ) )
		self.assertFileModified( updated_files, 'Updated', self.cssresource_path( 'regression_MMT-80_local.json' ) )

		self.assertFileExists( self.jsresource_path( 'regression_MMT-80_inline.json' ) )
		self.assertFileExists( self.jsresource_path( 'regression_MMT-80_local.json' ) )
		self.assertFileExists( self.cssresource_path( 'regression_MMT-80_inline.json' ) )
		self.assertFileExists( self.cssresource_path( 'regression_MMT-80_local.json' ) )

		# Verify only the source data files were deleted
		self.assertFileModified( updated_files, 'Deleted', self.jsresource_path( 'regression_MMT-80_inline.mvt' ) )
		self.assertFileModified( updated_files, 'Deleted', self.jsresource_path( 'regression_MMT-80_local.js' ) )
		self.assertFileModified( updated_files, 'Deleted', self.cssresource_path( 'regression_MMT-80_inline.mvt' ) )
		self.assertFileModified( updated_files, 'Deleted', self.cssresource_path( 'regression_MMT-80_local.css' ) )

		self.assertFileNotExists( self.jsresource_path( 'regression_MMT-80_inline.mvt' ) )
		self.assertFileNotExists( self.jsresource_path( 'regression_MMT-80_local.js' ) )
		self.assertFileNotExists( self.cssresource_path( 'regression_MMT-80_inline.mvt' ) )
		self.assertFileNotExists( self.cssresource_path( 'regression_MMT-80_local.css' ) )

		# Verify the resource types were modified
		with self.jsresource_open( 'regression_MMT-80_inline.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'M' } )

		with self.jsresource_open( 'regression_MMT-80_local.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'E' } )

		with self.cssresource_open( 'regression_MMT-80_inline.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'Y' } )

		with self.cssresource_open( 'regression_MMT-80_local.json' ) as fh:
			self.assertSettingsEqual( fh.read(), { 'type': 'M' } )
