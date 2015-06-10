from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int superposition_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int superposition_%ID%(%ARGS%) {
    int retval;
%RESULTSD%
%COMPUTER%
%CALL%
    return retval;
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

    resultsd = ""
    computer = ""
    resultsar = ""
    for i in range(1, len(ar)):
        resultsd += "    int result%d;\n" % i
        computer += "    result%d = %s(%s);\n" % (i, ar[i].name, arggs)
        resultsar += "result%d, " % i
    resultsar = resultsar[:-2]
    call = "    retval = %s(%s);\n" % (ar[0].name, resultsar)
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%RESULTSD%", resultsd)
    code = code.replace("%COMPUTER%", computer)
    code = code.replace("%CALL%", call)
    return "superposition_%s" % identification, code
