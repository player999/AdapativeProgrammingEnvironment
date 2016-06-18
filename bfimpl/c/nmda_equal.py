from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int nmda_equal();

//Stop:Declarations
//Start:Definitions
int nmda_equal() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    code = PATTERN
    return "nmda_equal_%s" % identification, code
