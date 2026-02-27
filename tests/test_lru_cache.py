# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-FileCopyrightText: Python Software Foundation
#
# SPDX-License-Identifier: MIT
# SPDX-License-Identifier: PSF-2.0

"""Tests for lru_cache."""

import pytest

from circuitpython_functools import lru_cache

# Factorial example adapted from CPython documentation

TOTAL_CALLS = 0


def test_lru_cache_default():
    """Tests the lru_cache works with default settings (no arguments provided)."""
    global TOTAL_CALLS  # noqa: PLW0603

    @lru_cache
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    _ = factorial(10)
    assert TOTAL_CALLS == 11  # noqa: PLR2004

    _ = factorial(5)
    assert TOTAL_CALLS == 11  # noqa: PLR2004

    _ = factorial(12)
    assert TOTAL_CALLS == 13  # noqa: PLR2004

    TOTAL_CALLS = 0


def test_lru_cache_maxsize_arg():
    """Tests the lru_cache maxsize function when given as arg."""
    global TOTAL_CALLS  # noqa: PLW0603

    @lru_cache(5)
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    _ = factorial(10)
    assert TOTAL_CALLS == 11  # noqa: PLR2004
    print("---")

    _ = factorial(5)
    assert TOTAL_CALLS == 17  # noqa: PLR2004
    print("---")

    _ = factorial(12)
    assert TOTAL_CALLS == 24  # noqa: PLR2004

    TOTAL_CALLS = 0


def test_lru_cache_maxsize_kwarg():
    """Tests the lru_cache maxsize function when given as kwarg."""
    global TOTAL_CALLS  # noqa: PLW0603

    @lru_cache(maxsize=5)
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    _ = factorial(10)
    assert TOTAL_CALLS == 11  # noqa: PLR2004
    print("---")

    _ = factorial(5)
    assert TOTAL_CALLS == 17  # noqa: PLR2004
    print("---")

    _ = factorial(12)
    assert TOTAL_CALLS == 24  # noqa: PLR2004

    TOTAL_CALLS = 0


def test_lru_cache_func_kwarg():
    """Tests the lru_cache when function has kwargs."""
    global TOTAL_CALLS  # noqa: PLW0603

    @lru_cache
    def factorial(*, n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n=n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    _ = factorial(n=10)
    assert TOTAL_CALLS == 11  # noqa: PLR2004

    _ = factorial(n=5)
    assert TOTAL_CALLS == 11  # noqa: PLR2004

    _ = factorial(n=12)
    assert TOTAL_CALLS == 13  # noqa: PLR2004

    TOTAL_CALLS = 0


def test_lru_cache_typed_error_args():
    """Tests that lru_cache raises an error if "typed" given as arg."""
    with pytest.raises(NotImplementedError):

        @lru_cache(100, True)
        def factorial(n):
            return n * factorial(n=n - 1) if n else 1


def test_lru_cache_typed_error_kwargs():
    """Tests that lru_cache raises an error if "typed" given as kwarg."""
    with pytest.raises(NotImplementedError):

        @lru_cache(typed=True)
        def factorial(n):
            return n * factorial(n=n - 1) if n else 1


def test_lru_cache_syntax_error():
    """Tests that lru_cache raises an error if arguments are incorrect."""
    with pytest.raises(SyntaxError):

        @lru_cache(100, True, "a")
        def factorial(n):
            return n * factorial(n=n - 1) if n else 1
