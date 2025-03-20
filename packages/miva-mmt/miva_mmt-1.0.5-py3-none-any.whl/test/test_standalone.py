import os
import unittest
import subprocess


class StandaloneTest( unittest.TestCase ):
	@staticmethod
	def _run_mmt( args: [] ) -> ( int, bytes, bytes ):
		p				= subprocess.Popen( args, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
		stdout, stderr	= p.communicate()
		status			= p.returncode

		return status, stdout.strip(), stderr.strip()


class Test( StandaloneTest ):
	def test_standalone_checkout( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'checkout', 'invalid', '/' ] )

		self.assertIn( b'Remote key \'invalid\' does not exist', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_status( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'status', '.' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_push( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'push', '--notes="hello world"' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_pull( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'pull' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_log( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'log', '.' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_tag( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'tag', 'list' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_diff( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'diff' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_revert( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'revert' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_credential( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'credential', 'delete', 'some_fake_key' ] )

		self.assertIn( b'Credential key \'some_fake_key\' does not exist', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_info( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'info', '.' ] )

		self.assertIn( b'MMT has not been configured for path \'.\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_config( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'config', 'set', 'some_invalid_setting', 'some_value' ] )

		self.assertIn( b'Invalid config setting \'some_invalid_setting\'', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	def test_standalone_version( self ):
		status, stdout, stderr	= self._run_mmt( [ 'mmt', '--version' ] )

		self.assertIsNotNone( os.environ.get( 'MMT_VERSION' ), 'MMT_VERSION environment variable is not set' )
		self.assertEqual( status, 0 )
		self.assertEqual( stdout.decode( 'ascii' ), os.environ.get( 'MMT_VERSION' ) )


class Regressions( StandaloneTest ):
	""" Branch create should use -c instead of -r for the credential key argument """
	def test_regression_MMT_43( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'branch', 'create', '-f', 'Production', '-c', 'invalid', '-s', 'test', 'test_regression_MMT_43' ] )

		self.assertIn( b'Credential key \'invalid\' does not exist', stderr )
		self.assertEqual( b'', stdout )
		self.assertEqual( status, 1 )

	""" Empty mmt command raises an exception """
	def test_regressions_MMT_50( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt' ] )

		# Spot check the output for known values
		self.assertNotIn( b'Traceback', stderr )
		self.assertIn( b'checkout', stdout )
		self.assertIn( b'push', stdout )
		self.assertIn( b'pull', stdout )
		self.assertNotEqual( status, 0 )

	""" Empty mmt sub-command raises an exception """
	def test_regressions_MMT_52( self ):
		status, stdout, stderr = self._run_mmt( [ 'mmt', 'config' ] )

		# Spot check the output for known values
		self.assertNotIn( b'Traceback', stderr )
		self.assertIn( b'checkout', stdout )
		self.assertIn( b'push', stdout )
		self.assertIn( b'pull', stdout )
		self.assertNotEqual( status, 0 )
