import os

from test import MMTTest


class Test( MMTTest ):
	def test( self ):
		self.checkout()

		with self.template_open( 'sfnt.mvt', 'w' ) as fh:
			fh.write( 'test_regression_MMT_72' )

		with open( 'diff.sh', 'w' ) as fh:
			fh.write( '#!/bin/bash\n' )
			fh.write( 'echo -n $1 > regression_MMT_72.log' )

		os.chmod( 'diff.sh', 0o755 )

		self.config_set( 'diff', [ os.path.join( os.getcwd(), 'diff.sh' ) ] )

		self.diff()

		with open( 'regression_MMT_72.log' ) as fh:
			self.assertTrue( fh.read().endswith( 'sfnt.mvt' ) )
