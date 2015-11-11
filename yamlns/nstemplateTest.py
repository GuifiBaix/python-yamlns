#!/usr/bin/python3

import unittest
import yamlns
import sys

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



if __name__  == '__main__' :
	sys.exit(unittest.main())





