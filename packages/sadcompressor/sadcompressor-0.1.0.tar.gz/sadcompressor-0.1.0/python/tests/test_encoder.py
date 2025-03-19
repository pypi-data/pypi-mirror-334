import pytest

import sadcompressor as sad

def check_uint(number, minbytes, lengthbits, encoded):
    assert sad.encoder.encode_uint(number, minbytes, lengthbits) == encoded
    assert sad.encoder.decode_uint(encoded, minbytes, lengthbits) == (number, b'')

def test_encode_decode_uint():
    check_uint(0x13, 1, 0, b'\x13')
    check_uint(0xf3, 1, 0, b'\xf3')
    check_uint(0xf3, 1, 1, b'\x80\xf3')
    check_uint(0x1356, 2, 0, b'\x13\x56')
    check_uint(0x13, 2, 0, b'\x00\x13')
    check_uint(0x13, 0, 1, b'\x93')
    check_uint(0x13, 0, 2, b'\x53')
    check_uint(0x1356, 0, 2, b'\x93\x56')
    check_uint(0x13, 1, 1, b'\x13')
    check_uint(0x1356, 1, 1, b'\x93\x56')
    check_uint(0x1356, 1, 2, b'\x53\x56')
    check_uint(0x13, 1, 2, b'\x13')
    check_uint(0x5, 2, 3, b'\x00\x05')

def test_encode_uint():
    with pytest.raises(OverflowError):
        sad.encoder.encode_uint(-1, 1, 0)

    with pytest.raises(OverflowError):
        sad.encoder.encode_uint(0xf3, 0, 1)

def test_decode_uint():
    with pytest.raises(OverflowError):
        sad.encoder.decode_uint(b'\x80', 1, 1)

    assert sad.encoder.decode_uint(b'\x00\x05\xff', 2, 3) == (0x05, b'\xff')


def test_length_uint():
    assert sad.encoder.maxbytes_uint(1, 1) == 2
    assert sad.encoder.maxbytes_uint(1, 2) == 4

if __name__ == '__main__':
    pytest.main()
