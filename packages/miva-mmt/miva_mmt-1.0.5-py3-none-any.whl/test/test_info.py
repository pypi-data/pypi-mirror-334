from test import MMTTest


class Test( MMTTest ):
	def test_info( self ):
		branch		= self.branch_load_api( self.config.get( 'branch_name' ) )
		changeset	= self.changeset_load_latest()

		def verify( tags: str ):
			data = self.info()

			# Remote
			self.assertIn( f'Key: test_info',									data )
			self.assertIn( f'Store Code: {self.config.get( "store_code" )}',	data )
			self.assertIn( f'Branch Name: {branch.get_name()}',					data )

			# Branch
			self.assertIn( f'Name: {branch.get_name()}',						data )
			self.assertIn( f'Key: {branch.get_branch_key()}',					data )
			self.assertIn( f'Tags: {tags}',										data )

			# Changeset
			self.assertIn( f'ID: {changeset.get_id()}',							data )
			self.assertIn( f'Username: {changeset.get_user_name()}',			data )
			self.assertIn( f'Notes: {changeset.get_notes()}',					data )

		self.remote_add( 'test_info' )
		self.checkout( 'test_info' )

		self.tag_delete_all()
		verify( '<None>' )

		self.tag_add( [ 'test_info' ] )
		verify( '#test_info' )

	def test_info_token( self ):
		self.remote_add( 'test_info_token' )
		self.checkout( remote_key = 'test_info_token' )

		data = self.info()

		# Credential
		self.assertIn( f'Method: Token',									data )
		self.assertIn( f'URL: {self.config.get( "api_url" )}',				data )
		self.assertIn( f'Token: {self.config.get( "api_token" )}',			data )

	def test_info_ssh( self ):
		with open( self.other_data_path( 'id_rsa_pem.pub' ) ) as fh:
			public_key = fh.read()

		self.import_domain_provisioning_file( 'user_update_public_key.xml', [ ( '%username%', self.config.get( 'admin_username' ) ), ( '%public_key%', public_key ) ] )

		self.credential_add( 'test_info_ssh', ssh_username = self.config.get( 'admin_username' ), ssh_private_key = self.other_data_path( 'id_rsa_pem' ) )
		self.remote_add( 'test_info_ssh', credential_key = 'test_info_ssh' )
		self.checkout( remote_key = 'test_info_ssh' )

		data = self.info()

		# Credential
		self.assertIn( f'Method: SSH',										data )
		self.assertIn( f'URL: {self.config.get( "api_url" )}',				data )
		self.assertIn( f'Username: {self.config.get( "admin_username" )}',	data )
		self.assertIn( f'Filepath: {self.other_data_path( "id_rsa_pem" )}', data )
