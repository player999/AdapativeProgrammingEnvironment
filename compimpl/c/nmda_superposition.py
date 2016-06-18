from compimpl.compos import generateId


PATTERN = """//Start:Declarations
int nmda_superposition();

//Stop:Declarations
//Start:Definitions
int nmda_superposition%ID%(%ARGS%) {
    int retval;
    return retval;
}
//Stop:Definitions
"""


def generate(*args):
    identification = generateId()
    code = PATTERN
    return "nmda_superposition_%s" % identification, code
