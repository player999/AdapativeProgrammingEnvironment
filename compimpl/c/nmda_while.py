from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int nmda_while();

//Stop:Declarations
//Start:Definitions
int nmda_while%ID%(%ARGS%) {
    int retval;
    return retval;
}
//Stop:Definitions
"""


def generate(*args):
    identification = generateId()
    code = PATTERN
    return "nmda_while_%s" % identification, code
