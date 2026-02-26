from circuitpython_functools import wraps

def square_args(func):
    @wraps(func)
    def wrapper(x, y):
        a = x ** 2
        b = y ** 2
        return func(a, b)
    return wrapper
        
def test_wraps_unchanged():
    @square_args
    def add2(aa, bb):
        return aa + bb
    
    assert add2(3, 4) == 25
