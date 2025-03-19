import pytest
import numpy as np

# import numpy as np
# import numpy.testing as npt
from tempfile import mkstemp
import os

import sadcompressor as sad


# def setup_module(module):
#     sad.register_frameclasses()


###########################################################################################################

@pytest.fixture
def filename():
    return mkstemp()[1]

##########################################################################################################

# def test_bitfixes():
#     assert sad.find_bitfixes(np.array(0b00010100, dtype=np.uint8)) == (3, 2, 8)
#     assert sad.find_bitfixes(np.array(0b11111100, dtype=np.uint8)) == (0, 2, 8)
#     assert sad.find_bitfixes(np.array(0b01111111, dtype=np.uint8)) == (1, 0, 8)
#     assert sad.find_bitfixes(np.array(0b0001010110111010, dtype=np.uint16)) == (3, 1, 16)



##########################################################################################################

def check_readwrite(filename, frames, test=lambda a,b: a.content==b.content):
    with sad.PipeContainer() as c:
        for frame in frames:
            assert isinstance(frame, sad.TypedFrame) 
            c.write(frame)
            frame2 = c.read()
            assert frame.__class__ == frame2.__class__
            assert test(frame, frame2)


    with sad.ContainerWriter(filename) as c:
        for frame in frames:
            assert isinstance(frame, sad.TypedFrame) 
            c.write(frame)

    with sad.ContainerReader(filename) as c:
        for frame in frames:
            frame2 = c.read()
            assert frame.__class__ == frame2.__class__
            assert test(frame, frame2)
        assert c.read() == None

    os.remove(filename)


def test_timedelta(filename):
    check_readwrite(filename, [
        sad.TimeDeltaFrame(3.14),
        sad.TimeDeltaFrame(2.71),
    ], test=lambda a,b: abs(1-b.content/a.content)<1e-7)


def test_string(filename):
    check_readwrite(filename, [
        sad.StringFrame("Hi there!"),    
    ])


def test_ubjson(filename):
    check_readwrite(filename, [
        sad.UBJSONFrame(["Hi there!", 23]),  
        sad.UBJSONFrame({"name": "Dick"}),  
    ])

def test_ndarray(filename):
    check_readwrite(filename, [
        sad.ArrayFrame(content=np.random.randn(3)),  
        sad.ArrayFrame(content=np.random.randn(10)),  
    ], test=lambda a,b: np.linalg.norm(a.content-b.content)<1e-6)

def test_qarray(filename, nbits=6):
    check_readwrite(filename, [
        sad.QuantizedArrayFrame(content=np.ones(13), nbits=nbits, maxexp=0),  
        sad.QuantizedArrayFrame(content=-np.ones(12), nbits=nbits, maxexp=0),  
        sad.QuantizedArrayFrame(content=np.random.rand(13), nbits=nbits, maxexp=0),  
    ], test=lambda a,b: np.linalg.norm(a.content-b.content, ord=np.inf) <= 2**(-nbits) )

def check_qarray2(filename, nbits):
    def chk(a,b):
        e = np.linalg.norm(a.content-b.content, ord=np.inf) 
        t = 2**(1-nbits)
        return e <= t
    check_readwrite(filename, [
        sad.QuantizedArrayFrame2(content=np.ones(13), nbits=nbits, maxexp=0),  
        sad.QuantizedArrayFrame2(content=-np.ones(12), nbits=nbits, maxexp=0),  
        sad.QuantizedArrayFrame2(content=2*np.random.rand(18)-1, nbits=nbits, maxexp=0),  
    ], test=chk )

def test_qarray2(filename):
    assert sad.QuantizedArrayFrame2.nbytes(nbits=8)==1
    check_qarray2(filename, nbits=3)
    check_qarray2(filename, nbits=8)



def check_qarray3(filename, nbits):
    def chk(a,b):
        e = np.linalg.norm(a.content-b.content, ord=np.inf) 
        t = 2**(1-nbits)
        return e <= t
    check_readwrite(filename, [
        # sad.QuantizedArrayFrame3(content=np.ones(13), nbits=nbits, maxexp=0),  
        # sad.QuantizedArrayFrame3(content=-np.ones(12), nbits=nbits, maxexp=0),  
        sad.QuantizedArrayFrame3(content=np.zeros(9), nbits=nbits, maxexp=0),  
        # sad.QuantizedArrayFrame3(content=np.random.uniform(-1, 1, size=18), nbits=nbits, maxexp=0),  
    ], test=chk )

def test_qarray3(filename):
    assert sad.QuantizedArrayFrame3.nbytes(nbits=8)==1
    check_qarray3(filename, nbits=3)
    check_qarray3(filename, nbits=8)



if __name__ == '__main__':
    pytest.main()
