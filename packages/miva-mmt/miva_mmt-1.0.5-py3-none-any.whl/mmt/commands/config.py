"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2020 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-COMMAND-CONFIG-
Next Error Code: 9
"""

from mmt.exceptions import Error
from mmt.commands import Command


valid_settings = ( 'diff', 'editor' )


class ConfigListCommand( Command ):
	def run( self ):
		for setting_key in valid_settings:
			setting = self.configmanager.setting_lookup( setting_key )
			value	= '<Not Set>' if setting is None else setting.value

			print( f'{setting_key}: {value}' )


class ConfigSetCommand( Command ):
	def validate( self ):
		if len( self.args.get( 'key' ) ) == 0:
			raise Error( 'MMT-COMMAND-CONFIG-00001', 'Invalid config setting' )

		if self.args.get( 'key' ) not in valid_settings:
			raise Error( 'MMT-COMMAND-CONFIG-00002', f'Invalid config setting \'{self.args.get( "key" )}\'' )

		if self.args.get( 'key' ) == 'diff':
			if len( self.args.get( 'value' ) ) == 0:
				raise Error( 'MMT-COMMAND-CONFIG-00003', 'Setting value cannot be blank' )
		elif self.args.get( 'key' ) == 'editor':
			if len( self.args.get( 'value' ) ) == 0:
				raise Error( 'MMT-COMMAND-CONFIG-00008', 'Setting value cannot be blank' )

	def run( self ):
		key		= self.args.get( 'key' )
		value	= self.args.get( 'value' )

		# The value argument should always be an array, but we should
		# still explicitly cast the data type for each configuration
		# setting to be clear.
		if key == 'diff':
			value = list( value )
		elif key == 'editor':
			value = list( value )

		self.configmanager.setting_set( key, value )
		self.configmanager.save()


class ConfigDeleteCommand( Command ):
	def validate( self ):
		if len( self.args.get( 'key' ) ) == 0:
			raise Error( 'MMT-COMMAND-CONFIG-00006', 'Invalid config setting' )

		if self.args.get( 'key' ) not in valid_settings:
			raise Error( 'MMT-COMMAND-CONFIG-00007', f'Invalid config setting \'{self.args.get( "key" )}\'' )

	def run( self ):
		self.configmanager.setting_delete( self.args.get( 'key' ) )
		self.configmanager.save()
