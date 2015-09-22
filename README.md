# namespace

An ordered dictionary whose values can be accessed as items or attributes.

It also provides some goodies:

- It has direct mapping to YAML using `dump()` and `load()` methods.
- The items are stored in YAML as like the ones in a regular dictionary
  that is, without the `odict` tag, but still preserves insertion order.
  Preserving the order is not YAML compliant but quite convenient for most uses.
- YAML `floats` are loaded as Python `Decimal` and Python `Decimal` are stored as YAML `floats`..
  This preserves the precision of the stored data on succesive load/store cycles.
- Attribute access can be used to fill templates with complex structures
  from a YAML file using the stock `format` method.
- Given a template, `dumpTemplateVars` extracts an empty YAML skeleton
  you can fill to apply it to the template.
- Command line tools are provided to fill templates using YAML files
  and to extract YAML skeletons from existing templates.



## Example

```python
>>> from namespace import namespace as ns
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


