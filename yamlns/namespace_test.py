#!/usr/bin/python3
#-*- coding: utf-8 -*-

from . import namespace
from . import dateutils
from . import Path
import decimal
import datetime
import math
import unittest
import io
import sys

class Namespace_Test(unittest.TestCase) :

	def setUp(self):
		''

	def tearDown(self):
		import os
		try:
			os.unlink('test.yaml')
		except:
			pass

	def assertContent(self, expected):
		import io
		with io.open("test.yaml", encoding='utf-8') as f:
			result = f.read()
		self.assertEqual(result, expected)

	def writeFile(self, data):
		import io
		with io.open("test.yaml",'w',encoding='utf-8') as f:
			f.write(data)

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

	def test_loads_fromEncodedUtf8(self):
		yaml = u"hi: caña\n".encode('utf-8')
		result = namespace.loads(yaml)
		self.assertEqual(result,
			namespace(hi=u'caña'))

	def test_loads_unicode(self):
		yaml = u"hi: caña\n"
		result = namespace.loads(yaml)
		self.assertEqual(result,
			namespace(hi=u'caña'))

	# Numbers (int, decimal, float)

	def test_load_decimal(self) :
		yamlcontent = (
			"decimal: 3.41"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.decimal),
			decimal.Decimal)
		self.assertEqual(ns.decimal,
			decimal.Decimal('3.41'))

	def test_load_decimal_negative(self) :
		yamlcontent = (
			"decimal: -3.41"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.decimal),
			decimal.Decimal)
		self.assertEqual(ns.decimal,
			decimal.Decimal('-3.41'))

	def test_load_decimal_infinite(self) :
		ns = namespace.loads(
			"decimal: -.inf"
		)
		self.assertEqual(type(ns.decimal),
			float)
		# Why not decimal?
		self.assertEqual(ns.decimal,
			float("-inf"))

	def test_load_decimal_notANumber(self) :
		ns = namespace.loads(
			"decimal: .nan"
		)
		self.assertEqual(type(ns.decimal),
			float)
		# Why not decimal?
		self.assertTrue(math.isnan(ns.decimal) )

	def test_dump_decimal_inf(self) :
		ns = namespace()
		ns.decimal = decimal.Decimal('-inf')
		self.assertEqual(ns.dump(),
			"decimal: -.inf\n"
		)

	def test_dump_float(self) :
		ns = namespace()
		ns.decimal = 3.41
		self.assertEqual(ns.dump(),
			"decimal: 3.41\n"
		)

	def test_dump_float_inf(self) :

		ns = namespace()
		ns.decimal = float('-inf')
		self.assertEqual(ns.dump(),
			"decimal: -.inf\n"
		)

	def test_dump_decimal(self) :
		ns = namespace()
		ns.decimal = decimal.Decimal('3.41')
		self.assertEqual(ns.dump(),
			"decimal: 3.41\n"
		)

	def test_dump_float_nan(self):
		ns = namespace()
		ns.decimal = float('nan')
		self.assertEqual(ns.dump(),
			"decimal: .nan\n"
		)

	def test_dump_decimal_nan(self):
		ns = namespace()
		ns.decimal = decimal.Decimal('nan')
		self.assertEqual(ns.dump(),
			"decimal: .nan\n"
		)

	# Dates, times

	def test_load_date(self):
		yamlcontent = (
			"adate: 2000-02-28\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.adate),
			dateutils.Date)

	class tzoffset(datetime.tzinfo):
		def __init__(self, name=None, *args, **kwds):
			self._offset = datetime.timedelta(*args, **kwds)
			self._name = name
		def utcoffset(self, dt):
			return self._offset
		def dst(self):
			return datetime.timedelta(0)
		def tzname(self):
			return self._name


	def test_dump_datetime(self):
		yamlcontent = (
			"adate: 2000-02-28 10:20:30.000040+02:00\n"
			)
		ns = namespace()
		ns.adate = datetime.datetime(2000,2,28,10,20,30,40, self.tzoffset(hours=2))
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_dump_datetime_utc(self):
		yamlcontent = (
			"adate: 2000-02-28 10:20:30.000040+00:00\n"
			)
		ns = namespace()
		ns.adate = datetime.datetime(2000,2,28,10,20,30,40, self.tzoffset(hours=0))
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_dump_datetime_naive(self):
		yamlcontent = (
			"adate: 2000-02-28 10:20:30.000040\n"
			)
		ns = namespace()
		ns.adate = datetime.datetime(2000,2,28,10,20,30,40)
		self.assertEqual(ns.dump(),
			yamlcontent)

	def test_load_datetime(self):
		yamlcontent = (
			"adate: 2000-02-28 10:20:30.000040+02:00\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.adate),
			datetime.datetime)
		self.assertEqual(ns.adate,
			datetime.datetime(2000,2,28,10,20,30,40, self.tzoffset(hours=2)))

	def test_load_datetime_utc(self):
		yamlcontent = (
			"adate: 2000-02-28 10:20:30.000040Z\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.adate),
			datetime.datetime)
		self.assertEqual(ns.adate,
			datetime.datetime(2000,2,28,10,20,30,40, self.tzoffset(hours=0)))

	def test_load_datetime_naive(self):
		yamlcontent = (
			"adate: 2000-02-28 10:20:30.000040\n"
			)
		ns = namespace.loads(yamlcontent)
		self.assertEqual(type(ns.adate),
			datetime.datetime)
		self.assertEqual(ns.adate,
			datetime.datetime(2000,2,28,10,20,30,40))

	# dir just for values accessible as attribute

	def test_dir_withNonExistingAttributes(self):
		ns = namespace()
		ns.attr1 = 'value1'
		self.assertTrue('bad' not in dir(ns))

	def test_dir_withExistingAttributes(self):
		ns = namespace()
		ns.attr1 = 'value1'
		self.assertTrue('attr1' in dir(ns))

	def test_dir_withNonIdentifierNames(self):
		ns = namespace()
		ns['a-b'] = 'value1'

		self.assertTrue('a-b' not in dir(ns))

	# multiline strings

	def test_dump_multiline(self):
		ns = namespace()
		ns.text="line\nsecond line"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: |-\n"
			"  line\n"
			"  second line\n"
			"other: 2\n"
		)

	def test_dump_multiline_innnerIndentation(self):
		ns = namespace()
		ns.text="line\n  second line"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: |-\n"
			"  line\n"
			"    second line\n"
			"other: 2\n"
		)

	def test_dump_multiline_firstLineIndentation(self):
		ns = namespace()
		ns.text="  line\nsecond line"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: |2-\n"
			"    line\n"
			"  second line\n"
			"other: 2\n"
		)

	def test_dump_multiline_tabIndentation(self):
		ns = namespace()
		ns.text="\tline\nsecond line"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: \"\\tline\\nsecond line\"\n"
			"other: 2\n"
		)

	def test_dump_multiline_endSpaces(self):
		ns = namespace()
		ns.text="line   \nsecond line"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: \"line   \\nsecond line\"\n"
			"other: 2\n"
		)

	def test_dump_multiline_emptyLine(self):
		ns = namespace()
		ns.text="line\n\nsecond line"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: |-\n"
			"  line\n"
			"\n"
			"  second line\n"
			"other: 2\n"
		)

	def test_dump_multiline_emptyAtEnd(self):
		ns = namespace()
		ns.text="line\nsecond line\n"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: |\n" # this changes, was |-
			"  line\n"
			"  second line\n"
			"other: 2\n"
		)

	def test_dump_multiline_manyEmptyAtEnd(self):
		ns = namespace()
		ns.text="line\nsecond line\n\n\n"
		ns.other=2
		self.assertMultiLineEqual(ns.dump(),
			"text: |+\n" # this changes, was |-
			"  line\n"
			"  second line\n"
			"\n"
			"\n"
			"other: 2\n"
		)

	# Other

	def test_load_recursiveArray(self):
		ns = namespace.loads(
			"list:\n"
			"  - key1: value1\n"
			)
		self.assertEqual(ns,
			namespace(list=[namespace(key1='value1')]))

	# Sources an targets

	def test_load_fromFilename(self):
		self.writeFile(u"hi: caña\n")
		result = namespace.load("test.yaml")
		self.assertEqual(result,
			namespace(hi=u'caña'))

	def test_dump_toFileName(self):
		data = namespace(otra=u'caña')
		data.dump('test.yaml')
		self.assertContent(u"otra: caña\n")


	@unittest.skipIf(not Path, "neither pathlib or pathlib2 not installed")
	def test_load_fromPath(self):
		self.writeFile(u"hi: caña\n")
		result = namespace.load(Path("test.yaml"))
		self.assertEqual(result,
			namespace(hi=u'caña'))

	@unittest.skipIf(not Path, "neither pathlib or pathlib2 not installed")
	def test_dump_toPath(self):
		data = namespace(otra=u'caña')
		data.dump(Path('test.yaml'))
		self.assertContent(u"otra: caña\n")

	@unittest.skipIf(sys.version_info[0]>2,
		"PyYaml in Python 3 requires a text file")
	def test_load_fromBinaryFileObject(self):
		self.writeFile(u"hi: caña\n")
		with io.open('test.yaml', 'rb') as f:
			result = namespace.load(f)
		self.assertEqual(result,
			namespace(hi=u'caña'))

	@unittest.skipIf(sys.version_info[0]>2,
		"PyYaml in Python 3 requires a text file")
	def test_dump_toBinaryFileObject(self):
		data = namespace(otra=u'caña')
		with io.open('test.yaml', 'wb') as f:
			data.dump(f)
		self.assertContent(u"otra: caña\n")

	@unittest.skipIf(sys.version_info[0]==2,
		"PyYaml in Python 2 requires a binary file")
	def test_load_fromTextFileObject(self):
		self.writeFile(u"hi: caña\n")
		with io.open('test.yaml', 'r', encoding='utf8') as f:
			result = namespace.load(f)
		self.assertEqual(result,
			namespace(hi=u'caña'))

	@unittest.skipIf(sys.version_info[0]==2,
		"PyYaml in Python 2 requires a binary file")
	def test_dump_toTextFileObject(self):
		data = namespace(otra=u'caña')
		with io.open('test.yaml','w', encoding='utf8') as f:
			data.dump(f)
		self.assertContent(u"otra: caña\n")


if __name__ == '__main__':
	unittest.main()



# vim: sw=4 ts=4 noet
