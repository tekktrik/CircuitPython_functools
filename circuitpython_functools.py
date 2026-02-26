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
from collections import OrderedDict

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_functools.git"

_cache_records = {}
_lru_cache_records = {}


class _ObjectMark:
    pass


# Cache-related code ported from CPython

# As a general note, some weird things are happening here due to internal differences between
# CPython and CircuitPython, such as the fact that closures can't have things added to them,
# hence the need to create objects so that cache_clear can be called from the returned "wrapped"
# functions.


def _make_key(args, kwargs, kwd_mark=(_ObjectMark(),)):
    """Make a key for the cache records."""
    key = tuple(args)
    if kwargs:
        key += kwd_mark
        for item in kwargs.items():
            key += tuple(item)
    return hash(key)


class _CachedFunc:
    """Wrapped unbounded cache function."""

    def __init__(self, maxsize, user_func):
        """Initialize the wrapped cache function."""
        self._maxsize = maxsize
        checked_records = _cache_records if maxsize < 0 else _lru_cache_records

        def cache_wrapper(*args, **kwargs):
            sentinel = object()

            # Make the key for the inner dictionary
            key = _make_key(args, kwargs)

            # if there is no inner dictionary yet, make one
            if checked_records.get(user_func) is None:
                checked_records[user_func] = OrderedDict()

            # Attempt to get an existing entry, updating its location in the queue
            # and returning it if so
            result = checked_records[user_func].get(key, sentinel)
            if result is not sentinel:
                checked_records[user_func].move_to_end(key)
                return result

            # Calculate the actual value
            result = user_func(*args, **kwargs)

            # If the cache is bounded and too full to store the new result, eject the
            # least-recently-use entry
            if maxsize >= 0 and len(checked_records[user_func]) >= maxsize:
                first_key = next(iter(checked_records[user_func]))
                del checked_records[user_func][first_key]

            # Store the result
            checked_records[user_func][key] = result

            # Return the new result
            return result

        self._user_func = user_func
        self._wrapped_func = cache_wrapper

    def __call__(self, *args, **kwargs):
        """Call the wrapped function."""
        return self._wrapped_func(*args, **kwargs)

    def cache_clear(self):
        """Clear the cache."""
        checked_records = _cache_records if self._maxsize < 0 else _lru_cache_records
        if self._user_func in checked_records:
            checked_records[self._user_func].clear()
            gc.collect()


def cache(user_function):
    """Create an unbounded cache."""
    return _CachedFunc(-1, user_function)


def lru_cache(*args, **kwargs):
    """Create a bounded cache which ejects the least recently used entry."""
    cpython_max_args = 2
    if len(args) == cpython_max_args or "typed" in kwargs:
        raise NotImplementedError("Using typed is not supported")

    if len(args) == 1 and isinstance(args[0], int):
        maxsize = args[0]
    elif len(args) == 1 and str(type(args[0]) == "<class 'function'>"):
        return _CachedFunc(128, args[0])
    elif "maxsize" in kwargs:
        maxsize = kwargs["maxsize"]
    else:
        raise SyntaxError("lru_cache syntax incorrect")

    return partial(_CachedFunc, maxsize)


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
def wraps(wrapped, assigned=None, updated=None):
    """Define a wrapper function when writing function decorators."""
    def decorator(wrapper):
        return wrapper
    return decorator

