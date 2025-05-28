# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: Unlicense

"""Example usage of the circuitpython_functools module."""

from circuitpython_functools import cache


@cache
def add(a, b, *, c=1, d=2):
    """Perform addition."""
    return a + b + c + d


@cache
def subtract(first_value, second_value):
    """Perform subtraction."""
    return first_value - second_value


print(add(1, 1, c=2, d=3))
print(add(1, 1, c=2, d=3))  # Repeat call, will use cached result
print(add(1, 0, c=3, d=4))
print(subtract(42, 20))
print(add(1, b=1, c=2, d=3))
print(add(1, b=0, c=2, d=3))

# Clear all the caches so we don't use too much memory
add.cache_clear()
subtract.cache_clear()

print(add(1, 0, c=3, d=4))  # Cache was cleared, so this is caclulated again
print(subtract(18, 4))
