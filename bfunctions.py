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

# Generate CV matrix of ones
def cvOne(n, h, w):
    imp = loadImplementation("cv_one")
    (fname, code) = imp(n, h, w)
    def function(*args):
        CompError("cvOne not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Threshold cv matrix
def cvThresh(n, t):
    imp = loadImplementation("cv_thresh")
    (fname, code) = imp(n, t)
    def function(*args):
        CompError("cvThresh not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Convert cv matrix to gray
def cvRgb2Gray(n):
    imp = loadImplementation("cv_rgb2gray")
    (fname, code) = imp(n)
    def function(*args):
        CompError("cvThresh not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Calculate gaussian
def cvGaussian(n, sz, sigma):
    imp = loadImplementation("cv_gaussian")
    (fname, code) = imp(n, sz, sigma)
    def function(*args):
        CompError("cvGaussian not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Convert cv matrix to gray
def cvFindContours(n):
    imp = loadImplementation("cv_findcontours")
    (fname, code) = imp(n)
    def function(*args):
        CompError("cvFindContours not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Morphology close
def cvClose(n):
    imp = loadImplementation("cv_close")
    (fname, code) = imp(n)
    def function(*args):
        CompError("cvClose not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Morphology close
def cvBotHat(n):
    imp = loadImplementation("cv_bothat")
    (fname, code) = imp(n)
    def function(*args):
        CompError("cvBothat not implemented")
    f = Function(function, fname, n, [(fname, code)])
    return f

# Function table
table = [
    {"pattern": "I_([0-9]+)_([0-9]+)", "f": select, "genpattern": "I_%d_%d", "name": "Selector", "args": ["Index", "Arity"]},
    {"pattern": "zero([0-9]+)", "f": zero, "genpattern": "zero%d", "name": "Zero", "args": ["Arity"]},
    {"pattern": "one([0-9]+)", "f": one, "genpattern": "one%d", "name": "One", "args": ["Arity"]},
    {"pattern": "add([0-9]+)", "f": add, "genpattern": "add%d", "name": "Add", "args": ["Arity"]},
    {"pattern": "sub([0-9]+)", "f": sub, "genpattern": "sub%d", "name": "Sub", "args": ["Arity"]},
    {"pattern": "eq([0-9]+)", "f": equal, "genpattern": "eq%d", "name": "Equal", "args": ["Arity"]},
    {"pattern": "cvOnes([0-9]+)_([0-9]+)_([0-9]+)", "f": cvOne, "genpattern": "cv_ones_%d_%d", "name": "Ones", "args": ["Arity", "Height", "Width"]},
    {"pattern": "cvThresh([0-9]+)_([0-9]+)", "f": cvThresh, "genpattern": "cv_threshold_%d", "name": "Thresh", "args": ["Arity", "Thresh"]},
    {"pattern": "cvRgb2Gray([0-9]+)", "f": cvRgb2Gray, "genpattern": "cv_rgb2gray_%d", "name": "RGB2Gray", "args": ["Arity"]},
    {"pattern": "cvGaussian([0-9]+)_([0-9]+)_([0-9]+)", "f": cvGaussian, "genpattern": "cv_gaussian_%s_%d", "name": "Gaussian", "args": ["Arity", "Size", "Sigma"]},
    {"pattern": "cvFindContours([0-9]+)", "f": cvFindContours, "genpattern": "cv_findcontours_%d", "name": "FindContours", "args": ["Arity"]},
    {"pattern": "cvClose([0-9]+)", "f": cvClose, "genpattern": "cv_close_%d", "name": "MorphClose", "args": ["Arity"]},
    {"pattern": "cvBothat([0-9]+)", "f": cvBotHat, "genpattern": "cv_bothat_%d", "name": "MorphBothat", "args": ["Arity"]}
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