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

Prefix         : MMT-COMMAND-LOG-
Next Error Code: 1
"""

import datetime

import merchantapi.request

from mmt.commands import ConfiguredCommand


class LogCommand( ConfiguredCommand ):
	def run( self ):
		changeset_id_from	= self.args.get( 'c', 0 )
		changeset_id_exact	= self.args.get( 'C', 0 )
		verbose				= self.args.get( 'verbose', False )

		request				= merchantapi.request.ChangesetListLoadQuery()
		request.set_sort( 'id', request.SORT_DESCENDING )
		request.set_branch_id( self.configmanager.branch_id )

		if changeset_id_from > 0:
			request.set_filters( request.filter_expression().greater_than_equal( 'id', changeset_id_from ) )
		elif changeset_id_exact > 0:
			request.set_filters( request.filter_expression().equal( 'id', changeset_id_exact ) )

		response					= self.send_request( request )
		changesets					= response.get_changesets()
		total_changesets			= response.get_total_count()
		changesetversion_request	= merchantapi.request.ChangesetChangeListLoadQuery()

		for index, changeset in enumerate( changesets ):
			changeset_header		= f'c{changeset.get_id()} | {changeset.get_user_name()} | {datetime.datetime.fromtimestamp( changeset.get_date_time_stamp() )}'
			changeset_header_sep	= '-' * len( changeset_header )

			print( changeset_header_sep )
			print( changeset_header )

			if verbose:
				changesetversion_request.set_changeset_id( changeset.get_id() )

				print( 'Modified Files:' )

				for modified_file in self.send_request( changesetversion_request ).get_changeset_changes():
					print( f'\t{modified_file.get_item_identifier()}' )

			print( '' )
			print( changeset.get_notes() )
			print( '' )
			print( '' )

			if index + 1 == total_changesets:
				print( changeset_header_sep )
