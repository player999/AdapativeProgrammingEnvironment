from adaptivenv import Function, CompError
from bfimpl.bfunc import loadImplementation
import re

# Helpers


def check_arguments(n, *args):
    for a in args:
        if type(a) is not int:
            raise CompError("Argument type is not integer")
        if len(args) != n:
            raise CompError("Wrong argument count (%d) for function with %d arguments" % (len(args), n))


# Function generators

# Selector generation function

def select(m, n):
    if (type(m) is not int) or (type(n) is not int):
        raise CompError("Wrong argument types in selector function generator")
    if m > n:
        raise CompError('Element index in selector function generator is bigger then argument count')
    if m < 1:
        raise CompError("Element index in selector function generator is zero or negative")

    imp = loadImplementation("selector")
    (fname, code) = imp(m, n)

    def function(*args):
        check_arguments(n, *args)
        return args[m - 1]

    f = Function(function, fname, n, [(fname, code)])
    return f


# Zero generation function

def zero(n):
    if type(n) is not int:
        raise CompError("Wrong argument types in zero function generator")
    imp = loadImplementation("zero")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(n, *args)
        return 0

    f = Function(function, fname, n, [(fname, code)])
    return f


# One generation function

def one(n):
    if type(n) is not int:
        raise CompError("Wrong argument types in zero function generator")
    imp = loadImplementation("one")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(n, *args)
        return 1

    f = Function(function, fname, n, [(fname, code)])
    return f


# Add generation function

def add(n):
    if type(n) is not int:
        raise CompError("Wrong argument types in zero function generator")
    imp = loadImplementation("add")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(n, *args)
        return sum(args)

    f = Function(function, fname, n, [(fname, code)])
    return f


# Sub generation function

def sub(n):
    if type(n) is not int:
        raise CompError("Wrong argument types in zero function generator")
    imp = loadImplementation("sub")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(n, *args)
        retval = args[0]
        for i in range(1, len(args)):
            retval -= args[i]
        if retval < 0:
            return 0
        else:
            return retval

    f = Function(function, fname, n, [(fname, code)])
    return f


# Equality generation function

def equal(n):
    if type(n) is not int:
        raise CompError("Wrong argument types in zero function generator")
    imp = loadImplementation("equal")
    (fname, code) = imp(n)

    def function(*args):
        check_arguments(n, *args)
        if len(set(args)) == 1:
            return 1
        else:
            return 0

    f = Function(function, fname, n, [(fname, code)])
    return f

# Function table
table = [
    {"pattern": "I_([0-9]+)_([0-9]+)", "f": select},
    {"pattern": "zero([0-9]+)", "f": zero},
    {"pattern": "one([0-9]+)", "f": one},
    {"pattern": "add([0-9]+)", "f": add},
    {"pattern": "sub([0-9]+)", "f": sub},
    {"pattern": "eq([0-9]+)", "f": equal}
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
