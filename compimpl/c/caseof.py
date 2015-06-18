from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int caseof_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int branch_%ID%(%FARGS%) {
    switch(%PRED%(%FARGS%)) {
%VARIANTS%
        default:
            return %LAST%(%FARGS%);
    }
}

//Stop:Definitions
"""

CALL_PATTERN = """\t\tcase %VARIANT%:
\t\t\treturn %FUNCNAME%(%FARGS%);
"""


def generate(*args):
    identification = generateId()

    arguments = ""
    arggs = ""
    ar = args[0]
    for i in range(0, ar[0].argc):
        arguments += "int arg%d, " % (i + 1)
        arggs += "arg%d, " % (i + 1)
    arguments = arguments[:-2]
    arggs = arggs[:-2]

    variants = ""
    for i in range(0, len(ar)-2):
        variant = CALL_PATTERN
        variant = variant.replace("%VARIANT%", str(i))
        variant = variant.replace("%FARGS%", arggs)
        variant = variant.replace("%FUNCNAME%", ar[i + 1].name)
        variants += variant


    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%FARGS%", arggs)
    code = code.replace("%VARIANTS%", variants)
    code = code.replace("%PRED%", ar[0].name)
    code = code.replace("%LAST%", ar[-1].name)
    return "caseof_%s" % identification, code
