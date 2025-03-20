import os

from test import MMTTest


class Test( MMTTest ):
	def test( self ):
		self.checkout()

		with open( 'diff.sh', 'w' ) as fh:
			fh.write( '''#!/bin/bash

				touch regression_MMT-69.log
				echo "$# arguments were passed to this script" >> regression_MMT-69.log''' )

		os.chmod( 'diff.sh', 0o755 )

		self.config_set( 'diff', [ os.path.join( os.getcwd(), 'diff.sh' ) ] )

		with self.template_open( 'sfnt.mvt', 'w' ) as fh:
			fh.write( 'modified' )

		with self.template_open( 'abus.mvt', 'w' ) as fh:
			fh.write( 'modified' )

		self.diff()

		lineno = 0
		with open( 'regression_MMT-69.log' ) as fh:
			for line in fh:
				lineno = lineno + 1
				self.assertEqual( line.strip(), '2 arguments were passed to this script' )

		self.assertEqual( lineno, 2 )
