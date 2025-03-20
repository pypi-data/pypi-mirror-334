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

Prefix         : MMT-COMMAND-STATUS-
Next Error Code: 1
"""

from mmt.commands import ConfiguredCommand


class StatusCommand( ConfiguredCommand ):
	def run( self ):
		modified_files = self.load_modified_files()

		if len( modified_files ) == 0:
			print( 'No files modified' )
			return

		for state_file, file in modified_files:
			print( state_file.filepath )
