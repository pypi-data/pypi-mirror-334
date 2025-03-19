from sadcompressor._rusted import encode_uint, decode_uint, maxbytes_uint

# def maxbytes_uint(minbytes: int, lengthbits: int) -> int:
#     return minbytes + ( 1 << lengthbits ) - 1

# def encode_uint(number: int, minbytes: int, lengthbits: int) -> bytes:
#     """
#     Encode unsigned integer. 

#     Args:
#         number (int): integer to encode
#         minbytes (int): least number of bytes used by encoded number
#         lengthbits (int): number of bits to store length of the integer

#     Raises:
#         OverflowError: if number is negative or very large.

#     Returns:
#         bytes: encoded integer
#     """
#     b = number.to_bytes( (1<<lengthbits)+minbytes-1 , "big")
#     length = max(minbytes, len(b.lstrip(b'\0x00')))
#     idx = len(b)-length
#     if b[idx] >= ( 1 << (8-lengthbits) ): 
#         length += 1
#         idx -= 1
#     if idx<0: raise OverflowError
#     encoded_length = (length-minbytes) << (8-lengthbits) 
#     length_as_bytes = ( encoded_length+b[idx] ).to_bytes(1, "big")
#     return length_as_bytes+b[idx+1:]

# def decode_uint(data: bytes, minbytes: int, lengthbits: int) -> (int, bytes):
#     """
#     Decode unsigned integer encoded with `encode_uint`.

#     Args:
#         data (bytes): output of encode_uint concatenated with arbitrary data. Encoded integer must be prefix of the data.
#         minbytes (int), lengthbits (int): see `encode_uint`

#     Raises:
#         OverflowError: if `data` is shorter than expected integer length.

#     Result:
#         number (int): decoded integer
#         length (int): number of bytes consumed by the decoder from `data`
#     """
#     length = ( data[0] >> (8-lengthbits) ) + minbytes
#     if len(data)<length:
#         raise OverflowError
#     ba = bytearray(data[:length])
#     ba[0] = ba[0] & ( (1<<(8-lengthbits)) - 1)
#     number = int.from_bytes(ba, 'big')
#     return (number, data[length:])