from adaptivenv import Composition, Function, CompError
from compimpl.compos import loadImplementation
import itertools
import copy
import random
import hashlib
import re


# Helpers

def generate_id():
    randline = str(random.random()).encode('ASCII')
    identification = hashlib.sha256(randline).hexdigest()[1:10]
    return identification


def check_arguments(n, *args):
    for a in args:
        if type(a) is not int:
            raise CompError("Argument type is not integer")
        if len(args) != n:
            raise CompError("Wrong argument count (%d) for function with %d arguments" % (len(args), n))


def join_sources(src):
    src = list(map(lambda x: x.src, list(src)))
    return list(itertools.chain(*src))


# Compositions

class PPASuperposition(Composition):
    def __init__(self, *args):
        if len(args) < 2:
            raise CompError("Too few functions for superposition")
        Composition.__init__(self, args)
        if args[0].argc != (len(args) - 1):
            raise CompError("Bad argument count for functions-arguments")
        for i in range(1, len(args)):
            if args[i].argc != args[1].argc:
                raise CompError("Not equal argument count for functions in superposition")
        self.source_pattern = "S"

    def __str__(self):
        line = "Superposition of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("superposition")
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


class PPALoop(Composition):
    def __init__(self, *args):
        if len(args) < 2:
            raise CompError("Too few functions for loop")
        Composition.__init__(self, args)
        for i in range(0, len(args)):
            if args[i].argc != len(args) - 1:
                raise CompError("Not equal argument count for functions in loop")
        self.source_pattern = "For"

    def __str__(self):
        line = "Loop of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("loop")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(self.functions[1].argc, *args)
            results = list(args)
            while self.functions[0](*results):
                res = list(copy.copy(results))
                for i in range(1, len(self.functions)):
                    res[i-1] = self.functions[i](*results)
                results = res
            return results[0]
        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[0].argc, new_src)

        return func


class PPACaseof(Composition):
    def __init__(self, *args):
        for i in range(0, len(args)):
            if args[i].argc != args[0].argc:
                raise CompError("Not equal argument count for functions in case")
        if len(args) < 3:
            raise CompError("Not enough arguments for Caseof")
        Composition.__init__(self, args)
        self.source_pattern = "Caseof"

    def __str__(self):
        line = "Case of: \n"
        for f in self.functions:
            line += str(f)
        return line

    def function(self):
        imp = loadImplementation("caseof")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(self.functions[0].argc, *args)
            pred = self.functions[0](*args)
            if pred > len(self.functions) - 2:
                pred = len(self.functions) - 1
            result = self.functions[pred](*args)
            return result

        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[0].argc, new_src)
        return func


class PPABranch(Composition):
    def __init__(self, *args):
        if len(args) != 3:
            raise CompError("Not adequate function count")
        Composition.__init__(self, args)
        self.source_pattern = "If"

    def __str__(self):
        line = "Branch of: \n"
        for f in self.functions:
            line += str(f)

        return line

    def function(self):
        imp = loadImplementation("branch")
        (fname, code) = imp(self.functions)

        def f(*args):
            check_arguments(self.functions[1].argc, *args)
            if self.functions[0](*args) == 1:
                return self.functions[1](*args)
            elif self.functions[0](*args) == 0:
                return self.functions[2](*args)
            else:
                raise CompError("Wrong value returned predicate!")
        new_src = join_sources(self.functions)
        new_src.append((fname, code))
        func = Function(f, fname, self.functions[0].argc, new_src)
        return func


def COMP_Inm(sel, size):
    if sel > size:
        raise CompError("Wrong arguments" % (size, sel))

    def initializer(self, *args):
        if len(args) != size:
            raise CompError("This is %d-ary composition, not %d-ary" % (size, len(args)))
        Composition.__init__(self, args)
        self.functions = args
        self.source_pattern = "CI_%d_%d" % (size, sel)

    def stringifier(self):
            line = self.__class__.__name__ + " of: \n"
            for f in self.functions:
                line += str(f)
            return line

    def function(self):
            return self.functions[sel - 1]

    new_composition = type("inm_" + generate_id(), (Composition,), {"__init__": initializer,
                                                                    "__str__": stringifier,
                                                                    "function": function})
    return new_composition


# Composition table
table = [
    {"pattern": "^(S)$",      "f": PPASuperposition, "source_name":"S"},
    {"pattern": "^(For)$",    "f": PPALoop,          "source_name":"For"},
    {"pattern": "^(If)$",     "f": PPABranch,        "source_name":"IF"},
    {"pattern": "^(Caseof)$", "f": PPACaseof,        "source_name":"Caseof"},
    {"pattern": "^(CI)_([0-9]+)_([0-9]+)$", "f": COMP_Inm, "source_name":"CI_%d_%d"}
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

