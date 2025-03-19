import numpy as np
import os
import time

import sadcompressor as  sad

SHP = (1<<7,1<<7,1<<6)
NBITS = 7
MAXT = 100
DT = 0.1

def ones(_t):
    return np.ones(SHP, dtype=np.float32)

rand = np.random.rand(*SHP).astype(np.float32)
def constant(_t):
    return rand

def random(_t):
    return np.random.rand(*SHP).astype(np.float32)

x, y, z = [np.linspace(-1,1,s,dtype=np.float32) for s in SHP]
xx, yy, zz = np.meshgrid(x,y,z, indexing='ij')
def adiabatic(t, spd=0.01):
    return np.cos(xx+spd*t)*np.cos(yy+spd*t)*np.cos(zz+spd*t)

def compress(file, gen, maxt, dt=0.1):
    uncompressed_size = 0
    ellapsed = 0.
    start = time.process_time()
    with sad.SADWriter(file, prec_maxexp=0, prec_nbits=NBITS) as c:
        while c.t<maxt:
            end = time.process_time()
            ellapsed += end-start
            print(f"{c.t:.3f}                         ", end='\r')
            array = gen(c.t)
            uncompressed_size += array.nbytes
            start = time.process_time()            
            c['x'] = array
            c.next_key(dt=dt)
    end = time.process_time()
    ellapsed += end-start
    compressed_size = os.path.getsize(file)
    print(f"Uncompressed {uncompressed_size}")
    print(f"Compressed   {compressed_size}")
    print(f"Compression rate {uncompressed_size/compressed_size}")
    print(f"Compression time: {ellapsed:.3f} sec")
    print(f"Compression speed: uncompressed {uncompressed_size/ellapsed/1e6:.3f} MB/sec, compressed {compressed_size/ellapsed/1e6:.3f} MB/sec ")



if __name__ == "__main__":
    # compress(file="tmp/ones.sad", gen=ones, maxt=MAXT, dt=DT)    
    # compress(file="tmp/constant.sad", gen=constant, maxt=MAXT, dt=DT)  
    # compress(file="tmp/random.sad", gen=random, maxt=MAXT, dt=DT)  
    compress(file="tmp/adiabatic.sad", gen=adiabatic, maxt=MAXT, dt=DT) 
