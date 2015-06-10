from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int branch_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int branch_%ID%(%ARGS%) {
    if(%PRED%(%AR%)) return %YES%(%AR%);
    else return %NO%(%AR%);
}

//Stop:Definitions
"""


def generate(*args):
    identification = generateId()

    arguments = ""
    arggs = ""
    ar = args[0]
    for i in range(0, ar[1].argc):
        arguments += "int arg%d, " % (i + 1)
        arggs += "arg%d, " % (i + 1)
    arguments = arguments[:-2]
    arggs = arggs[:-2]

    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%AR%", arggs)
    code = code.replace("%PRED%", ar[0].name)
    code = code.replace("%YES%", ar[1].name)
    code = code.replace("%NO%", ar[2].name)
    return "branch_%s" % identification, code
