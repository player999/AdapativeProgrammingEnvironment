from compimpl.compos import generateId


PATTERN = """//Start:Declarations
%RTYPE% superposition_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
%RTYPE% superposition_%ID%(%ARGS%) {
    %RTYPE% retval;
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
        arguments += "%s arg%d, " % (ar[i+1].types[0], i + 1)
        arggs += "arg%d, " % (i + 1)
    arguments = arguments[:-2]
    arggs = arggs[:-2]

    resultsd = ""
    computer = ""
    resultsar = ""
    for i in range(1, len(ar)):
        resultsd += "    %s result%d;\n" % (ar[i].types[0], i)
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
    code = code.replace("%RTYPE%", ar[0].types[0])
    return "superposition_%s" % identification, code, ar[0].types[0]
