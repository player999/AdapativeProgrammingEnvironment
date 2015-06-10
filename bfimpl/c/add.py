from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int add_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int add_%ID%(%ARGS%) {
    int retval;
    retval = %EXPRESSION%;
    return retval;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    arguments = ""
    summa = ""
    for i in range(0, n):
        arguments += "int arg%d, " % (i + 1)
        summa += "arg%d + " % (i + 1)
    arguments = arguments[:-2]
    summa = summa[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%EXPRESSION%", summa)
    return "add_%s" % identification, code
