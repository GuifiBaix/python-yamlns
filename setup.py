#!/usr/bin/python3
from setuptools import setup

readme = open("README.md").read()

setup(
	name = "yamlnamespace",
	version = "0.1",
	description = "Attribute like accessible dictionary, with YAML IO",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/GuifiBaix/suro',
	long_description = readme,
	license = 'GNU General Public License v3 or later (GPLv3+)',
	packages=[
		'yamlns',
		],
	scripts=[
		'yamlns/nstemplate.py',
		],
	install_requires=[
		'PyYAML',
	],
	package_data = {
    },
	test_suite = 'yamlns',
	test_runner = 'colour_runner.runner.ColourTextTestRunner',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
)

