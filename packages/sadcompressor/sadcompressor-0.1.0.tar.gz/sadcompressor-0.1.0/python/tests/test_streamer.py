import pytest
import numpy as np
import numpy.testing as npt

# import numpy as np
# import numpy.testing as npt
from tempfile import mkstemp
import os

import sadcompressor as sad


###########################################################################################################

@pytest.fixture
def filename():
    return mkstemp()[1]

##########################################################################################################

def check_readwrite(filename, framesx, framesy=None, dicts=None, nbits=20, maxexp=8):
    with sad.SADWriter(filename, prec_nbits=nbits, prec_maxexp=maxexp) as c:
        for t in range(len(framesx)):
            print('write', t)
            if t>0: c.next_key(1.0)
            if framesx[t] is not None:
                c['x']=framesx[t]
            if framesy is not None and framesy[t] is not None:
                c['y']=framesy[t]
            if dicts is not None and dicts[t] is not None:
                c['d']=dicts[t]

    def find_not_None(a):
        for x in reversed(a):
            if x is not None:
                return x
        return None

    def check(t, c):
        print('read', t)
        prec = 2**(1-nbits+maxexp)
        npt.assert_allclose(t, c.t)

        x=find_not_None(framesx[:t+1])
        frame = c['x']
        print(f"x {type(frame)=}")
        assert isinstance(frame, np.ndarray)
        assert np.linalg.norm((x-frame).flatten(), ord=np.inf)<=prec

        if framesy is not None:
            y=find_not_None(framesy[:t+1])
            frame = c['y']
            print(f"y {type(frame)=}")
            assert isinstance(frame, np.ndarray)
            assert np.linalg.norm((y-frame).flatten(), ord=np.inf)<=prec

        if dicts is not None:
            d=find_not_None(dicts[:t+1])
            frame = c['d']
            print(f"d {type(frame)=}")
            assert frame is None or isinstance(frame, dict)
            assert d == frame

    print("SADReader")
    with sad.SADReader(filename) as c:
        for t in range(len(framesx)):
            assert not c.next_key()
            check(t, c)
        assert c.next_key()
        assert c.next_key()

    print("SADRadnomReader direct")
    with sad.SADRandomReader(filename) as c:
        for t in range(len(framesx)):
            c.seek(t)
            assert c.key == t
            check(t, c)

    print("SADRadnomReader reversed")
    with sad.SADRandomReader(filename) as c:
        for t in reversed(range(len(framesx))):
            c.seek(t)
            assert c.key == t
            check(t, c)

    os.remove(filename)


def test_constant_1(filename):
    a = np.random.randn(10,11,3)
    check_readwrite(filename, [a, a, a])

def test_random_1(filename):
    shp = (10,11)
    check_readwrite(filename, [np.random.randn(*shp) for _ in range(2)])


def test_constant(filename, nframes=10):
    a = np.random.randn(10,11,3)
    b = np.random.randn(32,13)
    check_readwrite(filename, framesx=[a]*nframes, framesy=[b]*nframes)

def test_random(filename, nframes=5):
    shpx = (10,11)
    shpy = (13,17,9)
    check_readwrite(filename,
        framesx = [np.random.randn(*shpx) for _ in range(nframes)],
        framesy = [np.random.randn(*shpy) for _ in range(nframes)],   
        )

def test_interleave(filename, nframes=12):
    assert nframes%6 == 0
    shpx = (10,11)
    shpy = (13,17,9)
    check_readwrite(filename,
        framesx = [np.random.randn(*shpx), None, None]*(nframes//3),
        framesy = [np.random.randn(*shpy), None]*(nframes//2)   
        )

def test_dict(filename):
    a = np.random.randn(3)
    check_readwrite(filename,
        framesx = [a]*7,
        dicts = [None, {'x':1}, None, {'x':1,'y':2}, None, {'y':2}, {}]
    )


##########################################################################################################


if __name__ == '__main__':
    pytest.main()
