import os
import sys

from tiny_basic.tiny_basic_terminal import run_tiny_basic, run_tiny_basic_program


def main(args):
    if 1 == len(args):
        run_tiny_basic()
    else:
        run_tiny_basic_program(args[1])


if __name__ == '__main__':
    os.chdir('examples')
    main(sys.argv)
