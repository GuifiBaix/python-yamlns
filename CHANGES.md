# Change Log

## yamlns 0.12.4 (2026-01-06)

- 🦖 Py2: black removed some string prefixes required for Py2

## yamlns 0.12.3 (2026-01-06)

- 💥 Private module structure modernized (should not alter documented interface, may break undocumented usage)
    - ♻️ `__init__` now does not contain definitions, only public imports
    - ♻️ ns/namespace definitions in `core` module
    - ♻️ yaml loader and dumper in `serialization`
    - ♻️ Py2 compatibility utilities in `compat`
    - ♻️ command line code into `cli` package
- 💥 YAML .inf and .nan properly loaded as Decimal Infinite and NaN consistently with other YAML floats.
    May break if you relied in them to be Python float NaN and inf.
- 💥 `load` and `dump` parameter renamed `filename` -> `source`/`target` as they could be open files or Path.
    Calls using keyword arguments should be updated.
- 🐛 pytest assert implementation in a different package to ensure pytest assert rewrite
- 🧹 Removed compatibility with old Python versions (<2.7) unable to use libpath or libpath2
- ✅ Better serialization test coverage
- 🔧 Recovered Py2 CI
- 🎨 Global code style changed to standard black

## yamlns 0.12.2 (2025-03-15)

- Fallback for pure python libyaml if compiled version not available

## yamlns 0.12.1 (2025-01-05)

- Fix: do not check for dotted attributes if key is not a string

## yamlns 0.12.0 (2024-11-07)

- Multilevel getting `value = a['b.c']`
- Multilevel setting `a['b.c'] = 'value'`
- Fix: `pytestutils`: ensure the asserts are registered for rewrite
- Fix: `pytestutils_test`: tolerant with spacing changes on pytest output

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


