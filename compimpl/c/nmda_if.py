from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int nmda_if();

//Stop:Declarations
//Start:Definitions
int nmda_if%ID%(%ARGS%) {
    int retval;
    return retval;
}
//Stop:Definitions
"""


def generate(*args):
    identification = generateId()
    code = PATTERN
    return "nmda_if_%s" % identification, code
