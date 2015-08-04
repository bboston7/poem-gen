#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    fname = sys.argv[1]
    num_spaces = int(sys.argv[2])
    spaces = " " * num_spaces

    newlines = 0
    with open(fname) as f:
        for line in f:
            # Remove line numbers
            tokens = line.split()
            try:
                if tokens:
                    chop = len(str(int(tokens[-1]))) + 1
                    line = line[:-chop].rstrip()
                    line += "\n"
            except ValueError:
                pass

            if line.startswith(spaces):
                print(line[num_spaces:], end="")
                newlines = 0
            elif line == "\n" and newlines < 2:
                print()
                newlines += 1
