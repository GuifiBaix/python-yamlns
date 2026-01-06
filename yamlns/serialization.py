import decimal
import datetime
from .core import namespace
from .dateutils import Date
from .compat import text
try:
	import numpy as np
except ImportError:
	np=None

import yaml
try:
	from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
	from yaml import SafeLoader, SafeDumper

class NamespaceYamlDumper(SafeDumper):

	def __init__(self, *args, **kwargs):
		super(NamespaceYamlDumper, self).__init__(*args, **kwargs)
		self.add_representer(
			namespace, NamespaceYamlDumper.represent_dict )
		self.add_representer(
			decimal.Decimal, NamespaceYamlDumper.represent_float)
		self.add_representer(
			Date, NamespaceYamlDumper.represent_date)
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
			value = text(data).lower()

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


class NamespaceYAMLLoader(SafeLoader):

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
			return sign*decimal.Decimal("Infinity")
		if value == '.nan':
			return decimal.Decimal("NaN")
		return sign*decimal.Decimal(value)

	def construct_yaml_map(self, node):
		data = namespace()
		yield data
		value = self.construct_mapping(node)
		data.update(value)

	def construct_yaml_timestamp(self, node) :
		result = super(NamespaceYAMLLoader,self).construct_yaml_timestamp(node)
		if not isinstance(result, datetime.datetime):
			return Date(result)
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


