#!/usr/bin/python3

import unittest
import yamlns
import sys
import io
import os
from . import nstemplate

class NSTemplate_test(unittest.TestCase) :

	def setUp(self) :
		self._toRemove = []

	def toRemove(self, f) :
		self._toRemove.append(f)

	def tearDown(self) :
		for f in self._toRemove :
			if os.path.exists(f):
				os.remove(f)

	def write(self, filename, content):
		with io.open(filename, 'w', encoding='utf8') as f:
			f.write(content)

	def read(self, filename):
		with io.open(filename, encoding='utf8') as f:
			return f.read()

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

	def test_collectVars_withManyVarsInALine(self) :
		content = "b{boo}o{far}34"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			'boo',
			'far',
			])

	def test_collectVars_multiline(self) :
		content = "b{boo}o\ndfs{nice}"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
			'boo',
			'nice',
			])

	def test_collectVars_indexinDroped(self) :
		content = "dfs{nice[3]}"
		result = yamlns._collectVars(content)
		self.assertEqual(result,[
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

	def test_templateVarsAsYaml(self):
		yaml = yamlns.namespace.fromTemplateVars("""\
			{var1.foo} {var1.lala} {var2}
		""")
		self.assertEqual(yaml.dump(), 
			'var1:\n'
			'  foo: \'\'\n'
			'  lala: \'\'\n'
			'var2: \'\'\n'
		)

	def test_extract(self):
		filemd = 'deleteme.md'
		fileyaml = 'deleteme.yaml'
		self.toRemove(filemd)
		self.toRemove(fileyaml)
		self.write(filemd, u"{var1} {var2.foo}")

		nstemplate.extract(filemd, fileyaml)

		self.assertEqual(self.read(fileyaml),
			u"var1: ''\n"
			u"var2:\n"
			u"  foo: ''\n"
		)

	def test_apply(self):
		filemd = 'deleteme.md'
		fileyaml = 'deleteme.yaml'
		fileout = 'deleteme-output.md'
		self.toRemove(filemd)
		self.toRemove(fileyaml)
		self.toRemove(fileout)

		self.write(filemd, u"{var1} {var2.foo}")
		self.write(fileyaml,
			u"var1: 'value1'\n"
			u"var2:\n"
			u"  foo: 666\n"
		)

		nstemplate.apply(fileyaml, filemd, fileout)

		self.assertEqual(self.read(fileout),
			u"value1 666")





if __name__  == '__main__' :
	sys.exit(unittest.main())




# vim: sw=4 ts=4 noet
