from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
Mat cv_rgb2gray_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
Mat cv_rgb2gray_%ID%(%ARGS%) {
    Mat gray;
    cvtColor(arg0, gray, CV_BGR2GRAY);
    return gray;
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
    return "cv_rgb2gray_%s" % (identification), code
