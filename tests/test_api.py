"""
A small test scaffold to verify the public API surface.
"""

from datetime import timedelta

import pytest

import src.pypc_utils as pu


def test_imports_public_api():
    """
    Ensure the public API surface is importable
    """
    assert hasattr(pu, "RunMode")
    assert hasattr(pu, "format_timedelta")
    assert callable(pu.format_timedelta)


def test_run_mode_type():
    """
    Ensure instanciation
    """
    assert isinstance(pu.run_mode(), pu.RunMode)


@pytest.mark.parametrize(
    "td, expected_contains",
    [
        (timedelta(seconds=5), "5s"),
        (timedelta(seconds=65), "1m 5s"),
    ],
)
def test_format_timedelta(td, expected_contains):
    """
    Test the return typing
    """
    s = pu.format_timedelta(td)
    assert expected_contains in s
