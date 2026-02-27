# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-FileCopyrightText: Python Software Foundation

# SPDX-License-Identifier: MIT
# SPDX-License-Identifier: PSF-2.0

"""Tests for cache."""

from circuitpython_functools import cache

# Example adapted from CPython documentation

TOTAL_CALLS = 0


def test_cache():
    """Tests that cache decorator works as expected."""

    @cache
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
