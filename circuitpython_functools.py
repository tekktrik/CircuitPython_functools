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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_functools.git"

cache_record = []

class ObjectMark:
    pass
    
def _make_key(args, kwargs, kwd_mark = (ObjectMark(), )):
    key = tuple(args)
    if kwargs:
        key += kwd_mark
        for item in kwargs.items():
            key += tuple(item)
    return hash(key)

def cache(user_function):
    """Unbounded cache"""
    sentinel = object()
    cache_dict = {}
    cache_get = cache_dict.get
    
    def cache_wrapper(*args, **kwargs):
        key = _make_key(args, kwargs)
        #print("key: {}".format(key))
        #print("key hash: {}", hash(key))
        result = cache_get(key, sentinel)
        if result is not sentinel:
            print("result found")
            return result
        print("result not found")
        result = user_function(*args, **kwargs)
        cache_dict[key] = result
        return result

    cache_record.append(cache_dict)

    return cache_wrapper

def clear_caches():
    for cache_contents in cache_record:
        cache_contents.clear()
    gc.collect()
