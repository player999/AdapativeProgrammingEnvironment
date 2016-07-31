from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int cv_ones_%h%_%w%_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int cv_ones_%h%_%w%_%ID%(%ARGS%) {
    return Mat::ones(%h%, %w%, CV_8U);
}

//Stop:Definitions
"""

def generate(n, h, w):
    identification = generateId()
    arguments = ""
    for i in range(0, n):
        arguments += "Mat arg%d, " % (i + 1)
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%h%", str(h))
    code = code.replace("%w%", str(w))
    return "cv_ones_%d_%d_%s" % (h, w, identification), code
