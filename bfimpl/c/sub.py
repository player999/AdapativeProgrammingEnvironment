from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int sub_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int sub_%ID%(%ARGS%) {
    int retval;
    retval = %EXPRESSION%;
    return retval;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    arguments = ""
    subtraction = ""
    for i in range(0, n):
        arguments += "int arg%d, " % (i + 1)
        subtraction += "arg%d - " % (i + 1)
    subtraction = subtraction[:-2]
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%EXPRESSION%", subtraction)
    return "sub_%s" % identification, code
