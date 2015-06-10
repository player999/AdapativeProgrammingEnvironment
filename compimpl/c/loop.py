from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int loop_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int loop_%ID%(%ARGS%) {
    int retval;
%DEFRES%
%INITRES%
    while(%PRED%(%ARGRES%)) {
%UPDRES%
    }
    retval = result1;
    return retval;
}

//Stop:Definitions
"""


def generate(*args):
    identification = generateId()

    arguments = ""
    arggs = ""
    resultsd = ""
    computer = ""
    reslist = ""
    ar = args[0]
    for i in range(0, ar[0].argc):
        arguments += "int arg%d, " % (i + 1)
        arggs += "arg%d, " % (i + 1)
        resultsd += "    int result%d;\n" % (i + 1)
        computer += "    result%d = arg%d;\n" % (i + 1, i + 1)
        reslist += "result%d, " % (i + 1)
    arguments = arguments[:-2]
    arggs = arggs[:-2]
    reslist = reslist[:-2]

    update = ""
    for i in range(1, len(ar)):
        update += "    result%d = %s(%s);\n" % (i, ar[i].name, reslist)

    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%DEFRES%", resultsd)
    code = code.replace("%INITRES%", computer)
    code = code.replace("%PRED%", ar[0].name)
    code = code.replace("%ARGRES%", reslist)
    code = code.replace("%UPDRES%", update)
    return "loop_%s" % identification, code
