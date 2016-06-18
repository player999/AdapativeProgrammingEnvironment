from adaptivenv import Composition, Function, CompError
from compimpl.compos import loadImplementation
import itertools
import copy
import random
import hashlib
import re
from namedset import NamedSet


# Helpers

def generate_id():
    randline = str(random.random()).encode('ASCII')
    identification = hashlib.sha256(randline).hexdigest()[1:10]
    return identification


def check_arguments(n, *args):
    for a in args:
        if type(a) is not NamedSet:
            raise CompError("Argument type is not named set")
    if (len(args) != n) and (n != 0):
        raise CompError("Wrong argument count (%d) for function with %d arguments" % (len(args), n))


def join_sources(src):
    src = list(map(lambda x: x.src, list(src)))
    return list(itertools.chain(*src))


#helper
def nmda_overlap(a, b):
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

# Compositions

class NMDAApplication(Composition):
    def __init__(self, *args):
        if len(args) < 2:
            raise CompError("Too few functions for application")
        for i in range(0, len(args)):
            if args[i].argc != 1:
                raise CompError("Sequential application must take functions with exactly one argument")
        Composition.__init__(self, args)
        self.source_pattern = "Ap"

    def __str__(self):
        line = "Sequential application of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("nmda_application")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(1, *args)
            h1d = args[0]
            h2d = None
            for i in range(0, len(self.functions)):
                h2d = nmda_overlap(h1d, self.functions[i](h1d))
                h1d = copy.copy(h2d)
            return copy.copy(h2d)
        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[1].argc, new_src)

        return func

class NMDAWhile(Composition):
    def __init__(self, *args):
        if len(args) != 2:
            raise CompError("Only body and predicate for \"While\"")

        if (args[0].argc != 0) and (args[0].argc != 0):
            if args[0].argc != args[1].argc:
                raise CompError("Body arg count must be equal to predicate")
        Composition.__init__(self, args)
        self.source_pattern = "While"

    def __str__(self):
        line = "While of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("nmda_while")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(1, *args)
            data = copy.copy(args)
            while self.functions[0](*data):
                data = (self.functions[1](*data),)
            return copy.copy(*data)

        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[1].argc, new_src)

        return func

class NMDAIf(Composition):
    def __init__(self, *args):
        if len(args) != 3:
            raise CompError("Only predicate and then and else for If")
        a = None
        b = None
        for i in range(1, len(args)):
            if args[i].argc == 0:
                break
            if a is None:
                a = args[i].argc
            b = args[i].argc
            if a != b:
                raise CompError("If must take all functions and predicates with equal argument numbers")
            a = b
        Composition.__init__(self, args)
        self.source_pattern = "If"

    def __str__(self):
        line = "If of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("nmda_if")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(1, *args)
            if (self.functions[0](*args)):
                return copy.copy(self.functions[1](*args))
            else:
                return copy.copy(self.functions[2](*args))
        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[1].argc, new_src)

        return func

class NMDASuperposition(Composition):
    def __init__(self, *args):
        if len(args) < 2:
            raise CompError("Too few functions for superposition")
        Composition.__init__(self, args)
        if args[0].argc != (len(args) - 1):
            raise CompError("Bad argument count for functions-arguments")

        a = None
        b = None
        for i in range(1, len(args)):
            if args[i].argc == 0:
                break
            if a is None:
                a = args[i].argc
            b = args[i].argc
            if a != b:
                raise CompError("Not equal argument count for functions in superposition")
            a = b

        self.source_pattern = "S"

    def __str__(self):
        line = "Superposition of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("nmda_superposition")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(self.functions[1].argc, *args)
            results = []
            for i in range(1, len(self.functions)):
                results.append(self.functions[i](*args))
            res = self.functions[0](*results)
            return res
        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[1].argc, new_src)

        return func

# Composition table
table = [
    {"pattern": "(NS)",      "f": NMDASuperposition, "source_name":"S"},
    {"pattern": "(NAp)",     "f": NMDASuperposition, "source_name":"Ap"},
    {"pattern": "(NWhile)",  "f": NMDASuperposition, "source_name":"While"},
    {"pattern": "(NIf)",     "f": NMDASuperposition, "source_name":"If"}
]

def getCompositionNames():
    names = list(map(lambda x: x["source_name"], table))
    return names

def getComposition(fname):
    for entry in table:
        res = re.findall(entry["pattern"], fname)
        if len(res) > 0:
            res = res[0]
            if (len(res) > 1) and ((type(res) == list) or (type(res) == tuple)):
                ar = list(map(lambda x: int(x), res[1:]))
                f = entry["f"](*ar)
            else:
                f = entry["f"]
            return f
    return None

