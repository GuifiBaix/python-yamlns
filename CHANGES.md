# Change Log

## yamlns 0.8.3

- Fix: datetimes were loaded as dates. Closes #2

## yamlns 0.8.2

- Fix: working on Py2 installs without Pathlib2

## yamlns 0.8.1

- Python3 fixes
- Removed rst README, setuptools supports markdown

## yamlns 0.8

- CVE-2020-1747 PyYAML RCE
- Dumping numpy arrays (loading not yet supported)
- Pathlib support

## yamlns 0.7

- Added yamlns.testutils.assertNsEqual
- Added dateutils.Date.spanishDate
- Using rednose as test runner

## yamlns 0.6

- Packaging changes

## yamlns 0.5

- Fix: `loads` in python2 failed to take utf-8 encoded strings as parameter

## yamlns 0.4

- Fix: file dumping in 2.7 used 3.0 encoding parameter

## yamlns 0.3

- Supported Python 2.7

## yamlns 0.2

- Include README.md in the distribution

## yamlns 0.1

- Initial release, striped from original project `suro`
- First PyPI release


