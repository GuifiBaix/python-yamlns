from . import Path
from . import namespace as ns
import pytest

def normalize(x):
    """Turns recursively all the dicts of a json like
    structure into yamlns namespaces with their keys sorted
    so that their dumps can be compared.
    """
    if isinstance(x, dict):
        return ns((
            (k, normalize(v))
            for k,v in sorted(x.items())
        ))
    if isinstance(x, (list, tuple)):
        return [normalize(item) for item in x]
    return x

@pytest.fixture
def test_name(request):
    """Returns the test name"""
    return '{}.{}'.format(request.node.module.__name__, request.node.name)


@pytest.fixture
def yaml_snapshot(test_name):
    """Returns an assertion function that compares the value with the last accepted execution.
    former results are stored in 'testdata/snapshots' with the name of the test and '.expected'
    suffix.
    The first time you run it or every time the tests fails a file with suffix '.result'
    will be generated.
    """
    def assertion(data, snapshot=None):
        snapshotdir = Path('testdata/snapshots/')
        snapshot = snapshot or test_name
        snapshotfile = snapshotdir / (snapshot+'.expected')
        resultfile = snapshotdir / (snapshot+'.result')
        snapshotdir.mkdir(parents=True, exist_ok=True)
        ns(snapshot=normalize(data)).dump(resultfile)
        assert snapshotfile.exists(), (
            "First snapshot, check results and accept them with:\n"
            "mv {} {}\n".format(resultfile, snapshotfile)
        )
        expected = ns.load(snapshotfile)
        assert resultfile.read_text(encoding='utf8') == snapshotfile.read_text('utf8'), (
            "Failed snapshot. Check the result and if it is ok accept it with:\n"
            "mv {} {}\n".format(resultfile, snapshotfile)
        )
        # the result is keept if any of the former asserts fails
        resultfile.unlink()
    return assertion

def assert_ns_equal(data, expectation):
    """
    Assert that data representation in yaml matches the expectation.
    Both ends can be either a dictionary like object or a yaml string.
    """
    def parse_and_normalize(x):
        if type(x) in (type(u''), type('')):
            x = ns.loads(x)
        return normalize(x).dump()
    assert parse_and_normalize(data) == parse_and_normalize(expectation)


