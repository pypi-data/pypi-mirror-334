from test import MMTTest


class Test( MMTTest ):
	def test_tag_list( self ):
		self.checkout()

		self.tag_set( [ 'hello', 'world' ] )

		self.assertEqual( self.tag_list(), '#hello #world' )

	def test_tag_add( self ):
		self.checkout()

		self.tag_add( [ 'red', 'white' ] )
		self.tag_add( [ 'blue', 'BLUE' ] )

		self.assertEqual( self.tag_list(), '#red #white #blue' )

	def test_tag_set( self ):
		self.checkout()

		self.tag_add( [ 'red', 'white' ] )
		self.tag_set( [ 'blue', 'BLUE' ] )

		self.assertEqual( '#blue', self.tag_list() )

	def test_tag_delete( self ):
		self.checkout()

		self.tag_set( [ 'big', 'small', 'medium' ] )
		self.tag_delete( [ 'SMALL' ] )

		self.assertEqual( '#big #medium', self.tag_list() )

		self.tag_delete_all()
		self.assertEqual( '', self.tag_list() )

		# Delete a non-existent tag and verify no exceptions are thrown
		self.tag_delete( [ 'invalid' ] )
