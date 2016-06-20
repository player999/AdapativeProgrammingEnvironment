from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int cons();

//Stop:Declarations
//Start:Definitions
int cons() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n, v):
    identification = generateId()
    code = PATTERN
    return "cons_%s" % identification, code
