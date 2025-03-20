#!/usr/bin/env python3

import abc
import json
import time
import typing
import argparse
import unittest


class MMTBaseOutput( abc.ABC ):
	def __init__( self, passed_tests: typing.List[ unittest.case.TestCase ], failed_tests: typing.List[ typing.Tuple[ unittest.case.TestCase, typing.Any ] ], skipped_tests: typing.List[ typing.Tuple[ unittest.case.TestCase, str ] ] ):
		self._passed_tests	= passed_tests
		self._failed_tests	= failed_tests
		self._skipped_tests	= skipped_tests

	@abc.abstractmethod
	def summary( self ):
		raise NotImplementedError

	def determine_titles( self, test: unittest.case.TestCase ) -> typing.Tuple[ str, str ]:
		name		= str( test )
		file		= name.split( '.' )[ 1 ]
		function	= name.split( ' ' )[ 0 ]

		return file.strip(), function.strip()


class MMTTestMochaOutput( MMTBaseOutput ):
	def summary( self ):
		passes		= []
		failures	= []
		skipped		= []

		for test in self._passed_tests:
			file, function				= self.determine_titles( test )

			testpass = {}
			testpass[ 'title' ]			= function
			testpass[ 'fullTitle' ]		= file
			testpass[ 'duration' ]		= 0

			passes.append( testpass )

		for test, err in self._failed_tests:
			file, function				= self.determine_titles( test )

			testfail					= {}
			testfail[ 'title' ]			= function
			testfail[ 'fullTitle' ]		= file
			testfail[ 'duration' ]		= 0
			testfail[ 'error' ]			= str( err[ 1 ] )

			failures.append( testfail )

		for test, reason in self._skipped_tests:
			file, function				= self.determine_titles( test )

			testskip					= {}
			testskip[ 'title' ]			= function
			testskip[ 'fullTitle' ]		= file
			testskip[ 'duration' ]		= 0
			testskip[ 'error' ]			= reason

			skipped.append( testskip )

		output							= {}
		output[ 'stats' ]				= {}
		output[ 'stats' ][ 'suites' ]	= 0
		output[ 'stats' ][ 'tests' ]	= len( self._passed_tests ) + len( self._failed_tests ) + len( self._skipped_tests )
		output[ 'stats' ][ 'passes' ]	= len( passes )
		output[ 'stats' ][ 'failures' ]	= len( failures )
		output[ 'stats' ][ 'skipped' ]	= len( skipped )
		output[ 'stats' ][ 'pending' ]	= 0
		output[ 'stats' ][ 'start' ]	= time.strftime( "%Y-%m-%dT%H:%M:%SZ", time.gmtime() )
		output[ 'stats' ][ 'end' ]		= time.strftime( "%Y-%m-%dT%H:%M:%SZ", time.gmtime() )
		output[ 'stats' ][ 'duration' ]	= 0
		output[ 'passes' ]				= passes
		output[ 'failures' ]			= failures
		output[ 'skipped' ]				= skipped

		print( json.dumps( output ) )


class MMTBasicOutput( MMTBaseOutput ):
	def summary( self ):
		print( 'Passed:' )
		if len( self._passed_tests ) == 0:
			print( '\tNo passed tests' )
		else:
			for test in self._passed_tests:
				file, function = self.determine_titles( test )

				print( f'\t{file}.{function}' )
		print( '' )

		print( 'Failed:' )
		if len( self._failed_tests ) == 0:
			print( '\tNo failed tests' )
		else:
			for test, err in self._failed_tests:
				file, function = self.determine_titles( test )

				print( f'\t{file}.{function}: {str( err[ 1 ] )}' )
		print( '' )

		print( 'Skipped:' )
		if len( self._skipped_tests ) == 0:
			print( '\tNo skipped tests' )
		else:
			for test, reason in self._skipped_tests:
				file, function = self.determine_titles( test )

				print( f'\t{file}.{function}: {reason}' )
		print( '' )

		print( 'Results:' )
		print( f'\tPassed: {len( self._passed_tests )}' )
		print( f'\tFailed: {len( self._failed_tests )}' )
		print( f'\tSkipped: {len( self._skipped_tests )}' )


class MMTLoader( unittest.TestLoader ):
	pass


class MMTestResult( unittest.TestResult ):
	def __init__( self ):
		super().__init__()

		self._passed_tests	= []
		self._failed_tests	= []
		self._skipped_tests	= []

	def addSuccess( self, test: unittest.case.TestCase ):
		self._passed_tests.append( test )

	def addError( self, test: unittest.case.TestCase, err: typing.Any ):
		self._failed_tests.append( ( test, err ) )

	def addFailure( self, test: unittest.case.TestCase, err: typing.Any ):
		self._failed_tests.append( ( test, err ) )

	def addSkip( self, test: unittest.case.TestCase, reason: str ):
		self._skipped_tests.append( ( test, reason ) )

	@property
	def passed_tests( self ) -> typing.List[ unittest.case.TestCase ]:
		return self._passed_tests

	@property
	def failed_tests( self ) -> typing.List[ typing.Any ]:
		return self._failed_tests

	@property
	def skipped_tests( self ) -> typing.List[ typing.Any ]:
		return self._skipped_tests


class MMTTestRunner:
	def run( self, args ):
		result	= MMTestResult()
		loader	= MMTLoader()
		suite	= loader.discover( '.' )

		suite.run( result )

		if args.output == 'basic':
			output = MMTBasicOutput
		else:
			output = MMTTestMochaOutput

		output( result.passed_tests, result.failed_tests, result.skipped_tests ).summary()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument( '--output', '-o', choices = [ 'basic', 'mocha' ], default = 'mocha' )

	MMTTestRunner().run( parser.parse_args() )
