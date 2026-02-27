# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-FileCopyrightText: Python Software Foundation
#
# SPDX-License-Identifier: MIT
# SPDX-License-Identifier: PSF-2.0

"""Tests for cache_clear method."""

from circuitpython_functools import cache, lru_cache

# Factorial example adapted from CPython documentation

TOTAL_CALLS = 0


def test_cache_cache_clear():
    """Tests the automatically attached cache_clear method works."""
    global TOTAL_CALLS  # noqa: PLW0603

    @cache
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n=n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    _ = factorial(n=10)
    assert TOTAL_CALLS == 11  # noqa: PLR2004

    factorial.cache_clear()

    _ = factorial(n=10)
    assert TOTAL_CALLS == 22  # noqa: PLR2004

    factorial.cache_clear()

    TOTAL_CALLS = 0


def test_cache_cache_clear_empty():
    """Tests the automatically attached cache_clear method works."""
    global TOTAL_CALLS  # noqa: PLW0603

    @cache
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n=n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    factorial.cache_clear()

    assert TOTAL_CALLS == 0

    TOTAL_CALLS = 0


def test_lru_cache_cache_clear():
    """Tests the automatically attached cache_clear method works."""
    global TOTAL_CALLS  # noqa: PLW0603

    @lru_cache
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n=n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    _ = factorial(n=10)
    assert TOTAL_CALLS == 11  # noqa: PLR2004

    factorial.cache_clear()

    _ = factorial(n=10)
    assert TOTAL_CALLS == 22  # noqa: PLR2004

    factorial.cache_clear()

    TOTAL_CALLS = 0


def test_lru_cache_cache_clear_empty():
    """Tests the automatically attached cache_clear method works."""
    global TOTAL_CALLS  # noqa: PLW0603

    @lru_cache
    def factorial(n):
        global TOTAL_CALLS  # noqa: PLW0603
        TOTAL_CALLS += 1
        return n * factorial(n=n - 1) if n else 1

    assert TOTAL_CALLS == 0  # noqa: PLR2004

    factorial.cache_clear()

    assert TOTAL_CALLS == 0

    TOTAL_CALLS = 0
