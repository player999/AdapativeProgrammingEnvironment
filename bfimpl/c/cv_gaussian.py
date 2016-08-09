from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
int cv_gaussian_%sz%_%sigma%_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
int cv_gaussian_%sz%_%sigma%_%ID%(%ARGS%) {
    Mat blured;
    GaussianBlur(arg0, blured, cv::Size(%sz%,%sz%), %sigma%);
    return blured;
}

//Stop:Definitions
"""

def generate(n, sz, sigma):
    identification = generateId()
    arguments = ""
    for i in range(0, n):
        arguments += "Mat arg%d, " % (i + 1)
    arguments = arguments[:-2]
    code = PATTERN
    code = code.replace("%ID%", identification)
    code = code.replace("%ARGS%", arguments)
    code = code.replace("%sz%", str(sz))
    code = code.replace("%sigma%", str(sigma))
    return "cv_gaussian_%d_%s_%s" % (sz, str(sigma).replace(".", ""), identification), code
