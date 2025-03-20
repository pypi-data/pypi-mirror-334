from mmt.exceptions import Error
from test import MMTTest


class Test( MMTTest ):
	def test_switch_validate( self ):
		self.checkout()

		with self.assertRaises( Error ) as e:
			self.switch( 'invalid' )

		self.assertEqual( e.exception.error_message, 'Remote key \'invalid\' does not exist' )

	def test_switch_invalid_branch( self ):
		self.branch_delete( 'test_switch_invalid_branch' )
		self.checkout()

		with self.assertRaises( Error ) as e:
			self.remote_add( 'test_switch_invalid_branch', branch_name = 'test_switch_invalid_branch' )
			self.switch( 'test_switch_invalid_branch' )

		self.assertEqual( e.exception.error_message, 'Branch \'test_switch_invalid_branch\' does not exist' )

	def test_switch_templates( self ):
		self.import_store_provisioning_file( 'test_switch_templates.xml' )

		# Create a new branch which is a copy of the existing branch
		self.branch_delete( 'test_switch_templates' )
		self.branch_create( 'test_switch_templates' )
		self.remote_add( 'test_switch_templates', branch_name = 'test_switch_templates' )

		def verify( ignore_unsynced_templates: bool ):
			def verify_state_file():
				entry = self.load_state_file()[ 'files' ].get( self.template_path( 'scriptresource-testswitchtemplates.mvt' ) )

				if ignore_unsynced_templates:
					self.assertIsNone( entry, 'Found the template file entry, but the only syncable templates should exist' )
				else:
					self.assertIsNotNone( entry, 'Failed to find the template file entry when all templates should be synced' )

			self.checkout( ignore_unsynced_templates = ignore_unsynced_templates )
			verify_state_file()

			# Modify and commit existing branch files with random data to cause differences between the branches
			with self.template_open( 'test_switch_templates_1.json' ) as fh:
				settings = self.json_loads( fh.read() )

			with self.template_open( 'test_switch_templates_1.mvt', 'w' ) as fh:
				fh.write( f'test_switch_templates_1 {self.generate_random()}' )

			with self.template_open( 'test_switch_templates_1.json', 'w' ) as fh:
				settings[ 'test_switch_templates' ] = self.generate_random()

				fh.write( self.json_dumps( settings ) )

			self.push( 'test_switch_templates' )

			modified_files = self.status()
			self.assertEqual( modified_files, 'No files modified' )

			# Switch the MMT instance over to the other branch
			self.switch( 'test_switch_templates' )
			verify_state_file()

			# Verify the previously modified and committed files are now marked as modified again
			modified_files = self.status()
			self.assertIn( self.template_path( 'test_switch_templates_1.mvt' ),		modified_files )
			self.assertIn( self.template_path( 'test_switch_templates_1.json' ),	modified_files )
			self.assertNotIn( self.template_path( 'test_switch_templates_2.mvt' ),	modified_files )
			self.assertNotIn( self.template_path( 'test_switch_templates_2.json' ),	modified_files )

			self.push( 'test_switch_templates' )
			self.assertEqual( self.status(), 'No files modified' )

		verify( ignore_unsynced_templates = True )
		verify( ignore_unsynced_templates = False )

	def test_switch_properties( self ):
		self.import_store_provisioning_file( 'test_switch_properties.xml' )

		# Create a new branch which is a copy of the existing branch
		self.branch_delete( 'test_switch_properties' )
		self.branch_create( 'test_switch_properties' )
		self.remote_add( 'test_switch_properties', branch_name = 'test_switch_properties' )

		def verify( ignore_unsynced_properties: bool ):
			def verify_state_file():
				entry = self.load_state_file()[ 'files' ].get( self.property_product_path( 'header', 'test_switch_properties.mvt' ) )

				if ignore_unsynced_properties:
					self.assertIsNone( entry, 'Found the template file entry, but the only syncable templates should exist' )
				else:
					self.assertIsNotNone( entry, 'Failed to find the template file entry when all templates should be synced' )

			self.checkout( ignore_unsynced_properties = ignore_unsynced_properties )
			verify_state_file()

			# Modify and commit existing branch files with random data to cause differences between the branches
			with self.property_open( 'readytheme_contentsection', 'test_switch_properties_1.json' ) as fh:
				settings = self.json_loads( fh.read() )

			with self.property_open( 'readytheme_contentsection', 'test_switch_properties_1.mvt', 'w' ) as fh:
				fh.write( f'test_switch_properties_1 {self.generate_random()}' )

			with self.property_open( 'readytheme_contentsection', 'test_switch_properties_1.json', 'w' ) as fh:
				settings[ 'test_switch_properties' ] = self.generate_random()

				fh.write( self.json_dumps( settings ) )

			self.push( 'test_switch_properties' )

			modified_files = self.status()
			self.assertEqual( modified_files, 'No files modified' )

			# Switch the MMT instance over to the other branch
			self.switch( 'test_switch_properties' )
			verify_state_file()

			# Verify the previously modified and committed files are now marked as modified again
			modified_files = self.status()
			self.assertIn( self.property_path( 'readytheme_contentsection', 'test_switch_properties_1.mvt' ),		modified_files )
			self.assertIn( self.property_path( 'readytheme_contentsection', 'test_switch_properties_1.json' ),		modified_files )
			self.assertNotIn( self.property_path( 'readytheme_contentsection', 'test_switch_properties_2.mvt' ),	modified_files )
			self.assertNotIn( self.property_path( 'readytheme_contentsection', 'test_switch_properties_2.json' ),	modified_files )

			self.push( 'test_switch_properties' )
			self.assertEqual( self.status(), 'No files modified' )

		verify( ignore_unsynced_properties = True )
		verify( ignore_unsynced_properties = False )

	def test_switch_jsresources( self ):
		self.import_store_provisioning_file( 'test_switch_jsresources.xml' )

		# Create a new branch which is a copy of the existing branch
		self.branch_delete( 'test_switch_jsresources' )
		self.branch_create( 'test_switch_jsresources' )
		self.remote_add( 'test_switch_jsresources', branch_name = 'test_switch_jsresources' )

		self.checkout()

		# Modify and commit existing branch files to cause differences between the branches
		with self.jsresource_open( 'test_switch_jsresources_external_1.json' ) as fh:
			settings = self.json_loads( fh.read() )

		with self.jsresource_open( 'test_switch_jsresources_external_1.json', 'w' ) as fh:
			settings[ 'active' ] = True

			fh.write( self.json_dumps( settings ) )

		self.push( 'test_switch_jsresources' )

		modified_files = self.status()
		self.assertEqual( modified_files, 'No files modified' )

		# Switch the MMT instance over to the other branch
		self.switch( 'test_switch_jsresources' )

		# Verify the previously modified and committed files are now marked as modified again
		modified_files = self.status()
		self.assertIn( self.jsresource_path( 'test_switch_jsresources_external_1.json' ),		modified_files )
		self.assertNotIn( self.jsresource_path( 'test_switch_jsresources_external_2.json' ),	modified_files )

		self.push( 'test_switch_jsresources' )
		self.assertEqual( self.status(), 'No files modified' )

	def test_switch_cssresources( self ):
		self.import_store_provisioning_file( 'test_switch_cssresources.xml' )

		# Create a new branch which is a copy of the existing branch
		self.branch_delete( 'test_switch_cssresources' )
		self.branch_create( 'test_switch_cssresources' )
		self.remote_add( 'test_switch_cssresources', branch_name = 'test_switch_cssresources' )

		self.checkout()

		# Modify and commit existing branch files to cause differences between the branches
		with self.cssresource_open( 'test_switch_cssresources_external_1.json' ) as fh:
			settings = self.json_loads( fh.read() )

		with self.cssresource_open( 'test_switch_cssresources_external_1.json', 'w' ) as fh:
			settings[ 'active' ] = True

			fh.write( self.json_dumps( settings ) )

		self.push( 'test_switch_cssresources' )

		modified_files = self.status()
		self.assertEqual( modified_files, 'No files modified' )

		# Switch the MMT instance over to the other branch
		self.switch( 'test_switch_cssresources' )

		# Verify the previously modified and committed files are now marked as modified again
		modified_files = self.status()
		self.assertIn( self.cssresource_path( 'test_switch_cssresources_external_1.json' ),	modified_files )
		self.assertNotIn( self.cssresource_path( 'test_switch_cssresources_external_2.json' ),	modified_files )

		self.push( 'test_switch_cssresources' )
		self.assertEqual( self.status(), 'No files modified' )

	def test_switch_resourcegroups( self ):
		self.import_store_provisioning_file( 'test_switch_resourcegroups.xml' )

		# Create a new branch which is a copy of the existing branch
		self.branch_delete( 'test_switch_resourcegroups' )
		self.branch_create( 'test_switch_resourcegroups' )
		self.remote_add( 'test_switch_resourcegroups', branch_name = 'test_switch_resourcegroups' )

		self.checkout()

		# Modify and commit existing branch files to cause differences between the branches
		with self.resourcegroup_open( 'test_switch_resourcegroups_1.json' ) as fh:
			settings = self.json_loads( fh.read() )

		with self.resourcegroup_open( 'test_switch_resourcegroups_1.json', 'w' ) as fh:
			settings[ 'linked_js_resources' ]	= []
			settings[ 'linked_css_resources' ]	= []

			fh.write( self.json_dumps( settings ) )

		self.push( 'test_switch_resourcegroups' )

		modified_files = self.status()
		self.assertEqual( modified_files, 'No files modified' )

		# Switch the MMT instance over to the other branch
		self.switch( 'test_switch_resourcegroups' )

		# Verify the previously modified and committed files are now marked as modified again
		modified_files = self.status()
		self.assertIn( self.resourcegroup_path( 'test_switch_resourcegroups_1.json' ),		modified_files )
		self.assertNotIn( self.resourcegroup_path( 'test_switch_resourcegroups_2.json' ),	modified_files )

		self.push( 'test_switch_resourcegroups' )
		self.assertEqual( self.status(), 'No files modified' )
