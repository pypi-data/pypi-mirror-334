"""Test the function get_state_file."""

import pytest

from piscada_foresight import http_piscada


def test_get_state_file() -> None:
    """Test retrieving the state file path.

    This test ensures that the state file path ends with the correct basename
    (/.test_state) and starts with a slash.
    """
    state_file = http_piscada._get_state_file("test")  # noqa: SLF001
    if not str(state_file).endswith("/.test_state"):
        pytest.fail("State file path does not end with '/.test_state'")
    if not str(state_file).startswith("/"):
        pytest.fail("State file path does not start with '/'")
