from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int modd();

//Stop:Declarations
//Start:Definitions
int modd() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n1, n2, n3):
    identification = generateId()
    code = PATTERN
    return "modd%s" % identification, code
