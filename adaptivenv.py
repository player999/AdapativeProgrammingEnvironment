class CompError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Function class
class Function:
    def __init__(self, fobject, fname, argc, src):
        if hasattr(fobject, "__call__"):
            self.f = fobject
        else:
            raise CompError("Object is not function")

        if type(fname) == str:
            self.name = fname
        else:
            raise CompError("Function name must be string")

        if (type(argc) is int) or (type(argc) is str):
            self.argc = argc
        else:
            raise CompError("Argument count must be integer")

        if type(src) == list:
            for el in src:
                if type(el[0]) != str:
                    raise CompError("Invalid source file name")
                if type(el[1]) != str:
                    raise CompError("Source code must be string")
                self.src = src
        else:
            raise CompError("Source code must be list of tuples")

    def __str__(self):
        return "Function %s\n" % self.name

    def __call__(self, *args):
        return self.f(*args)


# Composition class
class Composition:
    def __init__(self, args, function = None, sname = None):
        for arg in args:
            if not isinstance(arg, Function):
                raise CompError("Argument is not function")
        self.functions = tuple(args)
        self.argc = len(self.functions)
        if function is not None:
            self.function = function
        if sname is not None:
            self.__str__ = self.standart_str

    def standart_str(self):
        line = "Composition %s of following functions: {" % self.sname
        for i in range(0, len(self.functions)):
            line += self.functions[i].__str__()
        line += "\n}\n"


# Metacomosition class
class Metacomposition:
    def __init__(self, args, mname):
        for arg in args:
            if Composition not in arg.__bases__:
                raise CompError("Argument is not composition")
        self.compositions = tuple(args)
        self.argc = len(self.compositions)
        self.mname = mname

    def __str__(self):
        line = "Metacomposition %s of: {\n" % self.mname
        for i in range(0, len(self.compositions)):
            line += self.compositions[i].__name__ + "\n"
        line += "}\n"
        return line
