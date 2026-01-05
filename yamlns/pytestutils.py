from . import Path, text
from . import namespace as ns
from ._pytestutils_asserts.assert_impl import assert_ns_equal
import pytest
from .testutils import (
    normalize,
)


@pytest.fixture
def test_name(request):
    """Returns the test name"""
    return '{}.{}'.format(request.node.module.__name__, request.node.name)


@pytest.fixture
def text_snapshot(test_name):
    """Returns an assertion function that compares the value with the last accepted execution.
    former results are stored in 'testdata/snapshots' with the name of the test and '.expected'
    suffix.
    The first time you run it or every time the tests fails a file with suffix '.result'
    will be generated.
    """
    def assertion(result, name=None):
        snapshotdir = Path('testdata/snapshots/')
        name = name or test_name
        snapshotfile = snapshotdir / (name+'.expected')
        resultfile = snapshotdir / (name+'.result')
        snapshotdir.mkdir(parents=True, exist_ok=True)
        resultfile.write_text(text(result), encoding='utf8')
        assert snapshotfile.exists(), (
            "First snapshot, check results and accept them with:\n"
            "mv {} {}\n".format(resultfile, snapshotfile)
        )
        assert resultfile.read_text(encoding='utf8') == snapshotfile.read_text('utf8'), (
            "Failed snapshot. Check the result and if it is ok accept it with:\n"
            "mv {} {}\n".format(resultfile, snapshotfile)
        )
        # the result is keept if any of the former asserts fails
        resultfile.unlink()
    return assertion

@pytest.fixture
def yaml_snapshot(text_snapshot):
    """Returns an assertion function that compares the value with the last accepted execution.
    former results are stored in 'testdata/snapshots' with the name of the test and '.expected'
    suffix.
    The first time you run it or every time the tests fails a file with suffix '.result'
    will be generated.
    """
    def assertion(data, name=None):
        text = ns(snapshot=normalize(data)).dump()
        text_snapshot(text, name)

    return assertion

def assert_ns_contains(data, expected):
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
    assert_ns_equal(filter_keys(data, expected), expected)


