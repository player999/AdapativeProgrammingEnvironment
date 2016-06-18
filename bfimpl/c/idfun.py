from bfimpl.bfunc import generateId

#TODO: Implement

PATTERN = """//Start:Declarations
int idfun();

//Stop:Declarations
//Start:Definitions
int idfun() {
    int retval;
    retval = 0;
    return retval;
}

//Stop:Definitions
"""


def generate(n):
    identification = generateId()
    code = PATTERN
    return "idfun_%s" % identification, code
