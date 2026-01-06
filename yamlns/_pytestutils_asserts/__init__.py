import pytest

# This ensures that the file is registered for assert rewriting
# before assert_impl is imported

pytest.register_assert_rewrite("yamlns._pytestutils_asserts.assert_impl")
from .assert_impl import assert_ns_equal
