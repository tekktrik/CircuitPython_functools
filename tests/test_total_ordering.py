# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Tests for total_ordering."""

import pytest

from circuitpython_functools import total_ordering


class BaseClass:
    """Basic test base class."""

    def __init__(self, attr):
        """Initialize the instance."""
        self.attr = attr

    def __eq__(self, other):
        """Perform basic equal to operation."""
        if not isinstance(other, BaseClass):
            return False
        return self.attr == other.attr


class OtherClass:
    """A different class."""


parameters = []


@total_ordering
class UsesLT(BaseClass):
    """Basic class that implements less than."""

    def __lt__(self, other):
        """Perform basic less than operation."""
        if not isinstance(other, BaseClass):
            raise TypeError
        return self.attr < other.attr


parameters.append((UsesLT(1), UsesLT(1), UsesLT(2)))


@total_ordering
class UsesGT(BaseClass):
    """Basic class that implements greater than."""

    def __gt__(self, other):
        """Perform basic greater than operation."""
        if not isinstance(other, BaseClass):
            raise TypeError
        return self.attr > other.attr


parameters.append((UsesGT(1), UsesGT(1), UsesGT(2)))


@total_ordering
class UsesLE(BaseClass):
    """Basic class that implements less than or equal to."""

    def __le__(self, other):
        """Perform basic less than or equal to operation."""
        if not isinstance(other, BaseClass):
            raise TypeError
        return self.attr <= other.attr


parameters.append((UsesLE(1), UsesLE(1), UsesLE(2)))


@total_ordering
class UsesGE(BaseClass):
    """Basic class that implements greater than or equal to."""

    def __ge__(self, other):
        """Perform basic greater than or equal to operation."""
        if not isinstance(other, BaseClass):
            raise TypeError
        return self.attr >= other.attr


parameters.append((UsesGE(1), UsesGE(1), UsesGE(2)))


@pytest.mark.parametrize("x,y,z", parameters)
def test_comparisons(x, y, z):
    """Tests that comparisons are correct."""
    w = OtherClass()

    # lt
    assert not x < y
    assert x < z
    with pytest.raises(TypeError):
        x < w

    # gt
    assert not x > y
    assert z > x
    with pytest.raises(TypeError):
        x > w

    # le
    assert x <= y
    assert x <= z
    with pytest.raises(TypeError):
        x <= w

    # ge
    assert x >= y
    assert not x >= z
    with pytest.raises(TypeError):
        x >= w


def test_none_implemented():
    """Tests the not implementig compraison function results in an error."""
    with pytest.raises(ValueError):

        @total_ordering
        class NoneImplemented:
            """Class with nothing implemented."""
