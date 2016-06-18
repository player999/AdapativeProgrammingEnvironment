from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int unname();

//Stop:Declarations
//Start:Definitions
int unname() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    code = PATTERN
    return "unname%s" % identification, code
