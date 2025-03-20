from test import MMTTest


class Test( MMTTest ):
	def test_PS_workflow( self ):
		# This test will mimic the Professional Services workflow.
		# They will typically do the work across servers (dev and live) but we will
		# be using 3 branches on the same server and store for this test.  The development
		# branch will create a new page will a spelling mistake, which will then be pushed
		# to the staging / QA branch.  The staging branch will fix this issue and push
		# the change up to the the production branch.

		self.import_store_provisioning_file( 'test_PS_workflow.xml' )

		function_name				= 'test_PS_workflow'
		development_branch_source	= 'this is my super duper special pge'
		staging_branch_source		= 'this is my super duper special page'
		production_branch_source	= staging_branch_source

		branch_name_prefix			= function_name
		development_branch_name 	= f'{branch_name_prefix}_development'
		staging_branch_name			= f'{branch_name_prefix}_staging'
		production_branch_name		= f'{branch_name_prefix}_production'

		remote_key_prefix			= function_name
		development_remote_key		= f'{remote_key_prefix}_development'
		staging_remote_key			= f'{remote_key_prefix}_staging'
		production_remote_key		= f'{remote_key_prefix}_production'

		credential_key				= function_name

		self.branch_delete( development_branch_name )
		self.branch_delete( staging_branch_name )
		self.branch_delete( production_branch_name )

		development_branch			= self.branch_create_api( development_branch_name )
		staging_branch				= self.branch_create_api( staging_branch_name )
		production_branch			= self.branch_create_api( production_branch_name )

		self.credential_add( credential_key )
		self.remote_add( development_remote_key,	credential_key = credential_key, branch_name = development_branch.get_name() )
		self.remote_add( staging_remote_key,		credential_key = credential_key, branch_name = staging_branch.get_name() )
		self.remote_add( production_remote_key,		credential_key = credential_key, branch_name = production_branch.get_name() )

		def verify_branches_runtime_source( expected_development_branch_source: str, expected_staging_branch_source: str, expected_production_branch_source ):
			screen								= function_name
			actual_development_branch_source	= self.load_runtime_screen( screen, additional_parameters = { 'BranchKey': development_branch.get_branch_key() } )
			actual_staging_branch_source		= self.load_runtime_screen( screen, additional_parameters = { 'BranchKey': staging_branch.get_branch_key() } )
			actual_production_branch_source		= self.load_runtime_screen( screen, additional_parameters = { 'BranchKey': production_branch.get_branch_key() } )

			self.assertEqual( expected_development_branch_source,	actual_development_branch_source,	f'Development branch ({development_branch.get_name()}) screen "{screen}"' )
			self.assertEqual( expected_staging_branch_source,		actual_staging_branch_source,		f'Staging branch( {staging_branch.get_name()}) screen "{screen}"' )
			self.assertEqual( expected_production_branch_source,	actual_production_branch_source,	f'Production branch ({production_branch.get_name()}) screen "{screen}"' )

		# Run workflow (on dev branch)
		verify_branches_runtime_source( '', '', '' )

		self.checkout( remote_key = development_remote_key )

		with self.template_open( 'test_ps_workflow.mvt', 'w' ) as fh:
			fh.write( development_branch_source )

		self.push( f'{function_name}.development' )
		verify_branches_runtime_source( development_branch_source, '', '' )

		# Run workflow (on staging branch)
		self.switch( remote_key = staging_remote_key )
		verify_branches_runtime_source( development_branch_source, '', '' )

		self.push( f'{function_name}.staging 1' )
		verify_branches_runtime_source( development_branch_source, development_branch_source, '' )

		with self.template_open( 'test_ps_workflow.mvt', 'w' ) as fh:
			fh.write( staging_branch_source )

		self.push( f'{function_name}.staging 2' )
		verify_branches_runtime_source( development_branch_source, staging_branch_source, '' )

		# Run workflow (on production branch)
		self.switch( remote_key = production_remote_key )
		verify_branches_runtime_source( development_branch_source, staging_branch_source, '' )

		self.push( f'{function_name}.production' )
		verify_branches_runtime_source( development_branch_source, staging_branch_source, production_branch_source )
