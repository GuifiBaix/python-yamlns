# -*- coding: utf-8 -*-

import unittest
from . import namespace as ns

# Readable verbose testcase listing
unittest.TestCase.__str__ = unittest.TestCase.id

def assertNsEqual(self, dict1, dict2):

    """
    Asserts that both dict have equivalent structure.
    If parameters are strings they are parsed as yaml.
    Comparation by comparing the result of turning them
    to yaml sorting the keys of any dict within the structure.
    """
    def sortedDict(x):
        if type(x) in (dict, ns):
            return ns((k,sortedDict(v)) for k,v in sorted(x.items()))
        if type(x) in (list, tuple):
            return [sortedDict(y) for y in x]
        return x

    def parseIfString(x):
        if type(x) in (type(u''),type(b'')):
            return ns.loads(x)
        return x

    def yaml(x):
        x = parseIfString(x)
        if type(x) in (list, tuple):
            return sortedDict(ns(data=x)).dump()
        return sortedDict(x).dump()

    self.assertMultiLineEqual(
        yaml(dict1),
        yaml(dict2))

# vim: ts=4 sw=4 et
