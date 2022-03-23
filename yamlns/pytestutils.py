from . import Path, text
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

def assert_ns_equal(data, expectation):
    """
    Assert that data representation in yaml matches the expectation.
    Both ends can be either a dictionary like object or a yaml string.
    """
    def parse_and_normalize(x):
        # if strings are parsed as yaml
        if type(x) in (type(u''), type('')):
            x = ns.loads(x)
        # the resulting ns is normalized
        x = normalize(x)
        if type(x) == ns:
            return x.dump()
        return x

    assert parse_and_normalize(data) == parse_and_normalize(expectation)


