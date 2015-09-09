#!/usr/bin/env python


"""
Script to blindly generate valid assembly instructions
composed of alphanumeric shellcodes.
This could be useful when perfoming code injection through a buffer
where only alphanumeric characters are accepted.
"""


import itertools
from pwn import *


MAX_SIZE = {'i386':15}
charset = range(32, 127)


def main():
    for size in range(1, MAX_SIZE['i386']+1):
        combinations = itertools.combinations(charset, size)
        for numset in combinations:
            instruction = "".join([chr(num) for num in numset])
            disassembly = disasm(instruction)
            if (disassembly.count("\n") > 0):
                continue
            print disassembly




if __name__ == "__main__":
    main()


