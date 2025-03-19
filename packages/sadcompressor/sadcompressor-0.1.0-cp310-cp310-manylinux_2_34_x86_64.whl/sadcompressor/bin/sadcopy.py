#!/usr/bin/env python3

import argparse
from termcolor import colored
import numpy as np

import sadcompressor as sad

def main():
    # CLI
    parser = argparse.ArgumentParser(description='Copy content of SAD archive to another one doing recompression with another options.')
    parser.add_argument("source", help='SAD file to read')
    parser.add_argument("destination", help='SAD file to be created')

    parser.add_argument('--packbits', dest="packbits", action="store_true", default=False,
        help='Enable packbits option.')

    parser.add_argument('--prediction', dest="prediction", action="store_true", default=False,
        help='Enable prediction option.')

    parser.add_argument('--nbits', dest="nbits", default=None, help='Override number of pits ber float.', type=int)

    parser.add_argument('--fullframe', dest="fullframe", default=20, help='Override distance between full frames.', type=int)


    args = parser.parse_args()

    print(f"Source file {args.source}")
    with sad.SADReader(args.source) as src:
        with sad.SADWriter(args.destination, memory=src.memory, fullframe=args.fullframe, do_prediction=args.prediction, do_bitpack=args.packbits) as dst:

            while True:
                if src.next_key(): break

                print(f"{src.t:.3f} {src.dt:.3f}                 ", end='\n')

                if src.dt>0: dst.next_key(src.dt)

                for key in src.list_dictionaries():
                    dst.store_dict(key=key, value=src[key])

                for key in src.list_arrays():
                    meta = src.get_metadata(key)
                    nbits = meta.get('nbits') if args.nbits is None else args.nbits 
                    dst.store_array( key=key, value=src[key], nbits=nbits, maxexp=meta.get('maxexp') )

