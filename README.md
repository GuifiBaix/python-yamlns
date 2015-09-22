# namespace

An ordered dictionary whose values can be accessed either by indexing
and atribute dot syntax and has direct mapping to YAML.


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


