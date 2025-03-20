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

Prefix         : MMT-COMMAND-TAG-
Next Error Code: 2
"""

from mmt.commands import ConfiguredCommand


def normalize_tag( tag: str ) -> str:
	return tag.lower().replace( '#', '' ).replace( ' ', '' ).strip()


class TagListCommand( ConfiguredCommand ):
	def run( self ):
		if len( self.configmanager.branch_tags ) == 0:
			return

		print( self.build_branch_tags() )


class TagAddCommand( ConfiguredCommand ):
	def run( self ):
		normalized_tags = self.configmanager.branch_tags

		for tag in self.args.get( 'tags' ):
			tag = normalize_tag( tag )

			if len( tag ) > 0 and tag not in normalized_tags:
				normalized_tags.append( tag )

		self.configmanager.branch_tags = normalized_tags
		self.configmanager.save()


class TagSetCommand( ConfiguredCommand ):
	def run( self ):
		normalized_tags = []

		for tag in self.args.get( 'tags' ):
			tag = normalize_tag( tag )

			if len( tag ) > 0 and tag not in normalized_tags:
				normalized_tags.append( tag )

		self.configmanager.branch_tags = normalized_tags
		self.configmanager.save()


class TagDeleteCommand( ConfiguredCommand ):
	def run( self ):
		branch_tags = self.configmanager.branch_tags

		if self.args.get( 'all' ) is True:
			branch_tags = []
		else:
			for tag in self.args.get( 'tags' ):
				try:
					branch_tags.remove( normalize_tag( tag ) )
				except ValueError:
					pass

		self.configmanager.branch_tags = branch_tags
		self.configmanager.save()
