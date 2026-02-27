# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for wraps."""

from circuitpython_functools import wraps


def square_args(func):
    """Square arguments before calling function."""

    @wraps(func)
    def wrapper(x, y):
        a = x**2
        b = y**2
        return func(a, b)

    return wrapper


def test_wraps():
    """Tests that x is x."""

    @square_args
    def add2(aa, bb):
        return aa + bb

    assert add2(3, 4) == 25  # noqa: PLR2004
