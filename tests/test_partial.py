from circuitpython_functools import partial

def test_partial():
    def towerize(x, y, z):
        return (x * 100) + (y * 10) + z

    towerize100 = partial(towerize, 1)
    assert towerize100(5, 3) == 153
    assert towerize100(z=2, y=7) == 172

    towerize150 = partial(towerize, 1, 5)
    assert towerize150(6) == 156
    assert towerize150(z=8) == 158

    towerize20 = partial(towerize, y=2)
    assert towerize20(9, z=0) == 920
    assert towerize20(z=1, x=5) == 521
