from test import MMTTest


class Test( MMTTest ):
	def test_log( self ):
		self.checkout()

		data = self.log( c = 1 )
		self.assertIn( 'c1 |', 			data )
		self.assertIn( 'Store created', data )
		self.assertNotIn( '.mvc', 		data )

		data = self.log( C = 1, verbose = True )
		self.assertIn( 'c1 |',			data )
		self.assertIn( 'Store created',	data )
		self.assertIn( 'sfnt.mvc',		data )
