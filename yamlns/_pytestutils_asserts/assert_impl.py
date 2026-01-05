# DO NOT IMPORT THIS FILE DIRECTLY FROM pytestutils
# IT WOULD BREAK pytest ASSERT REWRITE

def _ensure_pytest_assert_rewrite_active(): # pragma: no cover
    spec = globals().get("__spec__")
    loader = getattr(spec, "loader", None)

    if loader and loader.__class__.__name__ == "AssertionRewritingHook":
        # Using rewrite loader -> good
        return

    msg = [
        "assert_ns_equal was imported without pytest assert rewriting.",
        "",
        "Import it from yamlns.pytestutils",
        "",
    ]

    raise RuntimeError("\n".join(msg))


_ensure_pytest_assert_rewrite_active()


from ..testutils import (
    _parse_normalize_and_dump,
)

def assert_ns_equal(data, expectation):
    """
    Assert that data representation in yaml matches the expectation.
    Both ends can be either a dictionary like object or a yaml string.
    """
    assert _parse_normalize_and_dump(data) == _parse_normalize_and_dump(expectation)


