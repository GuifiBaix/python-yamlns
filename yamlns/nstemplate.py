#!/usr/bin/python3

import unittest
import yamlns
import sys

def templateVarsAsYaml(content):
	ns = yamlns.namespace.fromTemplateVars(content)
	return ns.dump()

class NSTemplate_test(unittest.TestCase) :

	def setUp(self) :
		self._toRemove = []

	def toRemove(self, f) :
		self._toRemove.append(f)

	def tearDown(self) :
		for f in self._toRemove :
			os.remove(f)


	def test_collectVars_withNoVar(self) :
		content = "booo"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			])

	def test_collectVars_withVar(self) :
		content = "b{boo}o"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			'boo',
			])

	def test_collectVars_withVar(self) :
		content = "b{boo}o{far}34"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			'boo',
			'far',
			])

	def test_collectVars_multiline(self) :
		content = "b{boo}o{far}34\ndfs{nice}"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			'boo',
			'far',
			'nice',
			])

	def test_collectVars_indexinDroped(self) :
		content = "b{boo}o{far}34\ndfs{nice[3]}"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			'boo',
			'far',
			'nice',
			])

	def test_varsTree_plainVars(self) :
		theVars = [
			'boo',
			'far',
			'nice',
			]
		yaml = yamlns._varsTree(theVars).dump()
		self.assertEqual(yaml,
			'boo: \'\'\n'
			'far: \'\'\n'
			'nice: \'\'\n'
			)

	def test_varsTree_unordered(self) :
		theVars = [
			'nice',
			'far',
			'boo',
			]
		yaml = yamlns._varsTree(theVars).dump()
		self.assertEqual(yaml,
			'boo: \'\'\n'
			'far: \'\'\n'
			'nice: \'\'\n'
			)

	def test_varsTree_withSubVars(self) :
		theVars = [
			'upper.boo',
			'upper.far',
			'upper.nice',
			]
		yaml = yamlns._varsTree(theVars).dump()
		self.assertEqual(yaml,
			'upper:\n'
			'  boo: \'\'\n'
			'  far: \'\'\n'
			'  nice: \'\'\n'
			)

	def test_varsTree_withManySubVars(self) :
		theVars = [
			'upper.boo',
			'lower.nice',
			'upper.far',
			]
		yaml = yamlns._varsTree(theVars).dump()
		self.assertEqual(yaml,
			'lower:\n'
			'  nice: \'\'\n'
			'upper:\n'
			'  boo: \'\'\n'
			'  far: \'\'\n'
			)

	def test_varsTree_withSubSubVars(self) :
		theVars = [
			'upper.lower.boo',
			'upper.lower.far',
			'upper.lower.nice',
			]
		yaml = yamlns._varsTree(theVars).dump()
		self.assertEqual(yaml,
			'upper:\n'
			'  lower:\n'
			'    boo: \'\'\n'
			'    far: \'\'\n'
			'    nice: \'\'\n'
			)



def apply(yamlfile, template, output, encoding='utf-8') :
	yaml = yamlns.namespace.load(yamlfile)
	with open(template, encoding=encoding) as f :
		content = f.read()
	result = content.format(**yaml)
	with open(output, 'w', encoding=encoding) as f :
		f.write(result)

def extract(input_template, output_yaml, encoding='utf-8') :
	with open(input_template, encoding=encoding) as f :
		content = f.read()
	ns = yamlns.namespace.fromTemplateVars(content)
	with open(output_yaml, 'w') as f :
		f.write(ns.dump())


def main(args=sys.argv) :
	import argparse

	parser = argparse.ArgumentParser(
		description="Takes a template and extract a yaml to fill it.",
		)
	parser.add_argument(
		'--test',
		action='store_true',
		help="Run unittests",
		)

	parser.add_argument(
		'--encoding',
		default=None,
		help="forces input encoder for templates",
		dest='encoding',
		)

	sub = parser.add_subparsers(
		dest='subcommand',
		)

	subparser = sub.add_parser(
		'extract',
		help='Collects the template vars from a template and renders an empty yaml file with them',
		)
	subparser.add_argument(
		metavar='input.template',
		dest='input_template',
		)
	subparser.add_argument(
		metavar='output.yaml',
		dest='output_yaml',
		)

	subparser = sub.add_parser(
		'apply',
		help='Apply structured data in a YAML file to a template',
		)
	subparser.add_argument(
		metavar='input.yaml',
		dest='input_yaml',
		)
	subparser.add_argument(
		metavar='template',
		dest='template',
		)
	subparser.add_argument(
		metavar='output',
		dest='output',
		)

	args = parser.parse_args()

	if args.subcommand == 'extract' :
		extract(args.input_template, args.output_yaml, args.encoding)
		return 0

	if args.subcommand == 'apply' :
		apply(args.input_yaml, args.template, args.output, args.encoding)
		return 0

	parser.print_help()
	return -1


if __name__  == '__main__' :
	if '--test' in sys.argv :
		sys.argv.remove('--test')
		sys.exit(unittest.main())

	sys.exit(main())




