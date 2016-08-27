from bfimpl.bfunc import generateId


PATTERN = """//Start:Declarations
std::vector<std::vector<Point> > cv_findcontours_%ID%(%ARGS%);

//Stop:Declarations
//Start:Definitions
std::vector<std::vector<Point> > cv_findcontours_%ID%(%ARGS%) {
    std::vector<std::vector<Point> > contours;
    std::vector<cv::Vec4i> hierarchy;
    findContours(arg1.clone(), contours, hierarchy, cv::RETR_LIST,
		cv::CHAIN_APPROX_SIMPLE);
    return contours;
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
    return "cv_findcontours_%s" % (identification), code, "std::vector<std::vector<Point> >"
