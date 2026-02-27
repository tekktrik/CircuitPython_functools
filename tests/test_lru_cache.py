import pytest

from circuitpython_functools import lru_cache, _lru_cache_records

# Example adapted from CPython documentation

TOTAL_CALLS = 0

def test_lru_cache():

    global TOTAL_CALLS

    @lru_cache
    def factorial(n):
        global TOTAL_CALLS
        TOTAL_CALLS += 1
        return n * factorial(n-1) if n else 1
    
    assert TOTAL_CALLS == 0

    _ = factorial(10)
    assert TOTAL_CALLS == 11

    _ = factorial(5)
    assert TOTAL_CALLS == 11

    _ = factorial(12)
    assert TOTAL_CALLS == 13

    TOTAL_CALLS = 0


def test_lru_cache_default():

    global TOTAL_CALLS

    @lru_cache
    def factorial(n):
        global TOTAL_CALLS
        TOTAL_CALLS += 1
        return n * factorial(n-1) if n else 1
    
    assert TOTAL_CALLS == 0

    _ = factorial(10)
    assert TOTAL_CALLS == 11

    _ = factorial(5)
    assert TOTAL_CALLS == 11

    _ = factorial(12)
    assert TOTAL_CALLS == 13

    TOTAL_CALLS = 0


def test_lru_cache_maxsize_arg():

    global TOTAL_CALLS

    @lru_cache(5)
    def factorial(n):
        global TOTAL_CALLS
        TOTAL_CALLS += 1
        return n * factorial(n-1) if n else 1
    
    assert TOTAL_CALLS == 0

    _ = factorial(10)
    assert TOTAL_CALLS == 11
    print("---")

    _ = factorial(5)
    assert TOTAL_CALLS == 17
    print("---")

    _ = factorial(12)
    assert TOTAL_CALLS == 24

    TOTAL_CALLS = 0


def test_lru_cache_maxsize_kwarg():

    global TOTAL_CALLS

    @lru_cache(maxsize=5)
    def factorial(n):
        global TOTAL_CALLS
        TOTAL_CALLS += 1
        return n * factorial(n-1) if n else 1
    
    assert TOTAL_CALLS == 0

    _ = factorial(10)
    assert TOTAL_CALLS == 11
    print("---")

    _ = factorial(5)
    assert TOTAL_CALLS == 17
    print("---")

    _ = factorial(12)
    assert TOTAL_CALLS == 24

    TOTAL_CALLS = 0


def test_lru_cache_func_kwarg():

    global TOTAL_CALLS

    @lru_cache
    def factorial(*, n):
        global TOTAL_CALLS
        TOTAL_CALLS += 1
        return n * factorial(n=n-1) if n else 1
    
    assert TOTAL_CALLS == 0

    _ = factorial(n=10)
    assert TOTAL_CALLS == 11

    _ = factorial(n=5)
    assert TOTAL_CALLS == 11

    _ = factorial(n=12)
    assert TOTAL_CALLS == 13

    TOTAL_CALLS = 0


def test_lru_cache_cache_clear():

    global TOTAL_CALLS

    @lru_cache
    def factorial(n):
        global TOTAL_CALLS
        TOTAL_CALLS += 1
        return n * factorial(n=n-1) if n else 1
    
    assert TOTAL_CALLS == 0

    _ = factorial(n=10)
    assert TOTAL_CALLS == 11

    factorial.cache_clear()

    _ = factorial(n=10)
    assert TOTAL_CALLS == 22

    TOTAL_CALLS = 0


def test_lru_cache_typed_error_args():

    with pytest.raises(NotImplementedError):
        @lru_cache(100, True)
        def factorial(n):
            return n * factorial(n=n-1) if n else 1
        

def test_lru_cache_typed_error_kwargs():

    with pytest.raises(NotImplementedError):
        @lru_cache(typed=True)
        def factorial(n):
            return n * factorial(n=n-1) if n else 1


def test_lru_cache_syntax_error():

    with pytest.raises(SyntaxError):
        @lru_cache(100, True, "a")
        def factorial(n):
            return n * factorial(n=n-1) if n else 1
