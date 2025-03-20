from test import MMTTest


class Test( MMTTest ):
	def test_debug_omitted( self ):
		args = self.checkout_args()
		data = self.checkout( args = args )

		self.assertEqual( '', data )

	def test_debug_False( self ):
		args			= self.checkout_args()
		args[ 'debug' ]	= False
		data			= self.checkout( args = args )

		self.assertEqual( '', data )

	def test_debug_True( self ):
		args			= self.checkout_args()
		args[ 'debug' ]	= True
		data			= self.checkout( args = args )

		self.assertIn( '============= Request: BranchList_Load_Query [HEADERS] =============', data )
		self.assertIn( '============= Request: BranchList_Load_Query [BODY] =============', data )
		self.assertIn( '============= Response: BranchList_Load_Query [HEADERS] =============', data )
		self.assertIn( '============= Response: BranchList_Load_Query [BODY] =============', data )
