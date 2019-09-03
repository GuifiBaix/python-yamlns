# -*- encoding: utf8 -*-

import unittest
from . import namespace as ns

class TestUtils_Test(unittest.TestCase):

	from .testutils import assertNsEqual

	def test_assertNsEqual_differentValues(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual(ns(a=3), ns(a=4))
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a: 3\\n' != 'a: 4\\n'\n"
			"- a: 3\n"
			"?    ^\n"
			"+ a: 4\n"
			"?    ^\n"
			)


	def test_assertNsEqual_differentKeys(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual(ns(b=2), ns(c=2))
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'b: 2\\n' != 'c: 2\\n'\n"
			"- b: 2\n"
			"? ^\n"
			"+ c: 2\n"
			"? ^\n"
			)

	def test_assertNsEqual_withOneDict(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual(dict(a=3), ns(a=4))
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a: 3\\n' != 'a: 4\\n'\n"
			"- a: 3\n"
			"?    ^\n"
			"+ a: 4\n"
			"?    ^\n"
			)

	def test_assertNsEqual_withOtherDict(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual(ns(a=3), dict(a=4))
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a: 3\\n' != 'a: 4\\n'\n"
			"- a: 3\n"
			"?    ^\n"
			"+ a: 4\n"
			"?    ^\n"
			)

	def test_assertNsEqual_withOneYaml(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual("a: 3", ns(a=4))
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a: 3\\n' != 'a: 4\\n'\n"
			"- a: 3\n"
			"?    ^\n"
			"+ a: 4\n"
			"?    ^\n"
			)

	def test_assertNsEqual_withOtheYaml(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual(ns(a=3), "a: 4")
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a: 3\\n' != 'a: 4\\n'\n"
			"- a: 3\n"
			"?    ^\n"
			"+ a: 4\n"
			"?    ^\n"
			)

	def test_assertNsEqual_keysGetSorted(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual("a: 3\nb: 4", "b: 4\na: different")
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a: 3\\nb: 4\\n' != 'a: different\\nb: 4\\n'\n"
			"- a: 3\n"
			"+ a: different\n"
			"  b: 4\n"
			)

	def test_assertNsEqual_innerDictsGetSortedToo(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual(
				"a:\n  b: 4\n  c: 3",
				"a:\n  c: 3\n  b: different"
				)
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a:\\n  b: 4\\n  c: 3\\n' != 'a:\\n  b: different\\n  c: 3\\n'\n"
			"  a:\n"
			"-   b: 4\n"
			"+   b: different\n"
			"    c: 3\n"
			)

	def test_assertNsEqual_dictInsideList(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual("a: [{c: 3, b: 2}, 4]", "a: [{b: 2}, 4]")
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'a:\\n- b: 2\\n  c: 3\\n- 4\\n' != 'a:\\n- b: 2\\n- 4\\n'\n"
			"  a:\n"
			"  - b: 2\n"
			"-   c: 3\n"
			"  - 4\n"
			)

	def test_assertNsEqual_lists(self):
		with self.assertRaises(AssertionError) as ctx:
			self.assertNsEqual("[3, 4]", [3, 5])
		self.assertMultiLineEqual(type('u')(ctx.exception),
			"'data:\\n- 3\\n- 4\\n' != 'data:\\n- 3\\n- 5\\n'\n"
			"  data:\n"
			"  - 3\n"
			"- - 4\n"
			"?   ^\n"
			"+ - 5\n"
			"?   ^\n"
			)


# vim: noet ts=4 sw=4
