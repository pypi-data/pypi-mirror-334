import os

from mmt.exceptions import Error, ErrorList
from test import MMTTest


class Test( MMTTest ):
	def test_no_files_modified( self ):
		self.checkout()
		self.assertEqual( self.pull( filepaths = [] ), 'No files updated' )

	def test_invalid_changeset( self ):
		self.checkout()

		with self.assertRaises( Error ) as e:
			self.pull( c = 10000000 )

		self.assertEqual( e.exception.error_message, 'Changeset 10000000 does not exist' )

	def test_pull_templates( self ):
		self.import_store_provisioning_file( 'test_pull_templates_setup.xml' )

		changeset_id		= 0
		expected_results	= self.load_expected_results( 'test_pull_templates.json' )

		def verify_original_data():
			expected_template_1				= expected_results.get( 'test_pull_templates_1' )
			expected_template_1_source		= expected_template_1.get( 'source' )

			expected_template_2				= expected_results.get( 'test_pull_templates_2' )
			expected_template_2_source		= expected_template_2.get( 'source' )

			with self.template_open( 'test_pull_templates_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_1_source )

			with self.template_open( 'test_pull_templates_1.json' ) as fh:
				self.assertIn( 'product_display', self.json_loads( fh.read() ) )

			with self.template_open( 'test_pull_templates_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_2_source )

			with self.template_open( 'test_pull_templates_3.json' ) as fh:
				self.assertIn( 'product_display', self.json_loads( fh.read() ) )

		def verify_updated_original_data():
			expected_template_1				= expected_results.get( 'test_pull_templates_1' )
			expected_template_1_source		= expected_template_1.get( 'source' )

			expected_template_2				= expected_results.get( 'test_pull_templates_2' )
			expected_template_2_source		= expected_template_2.get( 'source' )

			with self.template_open( 'test_pull_templates_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_1_source )

			with self.template_open( 'test_pull_templates_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_2_source )

			with self.template_open( 'test_pull_templates_3.json' ) as fh:
				self.assertIn( 'product_display', self.json_loads( fh.read() ) )

		def verify_updated_data():
			expected_template_1				= expected_results.get( 'test_pull_templates_1_updated' )
			expected_template_1_source		= expected_template_1.get( 'source' )
			expected_template_1_settings	= expected_template_1.get( 'settings' )

			expected_template_2				= expected_results.get( 'test_pull_templates_2' )
			expected_template_2_source		= expected_template_2.get( 'source' )

			expected_template_3				= expected_results.get( 'test_pull_templates_3_updated' )
			expected_template_3_settings	= expected_template_3.get( 'settings' )

			with self.template_open( 'test_pull_templates_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_1_source )

			with self.template_open( 'test_pull_templates_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_template_1_settings )

			with self.template_open( 'test_pull_templates_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_2_source )

			with self.template_open( 'test_pull_templates_3.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_template_3_settings )

		def verify_deleted_data():
			expected_template_2			= expected_results.get( 'test_pull_templates_2' )
			expected_template_2_source	= expected_template_2.get( 'source' )

			with self.template_open( 'test_pull_templates_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_template_2_source )

		def verify_files_added():
			nonlocal changeset_id

			self.checkout()
			self.import_store_provisioning_file( 'test_pull_templates_add.xml' )

			changeset_id	= self.latest_changeset_id()
			updated_files	= self.pull()

			self.assertIn( f'Added: {self.template_path( "test_pull_templates_1.mvt" )}',		updated_files )
			self.assertIn( f'Added: {self.template_path( "test_pull_templates_1.json" )}',		updated_files )
			self.assertIn( f'Added: {self.template_path( "test_pull_templates_2.mvt" )}',		updated_files )
			self.assertNotIn( f'Added: {self.template_path( "test_pull_templates_2.json" )}',	updated_files )
			self.assertIn( f'Added: {self.template_path( "test_pull_templates_3.mvt" )}',		updated_files )
			self.assertIn( f'Added: {self.template_path( "test_pull_templates_3.json" )}',		updated_files )

			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_1.mvt' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_1.json' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_2.mvt' ) ) )
			self.assertFalse( os.path.exists( self.template_path( 'test_pull_templates_2.json' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_3.mvt' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_3.json' ) ) )

			verify_original_data()

		def verify_files_updated():
			with self.template_open( 'test_pull_templates_1.mvt', 'w' ) as fh:
				fh.write( 'test_pull_templates_1 template updated' )

			with self.template_open( 'test_pull_templates_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( { 'test_pull_templates_1': 'updated' } ) )

			with self.template_open( 'test_pull_templates_3.json', 'w' ) as fh:
				fh.write( self.json_dumps( { 'test_pull_templates_3': 'updated' } ) )

			self.push( 'test_pull_templates.verify_files_updated' )

			updated_files = self.pull( c = changeset_id )

			self.assertIn( f'Updated: {self.template_path( "test_pull_templates_1.mvt" )}',		updated_files )
			self.assertIn( f'Updated: {self.template_path( "test_pull_templates_1.json" )}',	updated_files )

			verify_updated_original_data()

			updated_files = self.pull()

			self.assertIn( f'Updated: {self.template_path( "test_pull_templates_1.mvt" )}',		updated_files )
			self.assertIn( f'Updated: {self.template_path( "test_pull_templates_1.json" )}',	updated_files )
			self.assertNotIn( f'Updated: {self.template_path( "test_pull_templates_2.mvt" )}',	updated_files )
			self.assertNotIn( f'Updated: {self.template_path( "test_pull_templates_2.json" )}',	updated_files )

			verify_updated_data()

		def verify_files_deleted():
			self.import_store_provisioning_file( 'test_pull_templates_delete.xml' )

			updated_files = self.pull()

			self.assertIn( f'Deleted: {self.template_path( "test_pull_templates_1.mvt" )}',		updated_files )
			self.assertIn( f'Deleted: {self.template_path( "test_pull_templates_1.json" )}',	updated_files )
			self.assertNotIn( f'Deleted: {self.template_path( "test_pull_templates_2.mvt" )}',	updated_files )
			self.assertNotIn( f'Deleted: {self.template_path( "test_pull_templates_2.json" )}',	updated_files )
			self.assertNotIn( f'Deleted: {self.template_path( "test_pull_templates_3.mvt" )}',	updated_files )
			self.assertNotIn( f'Deleted: {self.template_path( "test_pull_templates_3.json" )}',	updated_files )

			self.assertFalse( os.path.exists( self.template_path( 'test_pull_templates_1.mvt' ) ) )
			self.assertFalse( os.path.exists( self.template_path( 'test_pull_templates_1.json' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_2.mvt' ) ) )
			self.assertFalse( os.path.exists( self.template_path( 'test_pull_templates_2.json' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_3.mvt' ) ) )
			self.assertTrue( os.path.exists( self.template_path( 'test_pull_templates_3.json' ) ) )

			verify_deleted_data()

		verify_files_added()
		verify_files_updated()
		verify_files_deleted()

	def test_pull_properties( self ):
		self.branch_delete_all_api()
		self.import_store_provisioning_file( 'test_pull_properties_setup.xml' )

		changeset_id		= 0
		expected_results	= self.load_expected_results( 'test_pull_properties.json' )

		def verify_original_data():
			expected_contentsection_1			= expected_results.get( 'test_pull_properties_readytheme_contentsection_1' )
			expected_contentsection_1_source	= expected_contentsection_1.get( 'source' )
			expected_contentsection_1_settings	= expected_contentsection_1.get( 'settings' )

			expected_contentsection_2			= expected_results.get( 'test_pull_properties_readytheme_contentsection_2' )
			expected_contentsection_2_source	= expected_contentsection_2.get( 'source' )
			expected_contentsection_2_settings	= expected_contentsection_2.get( 'settings' )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_contentsection_1_source )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_contentsection_1_settings )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_contentsection_2_source )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_contentsection_2_settings )

		def verify_updated_data():
			expected_contentsection_1			= expected_results.get( 'test_pull_properties_readytheme_contentsection_1_updated' )
			expected_contentsection_1_source	= expected_contentsection_1.get( 'source' )
			expected_contentsection_1_settings	= expected_contentsection_1.get( 'settings' )

			expected_contentsection_2			= expected_results.get( 'test_pull_properties_readytheme_contentsection_2' )
			expected_contentsection_2_source	= expected_contentsection_2.get( 'source' )
			expected_contentsection_2_settings	= expected_contentsection_2.get( 'settings' )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_contentsection_1_source )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_contentsection_1_settings )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_contentsection_2_source )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_contentsection_2_settings )

		def verify_deleted_data():
			expected_contentsection_2			= expected_results.get( 'test_pull_properties_readytheme_contentsection_2' )
			expected_contentsection_2_source	= expected_contentsection_2.get( 'source' )
			expected_contentsection_2_settings	= expected_contentsection_2.get( 'settings' )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_contentsection_2_source )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_contentsection_2_settings )

		def verify_files_added():
			nonlocal changeset_id

			self.checkout()
			self.import_store_provisioning_file( 'test_pull_properties_add.xml' )

			changeset_id	= self.latest_changeset_id()
			updated_files	= self.pull()

			self.assertIn( f'Added: {self.property_path( "readytheme_contentsection", "test_pull_properties_1.mvt" )}',		updated_files )
			self.assertIn( f'Added: {self.property_path( "readytheme_contentsection", "test_pull_properties_1.json" )}',	updated_files )
			self.assertIn( f'Added: {self.property_path( "readytheme_contentsection", "test_pull_properties_2.mvt" )}',		updated_files )
			self.assertIn( f'Added: {self.property_path( "readytheme_contentsection", "test_pull_properties_2.json" )}',	updated_files )

			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_1.mvt' ) ) )
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_1.json' ) ) )
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_2.mvt' ) ) )
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_2.json' ) ) )

			verify_original_data()

		def verify_files_updated():
			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.json' ) as fh:
				settings = self.json_loads( fh.read() )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.mvt', 'w' ) as fh:
				fh.write( 'test_pull_properties_1 template updated' )

			with self.property_open( 'readytheme_contentsection', 'test_pull_properties_1.json', 'w' ) as fh:
				settings[ 'active' ]	= 0
				settings[ 'name' ]		= 'test_pull_properties_1 updated'

				fh.write( self.json_dumps( settings ) )

			self.push( 'test_pull_properties.verify_files_updated' )

			self.pull( c = changeset_id )

			verify_original_data()

			updated_files = self.pull()

			self.assertIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_pull_properties_1.mvt" )}',		updated_files )
			self.assertIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_pull_properties_1.json" )}',		updated_files )
			self.assertNotIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_pull_properties_2.mvt" )}',	updated_files )
			self.assertNotIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_pull_properties_2.json" )}',	updated_files )

			verify_updated_data()

		def verify_files_deleted():
			self.import_store_provisioning_file( 'test_pull_properties_delete.xml' )

			updated_files = self.pull()

			self.assertIn( f'Deleted: {self.property_path( "readytheme_contentsection", "test_pull_properties_1.mvt" )}',		updated_files )
			self.assertIn( f'Deleted: {self.property_path( "readytheme_contentsection", "test_pull_properties_1.json" )}',		updated_files )
			self.assertNotIn( f'Deleted: {self.property_path( "readytheme_contentsection", "test_pull_properties_2.mvt" )}',	updated_files )
			self.assertNotIn( f'Deleted: {self.property_path( "readytheme_contentsection", "test_pull_properties_2.json" )}',	updated_files )

			self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_1.mvt' ) ) )
			self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_1.json' ) ) )
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_2.mvt' ) ) )
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_pull_properties_2.json' ) ) )

			verify_deleted_data()

		verify_files_added()
		verify_files_updated()
		verify_files_deleted()

	def test_pull_jsresources( self ):
		"""
		This test creates 2 sets of local and inline files.  Only the first set
		of both file types are modified.  This is done so the the we can verify
		the second set of file types always remain the same and are never modified
		in any way.
		"""

		self.branch_delete_all_api()
		self.import_store_provisioning_file( 'test_pull_jsresources_setup.xml' )

		changeset_id		= 0
		expected_results	= self.load_expected_results( 'test_pull_jsresources.json' )
		upload_response_1	= self.upload_file_from_data( 'JavaScriptResource_Upload', 'Script', 'test_pull_jsresources_local_1.js', 'console.log( \'test_pull_jsresources_local_1.js\' );' ).json()
		upload_filepath_1	= upload_response_1.get( 'data' ).get( 'file_path' )
		upload_response_2	= self.upload_file_from_data( 'JavaScriptResource_Upload', 'Script', 'test_pull_jsresources_local_2.js', 'console.log( \'test_pull_jsresources_local_2.js\' );' ).json()
		upload_filepath_2	= upload_response_2.get( 'data' ).get( 'file_path' )

		"""
		Verifies the initial versions for both sets of files
		"""
		def verify_original_data():
			expected_inline_1					 				= expected_results.get( 'test_pull_jsresources_inline_1' )
			expected_inline_1_settings							= expected_inline_1.get( 'settings' )
			expected_inline_1_source							= expected_inline_1.get( 'source' )

			expected_local_1									= expected_results.get( 'test_pull_jsresources_local_1' )
			expected_local_1_settings							= expected_local_1.get( 'settings' )
			expected_local_1_settings[ 'branchless_filepath' ]	= upload_filepath_1
			expected_local_1_source								= expected_local_1.get( 'source' )

			expected_inline_2					 				= expected_results.get( 'test_pull_jsresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_jsresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_1_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_1_source )

			with self.jsresource_open( 'test_pull_jsresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_1_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_1.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_1_source )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.jsresource_open( 'test_pull_jsresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_2.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		"""
		Verifies the initial versions of both sets of files with the caveat
		the modified local file is verified using the updated source value
		"""
		def verify_updated_original_data():
			expected_inline_1					 				= expected_results.get( 'test_pull_jsresources_inline_1' )
			expected_inline_1_settings							= expected_inline_1.get( 'settings' )
			expected_inline_1_source							= expected_inline_1.get( 'source' )

			expected_local_1									= expected_results.get( 'test_pull_jsresources_local_1' )
			expected_local_1_settings							= expected_local_1.get( 'settings' )
			expected_local_1_settings[ 'branchless_filepath' ]	= upload_filepath_1
			expected_local_1_source								= expected_results.get( 'test_pull_jsresources_local_1' ).get( 'source' )

			expected_inline_2					 				= expected_results.get( 'test_pull_jsresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_jsresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_1_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_1_source )

			with self.jsresource_open( 'test_pull_jsresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_1_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_1.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_1_source )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.jsresource_open( 'test_pull_jsresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_2.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		"""
		Verifies the updated versions for both sets of files
		"""
		def verify_updated_data():
			expected_inline_1					 				= expected_results.get( 'test_pull_jsresources_inline_1_updated' )
			expected_inline_1_settings							= expected_inline_1.get( 'settings' )
			expected_inline_1_source							= expected_inline_1.get( 'source' )

			expected_local_1									= expected_results.get( 'test_pull_jsresources_local_1_updated' )
			expected_local_1_settings							= expected_local_1.get( 'settings' )
			expected_local_1_settings[ 'branchless_filepath' ]	= upload_filepath_1
			expected_local_1_source								= expected_local_1.get( 'source' )

			expected_inline_2					 				= expected_results.get( 'test_pull_jsresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_jsresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_1_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_1_source )

			with self.jsresource_open( 'test_pull_jsresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_1_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_1.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_1_source )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.jsresource_open( 'test_pull_jsresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_2.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		"""
		Verifies the updated versions for both sets of files
		"""
		def verify_deleted_data():
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_pull_jsresources_inline_1.json' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_pull_jsresources_inline_1.mvt' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_pull_jsresources_local_1.json' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_pull_jsresources_local_1.js' ) ) )

			expected_inline_2					 				= expected_results.get( 'test_pull_jsresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_jsresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.jsresource_open( 'test_pull_jsresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.jsresource_open( 'test_pull_jsresources_local_2.js' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		def verify_files_added():
			nonlocal changeset_id

			self.checkout()
			self.import_store_provisioning_file( 'test_pull_jsresources_add.xml', [ ( '%test_pull_jsresources_local_1_filepath%', upload_filepath_1 ), ( '%test_pull_jsresources_local_2_filepath%', upload_filepath_2 ) ] )

			changeset_id	= self.latest_changeset_id()
			updated_files	= self.pull()

			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_inline_1.json" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_inline_1.mvt" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_inline_2.json" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_inline_2.mvt" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_local_1.json" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_local_1.js" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_local_2.json" ) )
			self.assertFileModified( updated_files, 'Added', self.jsresource_path( "test_pull_jsresources_local_2.js" ) )

			verify_original_data()

		def verify_files_updated():
			# Update only the first set of files
			with self.jsresource_open( 'test_pull_jsresources_inline_1.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'active' ]	= True

			with self.jsresource_open( 'test_pull_jsresources_inline_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.jsresource_open( 'test_pull_jsresources_inline_1.mvt', 'w' ) as fh:
				fh.write( 'console.log( \'test_pull_jsresources_inline_1.js updated\' );' )

			with self.jsresource_open( 'test_pull_jsresources_local_1.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'is_global' ]	= True

			with self.jsresource_open( 'test_pull_jsresources_local_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.jsresource_open( 'test_pull_jsresources_local_1.js', 'w' ) as fh:
				fh.write( 'console.log( \'test_pull_jsresources_local_1.js updated\' );' )

			# Commit the changes
			self.push( 'test_pull_jsresources.verify_updated' )

			# Update back to original versions
			updated_files = self.pull( c = changeset_id )

			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_inline_1.json" ) )
			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_inline_1.mvt" ) )
			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_local_1.json" ) )
			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_local_1.js" ) )

			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_inline_2.json' ),	updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_inline_2.mvt' ),		updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_local_2.json' ),		updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_local_2.js' ),		updated_files )

			# Verify the files are their original versions
			verify_updated_original_data()

			# Update back to the latest changeset
			updated_files = self.pull()

			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_inline_1.json" ) )
			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_inline_1.mvt" ) )
			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_local_1.json" ) )
			self.assertFileModified( updated_files, 'Updated', self.jsresource_path( "test_pull_jsresources_local_1.js" ) )

			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_inline_2.json' ),	updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_inline_2.mvt' ),		updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_local_2.json' ),		updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_local_2.js' ),		updated_files )

			verify_updated_data()

		def verify_files_deleted():
			self.import_store_provisioning_file( 'test_pull_jsresources_delete.xml' )
			updated_files = self.pull()

			self.assertFileModified( updated_files, 'Deleted', self.jsresource_path( "test_pull_jsresources_inline_1.json" ) )
			self.assertFileModified( updated_files, 'Deleted', self.jsresource_path( "test_pull_jsresources_inline_1.mvt" ) )
			self.assertFileModified( updated_files, 'Deleted', self.jsresource_path( "test_pull_jsresources_local_1.json" ) )
			self.assertFileModified( updated_files, 'Deleted', self.jsresource_path( "test_pull_jsresources_local_1.js" ) )

			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_inline_2.json' ),	updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_inline_2.mvt' ),		updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_local_2.json' ),		updated_files )
			self.assertNotIn( self.jsresource_path( 'test_pull_jsresources_local_2.js' ),		updated_files )

			verify_deleted_data()

		verify_files_added()
		verify_files_updated()
		verify_files_deleted()

	def test_pull_cssresources( self ):
		"""
		This test creates 2 sets of local and inline files.  Only the first set
		of both file types are modified.  This is done so the the we can verify
		the second set of file types always remain the same and are never modified
		in any way.
		"""

		self.branch_delete_all_api()
		self.import_store_provisioning_file( 'test_pull_cssresources_setup.xml' )

		changeset_id		= 0
		expected_results	= self.load_expected_results( 'test_pull_cssresources.json' )
		upload_response_1	= self.upload_file_from_data( 'CSSResource_Upload', 'Script', 'test_pull_cssresources_local_1.css', '#test_pull_cssresources_local_1 { color: red; }' ).json()
		upload_filepath_1	= upload_response_1.get( 'data' ).get( 'file_path' )
		upload_response_2	= self.upload_file_from_data( 'CSSResource_Upload', 'Script', 'test_pull_cssresources_local_2.css', '#test_pull_cssresources_local_2 { color: red; }' ).json()
		upload_filepath_2	= upload_response_2.get( 'data' ).get( 'file_path' )

		"""
		Verifies the initial versions for both sets of files
		"""
		def verify_original_data():
			expected_inline_1					 				= expected_results.get( 'test_pull_cssresources_inline_1' )
			expected_inline_1_settings							= expected_inline_1.get( 'settings' )
			expected_inline_1_source							= expected_inline_1.get( 'source' )

			expected_local_1									= expected_results.get( 'test_pull_cssresources_local_1' )
			expected_local_1_settings							= expected_local_1.get( 'settings' )
			expected_local_1_settings[ 'branchless_filepath' ]	= upload_filepath_1
			expected_local_1_source								= expected_local_1.get( 'source' )

			expected_inline_2					 				= expected_results.get( 'test_pull_cssresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_cssresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_1_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_1_source )

			with self.cssresource_open( 'test_pull_cssresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_1_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_1.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_1_source )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.cssresource_open( 'test_pull_cssresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_2.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		"""
		Verifies the initial versions of both sets of files with the caveat
		the modified local file is verified using the updated source value
		"""
		def verify_updated_original_data():
			expected_inline_1					 				= expected_results.get( 'test_pull_cssresources_inline_1' )
			expected_inline_1_settings							= expected_inline_1.get( 'settings' )
			expected_inline_1_source							= expected_inline_1.get( 'source' )

			expected_local_1									= expected_results.get( 'test_pull_cssresources_local_1' )
			expected_local_1_settings							= expected_local_1.get( 'settings' )
			expected_local_1_settings[ 'branchless_filepath' ]	= upload_filepath_1
			expected_local_1_source								= expected_results.get( 'test_pull_cssresources_local_1' ).get( 'source' )

			expected_inline_2					 				= expected_results.get( 'test_pull_cssresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_cssresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_1_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_1_source )

			with self.cssresource_open( 'test_pull_cssresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_1_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_1.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_1_source )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.cssresource_open( 'test_pull_cssresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_2.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		"""
		Verifies the updated versions for both sets of files
		"""
		def verify_updated_data():
			expected_inline_1					 				= expected_results.get( 'test_pull_cssresources_inline_1_updated' )
			expected_inline_1_settings							= expected_inline_1.get( 'settings' )
			expected_inline_1_source							= expected_inline_1.get( 'source' )

			expected_local_1									= expected_results.get( 'test_pull_cssresources_local_1_updated' )
			expected_local_1_settings							= expected_local_1.get( 'settings' )
			expected_local_1_settings[ 'branchless_filepath' ]	= upload_filepath_1
			expected_local_1_source								= expected_local_1.get( 'source' )

			expected_inline_2					 				= expected_results.get( 'test_pull_cssresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_cssresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_1_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_1_source )

			with self.cssresource_open( 'test_pull_cssresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_1_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_1.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_1_source )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.cssresource_open( 'test_pull_cssresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_2.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		"""
		Verifies the updated versions for both sets of files
		"""
		def verify_deleted_data():
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_pull_cssresources_inline_1.json' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_pull_cssresources_inline_1.mvt' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_pull_cssresources_local_1.json' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_pull_cssresources_local_1.css' ) ) )

			expected_inline_2					 				= expected_results.get( 'test_pull_cssresources_inline_2' )
			expected_inline_2_settings							= expected_inline_2.get( 'settings' )
			expected_inline_2_source							= expected_inline_2.get( 'source' )

			expected_local_2									= expected_results.get( 'test_pull_cssresources_local_2' )
			expected_local_2_settings							= expected_local_2.get( 'settings' )
			expected_local_2_settings[ 'branchless_filepath' ]	= upload_filepath_2
			expected_local_2_source								= expected_local_2.get( 'source' )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_inline_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_inline_2.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_inline_2_source )

			with self.cssresource_open( 'test_pull_cssresources_local_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_local_2_settings )

			with self.cssresource_open( 'test_pull_cssresources_local_2.css' ) as fh:
				self.assertEqual( fh.read(), expected_local_2_source )

		def verify_files_added():
			nonlocal changeset_id

			self.checkout()
			self.import_store_provisioning_file( 'test_pull_cssresources_add.xml', [ ( '%test_pull_cssresources_local_1_filepath%', upload_filepath_1 ), ( '%test_pull_cssresources_local_2_filepath%', upload_filepath_2 ) ] )

			changeset_id	= self.latest_changeset_id()
			updated_files	= self.pull()

			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_inline_1.json" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_inline_1.mvt" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_inline_2.json" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_inline_2.mvt" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_local_1.json" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_local_1.css" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_local_2.json" )}',	updated_files )
			self.assertIn( f'Added: {self.cssresource_path( "test_pull_cssresources_local_2.css" )}',	updated_files )

			verify_original_data()

		def verify_files_updated():
			# Update only the first set of files
			with self.cssresource_open( 'test_pull_cssresources_inline_1.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'active' ]	= True

			with self.cssresource_open( 'test_pull_cssresources_inline_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.cssresource_open( 'test_pull_cssresources_inline_1.mvt', 'w' ) as fh:
				fh.write( '#test_pull_cssresources_inline_1 { color: blue; }' )

			with self.cssresource_open( 'test_pull_cssresources_local_1.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'is_global' ]	= True

			with self.cssresource_open( 'test_pull_cssresources_local_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.cssresource_open( 'test_pull_cssresources_local_1.css', 'w' ) as fh:
				fh.write( '#test_pull_cssresources_local_1 { color: blue; }' )

			# Commit the changes
			self.push( 'test_pull_cssresources.verify_updated' )

			# Update back to original versions
			updated_files = self.pull( c = changeset_id )

			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_inline_1.json" )}',	updated_files )
			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_inline_1.mvt" )}',	updated_files )
			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_local_1.json" )}',	updated_files )
			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_local_1.css" )}',		updated_files )

			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_inline_2.json' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_inline_2.mvt' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_local_2.json' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_local_2.css' ),		updated_files )

			# Verify the files are their original versions
			verify_updated_original_data()

			# Update back to the latest changeset
			updated_files = self.pull()

			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_inline_1.json" )}',	updated_files )
			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_inline_1.mvt" )}',	updated_files )
			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_local_1.json" )}',	updated_files )
			self.assertIn( f'Updated: {self.cssresource_path( "test_pull_cssresources_local_1.css" )}',		updated_files )

			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_inline_2.json' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_inline_2.mvt' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_local_2.json' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_local_2.css' ),		updated_files )

			verify_updated_data()

		def verify_files_deleted():
			self.import_store_provisioning_file( 'test_pull_cssresources_delete.xml' )
			updated_files = self.pull()

			self.assertIn( f'Deleted: {self.cssresource_path( "test_pull_cssresources_inline_1.json" )}',	updated_files )
			self.assertIn( f'Deleted: {self.cssresource_path( "test_pull_cssresources_inline_1.mvt" )}',	updated_files )
			self.assertIn( f'Deleted: {self.cssresource_path( "test_pull_cssresources_local_1.json" )}',	updated_files )
			self.assertIn( f'Deleted: {self.cssresource_path( "test_pull_cssresources_local_1.css" )}',		updated_files )

			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_inline_2.json' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_inline_2.mvt' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_local_2.json' ),		updated_files )
			self.assertNotIn( self.cssresource_path( 'test_pull_cssresources_local_2.css' ),		updated_files )

			verify_deleted_data()

		verify_files_added()
		verify_files_updated()
		verify_files_deleted()

	def test_pull_resourcegroups( self ):
		self.branch_delete_all_api()
		self.import_store_provisioning_file( 'test_pull_resourcegroups_setup.xml' )

		expected_results = self.load_expected_results( 'test_pull_resourcegroups.json' )

		def verify_original_data():
			expected_1			= expected_results.get( 'test_pull_resourcegroups_1' )
			expected_1_settings	= expected_1.get( 'settings' )

			expected_2			= expected_results.get( 'test_pull_resourcegroups_2' )
			expected_2_settings	= expected_2.get( 'settings' )

			with self.resourcegroup_open( 'test_pull_resourcegroups_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_1_settings )

			with self.resourcegroup_open( 'test_pull_resourcegroups_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_2_settings )

		def verify_updated_data():
			expected_1			= expected_results.get( 'test_pull_resourcegroups_1_updated' )
			expected_1_settings	= expected_1.get( 'settings' )

			expected_2			= expected_results.get( 'test_pull_resourcegroups_2' )
			expected_2_settings	= expected_2.get( 'settings' )

			with self.resourcegroup_open( 'test_pull_resourcegroups_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_1_settings )

			with self.resourcegroup_open( 'test_pull_resourcegroups_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_2_settings )

		def verify_deleted_data():
			self.assertFalse( os.path.exists( self.resourcegroup_path( 'test_pull_resourcegroups_1.json' ) ) )

			expected_2			= expected_results.get( 'test_pull_resourcegroups_2' )
			expected_2_settings	= expected_2.get( 'settings' )

			with self.resourcegroup_open( 'test_pull_resourcegroups_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_2_settings )

		def verify_files_added():
			self.checkout()
			self.import_store_provisioning_file( 'test_pull_resourcegroups_add.xml' )

			updated_files = self.pull()

			self.assertIn( f'Added: {self.resourcegroup_path( "test_pull_resourcegroups_1.json" )}', updated_files )
			self.assertIn( f'Added: {self.resourcegroup_path( "test_pull_resourcegroups_2.json" )}', updated_files )

			verify_original_data()

		def verify_files_updated():
			changeset_id = self.latest_changeset_id()

			with self.resourcegroup_open( 'test_pull_resourcegroups_1.json' ) as fh:
				settings = self.json_loads( fh.read() )
				settings[ 'linked_js_resources' ].append( 'test_pull_resourcegroups_2' )
				settings[ 'linked_css_resources' ].append( 'test_pull_resourcegroups_2' )

			with self.resourcegroup_open( 'test_pull_resourcegroups_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			self.push( 'test_pull_resourcegroups.verify_files_updated' )

			updated_files = self.pull( c = changeset_id )

			self.assertIn( f'Updated: {self.resourcegroup_path( "test_pull_resourcegroups_1.json" )}',		updated_files )
			self.assertNotIn( f'Updated: {self.resourcegroup_path( "test_pull_resourcegroups_2.json" )}',	updated_files )

			verify_original_data()

			updated_files = self.pull()

			self.assertIn( f'Updated: {self.resourcegroup_path( "test_pull_resourcegroups_1.json" )}',		updated_files )
			self.assertNotIn( f'Updated: {self.resourcegroup_path( "test_pull_resourcegroups_2.json" )}',	updated_files )

			verify_updated_data()

		def verify_files_deleted():
			self.import_store_provisioning_file( 'test_pull_resourcegroups_delete.xml' )
			updated_files = self.pull()

			self.assertIn( f'Deleted: {self.resourcegroup_path( "test_pull_resourcegroups_1.json" )}',		updated_files )
			self.assertNotIn( f'Deleted: {self.resourcegroup_path( "test_pull_resourcegroups_2.json" )}',	updated_files )

			verify_deleted_data()

		verify_files_added()
		verify_files_updated()
		verify_files_deleted()

	def test_pull_specific_files( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout( ignore_unsynced_properties = False )

		changeset_id = self.latest_changeset_id()

		# Make modifications to all data types
		with self.template_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.template_open( 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.property_open( 'readytheme_contentsection', 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.property_open( 'readytheme_contentsection', 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.property_product_open( 'header', 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.property_product_open( 'header', 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.property_category_open( 'header', 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.property_category_open( 'header', 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.jsresource_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.jsresource_open( 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.cssresource_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.cssresource_open( 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		with self.resourcegroup_open( 'test_mmt_1.json' ) as fh:
			resourcegroup_settings_1 = self.json_loads( fh.read() )

		with self.resourcegroup_open( 'test_mmt_2.json' ) as fh:
			resourcegroup_settings_2 = self.json_loads( fh.read() )

		with self.resourcegroup_open( 'test_mmt_1.json', 'w' ) as fh:
			resourcegroup_settings_1[ 'linked_js_resources' ] = []

			fh.write( self.json_dumps( resourcegroup_settings_1 ) )

		with self.resourcegroup_open( 'test_mmt_2.json', 'w' ) as fh:
			resourcegroup_settings_2[ 'linked_js_resources' ] = []

			fh.write( self.json_dumps( resourcegroup_settings_2 ) )

		# Push the changes
		self.push( 'test_pull_specific_files' )

		# Pull the original changeset with specific files specified
		filepaths = []
		filepaths.append( self.template_path( 'test_mmt_1.mvt' ) )
		filepaths.append( self.property_path( 'readytheme_contentsection', 'test_mmt_1.mvt' ) )
		filepaths.append( self.property_product_path( 'header', 'test_mmt_1.mvt' ) )
		filepaths.append( self.property_category_path( 'header', 'test_mmt_1.mvt' ) )
		filepaths.append( self.jsresource_path( 'test_mmt_1.mvt' ) )
		filepaths.append( self.cssresource_path( 'test_mmt_1.mvt' ) )
		filepaths.append( self.resourcegroup_path( 'test_mmt_1.json' ) )

		data = self.pull( c = changeset_id, filepaths = filepaths )

		# Verify only the specific files specified were updated
		self.assertIn( f'Updated: {self.template_path( "test_mmt_1.mvt" )}',									data )
		self.assertIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_mmt_1.mvt" )}',		data )
		self.assertIn( f'Updated: {self.property_product_path( "header", "test_mmt_1.mvt" )}',					data )
		self.assertIn( f'Updated: {self.property_category_path( "header", "test_mmt_1.mvt" )}',					data )
		self.assertIn( f'Updated: {self.jsresource_path( "test_mmt_1.mvt" )}',									data )
		self.assertIn( f'Updated: {self.cssresource_path( "test_mmt_1.mvt" )}',									data )
		self.assertIn( f'Updated: {self.resourcegroup_path( "test_mmt_1.json" )}',								data )

		self.assertNotIn( f'Updated: {self.template_path( "test_mmt_2.mvt" )}',									data )
		self.assertNotIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_mmt_2.mvt" )}',	data )
		self.assertNotIn( f'Updated: {self.property_product_path( "header", "test_mmt_2.mvt" )}',				data )
		self.assertNotIn( f'Updated: {self.property_category_path( "header", "test_mmt_2.mvt" )}',				data )
		self.assertNotIn( f'Updated: {self.jsresource_path( "test_mmt_2.mvt" )}',								data )
		self.assertNotIn( f'Updated: {self.cssresource_path( "test_mmt_2.mvt" )}',								data )
		self.assertNotIn( f'Updated: {self.resourcegroup_path( "test_mmt_2.json" )}',							data )

		# Pull the original changeset, omitting specific files
		data = self.pull( c = changeset_id )

		# Verify all previously omitted files were updated
		self.assertNotIn( f'Updated: {self.template_path( "test_mmt_1.mvt" )}',									data )
		self.assertNotIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_mmt_1.mvt" )}',	data )
		self.assertNotIn( f'Updated: {self.property_product_path( "header", "test_mmt_1.mvt" )}',				data )
		self.assertNotIn( f'Updated: {self.property_category_path( "header", "test_mmt_1.mvt" )}',				data )
		self.assertNotIn( f'Updated: {self.jsresource_path( "test_mmt_1.mvt" )}',								data )
		self.assertNotIn( f'Updated: {self.cssresource_path( "test_mmt_1.mvt" )}',								data )
		self.assertNotIn( f'Updated: {self.resourcegroup_path( "test_mmt_1.json" )}',							data )

		self.assertIn( f'Updated: {self.template_path( "test_mmt_2.mvt" )}',									data )
		self.assertIn( f'Updated: {self.property_path( "readytheme_contentsection", "test_mmt_2.mvt" )}',		data )
		self.assertIn( f'Updated: {self.property_product_path( "header", "test_mmt_2.mvt" )}',					data )
		self.assertIn( f'Updated: {self.property_category_path( "header", "test_mmt_2.mvt" )}',					data )
		self.assertIn( f'Updated: {self.jsresource_path( "test_mmt_2.mvt" )}',									data )
		self.assertIn( f'Updated: {self.cssresource_path( "test_mmt_2.mvt" )}',									data )
		self.assertIn( f'Updated: {self.resourcegroup_path( "test_mmt_2.json" )}',								data )

	def test_pull_out_of_sync_with_server( self ):
		def modify_files():
			# Modify template, template settings
			with self.template_open( 'test_pull_out_of_sync.mvt', 'w' ) as fh:
				fh.write( self.generate_random() )

			with self.template_open( 'test_pull_out_of_sync.json', 'w' ) as fh:
				fh.write( self.json_dumps( { 'test_pull_out_of_sync': self.generate_random()} ) )

			# Modify property template, property settings
			with self.property_open( 'readytheme_contentsection', 'test_pull_out_of_sync.mvt', 'w' ) as fh:
				fh.write( self.generate_random() )

			with self.property_open( 'readytheme_contentsection', 'test_pull_out_of_sync.json', 'w' ) as fh:
				fh.write( self.json_dumps( { 'test_pull_out_of_sync': self.generate_random()} ) )

			# Modify JS resource settings, JS resource inline
			with self.jsresource_open( 'test_pull_out_of_sync.json' ) as fh:
				settings = self.json_loads( fh.read() )

			with self.jsresource_open( 'test_pull_out_of_sync.json', 'w' ) as fh:
				settings[ 'active' ] = False

				fh.write( self.json_dumps( settings ) )

			with self.jsresource_open( 'test_pull_out_of_sync.mvt', 'w' ) as fh:
				fh.write( self.generate_random() )

			# Modify CSS resource settings, CSS resource inline
			with self.cssresource_open( 'test_pull_out_of_sync.json' ) as fh:
				settings = self.json_loads( fh.read() )

			with self.cssresource_open( 'test_pull_out_of_sync.json', 'w' ) as fh:
				settings[ 'active' ] = False

				fh.write( self.json_dumps( settings ) )

			with self.cssresource_open( 'test_pull_out_of_sync.mvt', 'w' ) as fh:
				fh.write( self.generate_random() )

		# It should be noted that local JS and CSS resource files, as well as Resource Groups
		# are not tested here as they are not currently versioned
		self.import_store_provisioning_file( 'test_pull_out_of_sync.xml' )
		self.checkout()

		changeset_id = self.latest_changeset_id()

		# Modify all files and push the changes
		modify_files()
		self.push( 'test_pull_out_of_sync' )

		# Pull the original changeset back
		self.pull( c = changeset_id )

		# Modify all the files again and attempt to pull the latest changeset
		modify_files()

		with self.assertRaises( ErrorList ) as e:
			self.pull()

		# Verify the out-of-sync error is given
		self.assertIn( 'Update failed as the following files are out-of-sync with the server and contain local modifications',	e.exception.error_message )
		self.assertIn( self.template_path( 'test_pull_out_of_sync.mvt' ),														e.exception.error_message )
		self.assertIn( self.template_path( 'test_pull_out_of_sync.json' ),														e.exception.error_message )
		self.assertIn( self.property_path( 'readytheme_contentsection', 'test_pull_out_of_sync.mvt' ),							e.exception.error_message )
		self.assertIn( self.property_path( 'readytheme_contentsection', 'test_pull_out_of_sync.json' ),							e.exception.error_message )
		self.assertIn( self.jsresource_path( 'test_pull_out_of_sync.json' ),													e.exception.error_message )
		self.assertIn( self.jsresource_path( 'test_pull_out_of_sync.mvt' ),														e.exception.error_message )
		self.assertIn( self.cssresource_path( 'test_pull_out_of_sync.json' ),													e.exception.error_message )
		self.assertIn( self.cssresource_path( 'test_pull_out_of_sync.mvt' ),													e.exception.error_message )

		# Force pull the latest changeset
		self.pull( force = True )

	def test_pull_out_of_sync_specific_files( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		changeset_id = self.latest_changeset_id()

		# Make a change
		with self.template_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( 'Modified source template 1' )

		# Commit the change
		self.push( 'test_pull_out_of_sync', filepaths = [ self.template_path( 'test_mmt_1.mvt' ) ] )

		# Update back to the original changeset
		self.pull( c = changeset_id )

		# Make a change
		with self.template_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( 'Modified source template 2' )

		with self.assertRaises( ErrorList ) as e:
			self.pull( filepaths = [ self.template_path( 'test_mmt_1.mvt' ) ] )

		self.assertEqual( e.exception.error_message, f'Update failed as the following files contain local modifications:\n\t{self.template_path( "test_mmt_1.mvt" )}' )

		data = self.pull( force = True )

		self.assertIn( f'Updated: {self.template_path( "test_mmt_1.mvt" ) }', data )

		with self.template_open( 'test_mmt_1.mvt' ) as fh:
			self.assertEqual( fh.read(), 'Modified source template 1' )


class Regressions( MMTTest ):
	""" Non-unique property identifiers cause the certain commands from properly working """
	def test_regression_MMT_41( self ):
		self.import_store_provisioning_file( 'regression_MMT-41.xml' )
		self.checkout( ignore_unsynced_properties = False )

		self.assertEqual( self.pull(), 'No files updated' )

	""" Directories that do not exist prior to issuing pull / revert commands raise the FileNotFoundError exception """
	def test_regression_MMT_42( self ):
		self.import_store_provisioning_file( 'regression_MMT-42.xml' )
		self.checkout()

		changeset_id = self.latest_changeset_id()

		# Push a property change so a subsequent pull re-creates the directory structure
		with self.property_open( 'readytheme_contentsection', 'regression_MMT-42.mvt', 'w' ) as fh:
			fh.write( self.generate_random() )

		self.push( 'test_regression_MMT_42' )

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

		# The pull command will re-create all directories, but it will not re-download any files
		# since the state file sha256 hashes match the content on the server.
		self.pull()

		self.assertTrue( os.path.exists( 'templates' ) )
		self.assertTrue( os.path.exists( 'properties' ) )
		self.assertTrue( os.path.exists( 'js' ) )
		self.assertTrue( os.path.exists( 'css' ) )
		self.assertTrue( os.path.exists( 'resourcegroups' ) )
		self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'regression_MMT-42.mvt' ) ) )

		# Force a pull to the original changeset to re-create necessary directories.  Force is required
		# since the property template differs between the previous changeset and the latest changeset AND the property
		# has local modifications (since the file was deleted).
		self.pull( c = changeset_id, force = True )

		self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'regression_MMT-42.mvt' ) ) )

	""" Pull command pulls all file types even if only specific files are requested """
	def test_regression_MMT_59( self ):
		def pull_and_verify_single_file_updated( changeset_id: int, filepath: str ):
			data = self.pull( c = changeset_id, filepaths = [ filepath ] )

			self.assertEqual( data.strip(), f'Updated: {filepath}' )

		self.import_store_provisioning_file( 'regression_MMT-59.xml' )
		self.checkout( ignore_unsynced_properties = False )

		changeset_id = self.latest_changeset_id()

		with self.template_open( 'regression_mmt-59.mvt', 'w' ) as fh:
			fh.write( 'regression_MMT-59 template modified' )

		with self.property_open( 'readytheme_contentsection', 'regression_MMT-59.mvt', 'w' ) as fh:
			fh.write( 'regression_MMT-59 property template modified' )

		with self.property_product_open( 'header', 'regression_MMT-59.mvt', 'w' ) as fh:
			fh.write( 'regression_MMT-59 property product template modified' )

		with self.property_category_open( 'header', 'regression_MMT-59.mvt', 'w' ) as fh:
			fh.write( 'regression_MMT-59 property category template modified' )

		with self.cssresource_open( 'regression_MMT-59.json' ) as fh:
			cssresource_settings = self.json_loads( fh.read() )

		with self.cssresource_open( 'regression_MMT-59.json', 'w' ) as fh:
			cssresource_settings[ 'active' ] = True

			fh.write( self.json_dumps( cssresource_settings ) )

		with self.jsresource_open( 'regression_MMT-59.json' ) as fh:
			jsresource_settings = self.json_loads( fh.read() )

		with self.jsresource_open( 'regression_MMT-59.json', 'w' ) as fh:
			jsresource_settings[ 'active' ] = True

			fh.write( self.json_dumps( jsresource_settings ) )

		with self.resourcegroup_open( 'regression_MMT-59.json' ) as fh:
			resourcegroup_settings = self.json_loads( fh.read() )

		with self.resourcegroup_open( 'regression_MMT-59.json', 'w' ) as fh:
			resourcegroup_settings[ 'linked_js_resources' ].append( 'regression_MMT-59' )

			fh.write( self.json_dumps( resourcegroup_settings ) )

		# Push all changes in a single changeset
		self.push( 'test_regression_MMT_59' )

		# Pull and verify only a single file was updated
		pull_and_verify_single_file_updated( changeset_id, self.template_path( 'regression_mmt-59.mvt' ) )
		pull_and_verify_single_file_updated( changeset_id, self.property_path( 'readytheme_contentsection', 'regression_MMT-59.mvt' ) )
		pull_and_verify_single_file_updated( changeset_id, self.property_product_path( 'header', 'regression_MMT-59.mvt' ) )
		pull_and_verify_single_file_updated( changeset_id, self.property_category_path( 'header', 'regression_MMT-59.mvt' ) )
		pull_and_verify_single_file_updated( changeset_id, self.cssresource_path( 'regression_MMT-59.json' ) )
		pull_and_verify_single_file_updated( changeset_id, self.jsresource_path( 'regression_MMT-59.json' ) )
		pull_and_verify_single_file_updated( changeset_id, self.resourcegroup_path( 'regression_MMT-59.json' ) )

		# Update to the latest changeset
		data = self.pull()

		# Verify multiple files are updated
		self.assertIn( f'Updated: {self.template_path( "regression_mmt-59.mvt" )}', data )
		self.assertIn( f'Updated: {self.property_path( "readytheme_contentsection", "regression_MMT-59.mvt" )}', data )
		self.assertIn( f'Updated: {self.property_product_path( "header", "regression_MMT-59.mvt" )}', data )
		self.assertIn( f'Updated: {self.property_category_path( "header", "regression_MMT-59.mvt" )}', data )
		self.assertIn( f'Updated: {self.cssresource_path( "regression_MMT-59.json" )}', data )
		self.assertIn( f'Updated: {self.jsresource_path( "regression_MMT-59.json" )}', data )
		self.assertIn( f'Updated: {self.resourcegroup_path( "regression_MMT-59.json" )}', data )
