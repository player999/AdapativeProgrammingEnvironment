from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int zero_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int zero_%ID%(%ARGS%) {
    return 0;
}

//Stop:Definitions
"""

def generate(n):
    identification = generateId()
    arguments = ""
    for i in range(0, n):
        arguments += "int arg%d, " % (i + 1)
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    return "zero_%s" % identification, code
