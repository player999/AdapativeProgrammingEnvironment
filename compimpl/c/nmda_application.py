from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int nmda_application();

//Stop:Declarations
//Start:Definitions
int nmda_application%ID%(%ARGS%) {
    int retval;
    return retval;
}
//Stop:Definitions
"""


def generate(*args):
    identification = generateId()
    code = PATTERN
    return "nmda_application_%s" % identification, code
