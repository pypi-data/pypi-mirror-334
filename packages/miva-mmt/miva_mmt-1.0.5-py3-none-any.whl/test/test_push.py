import os
import tempfile

import merchantapi.request

from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_push_validate( self ):
		self.checkout()

		with self.assertRaises( Error ) as e:
			self.push( None )

		self.assertEqual( e.exception.error_message, 'Either the --notes parameter must be specified or the \'editor\' configuration setting must be set' )

		with self.assertRaises( Error ) as e:
			self.push( '' )

		self.assertEqual( e.exception.error_message, 'Notes cannot be blank' )

	def test_push_no_files_modified( self ):
		self.checkout()

		data = self.push( 'test_push_no_files_modified' )

		self.assertEqual( data, 'No files to commit' )

	def test_push_invalid_template_settings_json( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.template_open( 'test_mmt_1.json', 'w' ) as fh:
			fh.write( 'invalid test_push_invalid_template_settings_json' )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_json' )

		self.assertIn( f'Failed to parse JSON in \'{self.template_path( "test_mmt_1.json" )}\': ', e.exception.error_message )

	def test_push_invalid_property_settings_json( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.property_open( 'readytheme_contentsection', 'test_mmt_1.json', 'w' ) as fh:
			fh.write( 'invalid json' )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_property_settings_json' )

		self.assertIn( f'Failed to parse JSON in \'{self.property_path( "readytheme_contentsection", "test_mmt_1.json" )}\': ', e.exception.error_message )

	def test_push_invalid_jsresource_settings_json( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.jsresource_open( 'test_mmt_1.json', 'w' ) as fh:
			fh.write( 'invalid json' )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_jsresource_settings_json' )

		self.assertIn( f'Failed to parse JSON in \'{self.jsresource_path( "test_mmt_1.json" )}\': ', e.exception.error_message )

		self.revert()

		with self.jsresource_open( 'test_mmt_2.json' ) as fh:
			settings = self.json_loads( fh.read() )

		with self.jsresource_open( 'test_mmt_2.json', 'w' ) as fh:
			del settings[ 'active' ]

			fh.write( self.json_dumps( settings ) )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_jsresource_settings_json' )

		self.assertIn( f'Failed building JS resource changeset for \'{self.jsresource_path( "test_mmt_2.json" )}\'', e.exception.error_message )

	def test_push_invalid_cssresource_settings_json( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.cssresource_open( 'test_mmt_1.json', 'w' ) as fh:
			fh.write( 'invalid json' )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_cssresource_settings_json' )

		self.assertIn( f'Failed to parse JSON in \'{self.cssresource_path( "test_mmt_1.json" )}\': ', e.exception.error_message )

		self.revert()

		with self.cssresource_open( 'test_mmt_2.json' ) as fh:
			settings = self.json_loads( fh.read() )

		with self.cssresource_open( 'test_mmt_2.json', 'w' ) as fh:
			del settings[ 'active' ]

			fh.write( self.json_dumps( settings ) )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_cssresource_settings_json' )

		self.assertIn( f'Failed building CSS resource changeset for \'{self.cssresource_path( "test_mmt_2.json" )}\'', e.exception.error_message )

	def test_push_invalid_resourcegroup_settings_json( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.resourcegroup_open( 'test_mmt_1.json', 'w' ) as fh:
			fh.write( 'invalid json' )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_resourcegroup_settings_json' )

		self.assertIn( f'Failed to parse JSON in \'{self.resourcegroup_path( "test_mmt_1.json" )}\': ', e.exception.error_message )

		self.revert()

		with self.resourcegroup_open( 'test_mmt_2.json' ) as fh:
			settings = self.json_loads( fh.read() )

		with self.resourcegroup_open( 'test_mmt_2.json', 'w' ) as fh:
			del settings[ 'linked_js_resources' ]

			fh.write( self.json_dumps( settings ) )

		with self.assertRaises( Error ) as e:
			self.push( 'test_push_invalid_resourcegroup_settings_json' )

		self.assertIn( f'Failed building Resource Group changeset for \'{self.resourcegroup_path( "test_mmt_2.json" )}\'', e.exception.error_message )

	def test_push_empty_notes( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.template_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( '' )

		self.config_set( 'editor', [ 'true' ] )

		data = self.push( None )

		self.assertEqual( data, 'Aborting commit due to empty commit notes' )

	def test_push_invalid_external_editor( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.template_open( 'test_mmt_1.mvt', 'w' ) as fh:
			fh.write( '' )

		with self.assertRaises( Error ) as e:
			self.config_set( 'editor', [ 'some_fake_binary' ] )

			self.push( None )

		self.assertIn( 'Failed to open external editor \'some_fake_binary\': ', e.exception.error_message )

	def test_push( self ):
		self.import_store_provisioning_file( 'test_push.xml' )

		# Checkout and make modifications to both the page template and the settings
		self.checkout()
		with self.template_open( 'test_push.json', 'r' ) as fh:
			settings			= self.json_loads( fh.read() )
			per_page			= settings.get( 'all_products' ).get( 'per_page' )
			page_display_count	= settings.get( 'all_products' ).get( 'page_display_count' )

		with self.template_open( 'test_push.mvt', 'w' ) as fh:
			fh.write( 'updated template code' )

		with self.template_open( 'test_push.json', 'w' ) as fh:
			settings[ 'all_products' ][ 'per_page' ]	= per_page + 500 # modify the per_page value
			settings[ 'test_push' ]					= True # add custom setting

			fh.write( self.json_dumps( settings ) )

		with self.property_open( 'readytheme_contentsection', 'test_push.json', 'r' ) as fh:
			settings			= self.json_loads( fh.read() )

		with self.property_open( 'readytheme_contentsection', 'test_push.mvt', 'w' ) as fh:
			fh.write( 'updated readytheme contentsection template code' )

		with self.property_open( 'readytheme_contentsection', 'test_push.json', 'w' ) as fh:
			settings[ 'name' ] = 'test_push updated'

			fh.write( self.json_dumps( settings ) )

		# Commit only some of the changes
		data = self.push( 'test_push', [ 'templates/test_push.mvt', 'templates/test_push.json' ] )

		self.assertIn( 'templates/test_push.mvt',									data )
		self.assertIn( 'templates/test_push.json',								data )
		self.assertNotIn( 'properties/readytheme_contentsection/test_push.mvt',	data )
		self.assertNotIn( 'properties/readytheme_contentsection/test_push.json',	data )

		# Commit the rest of the changes
		data = self.push( 'test_push' )

		self.assertNotIn( 'templates/test_push.mvt',								data )
		self.assertNotIn( 'templates/test_push.json',								data )
		self.assertIn( 'properties/readytheme_contentsection/test_push.mvt',		data )
		self.assertIn( 'properties/readytheme_contentsection/test_push.json',		data )

		# Checkout and verify the changes
		self.checkout()
		with self.template_open( 'test_push.mvt', 'r' ) as fh:
			self.assertEqual( 'updated template code', fh.read() )

		with self.template_open( 'test_push.json', 'r' ) as fh:
			settings = self.json_loads( fh.read() )

			self.assertEqual( per_page + 500,		settings.get( 'all_products' ).get( 'per_page' ) )
			self.assertEqual( page_display_count,	settings.get( 'all_products' ).get( 'page_display_count' ) )
			self.assertEqual( 1,					settings.get( 'test_push' ) )

		with self.property_open( 'readytheme_contentsection', 'test_push.mvt', 'r' ) as fh:
			self.assertEqual( 'updated readytheme contentsection template code', fh.read() )

		with self.property_open( 'readytheme_contentsection', 'test_push.json', 'r' ) as fh:
			settings = self.json_loads( fh.read() )

			self.assertEqual( 'test_push updated', settings.get( 'name' ) )

	def test_push_jsresources( self ):
		expected_results	= self.load_expected_results( 'test_push_jsresources.json' )

		# Upload 2 files to verify switching file paths works as expected
		upload_response_1	= self.upload_js_file_from_data( 'test_push_jsresources_local_log.js', 'console.log( \'test_push_jsresources_local_log.js\' );' ).json()
		upload_filepath_1	= upload_response_1.get( 'data' ).get( 'file_path' )
		upload_response_2	= self.upload_js_file_from_data( 'test_push_jsresources_local_alert.js', 'alert( \'test_push_jsresources_local_alert.js\' );' ).json()
		upload_filepath_2	= upload_response_2.get( 'data' ).get( 'file_path' )

		def modify_inline():
			with self.jsresource_open( 'test_push_jsresources_inline.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'active' ]	= False

				del settings[ 'attributes' ][ 1 ]
				del settings[ 'linked_pages' ][ 1 ]

			with self.jsresource_open( 'test_push_jsresources_inline.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.jsresource_open( 'test_push_jsresources_inline.mvt', 'w' ) as fh:
				fh.write( 'console.log( \'test_push_jsresources_inline.mvt updated\' );' )

		def modify_local():
			with self.jsresource_open( 'test_push_jsresources_local_1.json' ) as fh:
				settings							= self.json_loads( fh.read() )
				settings[ 'branchless_filepath' ]	= upload_filepath_2

			with self.jsresource_open( 'test_push_jsresources_local_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.jsresource_open( 'test_push_jsresources_local_1.js', 'w' ) as fh:
				fh.write( 'console.log( \'test_push_jsresources_local_1.js updated\' );' )

		def modify_external():
			with self.jsresource_open( 'test_push_jsresources_external.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'filepath' ]	= 'http://localhost/test_push_jsresources_external_updated.js'
				settings[ 'is_global' ]	= True

			with self.jsresource_open( 'test_push_jsresources_external.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

		def modify_combinedresource():
			with self.jsresource_open( 'test_push_jsresources_combined.json' ) as fh:
				settings				= self.json_loads( fh.read() )

				del settings[ 'linked_resources' ][ 1 ]

			with self.jsresource_open( 'test_push_jsresources_combined.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

		def verify_inline():
			expected			= expected_results.get( 'test_push_jsresources_inline' )
			expected_source		= expected.get( 'source' )
			expected_settings	= expected.get( 'settings' )

			with self.jsresource_open( 'test_push_jsresources_inline.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.jsresource_open( 'test_push_jsresources_inline.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_local():
			expected									= expected_results.get( 'test_push_jsresources_local_1' )
			expected_source								= expected.get( 'source' )
			expected_settings							= expected.get( 'settings' )
			expected_settings[ 'branchless_filepath' ]	= upload_filepath_2

			with self.jsresource_open( 'test_push_jsresources_local_1.js' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.jsresource_open( 'test_push_jsresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_external():
			expected			= expected_results.get( 'test_push_jsresources_external' )
			expected_settings	= expected.get( 'settings' )

			with self.jsresource_open( 'test_push_jsresources_external.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_combinedresource():
			expected			= expected_results.get( 'test_push_jsresources_combined' )
			expected_settings	= expected.get( 'settings' )

			with self.jsresource_open( 'test_push_jsresources_combined.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		self.import_store_provisioning_file( 'test_push_jsresources.xml', [ ( '%test_push_jsresources_local_filepath%', upload_filepath_1 ) ] )
		self.checkout()

		modify_inline()
		modify_local()
		modify_external()
		modify_combinedresource()

		self.push( 'test_push_jsresources' )
		self.assertEqual( self.status(), 'No files modified' )

		self.checkout()

		verify_inline()
		verify_local()
		verify_external()
		verify_combinedresource()

	def test_push_cssresources( self ):
		expected_results	= self.load_expected_results( 'test_push_cssresources.json' )

		# Upload 2 files to verify switching file paths works as expected
		upload_response_1	= self.upload_css_file_from_data( 'test_push_cssresources_local_div.css', 'div { font-weight: bold; }' ).json()
		upload_filepath_1	= upload_response_1.get( 'data' ).get( 'file_path' )
		upload_response_2	= self.upload_css_file_from_data( 'test_push_cssresources_local_span.css', 'span { font-style: italic; }' ).json()
		upload_filepath_2	= upload_response_2.get( 'data' ).get( 'file_path' )

		def modify_inline():
			with self.cssresource_open( 'test_push_cssresources_inline.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'active' ]	= False

				del settings[ 'attributes' ][ 1 ]
				del settings[ 'linked_pages' ][ 1 ]

			with self.cssresource_open( 'test_push_cssresources_inline.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.cssresource_open( 'test_push_cssresources_inline.mvt', 'w' ) as fh:
				fh.write( 'span { margin: 50px; }' )

		def modify_local():
			with self.cssresource_open( 'test_push_cssresources_local_1.json' ) as fh:
				settings							= self.json_loads( fh.read() )
				settings[ 'branchless_filepath' ]	= upload_filepath_2

			with self.cssresource_open( 'test_push_cssresources_local_1.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

			with self.cssresource_open( 'test_push_cssresources_local_1.css', 'w' ) as fh:
				fh.write( 'div { color: orange; }' )

		def modify_external():
			with self.cssresource_open( 'test_push_cssresources_external.json' ) as fh:
				settings				= self.json_loads( fh.read() )
				settings[ 'filepath' ]	= 'http://localhost/test_push_cssresources_external_updated.css'
				settings[ 'is_global' ]	= True

			with self.cssresource_open( 'test_push_cssresources_external.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

		def modify_combinedresource():
			with self.cssresource_open( 'test_push_cssresources_combined.json' ) as fh:
				settings				= self.json_loads( fh.read() )

				del settings[ 'linked_resources' ][ 1 ]

			with self.cssresource_open( 'test_push_cssresources_combined.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

		def verify_inline():
			expected			= expected_results.get( 'test_push_cssresources_inline' )
			expected_source		= expected.get( 'source' )
			expected_settings	= expected.get( 'settings' )

			with self.cssresource_open( 'test_push_cssresources_inline.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.cssresource_open( 'test_push_cssresources_inline.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_local():
			expected									= expected_results.get( 'test_push_cssresources_local_1' )
			expected_source								= expected.get( 'source' )
			expected_settings							= expected.get( 'settings' )
			expected_settings[ 'branchless_filepath' ]	= upload_filepath_2

			with self.cssresource_open( 'test_push_cssresources_local_1.css' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.cssresource_open( 'test_push_cssresources_local_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_external():
			expected			= expected_results.get( 'test_push_cssresources_external' )
			expected_settings	= expected.get( 'settings' )

			with self.cssresource_open( 'test_push_cssresources_external.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_combinedresource():
			expected			= expected_results.get( 'test_push_cssresources_combined' )
			expected_settings	= expected.get( 'settings' )

			with self.cssresource_open( 'test_push_cssresources_combined.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		self.import_store_provisioning_file( 'test_push_cssresources.xml', [ ( '%test_push_cssresources_local_filepath%', upload_filepath_1 ) ] )
		self.checkout()

		modify_inline()
		modify_local()
		modify_external()
		modify_combinedresource()

		self.push( 'test_push_cssresources' )
		self.assertEqual( self.status(), 'No files modified' )

		self.checkout()

		verify_inline()
		verify_local()
		verify_external()
		verify_combinedresource()

	def test_push_resourcegroups( self ):
		expected_results = self.load_expected_results( 'test_push_resourcegroups.json' )

		def modify_settings_file():
			with self.resourcegroup_open( 'test_push_resourcegroups.json' ) as fh:
				settings = self.json_loads( fh.read() )

				del settings[ 'linked_js_resources' ][ 1 ]
				del settings[ 'linked_css_resources' ][ 0 ]

			with self.resourcegroup_open( 'test_push_resourcegroups.json', 'w' ) as fh:
				fh.write( self.json_dumps( settings ) )

		def verify_settings_file():
			expected			= expected_results.get( 'test_push_resourcegroups' )
			expected_settings	= expected.get( 'settings' )

			with self.resourcegroup_open( 'test_push_resourcegroups.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		self.import_store_provisioning_file( 'test_push_resourcegroups.xml' )
		self.checkout()

		modify_settings_file()

		self.push( 'test_push_resourcegroups' )
		self.assertEqual( self.status(), 'No files modified' )

		self.checkout()

		verify_settings_file()

	def test_push_delete_template( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.template_open( 'test_mmt_1.mvt' ) as fh:
			self.assertNotEqual( fh.read(), '' )

		os.remove( self.template_path( 'test_mmt_1.mvt' ) )
		self.push( 'test_push_delete_template' )

		self.checkout()

		with self.template_open( 'test_mmt_1.mvt' ) as fh:
			self.assertEqual( fh.read(), '' )

	def test_push_delete_template_settings( self ):
		self.import_store_provisioning_file( 'test_push_delete_template_settings.xml' )
		self.checkout()

		with self.template_open( 'test_push_delete_template_settings.json', 'w' ) as fh:
			fh.write( '' )

		self.push( 'test_push_delete_template_settings' )

		self.assertFalse( os.path.exists( self.template_path( 'test_push_delete_template_settings.json' ) ) )

	def test_push_delete_property_template( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.property_open( 'readytheme_contentsection', 'test_mmt_1.mvt' ) as fh:
			self.assertNotEqual( fh.read(), '' )

		os.remove( self.property_path( 'readytheme_contentsection', 'test_mmt_1.mvt' ) )
		self.push( 'test_push_delete_property_template' )

		self.checkout()

		with self.property_open( 'readytheme_contentsection', 'test_mmt_1.mvt' ) as fh:
			self.assertEqual( fh.read(), '' )

	def test_push_delete_property_settings( self ):
		self.import_store_provisioning_file( 'test_push_delete_property_settings.xml' )
		self.checkout()

		with self.property_open( 'readytheme_contentsection', 'test_push_delete_property_settings.json', 'w' ) as fh:
			fh.write( '' )

		self.push( 'test_push_delete_property_settings' )

		self.assertFalse( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_push_delete_property_settings.json' ) ) )

	def test_push_external_editor( self ):
		def verify_external_editor_commit_file_contents():
			# Commit does not work here as the commit output file is never populated with a message
			temp_output_file			= tempfile.NamedTemporaryFile( delete = False )
			custom_external_editor_file	= self._create_custom_external_editor( f'cat $1 > {temp_output_file.name}' )

			try:
				with self.template_open( 'test_push_external_editor_1.mvt', 'w' ) as fh:
					fh.write( 'test_push_external_editor_1' )

				self.tag_delete_all()

				# Attempt a commit and verify the tags and files to be committed
				self.push( None )

				with open( temp_output_file.name ) as fh:
					data = fh.read()

					self.assertIn( 'Tags: <None>', data )
					self.assertIn( self.template_path( 'test_push_external_editor_1.mvt' ), data )
					self.assertNotIn( self.template_path( 'test_push_external_editor_2.mvt' ), data )

				self.tag_set( [ 'test', 'case', 'passes' ] )

				# Attempt a commit and verify the tags and files to be committed
				self.push( None )

				with open( temp_output_file.name ) as fh:
					data = fh.read()

					self.assertIn( 'Tags: #test #case #passes', data )
					self.assertIn( self.template_path( 'test_push_external_editor_1.mvt' ), data )
					self.assertNotIn( self.template_path( 'test_push_external_editor_2.mvt' ), data )
			finally:
				os.unlink( custom_external_editor_file.name )
				os.unlink( temp_output_file.name )

		def verify_external_editor_commit():
			# Commit works here as the commit output file is populated via the echo
			custom_external_editor_file = self._create_custom_external_editor( f'echo test_push_external_editor_1 > $1' )

			try:
				with self.template_open( 'test_push_external_editor_1.mvt', 'w' ) as fh:
					fh.write( custom_external_editor_file.name )

				self.push( None )
			finally:
				os.unlink( custom_external_editor_file.name )

			self.pull()

			with self.template_open( 'test_push_external_editor_1.mvt' ) as fh:
				self.assertEqual( fh.read(), custom_external_editor_file.name )

			# Load the latest changeset to verify that the commit message was set correctly
			request		= merchantapi.request.ChangesetListLoadQuery( self.merchantapi_client() )
			request.set_count( 1 )
			request.set_sort( 'id', request.SORT_DESCENDING )
			request.set_branch_name( self.config.get( 'branch_name' ) )

			response	= request.send()
			self.assertTrue( len( response.get_changesets() ) > 0 )
			self.assertEqual( response.get_changesets()[ 0 ].get_notes(), 'test_push_external_editor_1' )

		self.import_store_provisioning_file( 'test_push_external_editor.xml' )
		self.checkout()

		verify_external_editor_commit_file_contents()
		verify_external_editor_commit()

	def _create_custom_external_editor( self, script: str ) -> tempfile.NamedTemporaryFile:
		file = tempfile.NamedTemporaryFile( mode = 'w+', delete = False )

		try:
			file.write( '#!/bin/bash\n' )
			file.write( script )
			file.close()

			os.chmod( file.name, 0o777 )

			self.config_set( 'editor', [ file.name ] )
		except:
			os.unlink( file.name )

			raise

		return file


class Regressions( MMTTest ):
	def test_regression_MMT_53( self ):
		self.import_store_provisioning_file( 'regression_MMT-53.xml' )
		self.checkout( ignore_unsynced_properties = False )

		with self.property_product_open( 'header', 'regression_MMT-53.mvt', 'w' ) as fh:
			fh.write( 'regression_MMT-53 product header updated' )

		with self.property_category_open( 'header', 'regression_MMT-53.mvt', 'w' ) as fh:
			fh.write( 'regression_MMT-53 category header updated' )

		self.push( 'test_regression_MMT_53' )

		self.checkout( ignore_unsynced_properties = False )

		with self.property_product_open( 'header', 'regression_MMT-53.mvt' ) as fh:
			self.assertEqual( fh.read(), 'regression_MMT-53 product header updated' )

		with self.property_category_open( 'header', 'regression_MMT-53.mvt' ) as fh:
			self.assertEqual( fh.read(), 'regression_MMT-53 category header updated' )
