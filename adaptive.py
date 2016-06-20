import argparse
import sys
import srcparser
import linker
import config
from bfimpl.bfunc import compile
from adaptivegui import start_windowed
from namedset import NamedSet

if __name__ == "__main__":
    if len(sys.argv) == 1:
       start_windowed(sys.argv)

    conf = config.getConfig()
    aparser = argparse.ArgumentParser(prog='adaptive')
    aparser.add_argument('--src', type=str, required=True, help='file of source code')
    aparser.add_argument('--odir', type=str, help='output direcotry')
    aparser.add_argument('--args', type=str, nargs='*',help='test arguments')
    arguments = aparser.parse_args(sys.argv[1:])
    config.configuration["output_folder"] = arguments.odir
    src = open(arguments.src, 'r').read()

    program = srcparser.parse_source(src)
    resolved = linker.link_functions(srcparser.valueSymList, srcparser.funcSymList, srcparser.compSymList)
    if arguments.args:
        if conf["algebra"] == "spa":
            ar = "".join(arguments.args)
            ars = NamedSet(ar)
            print(resolved(ars))
        elif conf["algebra"] == "ppa":
            ars = list(map(int, arguments.args))
            print(resolved(*ars))

    #
    # if arguments.odir != None:
    #     compile(resolved)

