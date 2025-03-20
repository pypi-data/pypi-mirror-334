"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2024 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-
Next Error Code: 3
"""

import sys
import argparse
import importlib

import mmt.version
import mmt.exceptions


def main():
	parser		= argparse.ArgumentParser( prog = sys.argv[ 0 ] )
	subparsers	= parser.add_subparsers( title = 'Subcommands', dest = 'command' )

	# Checkout
	parser_checkout = subparsers.add_parser( 'checkout',																help = 'Checkout a branch' )
	parser_checkout.add_argument( '-c',										type = int, required = False, default = 0,	help = 'Checkout a specific changeset.  If omitted the last changeset is used.' )
	parser_checkout.add_argument( '--ignore-unsynced-templates',	'-t',	action = 'store_true',						help = 'Ignore templates that do not have the sync flag' )
	parser_checkout.add_argument( '--ignore-unsynced-properties',	'-p',	action = 'store_true',						help = 'Ignore properties that do not have the sync flag' )
	parser_checkout.add_argument( '--include-hidden-settings',		'-s',	action = 'store_true',						help = 'Include hidden settings in the managed template and managed property settings files' )
	parser_checkout.add_argument( '--reinitialize',					'-z',	action = 'store_true',						help = 'Reinitialize the state file to the specified changeset.  Files that do not exist are added while files that already exist are left unmodified.' )
	parser_checkout.add_argument( 'remote-key',								type = str, 								help = 'The key associated with the stored remote resource' )
	parser_checkout.add_argument( 'path',									type = str,	nargs = '?',					help = 'The path where the checked out branch should be created' )

	# Push
	parser_push = subparsers.add_parser( 'push',					help = 'Commit and push the local files to the remote server' )
	parser_push.add_argument( '--notes', '-n', required = False,	help = 'Notes describing the changes to be committed' )
	parser_push.add_argument( 'filepaths', nargs = '*',				help = 'The list of local files to commit and push.  If blank, all locally modified files will be committed' )

	# Pull
	parser_pull = subparsers.add_parser( 'pull',						help = 'Update local files to remote server\'s version' )
	parser_pull.add_argument( '-c', type = int, default = 0,			help = 'Update to specified changeset' )
	parser_pull.add_argument( '--force', '-f', action = 'store_true',	help = 'Overwrite any locally modified files' )
	parser_pull.add_argument( 'filepaths', nargs = '*',					help = 'The list of local files to update.  If blank, all files within the checked out changeset / the specified changeset will be updated' )

	# Tags
	parser_tag				= subparsers.add_parser( 'tag',					help = 'List, add, set, or delete the branch tags' )
	parser_tag_subparser	= parser_tag.add_subparsers( title = 'Tag Command', dest = 'tag_command', metavar = '' )

	parser_tag_list			= parser_tag_subparser.add_parser( 'list',		help = 'List tags' )

	parser_tag_add			= parser_tag_subparser.add_parser( 'add',		help = 'Add one or more tags' )
	parser_tag_add.add_argument( 'tags', nargs = '+',						help = 'The tags to be added' )

	parser_tag_set			= parser_tag_subparser.add_parser( 'set',		help = 'Overwrite existing tags' )
	parser_tag_set.add_argument( 'tags', nargs = '+',						help = 'The tags to be set' )

	parser_tag_delete		= parser_tag_subparser.add_parser( 'delete',	help = 'Delete one or more existing tags' )
	parser_tag_delete.add_argument( '--all', '-a', action = 'store_true',	help = 'Delete all existing tags' )
	parser_tag_delete.add_argument( 'tags', nargs = '*',					help = 'The tags to be deleted' )

	# Log
	parser_log				= subparsers.add_parser( 'log',				help = 'Lists the changes made to a specific changeset or to a group of changesets' )
	parser_log_changesets	= parser_log.add_mutually_exclusive_group()
	parser_log_changesets.add_argument( '-c', type = int, default = 0,	help = 'Get the changes since a specific changeset' )
	parser_log_changesets.add_argument( '-C', type = int, default = 0,	help = 'Get the changes for a specific changeset' )
	parser_log.add_argument( '--verbose', '-v', action = 'store_true',	help = 'Include a list of modified files within each changeset' )
	parser_log.add_argument( 'path', type = str, nargs = '?',			help = '' )

	# Status
	parser_status = subparsers.add_parser( 'status',				help = 'Lists files that have been locally modified' )
	parser_status.add_argument( 'path', type = str, nargs = '?',	help = '' )

	# Diff
	parser_diff = subparsers.add_parser( 'diff',		help = 'Diff files that have been locally modified' )
	parser_diff.add_argument( 'filepaths', nargs = '*',	help = 'The list of local files to diff.  If blank, all locally modified files will be diffed' )

	# Revert
	parser_revert = subparsers.add_parser( 'revert',						help = 'Revert files that have been locally modified' )
	parser_revert.add_argument( '--all', '-a', action = 'store_true',		help = 'Revert all files' )
	parser_revert.add_argument( 'filepaths', nargs = '*', default = [],		help = 'The list of local files to revert' )

	# Credentials
	parser_credential		 		= subparsers.add_parser( 'credential', help = 'Store credentials' )
	parser_credential_subparser		= parser_credential.add_subparsers( title = 'Credentials Commands', dest = 'credential_command', metavar = ''  )

	parser_credential_list			= parser_credential_subparser.add_parser( 'list', help = 'List credentials' )

	parser_credential_add			= parser_credential_subparser.add_parser( 'add',						help = 'Add a credential' )
	parser_credential_add.add_argument( '--url',						'-u', type = str, required = True,	help = 'The API URL where API will requests will be sent' )
	parser_credential_add.add_argument( '--http-basic-auth-username',	'-m', type = str, required = False,	help = 'HTTP Basic Authentication username' )
	parser_credential_add.add_argument( '--http-basic-auth-password',	'-w', type = str, required = False,	help = 'HTTP Basic Authentication password (if the username argument is present and the password argument is omitted, you will be prompted for the password)' )

	parser_credential_add_token_group	= parser_credential_add.add_argument_group( 'Token Authentication' )
	parser_credential_add_token_group.add_argument( '--token',			'-t', type = str, required = False,	help = 'The API token used to make API requests' )
	parser_credential_add_token_group.add_argument( '--signing-key',	'-s', type = str, required = False,	help = 'The API signing key used to sign API requests' )

	parser_credential_add_ssh_group		= parser_credential_add.add_argument_group( 'SSH Authentication' )
	parser_credential_add_ssh_group.add_argument( '--ssh-username',		'-n', type = str, required = False,	help = 'The Miva Merchant username associated with the SSH credential' )
	parser_credential_add_ssh_group.add_argument( '--ssh-private-key',	'-k', type = str, required = False,	help = 'The filepath to the SSH private key' )

	parser_credential_add.add_argument( 'key', type = str, help = 'The key to associate the credential with' )

	parser_credential_update		= parser_credential_subparser.add_parser( 'update',	help = 'Update a credential' )
	parser_credential_update.add_argument( '--credential-key',				'-c', type = str, required = False, help = 'The new credential key value' )
	parser_credential_update.add_argument( '--url',							'-u', type = str, required = False, help = 'The API URL where API will requests will be sent' )
	parser_credential_update.add_argument( '--http-basic-auth-username',	'-m', type = str, required = False,	help = 'HTTP Basic Authentication username' )
	parser_credential_update.add_argument( '--http-basic-auth-password',	'-w', type = str, required = False,	help = 'HTTP Basic Authentication password (if the username argument is present and the password argument is omitted, you will be prompted for the password)' )

	parser_credential_update_token_group	= parser_credential_update.add_argument_group( 'Token Authentication' )
	parser_credential_update_token_group.add_argument( '--token',		'-t', type = str, required = False,	help = 'The API token used to make API requests' )
	parser_credential_update_token_group.add_argument( '--signing-key',	'-s', type = str, required = False,	help = 'The API signing key used to sign API requests' )

	parser_credential_update_ssh_group		= parser_credential_update.add_argument_group( 'SSH Authentication' )
	parser_credential_update_ssh_group.add_argument( '--ssh-username',		'-n', type = str, required = False,	help = 'The Miva Merchant username associated with the SSH credential' )
	parser_credential_update_ssh_group.add_argument( '--ssh-private-key',	'-k', type = str, required = False,	help = 'The filepath to the SSH private key' )

	parser_credential_update.add_argument( 'key', type = str, help = 'The key to associate the credential with' )

	parser_credential_delete		= parser_credential_subparser.add_parser( 'delete',	help = 'Delete a credential' )
	parser_credential_delete.add_argument( 'key', type = str,							help = 'Delete credential associated with the key' )

	# Info
	parser_info = subparsers.add_parser( 'info', help = 'Shows information about a local MMT directory' )
	parser_info.add_argument( 'path', type = str, nargs = '?' )

	# Config
	parser_config			= subparsers.add_parser( 'config', help = 'Configure settings' )
	parser_config_subparser	= parser_config.add_subparsers( title = 'Config Commands', dest = 'config_command', metavar = '' )

	parser_config_list		= parser_config_subparser.add_parser( 'list',	help = 'List configuration settings' )

	parser_config_set		= parser_config_subparser.add_parser( 'set',	help = f'Set a configuration setting (valid values include \'diff, editor\')' )
	parser_config_set.add_argument( 'key',		type = str,					help = 'Name of the configuration setting' )
	parser_config_set.add_argument( 'value',	type = str,	nargs = '*',	help = 'Value of the configuration setting' )

	parser_config_delete	= parser_config_subparser.add_parser( 'delete',	help = f'Delete configuration setting (valid values include \'diff, editor\')' )
	parser_config_delete.add_argument( 'key', type = str,					help = 'Name of the configuration setting' )

	# Remote
	parser_remote			= subparsers.add_parser( 'remote', help = 'Configure a remote resource' )
	parser_remote_subparser	= parser_remote.add_subparsers( title = 'Remote Commands', dest = 'remote_command', metavar = '' )

	parser_remote_list		= parser_remote_subparser.add_parser( 'list', help = 'List remote resources' )

	parser_remote_add		= parser_remote_subparser.add_parser( 'add', help = 'Add a remote resource' )
	parser_remote_add.add_argument( '--credential-key',	'-c',	type = str, required = True, help = 'The key associated with the stored credential' )
	parser_remote_add.add_argument( '--branch-name',	'-b',	type = str, required = True, help = 'The branch name to checkout' )
	parser_remote_add.add_argument( '--store-code',		'-s',	type = str, required = True, help = 'The store code from which to checkout' )
	parser_remote_add.add_argument( 'key',						type = str, help = 'The key of the remote resource' )

	parser_remote_update	= parser_remote_subparser.add_parser( 'update', help = 'Update a remote resource' )
	parser_remote_update.add_argument( '--remote-key',		'-r',	type = str, required = False, help = 'The new remote key value' )
	parser_remote_update.add_argument( '--credential-key',	'-c',	type = str, required = False, help = 'The key associated with the stored credential' )
	parser_remote_update.add_argument( '--store-code',		'-s',	type = str, required = False, help = 'The store code associated with the remote resource' )
	parser_remote_update.add_argument( '--branch-name',		'-b',	type = str, required = False, help = 'The branch name associated with the remote resource' )
	parser_remote_update.add_argument( 'key',						type = str, help = 'The key of the remote resource' )

	parser_remote_delete	= parser_remote_subparser.add_parser( 'delete', help = 'Delete one or more remote resources' )
	parser_remote_delete.add_argument( 'key', type = str, nargs = '+', help = 'Delete remote resources associated with the key' )

	# Switch
	parser_switch = subparsers.add_parser( 'switch',		help = 'Switch to a new remote source' )
	parser_switch.add_argument( 'remote-key', type = str,	help = 'The key associated with the stored remote resource' )

	# Branch
	parser_branch			= subparsers.add_parser( 'branch',		help = 'Create or delete a branch' )
	parser_branch_subparser	= parser_branch.add_subparsers( title = 'Branch Commands', dest = 'branch_command', metavar = '' )

	parser_branch_list		= parser_branch_subparser.add_parser( 'list', help = 'List all branches' )
	parser_branch_list.add_argument( '--credential-key',	'-c',	type = str, required = True,	help = 'The key associated with the remote resource' )
	parser_branch_list.add_argument( '--store-code',		'-s',	type = str, required = True,	help = 'The store code' )

	parser_branch_create	= parser_branch_subparser.add_parser( 'create', help = 'Create a branch' )
	parser_branch_create.add_argument( '--color',			'-l',	type = str, required = False,	help = 'The color used to identify the new branch in the Administrative Interface' )

	parser_branch_create_credential_group	= parser_branch_create.add_argument_group( 'Credential Key' )
	parser_branch_create_credential_group.add_argument( '--from',			'-f',	type = str, required = False, help = 'The branch name from which to create a new branch' )
	parser_branch_create_credential_group.add_argument( '--store-code',		'-s',	type = str, required = False, help = 'The store code' )
	parser_branch_create_credential_group.add_argument( '--credential-key',	'-c',	type = str, required = False, help = 'The key associated with the stored credential' )

	parser_branch_create_remote_group		= parser_branch_create.add_argument_group( 'Remote Key', description = 'Use a Remote Key to automatically derive the credential key, store code, and parent branch name' )
	parser_branch_create_remote_group.add_argument( '--remote-key', '-r', type = str, required = False, help = 'The key associated with the stored remote resource' )

	parser_branch_create.add_argument( 'name', type = str, help = 'The branch name' )

	parser_branch_delete	= parser_branch_subparser.add_parser( 'delete', help = 'Delete a branch' )
	parser_branch_delete.add_argument( '--credential-key',	'-c',	type = str, required = True,	help = 'The key associated with the remote resource' )
	parser_branch_delete.add_argument( '--store-code',		'-s',	type = str, required = True,	help = 'The store code' )
	parser_branch_delete.add_argument( 'name',						type = str,						help = 'The branch name' )

	parser.add_argument('--debug',		'-d', action = 'store_true', help = 'Output HTTP request / response logs' )
	parser.add_argument( '--version',	'-v', action = 'store_true', help = 'Outputs version of MMT and exits' )

	try:
		run( parser )
	except mmt.exceptions.Error as e:
		sys.stderr.write( f'{e}\n' )
		sys.exit( 1 )

def run( parser ):
	args	= vars( parser.parse_args() )
	command	= args.get( 'command' )

	if args.get( 'version' ):
		print( mmt.version.__version__ )
		quit()

	if command is None:
		parser.print_usage()
		sys.exit( 1 )

	module_path = f'mmt.commands.{command}'
	class_name	= f'{command.capitalize()}Command'

	for key, value in args.items():
		if key.endswith( '_command' ):
			if value is None:
				parser.print_usage()
				sys.exit( 1 )

			class_name = f'{command.capitalize()}{value.capitalize()}Command'
			break

	try:
		module = importlib.import_module( module_path )
	except ModuleNotFoundError:
		raise mmt.exceptions.Error( 'MMT-00001', 'Invalid command' )

	try:
		command = getattr( module, class_name )
	except AttributeError:
		raise mmt.exceptions.Error( 'MMT-00002', 'Invalid command' )

	mmt_command = command( args )
	mmt_command.validate()
	mmt_command.initialize()
	mmt_command.run()


if __name__ == '__main__':
	main()
