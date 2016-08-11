from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
Mat cv_bothat_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
Mat cv_bothat_%ID%(%ARGS%) {
    Mat result;
    morphologyEx(arg0, result, MORPH_BLACKHAT, arg1);
    return result;
}

//Stop:Definitions
"""

def generate(n):
    identification = generateId()
    arguments = ""
    for i in range(0, n):
        arguments += "Mat arg%d, " % (i + 1)
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    return "cv_bothat_%s" % (identification), code
