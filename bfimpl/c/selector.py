from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int select_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int select_%ID%(%ARGS%) {
    return %RETVAL%;
}

//Stop:Definitions
"""

def generate(m, n):
    identification = generateId()
    arguments = ""
    for i in range(0, n):
        arguments += "int arg%d, " % (i + 1)
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%RETVAL%", "arg%d" % m)
    return "select_%s" % identification, code
