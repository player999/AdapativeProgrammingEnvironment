from adaptivenv import Function, CompError
from bfimpl.namedfunc import loadImplementation
from namedset import NamedSet
import re
import copy

# Helpers


def check_arguments(n, *args):
    for a in args:
        if type(a) is not NamedSet:
            raise CompError("Argument type is not named set but %s"%(type(a)))
        if len(args) != n:
            raise CompError("Wrong argument count (%d) for function with %d arguments" % (len(args), n))


# Function generators

# Overlap
def overlap():
    imp = loadImplementation("overlap")
    (fname, code) = imp()

    def function(*args):
        check_arguments(2, *args)
        a = args[0]
        b = args[1]
        if a is None:
            return copy.copy(b)
        if b is None:
            return copy.copy(a)

        retval = copy.copy(b)
        keys_b = list(map(lambda x: x[0], b.nset))
        for i in range(0, len(a.nset)):
            elem = a.nset[i]
            if elem[0] not in keys_b:
                retval.nset.append(elem)
        return retval
    f = Function(function, fname, 2, [(fname, code)])
    return f


# Naming function
def name(n):
    imp = loadImplementation("name")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(1, *args)
        return NamedSet([(n, args[0].value)])

    f = Function(function, fname, 1, [(fname, code)])
    return f

# Unnaming function
def unname(n):
    imp = loadImplementation("unname")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(1, *args)
        for elem in args[0].nset:
            if elem[0] == n:
                return NamedSet(elem[1])
    f = Function(function, fname, 1, [(fname, code)])
    return f

def cons(n, v):
    imp = loadImplementation("const")
    (fname, code) = imp(n, v)

    def function(*args):
        return NamedSet([(str(n), int(v))])

    f = Function(function, fname, 0, [(fname, code)])
    return f

def idfun(n):
    imp = loadImplementation("idfun")
    (fname, code) = imp(n)

    def function(*args):
        return copy.copy(args[n])

    f = Function(function, fname, 0, [(fname, code)])
    return f

def modd(n1, n2, n3):
    imp = loadImplementation("modd")
    (fname, code) = imp(n1, n2, n3)

    def function(*args):
        check_arguments(1, *args)
        x1 = None
        x2 = None
        for e in args[0].nset:
            if e[0] == n1:
                x1 = e[1]
            if e[0] == n2:
                x2 = e[1]
        x3 = x1 % x2
        return NamedSet([(str(n3), x3)])

    f = Function(function, fname, 1, [(fname, code)])
    return f

def div(n1, n2, n3):
    imp = loadImplementation("modd")
    (fname, code) = imp(n1, n2, n3)

    def function(*args):
        check_arguments(1, *args)
        x1 = None
        x2 = None
        for e in args[0].nset:
            if e[0] == n1:
                x1 = e[1]
            if e[0] == n2:
                x2 = e[1]
        x3 = int(x1 / x2)
        return NamedSet([(str(n3), x3)])

    f = Function(function, fname, 1, [(fname, code)])
    return f

def equal(n):
    imp = loadImplementation("nmda_equal")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(2, *args)
        v1 = None
        v2 = None
        for e in args[0].nset:
            if e[0] == n:
                v1 = e[1]

        for e in args[1].nset:
            if e[0] == n:
                v2 = e[1]

        if v1 is None:
            return False
        if v2 is None:
            return False

        if v1 == v2:
            return True
        else:
            return False

    f = Function(function, fname, 2, [(fname, code)])
    return f


# Function table
table = [
    {"pattern": "overlap()", "f": overlap, "genpattern": "overlap", "name": "Overlap", "args": []},
    {"pattern": "idfun_([0-9]+)", "f": idfun, "genpattern": "idfun", "name": "IdFun", "args": ["Value"]},
    {"pattern": "nmdaequal_(.*?)", "f": equal, "genpattern": "nmdaequal", "name": "Nmdaequal", "args": ["Name"]},
    #{"pattern": "nmdagt()", "f": gt, "genpattern": "nmdagt", "name": "Nmdagt", "args": []},
    #{"pattern": "nmdaadd()", "f": add, "genpattern": "nmdaadd", "name": "Nmdaadd", "args": []},
    #{"pattern": "nmdasub()", "f": sub, "genpattern": "nmdasub", "name": "Nmdasub", "args": []},
    {"pattern": "mod_(.*?)_(.*?)_(.*?)", "f": modd, "genpattern": "nmdamod", "name": "Nmdamod", "args": ["Name", "Name", "Name"]},
    {"pattern": "div_(.*?)_(.*?)_(.*?)", "f": div, "genpattern": "nmdadiv", "name": "Nmdadiv", "args": ["Name", "Name", "Name"]},
    {"pattern": "nmdaconst_(.*?)_(.*?)", "f": cons, "genpattern": "nmdaadd", "name": "Nmdaadd", "args": ["Name", "Value"]},
    {"pattern": "name(.*?)", "f": name, "genpattern": "name_%s", "name": "Name", "args": ["Name"]},
    {"pattern": "unname(.*?)", "f": unname, "genpattern": "unname_%s", "name": "Unname", "args": ["Name"]}
]


def getFunction(fname):
    for entry in table:
        res = re.findall(entry["pattern"], fname)
        if len(res) > 0:
            res = res[0]
            ar = list(map(lambda x: int(x), res))
            f = entry["f"](*ar)
            return f
    return None

def getFunctionEntry(fname):
    for entry in table:
        if fname == entry["name"]:
            return entry
    return None