#!/usr/bin/python3


import yaml
from collections import OrderedDict
import decimal
import datetime
from . import dateutils
try:
	from pathlib2 import Path
except ImportError:
	try:
		from pathlib import Path
	except ImportError:
		Path = None

try:
	import numpy as np
except ImportError:
	np=None

_sorted = sorted

def text(data):
	if type(data) is type(u''):
		return data
	if type(data) is type(b''):
		return data.decode('utf8')
	return type(u'')(data)

class namespace(OrderedDict) :
	"""A dictionary whose values can be accessed also as attributes
	and can be loaded and dumped as YAML."""

	def __init__(self, *args, **kwd) :
		super(namespace, self).__init__(*args, **kwd)

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

	def __dir__(self):

		def isidentifier(candidate):
			"Is the candidate string an identifier in Python 2.x"
			try:
				return candidate.isidentifier()
			except AttributeError: pass
			import keyword
			import re
			is_not_keyword = candidate not in keyword.kwlist
			pattern = re.compile(r'^[a-z_][a-z0-9_]*$', re.I)
			matches_pattern = bool(pattern.match(candidate))
			return is_not_keyword and matches_pattern

		try:
			attributes = super(namespace, self).__dir__()
		except AttributeError: # Py2 OrderedDict has no __dir__
			attributes = []
		attributes.extend(k for k in self.keys() if isidentifier(k))
		return attributes

	def deepcopy(self) :
		return self.loads(self.dump())

	@classmethod
	def deep(cls, x, sorted=False):
		"""Turns recursively all the dicts of a json like
		structure into yamlns namespaces. Set sorted to true
		to force alphabetical order of the keys
		so that their dumps can be compared.
		"""
		sort_function = _sorted if sorted else lambda x:x
		if type(x) in (dict, namespace):
			return ns(
				(k,cls.deep(v, sorted=sorted))
				for k,v in sort_function(x.items())
			)
		if type(x) in (list, tuple):
			return [
				cls.deep(y, sorted=sorted)
				for y in x
			]
		return x

	@classmethod
	def loads(cls, yamlContent) :
		yamlContent = text(yamlContent)
		import io
		return cls.load(io.StringIO(yamlContent))

	@classmethod
	def load(cls, inputfile) :

		if hasattr(inputfile, 'read') :
			return yaml.load(stream=inputfile, Loader=NamespaceYAMLLoader)
		if Path:
			with Path(inputfile).open() as f:
				return yaml.load(stream=f, Loader=NamespaceYAMLLoader)
		with open(inputfile) as f:
			return yaml.load(stream=f, Loader=NamespaceYAMLLoader)

	def dump(self, filename=None) :

		def dumpit(stream) :

			return yaml.dump(self, stream=stream,
				default_flow_style=False,
				allow_unicode=True,
				Dumper = NamespaceYamlDumper,
			)

		# TODO: Test None (stdout)
		if filename is None:
			return dumpit(filename)

		# TODO: Test file
		if hasattr(filename,'write') :
			return dumpit(filename)

		import sys
		mode = 'wb' if sys.version_info[0] == 2 else 'w'

		from io import open
		if not Path:
			with open(filename, mode) as f :
				return dumpit(f)

		with Path(filename).open(mode) as f :
			return dumpit(f)

	@classmethod
	def fromTemplateVars(clss, templateContent):
		"""Given a string with format template substitutions
		it builds a namespace having the fields to fill it.
		Namespace leaf values will be set as empty strings.
		"""
		templateVariables = _collectVars(templateContent)
		return _varsTree(templateVariables)

def _collectVars(content) :
	import re
	pattern = r'{([^}^[]*)(\[[^]]\])?}'
	return [item.group(1) for item in re.finditer(pattern, content)]

def _varsTree(theVars):
	ns = namespace()
	for segments in (var.split('.') for var in sorted(theVars)) :
		target = ns
		for segment in segments[:-1] :
			if segment not in target:
				target[segment] = namespace()
			# TODO: double check it is a ns
			target = target[segment]
		target[segments[-1]] = ''
	return ns


class NamespaceYamlDumper(yaml.CSafeDumper):

	def __init__(self, *args, **kwargs):
		super(NamespaceYamlDumper, self).__init__(*args, **kwargs)
		self.add_representer(
			namespace, NamespaceYamlDumper.represent_dict )
		self.add_representer(
			decimal.Decimal, NamespaceYamlDumper.represent_float)
		self.add_representer(
			dateutils.Date, NamespaceYamlDumper.represent_date)
		if np:
			self.add_representer(
				np.ndarray, NamespaceYamlDumper.represent_np)

		self.add_representer(type(u''), NamespaceYamlDumper.represent_str)
		if type(u'')!=type(''): # Py2 compat
			self.add_representer(type(''), NamespaceYamlDumper.represent_str)

	def represent_str(self, data):
		if '\n' in data:  # check for multiline string
			return self.represent_scalar('tag:yaml.org,2002:str', data, style='|')
		return self.represent_scalar('tag:yaml.org,2002:str', data)

	def represent_date(self, data):
		return self.represent_scalar('tag:yaml.org,2002:timestamp', type(u'')(data))

	def represent_float(self, data):
		if data != data or (data == 0.0 and data == 1.0):
			value = '.nan'
		elif data == self.inf_value:
			value = '.inf'
		elif data == -self.inf_value:
			value = '-.inf'
		else:
# Here previous version called repr
			value = type(u'')(data).lower()
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

	def represent_np(self, data):
		return self.represent_sequence('tag:yaml.org,2002:seq', [float(x) for x in data])


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


class NamespaceYAMLLoader(yaml.CSafeLoader):

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
		if not isinstance(result, datetime.datetime):
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

ns = namespace # alias

# vim: sw=4 ts=4 noet
