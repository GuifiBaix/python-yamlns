# Do not import this file directly
# This is a hack ensure this file is registered 
# for pytest to rewrite asserts before importing it.

from .testutils import (
    _parse_normalize_and_dump,
)

def assert_ns_equal(data, expectation):
    """
    Assert that data representation in yaml matches the expectation.
    Both ends can be either a dictionary like object or a yaml string.
    """
    assert _parse_normalize_and_dump(data) == _parse_normalize_and_dump(expectation)


