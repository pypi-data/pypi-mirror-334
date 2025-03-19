#!/usr/bin/env python3

import argparse
from termcolor import colored
import numpy as np

import sadcompressor as sad

def main():
    # CLI
    parser = argparse.ArgumentParser(description='List all frames in SAD archive.')
    parser.add_argument("filename", help='SAD file')
    parser.add_argument('--stat', dest="stat", action="store_true", default=False,
        help='Compute statistics for supported dataframes.')

    args = parser.parse_args()

    print(f"File {args.filename}")
    with sad.ContainerReader(args.filename) as c:
        print(f"{colored('Header:','yellow')}")
        print(f"  minbytes {c.minbytes}")
        print(f"  lengthbits {c.lengthbits}")
        print(f"{colored('Frames:','yellow')}")
        nframes = 0
        ntimesteps = 0
        timeinterval = 0.
        while True:
            try:
                frame, length = c.read(return_length=True)
            except IOError as e:
                print(colored('ERROR','red'), str(e))
                break
            nframes += 1
            length_str = colored(str(length),'blue')
            cls_str = colored(frame.__class__.__name__,'red')
            if frame is None: break
            if isinstance(frame, sad.UBJSONFrame):
                print(f"  {length_str} {cls_str} {frame.content}")
            elif isinstance(frame, sad.ArrayFrame):
                print(f"  {length_str} {cls_str} {frame.content.dtype.str} {frame.content.shape}")
            elif isinstance(frame, sad.QuantizedArrayFrame) or isinstance(frame, sad.QuantizedArrayFrame2):
                if args.stat:
                    data = frame.to_int()
                    stat = f"[{np.min(data)} .. {np.max(data)}] Nonzero {np.count_nonzero(data)/data.size*100:.2f}% [{np.min(frame.content)} .. {np.max(frame.content)}]"
                else:
                    stat = ""
                comp = length / (frame.nbits/8*frame.content.size)
                print(f"  {length_str} {cls_str} {frame.content.dtype.str} {frame.content.shape} nbits={frame.nbits} maxexp={frame.maxexp} compressed {comp*100:.2f}% {stat}")
            elif isinstance(frame, sad.QuantizedArrayFrame3):
                if args.stat:
                    data, mn = frame.to_int()
                    stat = f"[{np.min(data)} .. {np.max(data)}]{mn:+d} Nonzero {np.count_nonzero(data+mn)/data.size*100:.2f}% [{np.min(frame.content)} .. {np.max(frame.content)}]"
                else:
                    stat = ""
                comp = length / (frame.nbits/8*frame.content.size)
                print(f"  {length_str} {cls_str} {frame.content.dtype.str} {frame.content.shape} nbits={frame.nbits} maxexp={frame.maxexp} compressed {comp*100:.2f}% {stat}")
            elif isinstance(frame, sad.EndFrame):
                ntimesteps += 1
                print("+", end='')
            elif isinstance(frame, sad.TimeDeltaFrame):
                timeinterval += frame.content
                print(colored(f"{frame.content:.6f}",'green'),  f"#{ntimesteps} t={timeinterval:.3f}", f"{length_str}")
            else:
                print(f"  {length_str} {frame}")
        print(colored("Statistics:",'yellow'))
        print(f"  number of frames: {nframes}")
        print(f"  number of timesteps: {ntimesteps}")
        print(f"  time interval: {timeinterval}")


