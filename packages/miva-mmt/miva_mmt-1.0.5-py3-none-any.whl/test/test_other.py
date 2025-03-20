import merchantapi.request

from test import MMTTest

from mmt.commands import Command
from mmt.version import __version__ as version


class Regressions( MMTTest ):
	def test_regression_MMT_60( self ):
		test = self

		class DummyCommand( Command ):
			def run( self ):
				response		= self.send_request_lowlevel( merchantapi.request.BranchListLoadQuery(), 'regression_MMT-60', test.config.get( 'store_code' ) )
				request_headers	= response.get_http_response().request.headers

				test.assertEqual( request_headers.get( 'User-Agent' ), f'MMT/{version}' )

		self.credential_add( 'regression_MMT-60' )

		command = DummyCommand( {} )
		command.validate()
		command.initialize()
		command.run()
