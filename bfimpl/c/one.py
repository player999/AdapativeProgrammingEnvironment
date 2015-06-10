from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int one_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int one_%ID%(%ARGS%) {
    return 1;
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
    return "one_%s" % identification, code
