#!/usr/bin/python3
from setuptools import setup, find_packages

readme = open("README.md").read()

setup(
	name = "yamlns",
	version = "0.4",
	description = "YAML serializable dictionary with dual item and attribute accessors",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/GuifiBaix/python-yamlns',
	long_description = readme,
	license = 'GNU General Public License v3 or later (GPLv3+)',
	packages=find_packages(exclude=['*[tT]est*']),
	scripts=[
		'yamlns/nstemplate.py',
		],
	install_requires=[
		'PyYAML',
	],
	include_package_data = True,
	test_suite = 'yamlns',
#	test_runner = 'colour_runner.runner.ColourTextTestRunner',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
)

