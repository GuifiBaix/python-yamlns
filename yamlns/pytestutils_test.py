from __future__ import unicode_literals
from .pytestutils import (
    yaml_snapshot,
    text_snapshot,
    test_name,
    assert_ns_equal,
    assert_ns_contains,
    normalize,
    Path,
    ns
)
import pytest
import sys

py2 = sys.version_info < (3,)


def rmrf(path):
    path = Path(path)
    if not path.exists():
        return
    if path.is_file():
        path.unlink()
        return
    for child in path.glob('*'):
        rmrf(child)
    path.rmdir()

@pytest.fixture
def clean_snapshotdir():
    """Ensures the snapshotdir is removed before and after the test"""
    snapshotdir = Path('testdata/snapshots')
    rmrf(snapshotdir)
    yield snapshotdir
    rmrf(snapshotdir)

@pytest.fixture
def snapshotdir(clean_snapshotdir):
    """Ensures an empty existing snapshotdir, removed after the test"""
    clean_snapshotdir.mkdir(exist_ok=True, parents=True)
    yield clean_snapshotdir

def assertContent(path, expected):
    path = Path(path)
    assert path.exists()
    assert path.read_text(encoding='utf8') == expected

# normalize

def test__normalize__str():
    assert normalize('text') == 'text'

def test__normalize__int():
    assert normalize(1) == 1

def test__normalize__float():
    x = normalize(1.2)
    assert x == 1.2
    assert type(x) == float

def test__normalize__list():
    x = [1,2,3]
    assert normalize(x) == [1,2,3]
    assert normalize(x) is not [1,2,3] # a copy

def test__normalize__dict__turns_into_ns():
    x = dict()
    assert normalize(x) == dict()
    assert type(normalize(x)) == ns

def test__normalize__dict_inside_list__turns_into_ns():
    x = [dict()]
    assert normalize(x) == [dict()]
    assert type(normalize(x)[0]) == ns

def test__normalize__keys_get_sorted():
    x = normalize(ns.loads("""
        key2: value2
        key1: value1
    """))
    assert x.dump() == (
        "key1: value1\n"
        "key2: value2\n"
    )


# test_name fixture

def test__test_name(test_name):
    assert test_name == 'yamlns.pytestutils_test.test__test_name'


# yaml_snapshot fixture

def test__yaml_snapshot__no_expectation(
    yaml_snapshot,
    clean_snapshotdir,
    test_name,
):
    with pytest.raises(AssertionError) as exception:
        yaml_snapshot("content")

    expected = (
        "First snapshot, check results and accept them with:\n"
        "mv testdata/snapshots/{0}.result testdata/snapshots/{0}.expected\n"
    ).format(test_name)
    assert format(exception.value)[:len(expected)] == expected
    assertContent(clean_snapshotdir / '{}.result'.format(test_name),
        "snapshot: content\n"
    )
    assert not (clean_snapshotdir / '{}.expected'.format(test_name)).exists()

def test__yaml_snapshot__differentExpectation(
    yaml_snapshot,
    snapshotdir,
    test_name,
):
    expectation = snapshotdir / (test_name + '.expected')
    expectation.write_text("snapshot: unexpected\n", encoding='utf8')

    with pytest.raises(AssertionError) as exception:
        yaml_snapshot("content")

    expected=(
        "Failed snapshot. Check the result and if it is ok accept it with:\n"
        "mv testdata/snapshots/{0}.result testdata/snapshots/{0}.expected\n"
    ).format(test_name)
    assert format(exception.value)[:len(expected)] == expected

    assertContent(snapshotdir/'{}.result'.format(test_name),
        'snapshot: content\n'
    )
    assertContent(snapshotdir/'{}.expected'.format(test_name),
        'snapshot: unexpected\n'
    )

def test__yaml_snapshot__ok(yaml_snapshot, snapshotdir, test_name):
    expectation = snapshotdir / (test_name + '.expected')
    expectation.write_text("snapshot: content\n", encoding='utf8')

    yaml_snapshot("content")

    assert not (snapshotdir/'{}.result'.format(test_name)).exists()
    assertContent(snapshotdir/'{}.expected'.format(test_name),
        'snapshot: content\n'
    )


# assert_ns_equal assertion

def test__assert_ns_equal__value_differs():
    with pytest.raises(AssertionError) as exception:
        assert_ns_equal('key: result', 'key: expected')
    assert (
        "  - key: result\n"
        "  + key: expected"
        if py2 else
        "  - key: expected\n"
        "  + key: result"
    ) in format(exception.value)

def test__assert_ns_equal__result_dict():
    # Should not raise
    assert_ns_equal(dict(key='value'), 'key: value')

def test__assert_ns_equal__expected_dict():
    # Should not raise
    assert_ns_equal('key: value', dict(key='value'))

def test__assert_ns_equal__inner_values_differs():
    with pytest.raises(AssertionError) as exception:
        assert_ns_equal(
            'parent:\n'
            '  key1: mybad\n'
            '  key2: value2\n'
        ,
            'parent:\n'
            '  key2: value2\n'
            '  key1: value1\n'
        )
    assert (
        "    parent:\n"
        "  -   key1: mybad\n"
        "  +   key1: value1\n"
        "      key2: value2"
        if py2 else
        "    parent:\n"
        "  -   key1: value1\n"
        "  +   key1: mybad\n"
        "      key2: value2"
    ) in format(exception.value)

def test__assert_ns_equal__bothYaml():
    # Should not raise
    assert_ns_equal('key: same', 'key: same')

def test__assert_ns_equal__inverted_key_order():
    # Should not raise
    assert_ns_equal(
        'key1: value1\n'
        'key2: value2\n'
    ,
        'key2: value2\n'
        'key1: value1\n'
    )

def test__assert_ns_equal__inner_inverted_key_order():
    # Should not raise
    assert_ns_equal(
        'parent:\n'
        '  key1: value1\n'
        '  key2: value2\n'
    ,
        'parent:\n'
        '  key2: value2\n'
        '  key1: value1\n'
    )

def test__assert_ns_equal__common_indentation_ignored():
    # Should not raise
    assert_ns_equal("""
        parent:
          key1: value1
          key2: value2
    ""","""
        parent:
          key1: value1
          key2: value2
    """)

def test__assert_ns_equal__float_yaml():
    # Should not raise
    assert_ns_equal("1.2","1.2")

def test__assert_ns_equal__string_yaml():
    # Should not raise
    assert_ns_equal("text","text")

def test__assert_ns_contains__missing_key():
    with pytest.raises(AssertionError) as exception:
        assert_ns_contains(
            ns(common='common'),
            ns(common='common', missing='value'),
        )
    assert format(exception.value) == (
        "assert 'common: common\\n' == 'common: common\\nmissing: value\\n'\n"
        "    common: common\n"
        "  + missing: value"
        if py2 else
        "assert 'common: common\\n' == 'common: comm...sing: value\\n'\n  \n"
        "    common: common\n"
        "  - missing: value"
    )

def test__assert_ns_contains__differing_key():
    with pytest.raises(AssertionError) as exception:
        assert_ns_contains(
            ns(common='different'),
            ns(common='expected'),
        )
    print(repr(format(exception.value)))
    assert format(exception.value) == (
        "assert 'common: different\\n' == 'common: expected\\n'\n"
        "  - common: different\n"
        "  + common: expected"
        if py2 else
        "assert 'common: different\\n' == 'common: expected\\n'\n  \n"
        "  - common: expected\n"
        "  + common: different"
    )

def test__assert_ns_contains__key_missing_in_expectation_ignored():
    assert_ns_contains(
        ns(akey='value', ignored='value'),
        ns(akey='value'),
    )


