#!/usr/bin/python3


import yaml
from collections import OrderedDict
import decimal
import datetime
from namespace import dateutils

class namespace(OrderedDict) :
	"""A dictionary whose values can be accessed also as attributes
	and can be loaded and dumped as YAML."""

	def __init__(self, *args, **kwd) :
		super(namespace, self).__init__(*args, **kwd)
#		self.update(self.__dict__)
#		self.__dict__ = self

	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError as e:
			raise AttributeError(name)

	def __setattr__(self, name, value):
		if name.startswith('_'):
			super(namespace, self).__setattr__(name, value)
		else:
			self[name]=value

	def __delattr__(self, name) :
		try:
			del self[name]
		except KeyError:
			super(namespace, self).__delattr__(name)

	def deepcopy(self) :
		return self.loads(self.dump())

	@classmethod
	def loads(cls, yamlContent) :
		import io
		return cls.load(io.StringIO(yamlContent))

	@classmethod
	def load(cls, filename) :

		def wrap(data) :
			return data
			if type(data) is dict :
				return namespace({
					k: wrap(v)
					for k,v in data.items()
					})
			if isinstance(data, list) or isinstance(data, tuple) :
				return [wrap(v) for v in data]
			return data

		if hasattr(filename, 'read') :
			result = yaml.load(stream=filename, Loader=NamespaceYAMLLoader)
		else :
			with open(filename) as f:
				result = yaml.load(stream=f, Loader=NamespaceYAMLLoader)
		return wrap(result)

	def dump(self, filename=None) :

		def dumpit(afile) :

			return yaml.dump(self, stream=afile,
				default_flow_style=False,
				allow_unicode=True,
				Dumper = NamespaceYamlDumper,
				)

		if hasattr(filename,'write') :
			dumpit(filename)
			return

		# TODO: Test None
		# TODO: Test file
		if filename is None or hasattr(filename,'write') :
			return dumpit(filename)

		with open(filename, 'w', encoding='utf-8') as f :
			dumpit(f)

class NamespaceYamlDumper(yaml.SafeDumper):

	def __init__(self, *args, **kwargs):
		super(NamespaceYamlDumper, self).__init__(*args, **kwargs)
		self.add_representer(
			namespace, NamespaceYamlDumper.represent_dict )
		self.add_representer(
			decimal.Decimal, NamespaceYamlDumper.represent_float)
		self.add_representer(
			dateutils.Date, NamespaceYamlDumper.represent_date)

	def represent_date(self, data):
		return self.represent_scalar('tag:yaml.org,2002:timestamp', str(data))

	def represent_float(self, data):
		if data != data or (data == 0.0 and data == 1.0):
			value = '.nan'
		elif data == self.inf_value:
			value = '.inf'
		elif data == -self.inf_value:
			value = '-.inf'
		else:
# Here previous version called repr
			value = str(data).lower()
			# Note that in some cases `repr(data)` represents a float number
			# without the decimal parts.  For instance:
			#   >>> repr(1e17)
			#   '1e17'
			# Unfortunately, this is not a valid float representation according
			# to the definition of the `!!float` tag.  We fix this by adding
			# '.0' before the 'e' symbol.
			if '.' not in value and 'e' in value:
				value = value.replace('e', '.0e', 1)
		return self.represent_scalar('tag:yaml.org,2002:float', value)


	# Kludge: This is a rewritten version of yaml.representer.Representer.represent_mapping
	# to avoid sorting pairs by key
	def represent_mapping(self, tag, mapping, flow_style=None):
		value = []
		node = yaml.nodes.MappingNode(tag, value, flow_style=flow_style)
		if self.alias_key is not None:
			self.represented_objects[self.alias_key] = node
		best_style = True
		if hasattr(mapping, 'items'):
			mapping = list(mapping.items())
	# Those are the lines removed from official sources
	#		try:
	#			mapping = sorted(mapping)
	#		except TypeError:
	#			pass
		for item_key, item_value in mapping:
			node_key = self.represent_data(item_key)
			node_value = self.represent_data(item_value)
			if not (isinstance(node_key, yaml.nodes.ScalarNode) and not node_key.style):
				best_style = False
			if not (isinstance(node_value, yaml.nodes.ScalarNode) and not node_value.style):
				best_style = False
			value.append((node_key, node_value))
		if flow_style is None:
			if self.default_flow_style is not None:
				node.flow_style = self.default_flow_style
			else:
				node.flow_style = best_style
		return node


class NamespaceYAMLLoader(yaml.SafeLoader):

	def __init__(self, *args, **kwargs):
		super(NamespaceYAMLLoader, self).__init__(*args, **kwargs)
		self.add_constructor('tag:yaml.org,2002:map', type(self).construct_yaml_map)
		self.add_constructor('tag:yaml.org,2002:omap', type(self).construct_yaml_map)
		self.add_constructor('tag:yaml.org,2002:float', type(self).construct_decimal)
		self.add_constructor('tag:yaml.org,2002:timestamp', type(self).construct_yaml_timestamp)


	def construct_decimal(self, node):
		value = self.construct_scalar(node)
		value = value.replace('_', '').lower()
		sign = +1
		if value[0] == '-':
			sign = -1
		if value[0] in '+-':
			value = value[1:]
		if value == '.inf':
			return sign*self.inf_value
		elif value == '.nan':
			return self.nan_value
		elif ':' in value:
			digits = [float(part) for part in value.split(':')]
			digits.reverse()
			base = 1
			value = 0.0
			for digit in digits:
				value += digit*base
				base *= 60
			return sign*value
		else:
			return sign*decimal.Decimal(value)

	def construct_yaml_map(self, node):
		data = namespace()
		yield data
		value = self.construct_mapping(node)
		data.update(value)

	def construct_yaml_timestamp(self, node) :
		result = super(NamespaceYAMLLoader,self).construct_yaml_timestamp(node)
		if isinstance(result, datetime.date):
			return dateutils.Date(result)
		return result

	def construct_mapping(self, node, deep=False):
		if isinstance(node, yaml.MappingNode):
			self.flatten_mapping(node)
		else:
			raise yaml.constructor.ConstructorError( None, None,
				'expected a mapping node, but found {}'.format(node.id), node.start_mark )

		mapping = namespace()
		for key_node, value_node in node.value:
			key = self.construct_object(key_node, deep=True) # default is to not recurse into keys
			if isinstance(key, list): key = tuple(key)
			try:
				hash(key)
			except TypeError as exc:
				raise yaml.constructor.ConstructorError( 'while constructing a mapping',
					node.start_mark, 'found unacceptable key ({})'.format(exc), key_node.start_mark )
			value = self.construct_object(value_node, deep=deep)
			mapping[key] = value
		return mapping




import unittest

class namespace_Test(unittest.TestCase) :

	def test_construction_default(self):
		ns = namespace()
		self.assertEqual(ns.dump(),
			"{}\n")

	def test_setattribute(self):
		ns = namespace()
		ns.lala = "boo"
		self.assertEqual(ns.lala, 'boo')
		self.assertEqual(ns['lala'], 'boo')
		self.assertEqual(ns.dump(),
			"lala: boo\n")

	def test_setattribute_twice_overwrites(self):
		ns = namespace()
		ns.lala = "boo"
		ns.lala = "foo"
		self.assertEqual(ns.lala, 'foo')
		self.assertEqual(ns['lala'], 'foo')
		self.assertEqual(ns.dump(),
			"lala: foo\n")

	def test_setattribute_many(self):
		ns = namespace()
		ns.lala = "boo"
		ns.lola = "foo"
		self.assertEqual(ns.lola, 'foo')
		self.assertEqual(ns['lola'], 'foo')
		self.assertEqual(ns.dump(),
			"lala: boo\n"
			"lola: foo\n")

	def test_setattribute_differentOrder(self):
		ns = namespace()
		ns.lola = "foo"
		ns.lala = "boo"
		self.assertEqual(ns.dump(),
			"lola: foo\n"
			"lala: boo\n"
			)

	def test_delattribute(self):
		ns = namespace()
		ns.lola = "foo"
		ns.lala = "boo"
		del ns.lola
		self.assertEqual(ns.dump(),
			"lala: boo\n"
			)

	def test_delattribute(self):
		ns = namespace()
		ns.lola = "foo"
		with self.assertRaises(AttributeError):
			del ns.notexisting

	def test_load_None(self):
		self.assertEqual(namespace.loads(""),
			None)

	def test_load_empty(self):
		self.assertEqual(namespace.loads("{}"),
			namespace())

	def test_reload(self):
		yamlcontent = (
			"lala: boo\n"
			"lola: foo\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_reload_inverseOrder(self):
		yamlcontent = (
			"lola: foo\n"
			"lala: boo\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_subnamespaces(self) :
		ns = namespace()
		ns.sub = namespace()
		ns.sub.foo = "value1"
		ns.sub.bar = "value2"
		self.assertEqual(ns.dump(),
			"sub:\n"
			"  foo: value1\n"
			"  bar: value2\n"
			)

	def test_reload_subnamespaces(self) :
		yamlcontent = (
			"sub:\n"
			"  foo: value1\n"
			"  bar: value2\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_load_decimal(self) :
		yamlcontent = (
			"decimal: 3.41"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.decimal),
			decimal.Decimal)
		self.assertEqual(ns.decimal,
			decimal.Decimal('3.41'))

	def test_dump_float(self) :
		yamlcontent = (
			"decimal: 3.41\n"
			)
		ns = namespace()
		ns.decimal = 3.41
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_dump_decimal(self) :
		yamlcontent = (
			"decimal: 3.41\n"
			)
		ns = namespace()
		ns.decimal = decimal.Decimal('3.41')
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_load_date(self):
		yamlcontent = (
			"adate: 2000-02-28\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.adate),
			dateutils.Date)

	def test_dump_date(self):
		yamlcontent = (
			"adate: 2000-02-28\n"
			)
		ns = namespace()
		ns.adate = dateutils.Date(2000,2,28)
		self.assertEqual(ns.dump(),
			yamlcontent)

if __name__ == '__main__':
	unittest.main()





