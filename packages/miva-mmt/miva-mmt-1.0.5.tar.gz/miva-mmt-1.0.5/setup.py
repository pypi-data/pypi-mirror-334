import os
from setuptools import setup, find_packages

def get_version() -> str:
	version = {}

	with open( os.path.join( 'mmt', 'version.py' ) ) as fh:
		exec( fh.read(), version )

	return version[ '__version__' ]

setup(
	name							= 'miva-mmt',
	version							= get_version(),
	author							= 'Miva, Inc.',
	author_email					= 'support@miva.com',
	packages						= find_packages(),
	entry_points					= { 'console_scripts': [ 'mmt = mmt:main' ] },
	url								= 'https://docs.miva.com/template-branches/template-branches-overview#mmt_overview',
	install_requires				= [ 'merchantapi>=2.7.0' ],
	python_requires					= '>=3.6',
	license							= 'MMT License Agreement',
	long_description				= open( 'README.md', encoding = 'utf-8' ).read().strip(),
	long_description_content_type	= 'text/markdown',
	description						= 'Miva Managed Templates (MMT)'
)
