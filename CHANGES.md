# Change Log

## yamlns 0.11.0 (2022-11-06)

- New pytest assert `assert_ns_contains`: Assert for a subset of a ns
- New unittest assertion `assertNsContains`: Assert for a subset of a ns
- Optimization: Using CSafeLoader/Dumper instead SafeLoader/Dumper
- `json2yaml`: new script to have a yaml based pretty printed view on json data
- Renamed script `nstemplate.py` as `nstemplate` (removed `.py`)
- pytest utils documented

## yamlns 0.10.0 (2022-03-23)

- pytest utils:
  - `text_snapshot`: a pytest fixture that compares a text with the previous validated execution
  - `yaml_snapshot`: a pytest fixture that compares the yaml dump of the value with the previous validated execution
  - `assert_ns_equal`: a custom assertion equivalent to `assertNsEqual` for `unittest`
- `ns` alias for `namespace`

## yamlns 0.9.2

- github actions for ci and release
- improved test coverage

## yamlns 0.9.1

- py2 compatible loading

## yamlns 0.9.0

- Dump multiline strings verbatim (|) instead of quoted whenever possible
- Py3: removed 0 padded numbers in date tests
- Improved coverage in templating code
- Fix: removed a spurious trace

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


