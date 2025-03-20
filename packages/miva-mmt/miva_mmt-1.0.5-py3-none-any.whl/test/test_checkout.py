import os
import hashlib
import tempfile

import merchantapi.request

from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_checkout_validate( self ):
		with self.assertRaises( Error ) as e:
			self.checkout( args = { 'path': os.devnull } )

		self.assertEqual( e.exception.error_message, f'\'{os.devnull}\' is not a directory' )

		valid_args						= self.checkout_args()
		invalid_args					= valid_args.copy()
		invalid_args[ 'remote-key' ]	= 'invalid'

		with self.assertRaises( Error ) as e:
			self.checkout( args = invalid_args )

		self.assertEqual( e.exception.error_message, 'Remote key \'invalid\' does not exist' )

		self.credential_add( 'test_validate_credential_key' )
		self.remote_add( 'test_validate_remote_key', credential_key = 'test_validate_credential_key' )
		self.credential_delete( 'test_validate_credential_key' )

		with self.assertRaises( Error ) as e:
			self.checkout( remote_key = 'test_validate_remote_key' )

		self.assertEqual( e.exception.error_message, 'Credential key \'test_validate_credential_key\' associated with remote key \'test_validate_remote_key\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.checkout( path = '' )

		self.assertEqual( e.exception.error_message, 'A Path value is required' )

	def test_checkout_access_denied( self ):
		self.credential_add( key = 'test_checkout_access_denied', token = 'invalid' )
		self.remote_add( 'test_checkout_access_denied', credential_key = 'test_checkout_access_denied' )

		args					= self.checkout_args()
		args[ 'remote-key' ]	= 'test_checkout_access_denied'

		with self.assertRaises( Error ) as e:
			self.checkout( args = args )

		self.assertEqual( e.exception.error_message, 'BranchList_Load_Query: Access denied' )

	def test_checkout_invalid_branch( self ):
		self.remote_add( 'test_checkout_invalid_branch', branch_name = 'invalid' )

		with self.assertRaises( Error ) as e:
			self.checkout( remote_key = 'test_checkout_invalid_branch' )

		self.assertEqual( e.exception.error_message, 'Branch \'invalid\' does not exist' )

	def test_checkout_invalid_changeset( self ):
		with self.assertRaises( Error ) as e:
			self.checkout( c = 100000 )

		self.assertEqual( e.exception.error_message, 'Changeset 100000 does not exist' )

	def test_checkout_invalid_path( self ):
		invalid_directory = 'd' * 1024

		with self.assertRaises( Error ) as e:
			self.checkout( path = invalid_directory )

		self.assertIn( f'Failed to create directory \'{invalid_directory}\'', e.exception.error_message )

	def test_checkout( self ):
		self.import_store_provisioning_file( 'test_checkout.xml' )

		args = self.checkout_args()
		os.chdir( args.get( 'path' ) )

		def checkout():
			self.checkout( args = args )

			self.assertTrue( os.path.isdir( '.mmt' ) )
			self.assertTrue( os.path.isfile( os.path.join( '.mmt', 'state.json' ) ) )
			self.assertTrue( os.path.isfile( os.path.join( '.mmt', 'config.json' ) ) )

		# Verify checking out 2 times into the same directory works

		checkout()

		with self.template_open( 'test_checkout_1.mvt', 'w' ) as fh:
			fh.write( 'test_checkout_1 updated' )

		checkout()

		with self.template_open( 'test_checkout_1.mvt' ) as fh:
			self.assertEqual( fh.read(), 'test_checkout_1 template' )

	def test_checkout_reinitialize( self ):
		self.import_store_provisioning_file( 'basic_setup.xml' )
		self.checkout()

		with self.template_open( 'test_mmt_1.mvt' ) as fh:
			test_mmt_1_source = fh.read()

		with self.template_open( 'test_mmt_2.mvt', 'w' ) as fh:
			fh.write( 'test_checkout_reinitialize' )

		os.unlink( self.template_path( 'test_mmt_1.mvt' ) )

		self.checkout( path = '.', reinitialize = True )

		self.assertNotIn( self.template_path( 'test_mmt_1.mvt' ),	self.status() )
		self.assertIn( self.template_path( 'test_mmt_2.mvt' ),		self.status() )

		with self.template_open( 'test_mmt_1.mvt' ) as fh:
			self.assertEqual( fh.read(), test_mmt_1_source )

		with self.template_open( 'test_mmt_2.mvt' ) as fh:
			self.assertEqual( fh.read(), 'test_checkout_reinitialize' )

	def test_checkout_ssh( self ):
		self.import_store_provisioning_file( 'test_checkout_ssh.xml' )

		def verify( test: str, private_key: str, public_key: str ):
			with self.other_data_open( public_key ) as fh:
				public_key = fh.read()

			self.import_domain_provisioning_file( 'user_update_public_key.xml', [ ( '%username%', self.config.get( 'admin_username' ) ), ( '%public_key%', public_key ) ] )

			self.credential_add( key = test, ssh_private_key = private_key )
			self.remote_add( key = test, credential_key = test )

			self.checkout( remote_key = test )

			self.assertTrue( os.path.exists( self.template_path( 'test_checkout_ssh.mvt' ) ) )

			with self.template_open( 'test_checkout_ssh.mvt' ) as fh:
				self.assertEqual( fh.read(), 'test_checkout_ssh template' )

		verify( 'RSA OpenSSH',	self.other_data_path( 'id_rsa_openssh' ),	self.other_data_path( 'id_rsa_openssh.pub' ) )
		verify( 'RSA PEM',		self.other_data_path( 'id_rsa_pem' ),		self.other_data_path( 'id_rsa_pem.pub' ) )

	def test_checkout_templates( self ):
		expected_results = self.load_expected_results( 'test_checkout_templates.json' )

		def verify_checkout_template():
			self.assertTrue( os.path.isfile( self.template_path( 'test_checkout_templates.mvt' ) ) )
			self.assertTrue( os.path.isfile( self.template_path( 'test_checkout_templates.json' ) ) )

			expected			= expected_results.get( 'test_checkout_templates' )
			expected_source		= expected.get( 'source' )
			expected_settings	= expected.get( 'settings' ).get( 'product_display' )

			with self.template_open( 'test_checkout_templates.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

			with self.template_open( 'test_checkout_templates.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings, settings_sub_section = 'product_display' )

		def verify_checkout_template_no_settings():
			self.assertTrue( os.path.isfile( self.template_path( 'test_checkout_templates_no_settings.mvt' ) ) )
			self.assertFalse( os.path.isfile( self.template_path( 'test_checkout_templates_no_settings.json' ) ) )

			expected		= expected_results.get( 'test_checkout_templates_no_settings' )
			expected_source	= expected.get( 'source' )

			with self.template_open( 'test_checkout_templates_no_settings.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

		self.import_store_provisioning_file( 'test_checkout_templates.xml' )
		self.checkout()

		verify_checkout_template()
		verify_checkout_template_no_settings()

	def test_checkout_properties( self ):
		expected_results = self.load_expected_results( 'test_checkout_properties.json' )

		def verify_checkout_property():
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_checkout_properties.mvt' ) ) )
			self.assertTrue( os.path.exists( self.property_path( 'readytheme_contentsection', 'test_checkout_properties.json' ) ) )

			expected			= expected_results.get( 'readytheme_contentsection_property' )
			expected_settings	= expected.get( 'settings' )
			expected_source		= expected.get( 'source' )

			with self.property_open( 'readytheme_contentsection', 'test_checkout_properties.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			with self.property_open( 'readytheme_contentsection', 'test_checkout_properties.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

		def verify_checkout_property_product():
			self.assertTrue( os.path.exists( self.property_product_path( 'header', 'test_checkout_properties.mvt' ) ) )
			self.assertFalse( os.path.exists( self.property_product_path( 'header', 'test_checkout_properties.json' ) ) )

			self.assertTrue( os.path.exists( self.property_product_path( 'footer', 'test_checkout_properties.mvt' ) ) )
			self.assertFalse( os.path.exists( self.property_product_path( 'footer', 'test_checkout_properties.json' ) ) )

			expected_header			= expected_results.get( 'product_property' ).get( 'header' )
			expected_header_source	= expected_header.get( 'source' )

			expected_footer			= expected_results.get( 'product_property' ).get( 'footer' )
			expected_footer_source	= expected_footer.get( 'source' )

			with self.property_product_open( 'header', 'test_checkout_properties.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_header_source )

			with self.property_product_open( 'footer', 'test_checkout_properties.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_footer_source )

		def verify_checkout_property_category():
			self.assertTrue( os.path.exists( self.property_category_path( 'header', 'test_checkout_properties.mvt' ) ) )
			self.assertFalse( os.path.exists( self.property_category_path( 'header', 'test_checkout_properties.json' ) ) )

			self.assertTrue( os.path.exists( self.property_category_path( 'footer', 'test_checkout_properties.mvt' ) ) )
			self.assertFalse( os.path.exists( self.property_category_path( 'footer', 'test_checkout_properties.json' ) ) )

			expected_header			= expected_results.get( 'category_property' ).get( 'header' )
			expected_header_source	= expected_header.get( 'source' )

			expected_footer			= expected_results.get( 'category_property' ).get( 'footer' )
			expected_footer_source	= expected_footer.get( 'source' )

			with self.property_category_open( 'header', 'test_checkout_properties.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_header_source )

			with self.property_category_open( 'footer', 'test_checkout_properties.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_footer_source )

		def verify_checkout_property_notemplate():
			self.assertTrue( os.path.exists( self.property_category_path( 'cssui_cattitle', 'test_checkout_properties.json' ) ) )
			self.assertFalse( os.path.exists( self.property_category_path( 'cssui_cattitle', 'test_checkout_properties.mvt' ) ) )

			expected			= expected_results.get( 'notemplate' )
			expected_settings	= expected.get( 'settings' )

			with self.property_category_open( 'cssui_cattitle', 'test_checkout_properties.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_checkout_property_nosettings():
			# Currently there are no properties that exist / can be created that do
			# not have settings that are not a product / category property, so this
			# is tested in the product / category checkout functions above
			pass

		self.import_store_provisioning_file( 'test_checkout_properties.xml' )
		self.checkout( ignore_unsynced_properties = False ) # sync all properties to get the product / category header and footers along with the cattitle settings

		verify_checkout_property()
		verify_checkout_property_product()
		verify_checkout_property_category()
		verify_checkout_property_notemplate()
		verify_checkout_property_nosettings()

	def test_checkout_jsresources( self ):
		expected_results	= self.load_expected_results( 'test_checkout_jsresources.json' )
		upload_response		= self.upload_js_file_from_data( 'test_checkout_jsresources_local.js', 'console.log( \'test_checkout_jsresources_local.js\' )' ).json()
		upload_filepath		= upload_response.get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_checkout_jsresources.xml', [ ( '%test_checkout_jsresources_local_filepath%', upload_filepath ) ] )
		self.checkout()

		def verify_checkout_local():
			self.assertTrue( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_local.json' ) ) )
			self.assertTrue( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_local.js' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_local.mvt' ) ) )

			expected									= expected_results.get( 'test_checkout_jsresources_local' )
			expected_settings							= expected.get( 'settings' )
			expected_settings[ 'branchless_filepath' ]	= upload_filepath
			expected_source								= expected.get( 'source' )

			with self.jsresource_open( 'test_checkout_jsresources_local.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			with self.jsresource_open( 'test_checkout_jsresources_local.js' ) as fh:
				self.assertEqual( fh.read(), expected_source )

		def verify_checkout_external():
			self.assertTrue( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_external.json' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_external.js' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_external.mvt' ) ) )

			expected			= expected_results.get( 'test_checkout_jsresources_external' )
			expected_settings	= expected.get( 'settings' )

			with self.jsresource_open( 'test_checkout_jsresources_external.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_checkout_inline():
			self.assertTrue( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_inline.json' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_inline.js' ) ) )
			self.assertTrue( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_inline.mvt' ) ) )

			expected			= expected_results.get( 'test_checkout_jsresources_inline' )
			expected_settings	= expected.get( 'settings' )
			expected_source		= expected.get( 'source' )

			with self.jsresource_open( 'test_checkout_jsresources_inline.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			with self.jsresource_open( 'test_checkout_jsresources_inline.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

		def verify_checkout_combined():
			self.assertTrue( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_combined.json' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_combined.js' ) ) )
			self.assertFalse( os.path.exists( self.jsresource_path( 'test_checkout_jsresources_combined.mvt' ) ) )

			expected			= expected_results.get( 'test_checkout_jsresources_combined' )
			expected_settings	= expected.get( 'settings' )

			with self.jsresource_open( 'test_checkout_jsresources_combined.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		verify_checkout_local()
		verify_checkout_external()
		verify_checkout_inline()
		verify_checkout_combined()

	def test_checkout_cssresources( self ):
		expected_results	= self.load_expected_results( 'test_checkout_cssresources.json' )
		upload_response		= self.upload_css_file_from_data( 'test_checkout_cssresources_local.css', 'html { margin: 0; }' ).json()
		upload_filepath		= upload_response.get( 'data' ).get( 'file_path' )

		self.import_store_provisioning_file( 'test_checkout_cssresources.xml', [ ( '%test_checkout_cssresources_local_filepath%', upload_filepath ) ] )
		self.checkout()

		def verify_checkout_local():
			self.assertTrue( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_local.json' ) ) )
			self.assertTrue( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_local.css' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_local.mvt' ) ) )

			expected									= expected_results.get( 'test_checkout_cssresources_local' )
			expected_settings							= expected.get( 'settings' )
			expected_settings[ 'branchless_filepath' ]	= upload_filepath
			expected_source								= expected.get( 'source' )

			with self.cssresource_open( 'test_checkout_cssresources_local.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			with self.cssresource_open( 'test_checkout_cssresources_local.css' ) as fh:
				self.assertEqual( fh.read(), expected_source )

		def verify_checkout_external():
			self.assertTrue( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_external.json' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_external.css' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_external.mvt' ) ) )

			expected			= expected_results.get( 'test_checkout_cssresources_external' )
			expected_settings	= expected.get( 'settings' )

			with self.cssresource_open( 'test_checkout_cssresources_external.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		def verify_checkout_inline():
			self.assertTrue( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_inline.json' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_inline.css' ) ) )
			self.assertTrue( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_inline.mvt' ) ) )

			expected			= expected_results.get( 'test_checkout_cssresources_inline' )
			expected_settings	= expected.get( 'settings' )
			expected_source		= expected.get( 'source' )

			with self.cssresource_open( 'test_checkout_cssresources_inline.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

			with self.cssresource_open( 'test_checkout_cssresources_inline.mvt' ) as fh:
				self.assertEqual( fh.read(), expected_source )

		def verify_checkout_combined():
			self.assertTrue( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_combined.json' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_combined.css' ) ) )
			self.assertFalse( os.path.exists( self.cssresource_path( 'test_checkout_cssresources_combined.mvt' ) ) )

			expected			= expected_results.get( 'test_checkout_cssresources_combined' )
			expected_settings	= expected.get( 'settings' )

			with self.cssresource_open( 'test_checkout_cssresources_combined.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_settings )

		verify_checkout_local()
		verify_checkout_external()
		verify_checkout_inline()
		verify_checkout_combined()

	def test_checkout_resourcegroups( self ):
		expected_results = self.load_expected_results( 'test_checkout_resourcegroups.json' )

		def checkout_settings_file():
			expected_1			= expected_results.get( 'test_checkout_resourcegroups_1' )
			expected_1_settings	= expected_1.get( 'settings' )

			expected_2			= expected_results.get( 'test_checkout_resourcegroups_2' )
			expected_2_settings	= expected_2.get( 'settings' )

			with self.resourcegroup_open( 'test_checkout_resourcegroups_1.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_1_settings )

			with self.resourcegroup_open( 'test_checkout_resourcegroups_2.json' ) as fh:
				self.assertSettingsEqual( fh.read(), expected_2_settings )

		self.import_store_provisioning_file( 'test_checkout_resourcegroups.xml' )
		self.checkout()

		checkout_settings_file()

	def test_checkout_changeset( self ):
		self.import_store_provisioning_file( 'test_checkout_changeset.xml' )

		request		= merchantapi.request.BranchListLoadQuery( self.merchantapi_client() )
		request.set_count( 1 )
		request.set_filters( request.filter_expression().equal( 'name', self.config.get( 'branch_name' ) ) )

		response	= request.send()
		self.assertTrue( len( response.get_branches() ) > 0 )

		branch		= response.get_branches()[ 0 ]

		request		= merchantapi.request.ChangesetListLoadQuery( self.merchantapi_client(), branch )
		request.set_count( 1 )
		request.set_sort( 'id', request.SORT_DESCENDING )

		response	= request.send()
		self.assertTrue( len( response.get_changesets() ) > 0 )

		changeset	= response.get_changesets()[ 0 ]

		# Checkout and verify the expected data
		self.checkout()
		with self.template_open( 'test_checkout_changeset.mvt', 'r' ) as fh:
			self.assertEqual( 'original template code', fh.read() )

		# Modify the template and commit the changes
		with self.template_open( 'test_checkout_changeset.mvt', 'w' ) as fh:
			fh.write( 'updated template code' )

		self.push( 'test_checkout_changeset' )

		# Checkout and verify the expected data again
		self.checkout()
		with self.template_open( 'test_checkout_changeset.mvt', 'r' ) as fh:
			self.assertEqual( 'updated template code', fh.read() )

		# Checkout a specific changeset and verify the expected data
		self.checkout( c = changeset.get_id() )
		with self.template_open( 'test_checkout_changeset.mvt', 'r' ) as fh:
			self.assertEqual( 'original template code', fh.read() )

	def test_checkout_sync_all( self ):
		def verify_checkout( ignore_unsynced_templates: bool, ignore_unsynced_properties: bool ):
			self.checkout( ignore_unsynced_templates = ignore_unsynced_templates, ignore_unsynced_properties = ignore_unsynced_properties )

			error_message = f'ignore_unsynced_templates: {ignore_unsynced_templates}, ignore_unsynced_properties: {ignore_unsynced_properties}'

			if ignore_unsynced_templates:
				template_callback = self.assertFalse
			else:
				template_callback = self.assertTrue

			if ignore_unsynced_properties:
				property_callback = self.assertFalse
			else:
				property_callback = self.assertTrue

			template_callback( os.path.exists( self.template_path( 'email_test_checkout_sync_all.mvt' ) ), error_message )
			template_callback( os.path.exists( self.template_path( 'email_test_checkout_sync_all.json' ) ), error_message )

			property_callback( os.path.exists( self.property_product_path( 'header', 'test_checkout_sync_all.mvt' ) ),	error_message )
			property_callback( os.path.exists( self.property_product_path( 'footer', 'test_checkout_sync_all.mvt' ) ),	error_message )

			property_callback( os.path.exists( self.property_category_path( 'header', 'test_checkout_sync_all.mvt' ) ),	error_message )
			property_callback( os.path.exists( self.property_category_path( 'footer', 'test_checkout_sync_all.mvt' ) ),	error_message )

			property_callback( os.path.exists( self.property_category_path( 'cssui_cattitle', 'test_checkout_sync_all.json' ) ), error_message )

			if not ignore_unsynced_templates:
				with self.template_open( 'email_test_checkout_sync_all.mvt', 'r' ) as fh:
					self.assertEqual( 'test_checkout_sync_all email template', fh.read() )

				with self.template_open( 'email_test_checkout_sync_all.json', 'r' ) as fh:
					self.assertIn( 'product_display', self.json_loads( fh.read() ) )

			if not ignore_unsynced_properties:
				with self.property_product_open( 'header', 'test_checkout_sync_all.mvt', 'r' ) as fh:
					self.assertEqual( 'test_checkout_sync_all product header', fh.read() )

				with self.property_product_open( 'footer', 'test_checkout_sync_all.mvt', 'r' ) as fh:
					self.assertEqual( 'test_checkout_sync_all product footer', fh.read() )

				with self.property_category_open( 'header', 'test_checkout_sync_all.mvt', 'r' ) as fh:
					self.assertEqual( 'test_checkout_sync_all category header', fh.read() )

				with self.property_category_open( 'footer', 'test_checkout_sync_all.mvt', 'r' ) as fh:
					self.assertEqual( 'test_checkout_sync_all category footer', fh.read() )

				with self.property_category_open( 'cssui_cattitle', 'test_checkout_sync_all.json', 'r' ) as fh:
					self.assertEqual( 'test_checkout_sync_all.jpg', self.json_loads( fh.read() ).get( 'image' ) )

			with open( os.path.join( '.mmt/config.json' ), 'r' ) as fh:
				config = self.json_loads( fh.read() )

				self.assertEqual( config.get( 'ignore_unsynced_templates' ),	ignore_unsynced_templates )
				self.assertEqual( config.get( 'ignore_unsynced_properties' ),	ignore_unsynced_properties )

		self.import_store_provisioning_file( 'test_checkout_sync_all.xml' )

		verify_checkout( ignore_unsynced_templates = False, ignore_unsynced_properties = False )
		verify_checkout( ignore_unsynced_templates = True, ignore_unsynced_properties = False )
		verify_checkout( ignore_unsynced_templates = False, ignore_unsynced_properties = True )
		verify_checkout( ignore_unsynced_templates = True, ignore_unsynced_properties = True )

	def test_checkout_hidden_settings_template( self ):
		expected_results = self.load_expected_results( 'test_checkout_hidden_settings_template.json' )

		self.import_store_provisioning_file( 'test_checkout_hidden_settings_template.xml' )

		# checkout and modify page settings to include both hidden and non-hidden settings
		self.checkout()

		with self.template_open( 'test_checkout_hidden_settings_template.json' ) as fh:
			settings								= self.json_loads( fh.read() )
			settings[ 'non_hidden_setting' ]		= 'cool beans'
			settings[ '.hidden_setting' ]			= 'hello world'
			settings[ 'hidden_settings_nested' ]	= { 'red': 123, '.white': 456, 'blue': [ 'abc', { 'def': 'ghi', '.jkl': 'mno' } ] }

		with self.template_open( 'test_checkout_hidden_settings_template.json', 'w' ) as fh:
			fh.write( self.json_dumps( settings ) )

		# push the change
		self.push( 'test_checkout_hidden_settings_template' )

		# checkout again, including hidden settings, and verify the settings are as expected
		self.checkout( include_hidden_settings = True )

		with self.template_open( 'test_checkout_hidden_settings_template.json' ) as fh:
			self.assertSettingsEqual( fh.read(), expected_results.get( 'test_checkout_hidden_settings_template_included' ) )

		# checkout again, excluding hidden settings, and verify the settings are as expected
		self.checkout( include_hidden_settings = False )

		with self.template_open( 'test_checkout_hidden_settings_template.json' ) as fh:
			self.assertSettingsEqual( fh.read(), expected_results.get( 'test_checkout_hidden_settings_template_excluded' ) )

	def test_checkout_hidden_settings_property( self ):
		expected_results = self.load_expected_results( 'test_checkout_hidden_settings_property.json' )

		self.import_store_provisioning_file( 'test_checkout_hidden_settings_property.xml' )

		# checkout and modify property settings to include both hidden and non-hidden settings
		self.checkout()

		with self.property_open( 'readytheme_contentsection', 'test_checkout_hidden_settings_property.json' ) as fh:
			settings								= self.json_loads( fh.read() )
			settings[ 'non_hidden_setting' ]		= 'cool beans'
			settings[ '.hidden_setting' ]			= 'hello world'
			settings[ 'hidden_settings_nested' ]	= { 'red': 123, '.white': 456, 'blue': [ 'abc', { 'def': 'ghi', '.jkl': 'mno' } ] }

		with self.property_open( 'readytheme_contentsection', 'test_checkout_hidden_settings_property.json', 'w' ) as fh:
			fh.write( self.json_dumps( settings ) )

		# push the change
		self.push( 'test_checkout_hidden_settings_property' )

		# checkout again, including hidden settings, and verify the settings are as expected
		self.checkout( include_hidden_settings = True )

		with self.property_open( 'readytheme_contentsection', 'test_checkout_hidden_settings_property.json' ) as fh:
			self.assertSettingsEqual( fh.read(), expected_results.get( 'test_checkout_hidden_settings_property_included' ) )

		# checkout again, excluding hidden settings, and verify the settings are as expected
		self.checkout( include_hidden_settings = False )

		with self.property_open( 'readytheme_contentsection', 'test_checkout_hidden_settings_property.json' ) as fh:
			self.assertSettingsEqual( fh.read(), expected_results.get( 'test_checkout_hidden_settings_property_excluded' ) )


class Regressions( MMTTest ):
	""" SSH Private Keys that no longer exist raise an exception when attempting requests """
	def test_regression_MMT_48( self ):
		with tempfile.TemporaryDirectory() as directory:
			os.chdir( directory )

			private_key_filename = 'id_rsa_pem'
			private_key_filepath = os.path.abspath( private_key_filename )

			with open( self.other_data_path( private_key_filename ), 'rb' ) as fh_read:
				with open( private_key_filename, 'wb' ) as fh_write:
					fh_write.write( fh_read.read() )

			self.credential_add( 'test_regression_MMT_48', ssh_private_key = private_key_filepath )
			self.remote_add( 'test_regression_MMT_48', credential_key = 'test_regression_MMT_48' )

			os.unlink( private_key_filename )

			with self.assertRaises( Error ) as e:
				self.checkout( remote_key = 'test_regression_MMT_48', path = '.' )

			self.assertEqual( e.exception.error_message, f'SSH private key \'{private_key_filepath}\' does not exist' )

	""" Fatal error when attempting to checkout a file that contains invalid OS file name characters """
	def test_regression_MMT_55( self ):
		self.import_domain_provisioning_file( 'strict_code_validation.xml', [ ( '%strict_code_validation%', '0' ) ] )
		self.import_store_provisioning_file( 'regression_MMT-55.xml' )

		self.checkout( ignore_unsynced_properties = False )

		hashed_filepath = f'{hashlib.md5( b"regression_MMT-55/4" ).hexdigest()}.mvt'

		with self.property_product_open( 'header', 'regression_MMT-55_1.mvt' ) as fh:
			self.assertEqual( fh.read(), 'regression_MMT-55_1' )

		with self.property_product_open( 'header', 'regression_MMT-55-2.mvt' ) as fh:
			self.assertEqual( fh.read(), 'regression_MMT-55-2' )

		with self.property_product_open( 'header', 'regression_MMT-55 3.mvt' ) as fh:
			self.assertEqual( fh.read(), 'regression_MMT-55 3' )

		with self.property_product_open( 'header', hashed_filepath ) as fh:
			self.assertEqual( fh.read(), 'regression_MMT-55/4' )
