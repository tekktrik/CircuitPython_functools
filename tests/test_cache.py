from circuitpython_functools import cache

# Example adapted from CPython documentation

TOTAL_CALLS = 0

def test_cache():

    @cache
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
