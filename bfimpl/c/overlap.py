from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int overlap();

//Stop:Declarations
//Start:Definitions
int overlap() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate():
    identification = generateId()
    code = PATTERN
    return "overlap_%s" % identification, code
