#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

readme = open("README.md").read()
py2 = sys.version_info < (3,)

setup(
	name = "yamlns",
	version = "0.9.2",
	description = "YAML serializable dictionary with dual item and attribute accessors",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/GuifiBaix/python-yamlns',
	long_description = readme,
	long_description_content_type = 'text/markdown',
	license = 'GNU General Public License v3 or later (GPLv3+)',
	packages=find_packages(exclude=['*_[tT]est*']),
	scripts=[
		'yamlns/nstemplate.py',
		],
	entry_points=dict(
		pytest11 = [
			"yamlns_tests = yamlns.pytestutils",
		],
	),
	install_requires=[
		'setuptools>=20.4', # markdown readme
		'PyYAML<6, >5.3.1' if py2 else 'PyYAML>=5.3.1', # security
		'pytest<4.7' if py2 else 'pytest',
		'pathlib2' if py2 else '', # Py2 backport
	],
	include_package_data = True,
	test_suite = 'yamlns',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Framework :: Pytest',
		'Intended Audience :: Developers',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
)

# vim: sw=4 ts=4 noet
