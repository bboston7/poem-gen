#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    fname = sys.argv[1]
    num_spaces = int(sys.argv[2])
    spaces = " " * num_spaces

    newlines = 0
    with open(fname) as f:
        for line in f:
            if line.startswith(spaces):
                print(line[num_spaces:], end="")
                newlines = 0
            elif line == "\n" and newlines < 2:
                print()
                newlines += 1
