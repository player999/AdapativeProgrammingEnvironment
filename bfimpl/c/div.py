from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int div();

//Stop:Declarations
//Start:Definitions
int div() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n1, n2, n3):
    identification = generateId()
    code = PATTERN
    return "div_%s" % identification, code
