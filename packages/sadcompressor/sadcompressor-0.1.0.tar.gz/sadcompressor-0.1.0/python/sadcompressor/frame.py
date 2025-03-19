import ubjson
import struct
import numpy as np
import zlib
import sys, inspect


# from .encoder import encode_uint, decode_uint
from sadcompressor._rusted import round_nbits


#######################################################################################################################
class FrameFactory:
    minbytes = 1 
    lengthbits = 2
    frameClasses = {} # List of all known children of the class

    def __init__(self):
        if len(self.frameClasses)>0: return
        self.register_frameclasses()

    @classmethod
    def append_type(cls, frameClass):
        if not issubclass(frameClass, TypedFrame):
            raise TypeError("Frame class must be children of TypedFrame")
        typeid = frameClass.typeid
        if typeid is None:
            raise KeyError(f"Typeid is not defined for {frameClass}.")
        if typeid in cls.frameClasses:
            raise KeyError(f"{frameClass} and {cls.frameClasses[typeid]} has the same typeid {typeid}")
        cls.frameClasses[typeid] = frameClass

    @classmethod
    def register_frameclasses(cls, verbose=True):
        if verbose:
            print("Default frame types:")
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            # print(name, obj, inspect.isclass(obj), issubclass(obj, TypedFrame))
            if inspect.isclass(obj) and issubclass(obj, TypedFrame) and obj.typeid is not None:
                if verbose:
                    print(f"    {obj.typeid}: {name}")
                FrameFactory.append_type(obj)


#######################################################################################################################

class TypedFrame:
    typeid = None

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @property
    def metadata(self):
        return {}

    @classmethod
    def from_bytes(cls, data: bytes):
        raise NotImplementedError

    def to_bytes(self) -> [bytes]:
        raise NotImplementedError


###################################################################################################################

# class NamedFrame(TypedFrame):
#     name_minbytes = 1 
#     name_lengthbits = 2
    
#     @classmethod
#     def extract_name(cls, data:bytes) -> (int, bytes):
#         name, data = decode_uint(data, minbytes=cls.name_minbytes, lengthbits=cls.name_lengthbits)
#         return name, data

#     @classmethod 
#     def encode_name(cls, name: int) -> bytes:
#         return encode_uint(name, minbytes=cls.name_minbytes, lengthbits=cls.name_lengthbits)

###################################################################################################################

class TimeDeltaFrame(TypedFrame):
    typeid = 0
    FORMAT = '<f'
    FORMAT_SIZE = struct.calcsize(FORMAT)

    def __init__(self, content: float):
        self.content = content

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content}"

    @classmethod
    def from_bytes(cls, data: bytes):
        s = struct.unpack(cls.FORMAT, data[:cls.FORMAT_SIZE])
        return TimeDeltaFrame( content = s[0] )

    def to_bytes(self) -> [bytes]:
        return [struct.pack( self.FORMAT, self.content )]

###################################################################################################################
class StringFrame(TypedFrame):
    typeid = 1
    ENCODING = 'utf-8'

    def __init__(self, content: str):
        self.content = content

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content}"

    @classmethod
    def from_bytes(cls, data: bytes):
        return StringFrame(content=data.decode(cls.ENCODING))

    def to_bytes(self) -> [bytes]:
        return [self.content.encode(self.ENCODING)]

###################################################################################################################
class UBJSONFrame(TypedFrame):
    typeid = 2

    def __init__(self, content: dict):
        self.content = content

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content}"

    @classmethod
    def from_bytes(cls, data: bytes):
        return UBJSONFrame( content = ubjson.loadb(data) )

    def to_bytes(self) -> [bytes]:
        return [ubjson.dumpb( self.content )]




#################################################################################################################

class ArrayFrame(TypedFrame):
    typeid = 3
    
    def __init__(self, content: np.ndarray):
        self.content = content

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content.dtype.str} {self.content.shape}"

    @classmethod
    def from_bytes(cls, data: bytes):
        ctype, data = chr(data[0]), data[1:]
        dtype = np.dtype(ctype)
        array = np.frombuffer(data, dtype=dtype)
        return ArrayFrame(content=array)

    def to_bytes(self) -> [bytes]:
        btype = self.content.dtype.char.encode()
        assert len(btype)==1
        barray = self.content.tobytes()
        return [btype, barray]


#################################################################################################################

class QuantizedArrayFrame(TypedFrame):
    typeid = 4

    DTYPE = ['b','b','h','i','i','l','l','l','l']

    def __init__(self, content: np.ndarray, nbits: int, maxexp: int):
        self.content = content
        self.nbits = nbits
        self.maxexp = maxexp

    @property
    def metadata(self):
        return {
            'nbits': self.nbits,
            'maxexp': self.maxexp,
            }

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content.dtype.str} {self.content.shape} nbits={self.nbits} maxexp={self.maxexp}"

    @property
    def nbytes(self):
        return self.nbits//8 + 1

    @staticmethod
    def scale(nbits: int, maxexp: int) -> float:
        return 2**(nbits-maxexp)

    def to_int(self):
        dtype = np.dtype(self.DTYPE[self.nbytes])
        return (self.content*self.scale(nbits=self.nbits, maxexp=self.maxexp)).astype(dtype)

    @classmethod
    def from_int(cls, data: np.ndarray, nbits: int, maxexp: int) -> np.ndarray:
        # dtype = np.float16 if nbits<10 else np.float32 if nbits<23 else np.float64 if nbits<52 else np.float128
        dtype = np.float32 if nbits<23 else np.float64 if nbits<52 else np.float128 # No float16
        return data.astype(dtype)/cls.scale(nbits=nbits, maxexp=maxexp)

    def to_bytes(self) -> [bytes]:
        bnbits = self.nbits.to_bytes(1, byteorder='big')
        bmaxexp = self.maxexp.to_bytes(1, byteorder='big', signed=True)
        data = self.to_int()
        btype = data.dtype.char.encode()
        assert len(btype)==1
        barray = data.tobytes()
        compressed = zlib.compress(barray)
        return [bnbits, bmaxexp, btype, compressed]

    @classmethod
    def from_bytes(cls, data: bytes):
        nbits, data = data[0], data[1:]
        maxexp, data = int.from_bytes(data[:1], byteorder='big', signed=True), data[1:]
        ctype, data = chr(data[0]), data[1:]
        dtype = np.dtype(ctype)
        barray = zlib.decompress(data)
        array = np.frombuffer(barray, dtype=dtype)
        content = cls.from_int(array, nbits=nbits, maxexp=maxexp) 
        return QuantizedArrayFrame(content=content, nbits=nbits, maxexp=maxexp)

#################################################################################################################

class QuantizedArrayFrame2(TypedFrame):
    typeid = 6

    DTYPE = ['b','b','h','i','i','l','l','l','l']

    def __init__(self, content: np.ndarray, nbits: int, maxexp: int):
        self.content = content
        self.nbits = nbits
        self.maxexp = maxexp

    @property
    def metadata(self):
        return {
            'nbits': self.nbits,
            'maxexp': self.maxexp,
            }

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content.dtype.str} {self.content.shape} nbits={self.nbits} maxexp={self.maxexp}"

    @staticmethod
    def nbytes(nbits):
        return (nbits-1)//8 + 1

    @staticmethod
    def scale(nbits: int, maxexp: int):
        return 2**(nbits-maxexp-1)

    def to_int(self):
        dtype = np.dtype(self.DTYPE[QuantizedArrayFrame2.nbytes(self.nbits)])
        s = self.scale(nbits=self.nbits, maxexp=self.maxexp)
        data = np.round(self.content*s)
        # print(f"{np.min(data)=} {np.max(data)=} ")
        info = np.iinfo(dtype)
        np.clip(data, info.min, info.max, out=data)
        data = data.astype(dtype)
        return data

    @classmethod
    def from_int(cls, data: np.ndarray, nbits: int, maxexp: int) -> np.ndarray:
        # dtype = np.float16 if nbits<10 else np.float32 if nbits<23 else np.float64 if nbits<52 else np.float128
        dtype = np.float32 if nbits<23 else np.float64 if nbits<52 else np.float128 # No float16
        return data.astype(dtype)/cls.scale(nbits=nbits, maxexp=maxexp)


    def to_bytes(self) -> [bytes]:
        data = self.to_int()
        bnbits = self.nbits.to_bytes(1, byteorder='big')
        bmaxexp = self.maxexp.to_bytes(1, byteorder='big', signed=True)
        btype = data.dtype.char.encode()
        assert len(btype)==1
        barray = data.tobytes()
        compressed = zlib.compress(barray)
        return [bnbits, bmaxexp, btype, compressed]

    @classmethod
    def from_bytes(cls, data: bytes):
        nbits, data = data[0], data[1:]
        maxexp, data = int.from_bytes(data[:1], byteorder='big', signed=True), data[1:]
        ctype, data = chr(data[0]), data[1:]
        dtype = np.dtype(ctype)

        barray = zlib.decompress(data)
        array = np.frombuffer(barray, dtype=dtype)
        content = cls.from_int(array, nbits=nbits, maxexp=maxexp) 
        return QuantizedArrayFrame2(content=content, nbits=nbits, maxexp=maxexp)

###################################################################################################################

# def round_nbits(nbits):
#     assert nbits>=0
#     if nbits<=1: return 1
#     elif nbits<=2: return 2
#     elif nbits<=4: return 4
#     elif nbits<=8: return 8
#     else: return nbits

def pack_bits(data, nbits):
    # return data, 0
    if nbits>=8: return data, 0
    assert 8%nbits==0
    packet_size = 8//nbits
    data = data.flatten()
    sz = int(np.ceil(data.size/packet_size))
    mask = (1<<nbits) - 1
    result = np.zeros(sz, dtype=np.uint8)
    for n in range(packet_size):
        d = data[n::packet_size]
        result[:len(d)] |= (d&mask)<<(n*nbits)
    ncut = sz*packet_size - data.size
    return result, ncut

def unpack_bits(data, nbits, ncut):
    # return data
    if nbits>=8: return data    
    packet_size = 8//nbits
    mask = (1<<nbits) - 1
    data = data.flatten()
    result = np.zeros(data.size*packet_size, dtype=np.uint8)
    for n in range(packet_size):
        result[n::packet_size] = (data>>(n*nbits))&mask 
    return result if ncut<=0 else result[:-ncut]

def find_bitfixes(data):
    msk = np.bitwise_or.reduce(data.flatten())
    bitspervalue = data.dtype.itemsize*8
    nsufix = 0
    for n in range(bitspervalue):
        if (1<<n)&msk: break
        else: nsufix+=1
    nprefix = 0
    for n in range(bitspervalue):
        if (1<<(bitspervalue-n-1))&msk: break
        else: nprefix+=1
    return nprefix, nsufix, bitspervalue


class QuantizedArrayFrame3(TypedFrame):
    typeid = 7

    DTYPE = ['B','B','H','I','I','L','L','L','L']

    def __init__(self, content: np.ndarray, nbits: int, maxexp: int):
        self.content = content
        self.nbits = nbits
        self.maxexp = maxexp

    @property
    def metadata(self):
        return {
            'nbits': self.nbits,
            'maxexp': self.maxexp,
            }

    def __repr__(self):
        return f"{self.__class__.__name__} {self.content.dtype.str} {self.content.shape} nbits={self.nbits} maxexp={self.maxexp}"

    @staticmethod
    def nbytes(nbits):
        return (nbits-1)//8 + 1

    @staticmethod
    def scale(nbits: int, maxexp: int):
        return 2**(nbits-maxexp-1)

    def to_int(self):
        dtype = np.dtype(self.DTYPE[QuantizedArrayFrame3.nbytes(self.nbits)])
        s = self.scale(nbits=self.nbits, maxexp=self.maxexp)
        mn =  int(np.round(np.min(self.content)*s+0.5))
        data = np.round(self.content*s-mn)
        # print(f"{np.min(data)=} {np.max(data)=} ")
        info = np.iinfo(dtype)
        np.clip(data, info.min, info.max, out=data)
        data = data.astype(dtype)
        return data, mn

    @classmethod
    def from_int(cls, data: np.ndarray, nbits: int, maxexp: int, mn) -> np.ndarray:
        # dtype = np.float16 if nbits<10 else np.float32 if nbits<23 else np.float64 if nbits<52 else np.float128
        dtype = np.float32 if nbits<23 else np.float64 if nbits<52 else np.float128 # No float16
        res = (data.astype(dtype)+dtype(mn))*dtype(1/cls.scale(nbits=nbits, maxexp=maxexp))
        return res

    def tighten_parameters(self, ints):
        nprefix, nsuffix, bitspervalue = find_bitfixes(ints)
        # print(f"{nprefix=}, {nsuffix=}, {bitspervalue=} {self.nbits=}")
        if nsuffix==bitspervalue:
            assert nprefix==bitspervalue
            nsuffix = 0
            nprefix = bitspervalue-1
        # Apply suffix
        self.nbits -= nsuffix
        nprefix += nsuffix
        ints = ints >> nsuffix
        # Apply prefix
        new_nbits = round_nbits(bitspervalue - nprefix)
        dnbits = new_nbits-self.nbits
        assert dnbits<=0
        self.maxexp += dnbits
        self.nbits = new_nbits
        # Change data type to avoid storing zeros.
        dtype = np.dtype(self.DTYPE[QuantizedArrayFrame3.nbytes(self.nbits)])
        return ints.astype(dtype)

    def to_bytes(self) -> [bytes]:
        data, mn = self.to_int()
        data = self.tighten_parameters(data)
        bnbits = self.nbits.to_bytes(1, byteorder='big')
        bmaxexp = self.maxexp.to_bytes(1, byteorder='big', signed=True)
        btype = data.dtype.char.encode()
        assert len(btype)==1
        # nbytes = QuantizedArrayFrame3.nbytes(self.nbits)
        nbytes = 8
        # print(f"Minimum {mn=} {nbytes=} {self.nbits=}")
        bmin = mn.to_bytes(nbytes, byteorder='big', signed=True)
        packed, ncut = pack_bits(data, self.nbits)
        bcut = ncut.to_bytes(1, byteorder='big')
        barray = packed.tobytes()
        compressed = zlib.compress(barray)
        return [bnbits, bmaxexp, btype, bmin, bcut, compressed]

    @classmethod
    def from_bytes(cls, data: bytes):
        nbits, data = data[0], data[1:]
        maxexp, data = int.from_bytes(data[:1], byteorder='big', signed=True), data[1:]
        ctype, data = chr(data[0]), data[1:]
        dtype = np.dtype(ctype)
        # nbytes = QuantizedArrayFrame3.nbytes(nbits)
        nbytes = 8
        mn, data = int.from_bytes(data[:nbytes], byteorder='big', signed=True), data[nbytes:]
        ncut, data = data[0], data[1:]

        barray = zlib.decompress(data)
        packed = np.frombuffer(barray, dtype=dtype)
        array = unpack_bits(packed, nbits=nbits, ncut=ncut)
        content = cls.from_int(array, nbits=nbits, maxexp=maxexp, mn=mn) 
        return QuantizedArrayFrame3(content=content, nbits=nbits, maxexp=maxexp)

#################################################################################################################

class EndFrame(TypedFrame):
    typeid = 5

    def __init__(self):
        pass

    @classmethod
    def from_bytes(cls, data: bytes):
        return EndFrame()

    def to_bytes(self) -> [bytes]:
        return []

    
