from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int name();

//Stop:Declarations
//Start:Definitions
int name() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    code = PATTERN
    return "name%s" % identification, code
