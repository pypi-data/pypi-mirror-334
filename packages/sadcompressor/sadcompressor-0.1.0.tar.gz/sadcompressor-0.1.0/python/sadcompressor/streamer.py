import numpy as np
from dataclasses import dataclass
from packaging import version

from .container import *
from .frame import *
from ._version import __version__

from .log import logging
logger = logging.getLogger(__name__)

###############################################################################################

def read_only_view(x):
    v = x[:]
    v.flags.writeable = False
    return v

###############################################################################################

@dataclass
class State:
    key: int
    dt: float
    value: np.ndarray

class Series:
    """
    Storage for history of single value/array.
    Values are stored together with timemark,
    and indexed by key numbers.
    Current key always has timemark zero.
             value0      value1        value2
    <-- dt --> | <-- dt --> | <-- dt --> | present
              key0        key1          key2
    """
    def __init__(self, key=0):
        self._key = key
        self._data = [None]
        self._dt = [0.]
        self._keys = [self._key]
    
    def __repr__(self):
        return "".join(
            f"{k}({dt}){'-' if d is None else '+'}"
            for k, dt, d in zip(self._keys, self._dt, self._data)
        )

    @property
    def key(self):
        return self._key
    
    def seek(self, key):
        self._key = key

    def next(self, dt):
        # logger.debug(f"Series.next {dt=} {self}")
        self._key += 1
        if self._data[-1] is None:
            self._dt[-1] += dt
            self._keys[-1] = self._key
        else:
            self._data.append(None)
            self._dt.append(dt)
            self._keys.append(self._key)
        # logger.debug(f">> {self}")

    def forget(self, but):
        """
        Forget all data, but given number of last values.
        """
        # logger.debug(f"Series.forget {but=} {self}")
        if self._data[-1] is None: but+=1
        self._data = self._data[-but:]
        self._dt = self._dt[-but:]
        self._keys = self._keys[-but:]
        # logger.debug(f">> {but=} {self}")

    def save(self, value):
        """Save `value` to the current frame."""
        self._data[-1] = value

    def last(self):
        """Return last saved value."""
        if self._data[-1] is not None:
            return State(value=self._data[-1], key=self._keys[-1], dt=self._dt[-1])
        if len(self._data)<2:
            return None
        assert self._data[-2] is not None
        return State(value=self._data[-2], key=self._keys[-2], dt=self._dt[-2])
        
    def chain(self, depth):
        start = -depth
        if self._data[-1] is None:
            start -= 1
        # if abs(start)>=len(self._depth):
        #     raise ValueError("More values are requested than stored")
        idx = slice(start-1+depth, start-1, -1)
        # logger.debug(f"Series.chain {depth=} {start=} {idx=} {self} {self._keys=} {self._keys[idx]=}")
        return  [ State(value=v, key=k, dt=dt) for v, k, dt in zip(self._data[idx], self._keys[idx], self._dt[idx])]

class DataFrame:
    def __init__(self):
        self._key = 0
        self._data = {}
    
    def __repr__(self):
        s = ', '.join(
            f"{k}: {v}"
            for k,v in self._data.items()
        )
        return f"{{ {s}, key={self._key} }}"

    @property
    def key(self):
        return self._key

    def reset(self, name):
        self._data[name] = Series(self._key)

    def __getitem__(self, name):
        if name not in self._data:
            self.reset(name)
        return self._data[name]

    def seek(self, key, variables):
        self._key = key
        for n, v in self._data.items():
            if variables is None or n in variables:
                v.seek(self._key)

    def next(self, dt, variables):
        self._key += 1
        for s in self._data.values():
            if variables is None or s in variables:
                s.next(dt)
        # logger.debug(f"DataFrame.next {dt=} {self}")

    def forget(self, but):
        for s in self._data.values():
            s.forget(but)

    def names(self):
        return list(self._data.keys())
    
    def __contains__(self, name):
        return name in self._data


#############################################################################################################################

class SADBase:
    def close(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

#############################################################################################################################

class SADReader(SADBase):
    def __init__(self, file, memory=1):
        if isinstance(file, BasicContainer):
            self._container = file
        else:
            self._container = ContainerReader(file)
        self._clear()
        self._t = 0.
        self._dt = 0. # First chain must not contain DeltaTimeFrame.
        self._memory = memory
        self._last_update = {}
        self._last_full_update = {}
        self._key = 0

    @property
    def dt(self):
        return self._dt

    def get_last_full_update(self, name):
        return self._last_full_update.get(name)

    def _update_variable(self, name, fullupdate:bool=False):
        self._last_update[name] = self._key
        if fullupdate:
            self._last_full_update[name] = self._key

    def _clear(self):
        self._state = DataFrame()
        self._dict = {}
        self._just_after_end_of_dataframe = True
        self._meta = {}

    def reset(self, variables):
        # logger.debug(f"SADReader.reset {variables=} {self._dict=} {self._state}")
        for n in variables:
            if n in self._state: self._state.reset(n)
            if n in self._meta: self._meta.pop(n)
            if n in self._dict: self._dict.pop(n)
        # logger.debug(f">> {self._dict=} {self._state}")

    def seek(self, pos: int, t: float, key: int):
        """UNSAFE seek position in file. 
        To preserve consistency of the container only seek to positions returned by `filepos`.
        Some frames used by `Container` can depend on previous frames, be careful.
        """
        # logger.debug(f"SADReader.seek({pos=}, {t=}, {key=})")
        self._container.seek(pos)
        self._t = t
        self._dt = 0.
        self._key = key

    def filepos(self):
        return self._container.filepos()

    def list_arrays(self):
        return self._state.names()

    def list_dictionaries(self):
        return self._dict.keys()

    def get_metadata(self, key: str):
        return self._meta.get(key, {})

    def _set_metadata(self, key: str, data: dict):
        if not key in self._meta: self._meta[key] = {}
        self._meta[key].update(data)

    def close(self):
        self._container.close()

    def get_last_update(self, name):
        return self._last_update.get(name)

    @property
    def memory(self):
        return self._memory

    @property
    def state(self) -> DataFrame:
        return self._state

    def __getitem__(self, key: str) -> np.ndarray:
        # logger.debug(f"SADReader.__getitem__ {key=} {self._dict=} {self._state=} {self._last_update=}")
        if key in self._dict:
            return self._dict[key]
        if key in self._state:
            last = self._state[key].last()
            return None if last is None else last.value
        return None

    @property
    def t(self) -> float:
        return self._t

    @property
    def key(self) -> int:
        return self._key

    def next_key(self, read_all_available=False, variables=None) -> bool:
        """
        Read data from container until next time key is reached.

        Parameters:
            read_all_available: If True, ignore EndFrame, read while data available. 
                If False, read until EndFrame, any incomplete frame raises an exception.

            variables: If not None, process only listed variables, all other stay unchanged.

        Returns:
            bool: True if end of file is reached.
        """
        assert variables is None or isinstance(variables, list) 
        while True:
            frame = self._container.read()
            if frame is None:
                if self._just_after_end_of_dataframe:
                    return True
                else:
                    raise("Unexpected end of file")
            elif isinstance(frame, Pending):
                if read_all_available: break
                else: raise IOError(f"Unexpected pending state of container")
            elif isinstance(frame, EndFrame):
                # self._dt = None
                self._just_after_end_of_dataframe = True
                self._key += 1
                if not read_all_available: break
            else:
                self._just_after_end_of_dataframe = False
                self._process_frame(frame, variables=variables)
        self._state.forget(self._memory)   
        return False

    def _process_frame(self, frame: TypedFrame, variables):
        if isinstance(frame, UBJSONFrame):
            # logger.debug(f"_process_frame {self._key=} {frame.content=}")
            mode = frame.content['mode']
            if mode=='dict':
                return self._process_dict(frame.content, variables=variables)
            elif mode == 'interp':
                return self._process_interp(frame.content, variables=variables)
            elif mode == 'setup':
                return self._process_setup(frame.content)
            name = frame.content['name']
            dataframe = self._container.read( skip=not (variables is None or name in variables) )
            # logger.debug(f"_process_frame {mode=} {name=} {dataframe=}")
            if dataframe is None:
                raise IOError(f"Unexpected end of data frame {frame}")
            if dataframe != ():
                self._set_metadata(key=frame.content['name'], data=dataframe.metadata)
                self._process_pair(desc=frame.content, data=dataframe.content)
            # else:
                # logger.debug(f">> ignoring")
        elif isinstance(frame, TimeDeltaFrame):
            self._dt = frame.content
            self._t += self._dt
            self._state.next(self._dt, variables=variables)
            self._state.forget(self._memory)
        else:
            raise IOError(f"Unexpected frame {frame}")

    def _process_dict(self, frame: dict, variables):
        # logger.debug(f"_process_dict {self._key=} {frame=} {variables=} {self._dict}")
        name = frame['name']
        if not (variables is None or name in variables): 
            # logger.debug(f">> ignoring")
            return
        data = self._dict.get(name, {})
        delta = frame['content']
        for k in delta:
            if delta[k] is None:
                data.pop(k, None)
            else:
                data[k] = delta[k]
        self._dict[name] = data
        self._update_variable(name)
        # logger.debug(f">> {data=} {delta=} {name=} {self._dict=}")

    def _process_interp(self, frame: dict, variables):
        name = frame['name']
        if not (variables is None or name in variables): 
            # logger.debug(f">> ignoring")
            return
        coefs = frame['coefs']
        if len(coefs)==0:
            raise IOError(f"Empty interpolation frame.")
        chain = self._state[name].chain(len(coefs))
        if len(chain)<len(coefs):
            raise IOError(f"Number of coefficients {len(coefs)} is larger than number of stored values {len(chain)}.")
        data = None
        for c, d in zip(coefs, chain):
            x = c*d.value
            if data is None: data = x
            else: data += x
        self._append_state(key=name, value=data)

    def _process_setup(self, frame: dict):
        frame.pop('mode')
        memory = frame.pop('memory')
        if memory is not None:
            self._memory = max(memory, self._memory)
            assert 0<self._memory<8
        file_version = frame.pop('version')
        if version is not None and version.parse(file_version)>version.parse(__version__):
            print(f"WARNING. File version is newer than installed library. Upgrade sadcompress library. {frame}") 
        _fullframe = frame.pop('fullframe')
        if len(frame)>0:
            print(f"WARNING. Unknown field(s) in setup frame. Upgrade sadcompress library. {frame}")            

    def _append_state(self, name:str, value: np.ndarray, fullupdate: bool=False):
        self._update_variable(name, fullupdate=fullupdate)
        self._state[name].save(value)
        # logger.debug(f"_append_state {name=} {value is None=} {self._state=}")

    def _process_pair(self, desc, data: np.ndarray):
        # logger.debug(f"_process_pair {desc=} {self._state=}")
        name = desc['name']
        # if self._dt is None:
        #     raise IOError("DeltaTimeFrame is not first in the chain")
        mode = desc['mode']
        if mode == 'init':
            data = data.reshape(desc['shape'])
            self._append_state(name=name, value=data, fullupdate=True)
        elif mode == 'delta':
            chain = self._state[name].chain(1)
            # logger.debug(f"{name=} {self._state=} {len(chain)=}")
            if len(chain)==0:
                raise IOError("Delta frame came before initialization frame.")
            old = chain[0].value
            new = data.reshape(old.shape) + old
            self._append_state(name=name, value=new)
        else:
            raise IOError(f"Unknown mode '{mode}'")

#############################################################################################################################

class UpdateTracker:
    def __init__(self, keyframe):
        """Create tracker of a variable modifications. 
        Can track complete, which does not and partial updates.
        when the result depends on previous state. 

        Args:
            keyframe (int):  The first frame number. Variable is assumed to be undefined in the previous frames. 
        """
        # The array stores for each keyframe the last time (keyframe), when the variable was completely updated,
        # that is the variable can be reconstructed without reading previous frames.
        self._complete = [None]*keyframe+[keyframe]
        # The array store for each keyframe the last time (keyframe), the variable was updated completely or partially. 
        self._updated = [None]*keyframe+[keyframe]
        # Current key  number.
        self._key = keyframe
    def __repr__(self):
        return " ".join(f"{c}<{u}" for c, u in zip(self._complete, self._updated))
    def next(self):
        self._key += 1
        self._complete.append(self._complete[-1])
        self._updated.append(self._updated[-1])
    def complete_update(self):
        self._complete[-1] = self._key
        self._updated[-1] = self._key
    def partial_update(self, depth):
        """Remember partial update based on `depth` previous modifications (not necessary complete).
        Any updates on the current step are ignored when counting to `depth`.

        Args:
            depth (int): Number of previous updates the current update depends on.
        """
        self._updated[-1] = self._key

        if depth==0:
            self._complete[-1] = min(self._complete[-1], self._key)
            return 
        last_complete = None
        test = self._key-1
        while depth>0:
            if test<0:
                raise ValueError("Update depends on more values than extists.")
            if self._updated[test] == test: 
                last_complete = test
                depth -= 1
            test -= 1
        self._complete[-1] = min(self._complete[-1], last_complete)
    def is_updated(self):
        return self._updated[self._key] == self._key
    def get_update(self, key):
        """Returns closest update before `key`."""
        return self._updated[key]
    def get_complete(self, key):
        return self._complete[key]
    
class VariablesTracker:
    def __init__(self):
        self._key = 0
        self._vars = {}

    def next(self):
        self._key += 1
        for v in self._vars.values():
            v.next()
    
    @property
    def key(self): return self._key
    
    def finish(self):
        self._key = None
    
    def __getitem__(self, name):
        v = self._vars.get(name)
        if v is None: 
            if self._key is None:
                raise KeyError
            v = UpdateTracker(self._key)
            self._vars[name] = v
        return v
    
    def __contains__(self, key):
        return key in self._vars
    
    def variables(self):
        return self._vars.keys()
    
    def __repr__(self):
        s = ", ".join(f"{n}: {v}" for n, v in self._vars.items())
        return f"{{ {s} }}"

class SADRandomReader(SADBase):
    """Random access SADReader. Upon initialization SAD file is scanned for keys.
    Then data can be read by the key index.
    """
    def __init__(self, file):
        self._container = ContainerReader(file)
        self._prepare_index()
        self._reader = SADReader(self._container)
        self._nkeys = len(self._timestamps)
        self._reader.next_key()
        self._key = 0
        assert self._key+1==self._reader.key 

    @property
    def nkeys(self):
        return self._nkeys

    @property
    def key(self):
        return self._key

    @property
    def t(self):
        return self._timestamps[self._key]

    @property
    def timestamps(self):
        return self._timestamps

    def get_update(self, name):
        if name not in self._tracker: return None 
        return self._tracker[name].get_update(self._key)

    def get_complete_update(self, name):
        if name not in self._tracker: return None 
        return self._tracker[name].get_complete(self._key)

    def __contains__(self, name: str) -> bool:
        return name in self._tracker

    def __getitem__(self, name: str) -> np.ndarray:
        # logger.debug(f"SADRandomReader.__getitem__ {name=} {self._key=} {self._reader.get_last_update(name)=}")
        assert 0 <= self._key < self.nkeys
    
        # Extract information on updates of the variable `name`
        try:
            history = self._tracker[name]
        except KeyError:
            # logger.debug(f"Unknown name {name}")
            return None 
        variables = [name]

        # If the variable is not updated after stored state, then return the stored value.
        expected_update = history.get_update(self._key)
        if expected_update is None:
            return None

        updated = self._reader.get_last_update(name)
        if updated is not None and self._key >= updated >= expected_update:
                # logger.debug(f"Ready {name} {self._key=} {updated=} {history=}")
                return self._reader[name]

        # Find safe point to start reading.
        complete = history.get_complete(self._key)
        assert complete is not None
        start = complete

        # Part of the frame can be already read.
        if updated is not None and complete <= updated < self._key:
            start = updated+1 
            resuming = True
        else:
            resuming = False

        # logger.debug(f"{resuming=} {updated=} {expected_update=} {complete=} {start=} {self._key=} {history=} {self._positions=} {self._timestamps=}")

        # Seek first unprocessed frame.
        assert 0<=start<=self._key
        self._reader.seek(pos=self._positions[start], t=self._timestamps[start], key=start)

        # Reading unprocessed frames.
        if resuming:
            self._reader.state.seek(key=start, variables=variables) 
        else:
            self._reader.reset(variables=variables)

        while start<=expected_update:
            start += 1
            self._reader.next_key(variables=variables)

        # logger.debug(f"{self._key=} {self._reader.get_last_update(name)=} {self._reader.key=} {self._reader.t=}")
        assert self._reader.get_last_update(name)==expected_update

        return self._reader[name]

    def seek(self, key_index):
        self._key = key_index

        # logger.debug(f"Seek {self._key}")

    def list_arrays(self):
        return set(self._tracker.variables()) - self.list_dictionaries()

    def list_dictionaries(self):
        return set(self._dict_fields.keys())

    def get_metadata(self, key: str):
        return self._reader.get_metadata(key)

    def close(self):
        self._reader.close()
        self._nkeys = 0

    def _prepare_index(self):
        self._positions=[self._container.filepos()]
        self._timestamps=[0.]
        self._tracker = VariablesTracker()
        self._dict_fields = {}
        t = 0.
        keyindex = 0
        while True:
            assert keyindex == self._tracker.key
            ipos = self._container.filepos()
            frame = self._container.read()
            # logger.debug(f"{ipos}:{frame}")
            if frame is None or isinstance(frame, Pending):
                break
            elif isinstance(frame, TimeDeltaFrame):
                t = t + frame.content
                self._positions.append(self._container.filepos())
                self._timestamps.append(t)
                self._tracker.next()
                keyindex += 1
                # logger.debug(f"{self._tracker.key} {keyindex=} {self._positions=} {self._tracker=}")
            elif isinstance(frame, EndFrame):
                pass
            elif isinstance(frame, UBJSONFrame):
                mode = frame.content['mode']
                if mode == 'setup':
                    continue
                name = frame.content['name']
                if mode == 'interp':
                    ncoefs = len(frame.content['coefs'])
                    self._tracker[name].partial_update(ncoefs)
                elif mode == 'delta':
                    self._tracker[name].partial_update(0 if self._tracker[name].is_updated() else 1)
                elif mode == 'init':
                    self._tracker[name].complete_update()
                elif mode == 'dict':
                    old_dict = self._dict_fields.get(name, set())
                    new_dict = set(frame.content['content'].keys())
                    is_full_update = old_dict.issubset(new_dict)
                    self._dict_fields[name] = old_dict | new_dict
                    self._tracker[name].partial_update(0 if is_full_update else 1)
                else:
                    raise ValueError(f"Unknown frame type `{mode}`: {frame}")
        
        self._timestamps = np.array(self._timestamps)
        self._positions = np.array(self._positions)
        self._tracker.finish()

        self._container.seek(self._positions[0])

#############################################################################################################################

class SADWriter(SADBase):
    """
    Writer class for SAD archive.
    The archive stores time-series, e.g. sequence of frames indexed by floating-point keys (time marks).
    Each frame contains collection of labeled `np.ndarrays`.
    The data is compressed using interframe analysis.
    """
    def __init__(self, file, memory=2, prec_nbits=32, prec_maxexp=8, do_prediction=True, do_bitpack=True, fullframe=20):
        """Create sequential writer to SAD file object.

        Args:
            file (str of file or Container): File to write to.
            memory (int, optional): History length for each variable. Defaults to 2.
            prec_nbits (int, optional): Bites in mantissa. Defaults to 32.
            prec_maxexp (int, optional): Largest allowed exponent. Defaults to 8.
            do_prediction (bool, optional): Use extrapolation to predict variable values. Defaults to True.
            do_bitpack (bool, optional): Pack bits (slower, higher compression rate). Defaults to True.
            fullframe (int, optional): Number of frames between full copies of variables. Defaults to 20.
        """
        self._do_prediction = do_prediction
        self._do_bitpack = do_bitpack
        self._fullframe = fullframe

        if isinstance(file, BasicContainer):
            self._container = file
        else:
            self._container = ContainerWriter(file)
        self._pipe = PipeContainer()
        self._reader = SADReader(file=self._pipe, memory=memory)
        self._t = 0.
        self._frame_ended = True
        self._prec_nbits = prec_nbits
        self._prec_maxexp = prec_maxexp
        self._write_setup()

    def _write_setup(self):
        desc = {
            'version': __version__,
            'mode': 'setup',
            'memory': self._reader.memory,
            "fullframe": self._fullframe,
        }
        self._write( UBJSONFrame(desc) )


    def _write(self, frame):
        self._container.write(frame)
        self._pipe.write(frame)
        self._frame_ended = isinstance(frame, EndFrame)

    def _sync_reader(self):
        self._reader.next_key(read_all_available=True)

    def end_frame(self):
        if self._frame_ended: return
        self._write(EndFrame())

    def close(self):
        self.end_frame()
        self._container.close()
        self._reader.close()

    def next_key(self, dt: float):
        self.end_frame()        

        self._write( TimeDeltaFrame(dt) )
        self._t = self._t + dt
        
        self._sync_reader()
        assert np.abs(self._reader.t-self._t)<=1e-6*np.abs(self._t)

    # @property
    # def state(self) -> State:
    #     return self._reader.state

    @property
    def t(self) -> float:
        return self._t

    def store_array(self, key:str, value: np.ndarray, nbits=None, maxexp=None):
        chain = self._reader.state[key].chain(1) 
        if nbits is None: nbits = self._prec_nbits
        if maxexp is None: maxexp = self._prec_maxexp

        fullupdate = self._reader.get_last_full_update(key)
        writefullframe = fullupdate is None or self._reader.key-fullupdate>self._fullframe
        if len(chain)==0 or writefullframe:
            self._write_init_frame(key=key, value=value, nbits=nbits, maxexp=maxexp)
        else:
            self._write_delta_frame(key=key, value=value, chain=chain, nbits=nbits, maxexp=maxexp)

    def store_dict(self, key:str, value: dict):
            self._write_dict(key, value)

    def __setitem__(self, key: str, value):
        if isinstance(value, dict):
            self.store_dict(key=key, value=value)
        elif isinstance(value, np.ndarray):
            self.store_array(key=key, value=value)
        else:
            raise ValueError(f"Unsupported type {type(value)}")

    def _write_dict(self, key:str, value:dict):
        old = self._reader[key]
        if old is None: old = {}
        if not isinstance(old, dict):
            raise ValueError(f"Value type has been changed from {type(old)} to {type(value)}")
        delta = {}
        for k in value:
            if value[k] is None:
                raise ValueError(f"An attmept to store None to {key}.")
            if k not in old or old[k]!=value[k]:
                delta[k] = value[k]
        for k in old:
            if k not in value:
                delta[k] = None
        if not bool(delta): return 
        frame = UBJSONFrame({
            'mode': 'dict',
            'name': key,
            'content': delta,
        })
        self._write( frame )
        self._sync_reader()

    def _write_init_frame(self, key: str, value: np.ndarray, nbits=None, maxexp=None):
        frame = QuantizedArrayFrame2(content=value, nbits=nbits, maxexp=maxexp)
        desc = {
            'mode': 'init',
            'shape': value.shape,
            'name': key,
        }
        self._write( UBJSONFrame(desc) )
        self._write( frame )
        self._sync_reader()

    def _write_delta_frame(self, key: str, value: np.ndarray, chain, nbits=None, maxexp=None):
        if self._do_prediction and len(chain)>1:
            self._write_prediction_frame(key=key, chain=chain)
            chain = self._reader.state[key].chain(1) 
        old_state = chain[0]
        delta = value-old_state.value
        if self._do_bitpack:
            frame = QuantizedArrayFrame3(content=delta, nbits=nbits, maxexp=maxexp)
        else:
            frame = QuantizedArrayFrame2(content=delta, nbits=nbits, maxexp=maxexp)
        desc = {
            'mode': 'delta',
            'name': key,
        }
        self._write( UBJSONFrame(desc) )
        self._write( frame )
        self._sync_reader()
        
    def _write_prediction_frame(self, key, chain):
        dt0, dt1 = chain[0].dt, chain[1].dt 
        t1 = -dt0
        t2 = t1-dt1
        assert t1<0
        assert t1>t2
        # f(t) = (s1*(t-t2)-s2*(t-t1))/(t1-t2) # Interpolation polynomial
        coefs = [-t2/(t1-t2), t1/(t1-t2)]
        desc = {
            'mode': 'interp',
            'name': key,
            'coefs': coefs,
        }
        self._write( UBJSONFrame(desc) )
        self._sync_reader()



