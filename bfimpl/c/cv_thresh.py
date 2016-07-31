from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int cv_thresh_%thresh%_%ID%(%ARGS%);
//Stop:Declarations
//Start:Definitions
int cv_thresh_%thresh%_%ID%(%ARGS%) {
    Mat result;
    threshold(arg0, result, %thresh%, 255, THRESH_BINARY);
    return result;
}

//Stop:Definitions
"""

def generate(n, thresh):
    identification = generateId()
    arguments = ""
    for i in range(0, n):
        arguments += "Mat arg%d, " % (i + 1)
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%thresh%", str(thresh))
    return "cv_thresh_%d_%s" % (thresh, identification), code
