# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT
"""
`circuitpython_functools`
================================================================================

A CircuitPython implementation of CPython's functools library


* Author(s): Alec Delaney

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import gc
from collections import OrderedDict

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_functools.git"

cache_record = []

# pylint: disable=too-few-public-methods
class _ObjectMark:
    pass


def _make_key(args, kwargs, kwd_mark=(_ObjectMark(),)):
    key = tuple(args)
    if kwargs:
        key += kwd_mark
        for item in kwargs.items():
            key += tuple(item)
    return hash(key)


def lru_cache(maxsize):

    def cache(user_function):
        """Unbounded cache"""
        sentinel = object()
        cache_dict = OrderedDict()
        cache_get = cache_dict.get
        cache_size = maxsize

        def cache_wrapper(*args, **kwargs):
            key = _make_key(args, kwargs)
            result = cache_get(key, sentinel)
            if result is not sentinel:
                return result
            result = user_function(*args, **kwargs)
            local_cache_dict = cache_dict
            if cache_size is not None:
                if len(local_cache_dict) == cache_size:
                    base_list = []
                    index = 0
                    for cache_key, cache_value in cache_dict.values():
                        if index == 0:
                            continue
                        base_list.append((cache_key, cache_value))
                    new_cache_dict = OrderedDict(base_list)
                    index = 0
                    local_cache_dict = new_cache_dict
            local_cache_dict[key] = result
            gc.collect()
            return result

        cache_record.append(cache_dict)

        return cache_wrapper

    return cache


def clear_caches():
    """Clears all the caches"""
    for cache_contents in cache_record:
        cache_contents.clear()
    gc.collect()
