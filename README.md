# yamlns.namespace

[![CI Status](https://github.com/GuifiBaix/python-yamlns/actions/workflows/main.yml/badge.svg)](https://github.com/GuifiBaix/python-yamlns/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/GuifiBaix/python-yamlns/badge.svg?branch=master)](https://coveralls.io/github/GuifiBaix/python-yamlns?branch=master)
![PyPI](https://img.shields.io/pypi/v/yamlns)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yamlns)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yamlns)

An extended dictionary to conveniently access your structured data
with direct mapping from and to YAML and other structured formats.
Besides the item like `['field']` access, an attribute like access `.field` is provided.
And it also provides many other goodies:

- Direct mapping to YAML using `dump()` and `load()` methods.
- Convenient variations from the pure YAML specs on how value types are mapped between YAML and Python:
    - Inner YAML mappings (`dict`s) are loaded as `namespace`s as well instead of Python `dict`.
    - Namespaces preserve the insertion order, as they are based on `odict`.
      This way the insertion order and the order in the original loaded file is preserved when stored.
    - YAML floats are loaded as `Decimal` and `Decimal` objects are stored as regular YAML floats.
      This avoids losing precision when succesive load/store cycles are alternated.
    - YAML dates are maped to an extension of `datetime.date` which provides output formats as attributes
      which are convenient to call in `format` templates.
- Tools to `format` templates with complex namespace structures.
    - Given the attribute like access, `format` templates result cleaner with multilevel dicts.
    - Function to extract an empty YAML scheletton given a template with substitutions.
    - Function to fill a `format` template like file with a YAML file.
    - Command line tool to run those two functions 
- `unittest` assertions
    - `assertNsEqual` to compare json like structures among them or with yaml strings and display the difference in a nice line by line diff.
    - `assertNsContains` to ensure that a json like structure is a superset of the expectation
- `pyunit` inegration
    - `pytestutils.assert_ns_equal`: equivalent to `assertNsEqual` to be used in pytest
    - `pytestutils.assert_ns_contains`: equivalent to `assertNsContains` to be used in pytest
    - `pytestutils.yaml_snapshot`: fixture to detect changes estructure changes between test executions in yaml format.
    - `pytestutils.text_snapshot`: fixture to detect changes text changes between test executions.


## Example

```python
>>> from yamlns import namespace as ns
>>> n = ns()
>>> n.attribute1 = "value1"
>>> ns['attribute2'] = "value2"
>>> print(n.dump())
attribute1: value1
attribute2: value2

>>> n.attribute2
'value2'
>>> n['attribute1']
'value1'

>>> n.update(ns.loads("""
... attribute3: value3
... attribute4:
...   attribute5: [ 4,3,2,value5 ] 
...   attribute6: 2015-09-23
... attribute7:
... - value7.1
... - value7.2
... """))
>>> n.attribute4.attribute5
[4, 3, 2, 'value5']
>>> n.attribute4.attribute6
datetime.date(2015,9,23)
>>> n.attribute7
['value7.1', 'value7.2']
```

### Templating example:

```python
>>> template = (
...     "{client.name} {client.midname[0]}. {client.surname} buys {item.name} "
...     "by {item.price.amount:0.02f} {item.price.coin}."
... )
...
>>> print(ns.fromTemplate(template).dump())
client:
  name: ''
  midname: ''
  surname: ''
item:
  name: ''
  price:
    amount: ''
    coin: ''

>>> template.format(**ns.loads("""
client:
  name: 'John'
  midname: 'Archivald'
  surname: 'Doe'
item:
  name: 'Apples'
  price:
    amount: 30
    coin: 'dollars'
"""))
John A. Doe buys Apples by 30.00 dollars.

```

## Command line tools usage

```bash
nstemplate apply <template> <yamlfile> <output>
nstemplate extract <template> <yamlskeleton>
cat file.json | json2yaml > file.yaml
```

## Testing structure content

```python
class MyTest(unittest.TestCase):

    from yamlns.testutils import assertNsEqual, assertNsContains

    def test(self):
        data = dict(letters = dict(
            (letter, i) for i,letter in enumerate('murcielago'))
        )
        self.assertNsEqual(data, """\
            letters:
                a: 7
                c: 3
                e: 5
                g: 8
                i: 4
                l: 6
                m: 0
                o: 9
                r: 2
                u: 1
        """)

        # Data is a superset of the expectation
        self.assertNsContains(data, """\
            letters:
                a: 7
                e: 5
                i: 4
                o: 9
                u: 1
        """)
```

## Pytest integration

The following helper tools for pytest are provided:

- `pytestutils.assert_ns_equal`: equivalent to `assertNsEqual` to be used in pytest
- `pytestutils.assert_ns_contains`: equivalent to `assertNsContains` to be used in pytest
- `pytestutils.yaml_snapshot`: fixture to detect changes estructure changes between test executions in yaml format.
- `pytestutils.text_snapshot`: fixture to detect changes text changes between test executions.


### `assert_ns_equal`

A custom assertion that normalizes both sides into namespaces and dumps them as yaml, which is compared side by side.

The normalization takes place, first if the data is a string, it is parsed as yaml.
Then the resulting data is converted recursively into namespaces, ordering keys alfabetically.
And finally the result is dumped as yaml to be compared line by line.

```python
from yamlns.pytestutils import assert_ns_equal

def test_with_assert_ns_equal():
    data = dict(hello='world')
    assert_ns_equal(data, """\
        hello: world
    """)

```

### `assert_ns_contains`

A custom assertion similar to `assert_ns_equal` but ignores any key not pressent in the expectation.

```python
from yamlns.pytestutils import assert_ns_equal

def test_with_assert_ns_equal():
    data = dict(hello='world', ignored=data)
    assert_ns_equal(data, """\
        hello: world
    """)

```

### `yaml_snapshot` and `text_snapshot`

`yaml_snapshot` and `text_snapshot` are fixtures available whenever you install yamlns.
You can use it to make snapshots of data that can be compared to previous executions.
Snapshots are stored into `testdata/snapshots/`
and are given a name that depends on the fully qualified name of the test.
The ones with the `.expected` suffix are accepted snapshots,
while the ones ending with `.result` are generated
when the current execution does not match.

If you consider the `.result` is valid, just rename it as `.expected`.
For convenience, the assert message indicates the commandline to perform the renaming.

`text_snapshot` just dumps verbatim text while
`yaml_snapshot` compares the normalized dump of the data
just like `assert_ns_equal` does.

```python
def test_with_yaml_snapshot(yaml_snapshot):
    data = dict(hello='world')
    yaml_snapshot(data)

def test_with_text_snapshot(text_snapshot):
    who = 'world'
    text_snapshot('hello {}'.format(who))

```

