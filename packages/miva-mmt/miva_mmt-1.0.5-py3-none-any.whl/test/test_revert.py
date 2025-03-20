import os

from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_revert_validate( self ):
		self.checkout()

		with self.assertRaises( Error ) as e:
			self.revert( _all = False, filepaths = [] )

		self.assertEqual( e.exception.error_message, 'Either the --all parameter or individual filepaths must be specified' )

	def test_revert_no_modified_files( self ):
		self.checkout()
		self.assertEqual( self.revert(), '' )

	def test_revert_templates( self ):
		expected_results = self.load_expected_results( 'test_revert_templates.json' )

		def revert_template():
			expected		= expected_results.get( 'test_revert_templates' )
			expected_source	= expected.get( 'source' )

			with self.template_open( 'test_revert_templates.mvt', 'w' ) as fh:
				fh.write( 'test_revert_templates template modified' )

			reverted_files = self.revert()

			self.assertIn( self.template_path( 'test_revert_templates.mvt' ), reverted_files )

			with self.template_open( 'test_revert_templates.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_template_settings():
			expected			= expected_results.get( 'test_revert_templates' )
			expected_settings	= expected.get( 'settings' ).get( 'product_display' )

			with self.template_open( 'test_revert_templates.json', 'w' ) as fh:
				fh.write( 'test_revert_templates settings modified' )

			reverted_files = self.revert()

			self.assertIn( self.template_path( 'test_revert_templates.json' ), reverted_files )

			with self.template_open( 'test_revert_templates.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings, settings_sub_section = 'product_display' )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_template_settings_delete():
			# Create an empty settings file and push it
			with self.template_open( 'test_revert_templates_settings_delete.json', 'w' ) as fh:
				fh.write( '' )

			self.push( 'test_revert_templates.revert_template_settings_delete' )

			self.assertFalse( os.path.exists( self.template_path( 'test_revert_templates_settings_delete.json' ) ) )

			# Modify the settings file and then revert to
			# verify the file is deleted again

			with self.template_open( 'test_revert_templates_settings_delete.json', 'w' ) as fh:
				fh.write( self.generate_random() )

			reverted_files = self.revert()

			self.assertIn( self.template_path( 'test_revert_templates_settings_delete.json' ), reverted_files )
			self.assertFalse( os.path.exists( self.template_path( 'test_revert_templates_settings_delete.json' ) ) )
			self.assertEqual( self.status(), 'No files modified' )

		def revert_template_no_settings():
			with self.template_open( 'test_revert_templates_no_settings.json', 'w' ) as fh:
				fh.write( 'test_revert_templates_no_settings settings created' )

			self.revert()

			self.assertFalse( os.path.exists( self.template_path( 'test_revert_templates_no_settings.json' ) ) )

		self.import_store_provisioning_file( 'test_revert_templates.xml' )
		self.checkout()

		revert_template()
		revert_template_settings()
		revert_template_settings_delete()
		revert_template_no_settings()

	def test_revert_properties( self ):
		expected_results = self.load_expected_results( 'test_revert_properties.json' )

		def revert_template():
			expected		= expected_results.get( 'readytheme_contentsection_test_revert_properties' )
			expected_source	= expected.get( 'source' )

			with self.property_open( 'readytheme_contentsection', 'test_revert_properties.mvt', 'w' ) as fh:
				fh.write( 'test_revert_properties template modified' )

			reverted_files = self.revert()

			self.assertIn( self.property_path( 'readytheme_contentsection', 'test_revert_properties.mvt' ), reverted_files )

			with self.property_open( 'readytheme_contentsection', 'test_revert_properties.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_settings():
			expected			= expected_results.get( 'readytheme_contentsection_test_revert_properties' )
			expected_settings	= expected.get( 'settings' )

			with self.property_open( 'readytheme_contentsection', 'test_revert_properties.json', 'w' ) as fh:
				fh.write( 'test_revert_properties settings modified' )

			reverted_files = self.revert()

			self.assertIn( self.property_path( 'readytheme_contentsection', 'test_revert_properties.json' ), reverted_files )

			with self.property_open( 'readytheme_contentsection', 'test_revert_properties.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_settings_delete():
			# Create an empty settings file and push it
			with self.property_open( 'readytheme_contentsection', 'test_revert_properties_deleted.json', 'w' ) as fh:
				fh.write( '' )

			self.push( 'test_revert_properties.revert_settings_delete' )

			self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_revert_properties_deleted.json' ) ) )

			# Modify the settings file and then revert to
			# verify the file is deleted again

			with self.property_open( 'readytheme_contentsection', 'test_revert_properties_deleted.json', 'w' ) as fh:
				fh.write( self.generate_random() )

			reverted_files = self.revert()

			self.assertIn( self.property_path( 'readytheme_contentsection', 'test_revert_properties_deleted.json' ), reverted_files )
			self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_revert_properties_deleted.json' ) ) )
			self.assertEqual( self.status(), 'No files modified' )

		def revert_product_template():
			expected_source = expected_results.get( 'product_test_revert_source' )

			with self.property_product_open( 'header', 'test_revert_properties_product.mvt', 'w' ) as fh:
				fh.write( 'test_revert_properties product template modified' )

			reverted_files = self.revert()

			self.assertIn( self.property_product_path( 'header', 'test_revert_properties_product.mvt' ), reverted_files )

			with self.property_product_open( 'header', 'test_revert_properties_product.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_category_template():
			expected_source = expected_results.get( 'category_test_revert_source' )

			with self.property_category_open( 'header', 'test_revert_properties_category.mvt', 'w' ) as fh:
				fh.write( 'test_revert_properties category template modified' )

			reverted_files = self.revert()

			self.assertIn( self.property_category_path( 'header', 'test_revert_properties_category.mvt' ), reverted_files )

			with self.property_category_open( 'header', 'test_revert_properties_category.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			self.assertEqual( self.status(), 'No files modified' )

		self.import_store_provisioning_file( 'test_revert_properties.xml' )
		self.checkout( ignore_unsynced_properties = False )

		revert_template()
		revert_settings()
		revert_settings_delete()
		revert_product_template()
		revert_category_template()

	def test_revert_jsresources( self ):
		expected_results	= self.load_expected_results( 'test_revert_jsresources.json' )
		upload_response		= self.upload_js_file_from_data( 'test_revert_jsresources_local.js', 'console.log( \'test_revert_jsresources_local.js\' );' ).json()
		upload_filepath		= upload_response.get( 'data' ).get( 'file_path' )

		def revert_settings_and_js_file():
			with self.jsresource_open( 'test_revert_jsresources_local.json', 'w' ) as fh:
				fh.write( 'modified settings file' )

			with self.jsresource_open( 'test_revert_jsresources_local.js', 'w' ) as fh:
				fh.write( 'modified JS file' )

			reverted_files = self.revert()

			self.assertIn( self.jsresource_path( 'test_revert_jsresources_local.json' ),	reverted_files )
			self.assertIn( self.jsresource_path( 'test_revert_jsresources_local.js' ),		reverted_files )

			expected									= expected_results.get( 'test_revert_jsresources_local' )
			expected_source								= expected.get( 'source' )
			expected_settings							= expected.get( 'settings' )
			expected_settings[ 'branchless_filepath' ]	= upload_filepath

			with self.jsresource_open( 'test_revert_jsresources_local.js' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.jsresource_open( 'test_revert_jsresources_local.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_settings_and_template_file():
			with self.jsresource_open( 'test_revert_jsresources_inline.json', 'w' ) as fh:
				fh.write( 'modified settings file' )

			with self.jsresource_open( 'test_revert_jsresources_inline.mvt', 'w' ) as fh:
				fh.write( 'modified JS template' )

			reverted_files = self.revert()

			self.assertIn( self.jsresource_path( 'test_revert_jsresources_inline.json' ),	reverted_files )
			self.assertIn( self.jsresource_path( 'test_revert_jsresources_inline.mvt' ),	reverted_files )

			expected			= expected_results.get( 'test_revert_jsresources_inline' )
			expected_source		= expected.get( 'source' )
			expected_settings	= expected.get( 'settings' )

			with self.jsresource_open( 'test_revert_jsresources_inline.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.jsresource_open( 'test_revert_jsresources_inline.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			self.assertEqual( self.status(), 'No files modified' )

		self.import_store_provisioning_file( 'test_revert_jsresources.xml', [ ( '%test_revert_jsresources_local_filepath%', upload_filepath ) ] )
		self.checkout()

		revert_settings_and_js_file()
		revert_settings_and_template_file()

	def test_revert_cssresources( self ):
		expected_results	= self.load_expected_results( 'test_revert_cssresources.json' )
		upload_response		= self.upload_css_file_from_data( 'test_revert_cssresources_local.css', '#test_revert_cssresources_local { margin: 0; }' ).json()
		upload_filepath		= upload_response.get( 'data' ).get( 'file_path' )

		def revert_settings_and_css_file():
			with self.cssresource_open( 'test_revert_cssresources_local.json', 'w' ) as fh:
				fh.write( 'modified settings file' )

			with self.cssresource_open( 'test_revert_cssresources_local.css', 'w' ) as fh:
				fh.write( 'modified CSS file' )

			reverted_files = self.revert()

			self.assertIn( self.cssresource_path( 'test_revert_cssresources_local.json' ),	reverted_files )
			self.assertIn( self.cssresource_path( 'test_revert_cssresources_local.css' ),	reverted_files )

			expected									= expected_results.get( 'test_revert_cssresources_local' )
			expected_source								= expected.get( 'source' )
			expected_settings							= expected.get( 'settings' )
			expected_settings[ 'branchless_filepath' ]	= upload_filepath

			with self.cssresource_open( 'test_revert_cssresources_local.css' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.cssresource_open( 'test_revert_cssresources_local.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			self.assertEqual( self.status(), 'No files modified' )

		def revert_settings_and_template_file():
			with self.cssresource_open( 'test_revert_cssresources_inline.json', 'w' ) as fh:
				fh.write( 'modified settings file' )

			with self.cssresource_open( 'test_revert_cssresources_inline.mvt', 'w' ) as fh:
				fh.write( 'modified CSS template' )

			reverted_files = self.revert()

			self.assertIn( self.cssresource_path( 'test_revert_cssresources_inline.json' ),	reverted_files )
			self.assertIn( self.cssresource_path( 'test_revert_cssresources_inline.mvt' ),	reverted_files )

			expected			= expected_results.get( 'test_revert_cssresources_inline' )
			expected_source		= expected.get( 'source' )
			expected_settings	= expected.get( 'settings' )

			with self.cssresource_open( 'test_revert_cssresources_inline.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.cssresource_open( 'test_revert_cssresources_inline.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			self.assertEqual( self.status(), 'No files modified' )

		self.import_store_provisioning_file( 'test_revert_cssresources.xml', [ ( '%test_revert_cssresources_local_filepath%', upload_filepath ) ] )
		self.checkout()

		revert_settings_and_css_file()
		revert_settings_and_template_file()

	def test_revert_resourcegroups( self ):
		expected_results = self.load_expected_results( 'test_revert_resourcegroups.json' )

		def revert_settings_file():
			with self.resourcegroup_open( 'test_revert_resourcegroups.json', 'w' ) as fh:
				fh.write( 'modified settings file' )

			self.assertIn( self.resourcegroup_path( 'test_revert_resourcegroups.json' ), self.revert() )

			expected			= expected_results.get( 'test_revert_resourcegroups' )
			expected_settings	= expected.get( 'settings' )

			with self.resourcegroup_open( 'test_revert_resourcegroups.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			self.assertEqual( self.status(), 'No files modified' )

		self.import_store_provisioning_file( 'test_revert_resourcegroups.xml' )
		self.checkout()

		revert_settings_file()


class Regressions( MMTTest ):
	""" Directories that do not exist prior to issuing pull / revert commands raise the FileNotFoundError exception """
	def test_regression_MMT_42( self ):
		self.import_store_provisioning_file( 'regression_MMT-42.xml' )
		self.checkout()

		self.delete_directory( 'templates' )
		self.delete_directory( 'properties' )
		self.delete_directory( 'js' )
		self.delete_directory( 'css' )
		self.delete_directory( 'resourcegroups' )

		self.assertFalse( os.path.exists( 'templates' ) )
		self.assertFalse( os.path.exists( 'properties' ) )
		self.assertFalse( os.path.exists( 'js' ) )
		self.assertFalse( os.path.exists( 'css' ) )
		self.assertFalse( os.path.exists( 'resourcegroups' ) )
		self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'regression_MMT-42.mvt' ) ) )

		self.revert()

		self.assertTrue( os.path.exists( 'templates' ) )
		self.assertTrue( os.path.exists( 'properties' ) )
		self.assertTrue( os.path.exists( 'js' ) )
		self.assertTrue( os.path.exists( 'css' ) )
		self.assertTrue( os.path.exists( 'resourcegroups' ) )
		self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'regression_MMT-42.mvt' ) ) )
