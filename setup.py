#!/usr/bin/python3
from setuptools import setup

readme = open("README.md").read()

setup(
	name = "namespace",
	version = "0.1",
	description = "Attribute like accessible dictionary, with YAML IO",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/GuifiBaix/suro',
	long_description = readme,
	license = 'GNU General Public License v3 or later (GPLv3+)',
	packages=[
		'namespace',
		],
	scripts=[
		'namespace/nstemplate.py',
		],
	install_requires=[
		'PyYAML',
	],
	package_data = {
    },
	test_suite = 'namespace',
	test_runner = 'colour_runner.runner.ColourTextTestRunner',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Multimedia',
		'Topic :: Scientific/Engineering',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
)

