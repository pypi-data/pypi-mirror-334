import queue

from .encoder import encode_uint, decode_uint, maxbytes_uint
from .frame import FrameFactory, TypedFrame

#############################################################################################
# Constants

SIGNATURE = b'SAD'

#############################################################################################
# Functions

class BacktrackableFile:
    def __init__(self, file):
        self._file = open(file, 'rb')
        self._buffer = bytes() # Bytes read, but not yet used.

    def seek(self, pos: int):
        self._file.seek(pos)
        self._buffer = b''

    def filepos(self):
        return self._file.tell()-len(self._buffer)

    def skip(self, length:int):
        buffer_len = len(self._buffer)
        remains = length-buffer_len
        if remains<=0:
            self._buffer = self._buffer[length:]
            return 
        self._buffer = b''
        self._file.seek(remains, 1)

    def read(self, length: int) -> bytes:
        buffer_len = len(self._buffer)
        remains = length-buffer_len
        if remains<=0:
            result = self._buffer[:length]
            self._buffer = self._buffer[length:]
            return result
        data = self._file.read(remains)
        result = self._buffer + data
        self._buffer = b''
        return result

    def unread(self, data: bytes):
        self._buffer = self._buffer + data

    def close(self):
        self._file.close()
        return len(self._buffer)==0

#############################################################################################
# Common ancestor of all containers
class BasicContainer:
    @property 
    def minbytes(self):
        return self._minbytes

    @property 
    def lengthbits(self):
        return self._lengthbits

    def close(self):
        """
        Close container. No further writting or reading is possible.
        """
        if self._file is not None:
            self._file.close()
            self._file = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def read_raw(self):
        raise NotImplementedError

    def write_raw(self, data: [bytes]):
        raise NotImplementedError

    def read(self, return_length=False, skip=False):
        data = self.read_raw()
        if data is None or isinstance(data, Pending):
            return data if not return_length else (data, 0)

        if skip:
            frame = ()
        else:
            typeid, data = decode_uint(data, minbytes=FrameFactory.minbytes, lengthbits=FrameFactory.lengthbits)
            classes = FrameFactory().frameClasses
            if not typeid in classes:
                raise IOError(f"Unknown frame type {typeid:x}")
            frame = classes[typeid].from_bytes(data)
            
        return frame if not return_length else (frame, len(data))

    def write(self, frame: TypedFrame):
        prefix = encode_uint(frame.typeid, minbytes=FrameFactory.minbytes, lengthbits=FrameFactory.lengthbits)
        body = frame.to_bytes()
        # print(f"Writing frame typeid {frame.typeid} of length {len(body)}")
        self.write_raw([prefix, *body])


#############################################################################################
# Reader class
class ContainerReader(BasicContainer):
    """
    Reader for SAD file container. 
    The class allows to read the container frame by frame.
    """
    def __init__(self, file):
        """
        Open container for read and check its signature.

        Args:
            file (str): File top open

        Raises:
            IOError: file has wrong signature
        """
        self._file = BacktrackableFile(file)
        signature = self._file.read(len(SIGNATURE))
        if SIGNATURE!=signature:
            raise IOError("Wrong signature")
        self._minbytes = int.from_bytes( self._file.read(1), byteorder='big' )
        self._lengthbits = int.from_bytes( self._file.read(1), byteorder='big' )

    def seek(self, pos: int):
        """UNSAFE seek position in file. 
        To preserve consistency of the container only seek at postions returned by `filepos`.
        Some frames used by `Container` can depend on previous frames, be careful.
        """
        self._file.seek(pos)

    def filepos(self):
        return self._file.filepos()

    @property
    def minbytes(self):
        return self._minbytes

    @property
    def lengthbits(self):
        return self._lengthbits

    def read_raw(self, skip=False):
        """
        Read single frame from the file.

        Parameters:
            skip: if True, do not read data, return empty bytes object.

        Result:
            None: if end of file is reached.
            bytes: content of the frame. 

        Raises:
            IOError: if frame is corrupted (longer than file).
        """
        l = maxbytes_uint(minbytes=self._minbytes, lengthbits=self._lengthbits)
        data = self._file.read(l)
        if len(data)==0: # EOF
            return None
        try:
            length, data = decode_uint(data, minbytes=self._minbytes, lengthbits=self._lengthbits)
        except OverflowError:
            raise IOError("Failed to read frame length")
        self._file.unread(data)

        if skip:
            self._file.skip(length)
            return bytes()

        # print(f"Reading {length} bytes ({data[:consumed]}).")
        return self._file.read(length)


#############################################################################################
# Writer class

class ContainerWriter(BasicContainer):
    """
    Writer for SAD file container. 
    The class allows to write to the container frame by frame.
    """
    def __init__(self, file, MINBYTES = 2, LENGTHBITS = 3):
        """
        Open SAD container for writting.

        Args:
            file (str): File to store the container.
        """
        self._file = open(file, 'wb')
        self._file.write(SIGNATURE)

        self._minbytes = MINBYTES
        self._lengthbits = LENGTHBITS

        self._file.write( self._minbytes.to_bytes(length=1, byteorder='big') )
        self._file.write( self._lengthbits.to_bytes(length=1, byteorder='big') )

    def write_raw(self, data: [bytes]):
        """
        Write single frame to the container,

        Args:
            data (bytes): content of the frame.
        """
        if isinstance(data, bytes): data = [data]
        data_len = sum([len(d) for d in data])
        length_encoded = encode_uint(data_len, minbytes=self._minbytes, lengthbits=self._lengthbits)
        # print(f"Writing {data_len} bytes ({length_encoded})")
        self._file.write(length_encoded)
        for d in data:
            self._file.write(d) 

#############################################################################################
# PipeContainer 
# Does not use actual files, instead buffer unread frames in memory.


class Pending:
    def __inti__(self):
        pass

class PipeContainer(BasicContainer):
    def __init__(self):
        self._eof = False
        self._buffer = queue.Queue()

    def close(self):
        self._eof = True

    def read_raw(self):
        if self._eof:
            return None
        try:
            frame = self._buffer.get(block=False)
            # print(f"<<< {frame}")
            return frame
        except queue.Empty:
            # print(f"<<< PENDING")
            return Pending()

    def write_raw(self, data: [bytes]):
        if self._eof:
            raise IOError("Writting attempt to closed file")
        if isinstance(data, bytes): data = [data]
        frame = b"".join(data)
        # print(f">>> {frame}")
        self._buffer.put(frame, block=True, timeout=3)