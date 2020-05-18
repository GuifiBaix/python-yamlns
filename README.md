# yamlns.namespace

[![Build Status](https://travis-ci.org/GuifiBaix/python-yamlns.svg?branch=master)](https://travis-ci.org/GuifiBaix/python-yamlns)

An ordered dictionary whose values can be accessed
either as items or as attributes,
like in Javascript Objects but with Pythonic sugar and YAML I/O.

It also provides some goodies:

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
    - Given the attribute like access, `format` templates result cleaner.
    - API to fill a `format` template like file with a YAML file.
    - API to extract an empty YAML scheletton given a template with substitutions.
    - Command line tool to make those two functions
- `unittest` assertion `assertNsEqual` to compare json like structures among them or with yaml strings.


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
```

## Testing structures

```python
class MyTest(unittest.TestCase):

    from yamlns.testutils import assertNsEqual

    def test(self):
        data = dict((letter, i) for i,letter in enumerate('murcielago'))
        self.assertNsEqual(data, """\
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
```


