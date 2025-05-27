# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
# SPDX-FileCopyrightText: Python Software Foundation
# SPDX-FileCopyrightText: MicroPython Developers
#
# SPDX-License-Identifier: MIT
# SPDX-License-Identifier: PSF-2.0

"""CircuitPython implementation of CPython's functools library.

* Author(s): Alec Delaney

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import gc

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_functools.git"

cache_records = {}


# pylint: disable=too-few-public-methods
class _ObjectMark:
    pass


# Cache-related code ported from CPython


def _make_key(args, kwargs, kwd_mark=(_ObjectMark(),)):
    """Make a key for the cache records."""
    key = tuple(args)
    if kwargs:
        key += kwd_mark
        for item in kwargs.items():
            key += tuple(item)
    return hash(key)


def _clear_cache(user_function):
    """Clear a specific cache."""
    if user_function in cache_records:
        cache_records[user_function].clear()
        gc.collect()


def cache(user_function):
    """Create an unbounded cache."""
    sentinel = object()
    func_key = user_function

    def cache_wrapper(*args, **kwargs):
        key = _make_key(args, kwargs)
        if cache_records.get(func_key) is None:
            cache_records[func_key] = {}
        result = cache_records[func_key].get(key, sentinel)
        if result is not sentinel:
            return result
        result = user_function(*args, **kwargs)
        cache_records[func_key][key] = result
        return result

    cache_wrapper.clear_cache = partial(_clear_cache, user_function)

    return cache_wrapper


# Partial ported from the MicroPython library
def partial(func, *args, **kwargs):
    """Create a partial of the function."""

    def _partial(*more_args, **more_kwargs):
        local_kwargs = kwargs.copy()
        local_kwargs.update(more_kwargs)
        return func(*(args + more_args), **local_kwargs)

    return _partial


# Thank you to the MicroPython Development team for
# their simplified implementation of the wraps function!
# pylint: disable=unused-argument
def wraps(wrapped, assigned=None, updated=None):
    """Define a wrapper function when writing function decorators."""
    return wrapped
