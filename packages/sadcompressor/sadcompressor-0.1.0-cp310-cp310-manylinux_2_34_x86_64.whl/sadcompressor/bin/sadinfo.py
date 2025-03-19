#!/usr/bin/env python3

import argparse
import numpy as np
from rich import print

import sadcompressor as sad

def main():
    # CLI
    parser = argparse.ArgumentParser(description='Decode stream from SAD archive and print statistics.')
    parser.add_argument("filename", help='SAD file')
    parser.add_argument('--reversed', dest="reversed", action="store_true", default=False,
        help='Read newest frame first.')

    args = parser.parse_args()

    print(f"File {args.filename}")
    with sad.SADRandomReader(args.filename) as c:
        print(f"[yellow]#frames:[/] {c.nkeys}")
        print(f"[yellow]Frames:[/]")
        for key in range(c.nkeys-1,-1,-1) if args.reversed else range(c.nkeys):
            c.seek(key)
            assert c.key==key
            def process(name, fix, s):
                if c.get_update(name)!=key: return
                r = f"{name}[blue]{fix}[/]"
                if c.get_complete_update(name)==key:
                    r += f"[red]![/]"
                s.append(r)
            s = []
            for n in c.list_arrays():
                process(n, '', s)
            for n in c.list_dictionaries():
                process(n, '@', s)
            print(f"  [magenta]{key}:[/]{c.t}:", ' '.join(sorted(s)) )

