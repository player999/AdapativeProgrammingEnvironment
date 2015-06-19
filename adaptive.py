import argparse
import sys
import srcparser
import linker
import config
from bfimpl.bfunc import compile
from adaptivegui import start_windowed

if __name__ == "__main__":
    if len(sys.argv) == 1:
       start_windowed(sys.argv)

    aparser = argparse.ArgumentParser(prog='adaptive')
    aparser.add_argument('--src', type=str, required=True, help='file of source code')
    aparser.add_argument('--odir', type=str, help='output direcotry')
    aparser.add_argument('--args', type=int, nargs='*',help='test arguments')
    arguments = aparser.parse_args(sys.argv[1:])
    config.configuration["output_folder"] = arguments.odir
    src = open(arguments.src, 'r').read()

    program = srcparser.parse_source(src)
    resolved = linker.link_functions(srcparser.valueSymList, srcparser.funcSymList, srcparser.compSymList)
    if arguments.args:
        print(resolved(*arguments.args))

    if arguments.odir != None:
        compile(resolved)

