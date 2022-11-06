# -*- coding: utf-8 -*-

import unittest
from . import namespace as ns

# Readable verbose testcase listing
unittest.TestCase.__str__ = unittest.TestCase.id

def assertNsEqual(self, dict1, dict2):

    """
    Asserts that both dicts have equivalent structure
    by comparing its dump as YAML with all the keys
    alphabetically sorted
    If parameters are strings they are parsed as yaml.

    YAML dump of both structures are
    Comparation by comparing the result of turning them
    to yaml sorting the keys of any dict within the structure.
    """
    def parseIfString(x):
        if type(x) in (type(u''),type(b'')):
            return ns.loads(x)
        return x

    def yaml(x):
        x = parseIfString(x)
        if type(x) in (list, tuple):
            return normalize(ns(data=x)).dump()
        return normalize(x).dump()

    self.assertMultiLineEqual(
        yaml(dict1),
        yaml(dict2))

def normalize(x):
    """Turns recursively all the dicts of a json like
    structure into yamlns namespaces with their keys sorted
    so that their dumps can be compared.
    """
    return ns.deep(x, sorted=True)


def _parse_and_normalize(x):
    if type(x) in (type(u''), type('')):
        x = ns.loads(x)
    return normalize(x)

def _parse_normalize_and_dump(x):
    x = _parse_and_normalize(x)
    if type(x) == ns:
        return x.dump()
    return x

def assertNsContains(self, data, expected):
    """
    Assert that all keys in expected have the same values
    in data than in expected.
    """
    def filter_keys(x, reference):
        if not isinstance(x, dict):
            return x
        return ns((
            (k, filter_keys(v, reference[k]))
            for k,v in x.items()
            if k in reference
        ))
    data = _parse_and_normalize(data)
    expected = _parse_and_normalize(expected)
    self.assertNsEqual(filter_keys(data, expected).dump(), expected.dump())

# vim: ts=4 sw=4 et
