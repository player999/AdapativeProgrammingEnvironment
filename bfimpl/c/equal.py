from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int equal_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int equal_%ID%(%ARGS%) {
%COMPARISON%
    return 1;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    arguments = ""
    comparison = ""
    for i in range(0, n):
        arguments += "int arg%d, " % (i + 1)
    arguments = arguments[:-2]
    for i in range(1, n):
        comparison += "    if (arg1 != arg%d) return 0;\n" % (i + 1)
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%COMPARISON%", comparison)
    return "equal_%s" % identification, code
