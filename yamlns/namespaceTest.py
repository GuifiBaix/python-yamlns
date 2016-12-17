#!/usr/bin/python3
#-*- coding: utf-8 -*-

from yamlns import namespace
import decimal
from yamlns import dateutils


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

	def test_dir_withNonExistingAttributes(self):
		ns = namespace()
		ns.attr1 = 'value1'
		self.assertFalse('bad' in dir(ns))

	def test_dir_withExistingAttributes(self):
		ns = namespace()
		ns.attr1 = 'value1'
		self.assertTrue('attr1' in dir(ns))

	def test_dir_withNonIdentifierNames(self):
		ns = namespace()
		ns['a-b'] = 'value1'

		self.assertFalse('a-b' in dir(ns))

	def test_load_recursiveArray(self):
		ns = namespace.loads(
			"list:\n"
			"  - key1: value1\n"
			)
		self.assertEqual(ns,
			namespace(list=[namespace(key1='value1')]))

	def test_load_fromFile(self):
		data = u"hi: caña\n"
		import codecs
		with codecs.open("test.yaml",'w',encoding='utf-8') as f:
			f.write(data)
		try:
			result = namespace.load("test.yaml")
			self.assertEqual(result,
				namespace(hi=u'caña'))
		except: raise
		finally:
			import os
			os.unlink("test.yaml")

	def test_dump_toFile(self):
		data = namespace(otra=u'caña')
		data.dump('test.yaml')
		try:
			import codecs
			with codecs.open("test.yaml",encoding='utf-8') as f:
				result = f.read()
			self.assertEqual(result, u"otra: caña\n")
		except: raise
		finally:
			import os
			os.unlink("test.yaml")


if __name__ == '__main__':
	unittest.main()





