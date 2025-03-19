import pytest

# import numpy as np
# import numpy.testing as npt
from tempfile import mkstemp
import os

import sadcompressor as sad

def test_constants(filename):
    c = sad.ContainerWriter(filename)
    assert 0 < c.lengthbits < 8
    assert 1 < c.minbytes
    c.close()

###########################################################################################################

@pytest.fixture
def filename():
    return mkstemp()[1]

def test_signature(filename):
    c = sad.ContainerWriter(filename)
    c.close()

    c = sad.ContainerReader(filename)
    c.close()

    os.remove(filename)

##########################################################################################################

def check_readwrite(filename, contents):
    with sad.ContainerWriter(filename) as c:
        for content in contents:
            c.write_raw([content])

    with sad.ContainerReader(filename) as c:
        positions = []
        for content in contents:
            positions.append(c.filepos())
            assert c.read_raw() == content
        assert c.read_raw() == None
        assert c.read_raw() == None

        prev = 0
        for p, content in zip(positions, contents):
            assert p>0 and p>prev 
            prev = p
            c.seek(p)
            assert c.read_raw() == content

    with sad.ContainerReader(filename) as c:
        for n, content in enumerate(contents):
            if n%2 == 0:
                assert c.read_raw() == content
            else: 
                assert c.read_raw(skip=True) == bytes()
        assert c.read_raw() == None
        assert c.read_raw() == None
    
    with sad.ContainerReader(filename) as c:
        for n, content in enumerate(contents):
            if n%2 == 1:
                assert c.read_raw() == content
            else: 
                assert c.read_raw(skip=True) == bytes()
        assert c.read_raw() == None
        assert c.read_raw() == None

    os.remove(filename)

    container = sad.PipeContainer()
    with container as c:
        for content in contents:
            c.write_raw([content])
        for content in contents:
            assert c.read_raw() == content
    assert container.read_raw() == None
    assert container.read_raw() == None

    container = sad.PipeContainer()
    with container as c:
        for content in contents:
            c.write_raw([content])
            assert c.read_raw() == content
    assert container.read_raw() == None
    assert container.read_raw() == None


    
def test_context(filename):
    check_readwrite(filename, [b'E2-E4', b'E3-E4'*100, b'E5-E4'*1000])


if __name__ == '__main__':
    pytest.main()
