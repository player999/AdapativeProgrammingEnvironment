import config
from adaptivenv import CompError


def get_function_parameter(fname, parameter):
    modlist = config.getConfig()["functions"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getFunctionEntry'])
        f = getattr(mod, 'getFunctionEntry')
        if f(fname):
            return f(fname)[parameter]
    return None


def list_reductions():
    modlist = config.getConfig()["reductions"]
    red_list = []
    for mod in modlist:
        mod = __import__(mod, fromlist=['table'])
        t = getattr(mod, 'table')
        reds = list(map(lambda x: x["name"], t))
        red_list.extend(reds)
    return red_list


def list_functions():
    modlist = config.getConfig()["functions"]
    f_list = []
    for mod in modlist:
        mod = __import__(mod, fromlist=['table'])
        t = getattr(mod, 'table')
        fs = list(map(lambda x: x["name"], t))
        f_list.extend(fs)
    return f_list


def list_compositions():
    modlist = config.getConfig()["compositions"]
    comp_list = []
    for mod in modlist:
        mod = __import__(mod, fromlist=['getCompositionNames'])
        f = getattr(mod, 'getCompositionNames')
        comp_list.extend(f())
    return comp_list


def find_reduction(rname):
    modlist = config.getConfig()["reductions"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getReduction'])
        f = getattr(mod, 'getReduction')
        return f(rname)
    return None


def find_function(fname):
    modlist = config.getConfig()["functions"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getFunction'])
        f = getattr(mod, 'getFunction')
        if f(fname):
            return f(fname)
    return None


def find_composition(fname):
    modlist = config.getConfig()["compositions"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getComposition'])
        f = getattr(mod, 'getComposition')
        if f(fname):
            return f(fname)
    return None


def find_metacomp(fname):
    modlist = config.getConfig()["metacomps"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getMetacomp'])
        f = getattr(mod, 'getMetacomp')
        if f(fname):
            return f(fname)
        return None


def resolve_composition_symbol(comp, fsym, csym):
    if type(comp) == list:
        if find_metacomp(comp[0]):
            comp[0] = comp[0]
        else:
            raise CompError("Unresolved metacomposition %s" % comp[0])
        for i in range(0, len(comp[1])):
            arg = comp[1][i]
            arg = resolve_composition_symbol(arg, fsym, csym)
            comp[1][i] = arg
    elif type(comp) == str:
        if comp in csym.keys():
            comp = resolve_composition_symbol(csym[comp], fsym, csym)
        elif find_composition(comp):
            comp = comp
        else:
            raise CompError("Unresolved composition %s" % comp)
    else:
        raise CompError("Linker error c")
    return comp


def resolve_function_symbol(program, fsym, csym):
    if type(program) == list:
        if program[0] in csym.keys():
            program[0] = resolve_composition_symbol(csym[program[0]], fsym, csym)
        elif find_composition(program[0]):
            program[0] = program[0]
        else:
            raise CompError("Unresolved composition %s" % program[0])
        for i in range(0, len(program[1])):
            arg = program[1][i]
            arg = resolve_function_symbol(arg, fsym, csym)
            program[1][i] = arg

    elif type(program) == str:
        if program in fsym.keys():
            program = resolve_function_symbol(fsym[program], fsym, csym)
        elif find_function(program):
            program = program
        else:
            raise CompError("Unresolved function %s" % program)
    else:
        raise CompError("Linker error f")

    return program


def generate_composition(comp):
    if type(comp) == str:
        return find_composition(comp)
    elif type(comp) == list:
        metacomp = find_metacomp(comp[0])
        argc = len(comp[1])
        argv = comp[1]
        ar = []
        for i in range(0, argc):
            ar.append(generate_composition(argv[i]))
        return metacomp(*ar).composition()
    else:
        raise CompError("Error generating composition")


def generate_function(program):
    # There is no compositions
    if type(program) == str:
        return find_function(program)

    # First, generate composition
    composition = generate_composition(program[0])

    # Second, generate arguments of composition
    argc = len(program[1])
    argv = program[1]
    ar = []
    for i in range(0, argc):
        ar.append(generate_function(argv[i]))

    # Third, apply composition
    result = composition(*ar).function()

    return result


def link_functions(vsym, fsym, csym):
    if "main" not in fsym.keys():
        raise CompError("No entry point in the program")
    program = fsym["main"]
    program = resolve_function_symbol(program, fsym, csym)
    function = generate_function(program)
    return function
