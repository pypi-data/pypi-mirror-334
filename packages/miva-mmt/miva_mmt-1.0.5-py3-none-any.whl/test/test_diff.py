import os

from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_diff_validate( self ):
		self.checkout()

		with self.assertRaises( Error ) as e:
			self.diff()

		self.assertEqual( e.exception.error_message, 'The \'diff\' configuration setting must be set' )

	def test_diff_invalid_diff_tool( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()
		self.config_set( 'diff', [ '/invalid/path' ] )

		with self.template_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.assertRaises( Error ) as e:
			self.diff()

		self.assertIn( 'Failed to open diff tool \'/invalid/path\':', e.exception.error_message )

	def test_diff_no_modified_files( self ):
		self.checkout()
		self.set_diff_tool()

		self.assertEqual( self.diff(), 'No files modified' )

	def test_diff_templates( self ):
		def diff_file( filepath: str ):
			data = f'random data for {filepath}'

			with self.template_open( filepath ) as fh:
				original_version = fh.read()

			with self.template_open( filepath, 'w' ) as fh:
				fh.write( data )

			self.diff( [ self.template_path( filepath ) ] )

			with open( 'diff.old' ) as fh:
				self.assertEqual( fh.read(), original_version )

			with open( 'diff.new' ) as fh:
				self.assertEqual( fh.read(), data )

		self.import_store_provisioning_file( 'test_diff_templates.xml' )
		self.checkout()
		self.set_diff_tool()

		diff_file( 'test_diff_templates.mvt' )
		diff_file( 'test_diff_templates.json' )

	def test_diff_properties( self ):
		def diff_file( filepath: str ):
			data = f'random data for {filepath}'

			with open( filepath ) as fh:
				original_version = fh.read()

			with open( filepath, 'w' ) as fh:
				fh.write( data )

			self.diff( [ filepath ] )

			with open( 'diff.old' ) as fh:
				self.assertEqual( fh.read(), original_version )

			with open( 'diff.new' ) as fh:
				self.assertEqual( fh.read(), data )

		self.import_store_provisioning_file( 'test_diff_properties.xml' )
		self.checkout( ignore_unsynced_properties = False )
		self.set_diff_tool()

		diff_file( self.property_path( 'readytheme_contentsection', 'test_diff_properties.mvt' ) )
		diff_file( self.property_path( 'readytheme_contentsection', 'test_diff_properties.json' ) )
		diff_file( self.property_product_path( 'header', 'test_diff_properties_product.mvt' ) )
		diff_file( self.property_category_path( 'header', 'test_diff_properties_category.mvt' ) )

	def test_diff_jsresources( self ):
		def diff_file( filepath: str ):
			data = f'random data for {filepath}'

			with self.jsresource_open( filepath ) as fh:
				original_version = fh.read()

			with self.jsresource_open( filepath, 'w' ) as fh:
				fh.write( data )

			self.diff( [ self.jsresource_path( filepath ) ] )

			with open( 'diff.old' ) as fh:
				self.assertEqual( fh.read(), original_version )

			with open( 'diff.new' ) as fh:
				self.assertEqual( fh.read(), data )

		upload_response = self.upload_js_file_from_data( 'test_diff_jsresources_local.js', 'alert( \'test_diff_jsresources_local.js\' );' ).json()
		upload_filepath	= upload_response.get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_diff_jsresources.xml', [ ( '%test_diff_jsresources_local_filepath%', upload_filepath ) ] )
		self.checkout()
		self.set_diff_tool()

		diff_file( 'test_diff_jsresources_local.json' )
		diff_file( 'test_diff_jsresources_local.js' )

		diff_file( 'test_diff_jsresources_inline.json' )
		diff_file( 'test_diff_jsresources_inline.mvt' )

	def test_diff_cssresources( self ):
		def diff_file( filepath: str ):
			data = f'random data for {filepath}'

			with self.cssresource_open( filepath ) as fh:
				original_version = fh.read()

			with self.cssresource_open( filepath, 'w' ) as fh:
				fh.write( data )

			self.diff( [ self.cssresource_path( filepath ) ] )

			with open( 'diff.old' ) as fh:
				self.assertEqual( fh.read(), original_version )

			with open( 'diff.new' ) as fh:
				self.assertEqual( fh.read(), data )

		upload_response = self.upload_css_file_from_data( 'test_diff_cssresources_local.css', '#test_diff_cssresources_local { margin: 0; }' ).json()
		upload_filepath	= upload_response.get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_diff_cssresources.xml', [ ( '%test_diff_cssresources_local_filepath%', upload_filepath ) ] )
		self.checkout()
		self.set_diff_tool()

		diff_file( 'test_diff_cssresources_local.json' )
		diff_file( 'test_diff_cssresources_local.css' )

		diff_file( 'test_diff_cssresources_inline.json' )
		diff_file( 'test_diff_cssresources_inline.mvt' )

	def test_diff_resourcegroups( self ):
		def diff_file( filepath: str ):
			data = f'random data for {filepath}'

			with self.resourcegroup_open( filepath ) as fh:
				original_version = fh.read()

			with self.resourcegroup_open( filepath, 'w' ) as fh:
				fh.write( data )

			self.diff( [ self.resourcegroup_path( filepath ) ] )

			with open( 'diff.old' ) as fh:
				self.assertEqual( fh.read(), original_version )

			with open( 'diff.new' ) as fh:
				self.assertEqual( fh.read(), data )

		self.import_store_provisioning_file( 'test_diff_resourcegroups.xml' )
		self.checkout()
		self.set_diff_tool()

		diff_file( 'test_diff_resourcegroups.json' )

	def test_diff_empty_template_settings( self ):
		self.import_store_provisioning_file( 'test_diff_empty_template_settings.xml' )
		self.checkout()
		self.set_diff_tool()

		data					= 'test_diff_empty_template_settings'
		template_settings_path	= self.template_path( 'test_diff_empty_template_settings.json' )

		self.assertTrue( os.path.exists( template_settings_path ) )

		# Remove the file and verify it does not exist
		os.remove( template_settings_path )
		self.assertFalse( os.path.exists( template_settings_path ) )

		# Push the changes up
		self.push( 'test_diff_empty_template_settings' )

		# Make a local modification
		with self.template_open( 'test_diff_empty_template_settings.json', 'w' ) as fh:
			fh.write( data )

		self.diff()

		with open( 'diff.old' ) as fh:
			self.assertEqual( fh.read(), '' )

		with open( 'diff.new' ) as fh:
			self.assertEqual( fh.read(), data )

	def test_diff_empty_property_settings( self ):
		self.import_store_provisioning_file( 'test_diff_empty_property_settings.xml' )
		self.checkout()
		self.set_diff_tool()

		data					= 'test_diff_empty_property_settings'
		property_settings_path	= self.property_path( 'readytheme_contentsection', 'test_diff_empty_property_settings.json' )

		self.assertTrue( os.path.exists( property_settings_path ) )

		# Remove the file and verify it does not exist
		os.remove( property_settings_path )
		self.assertFalse( os.path.exists( property_settings_path ) )

		# Push the changes up
		self.push( 'test_diff_empty_property_settings' )

		# Make a local modification
		with self.property_open( 'readytheme_contentsection', 'test_diff_empty_property_settings.json', 'w' ) as fh:
			fh.write( data )

		self.diff()

		with open( 'diff.old' ) as fh:
			self.assertEqual( fh.read(), '' )

		with open( 'diff.new' ) as fh:
			self.assertEqual( fh.read(), data )
