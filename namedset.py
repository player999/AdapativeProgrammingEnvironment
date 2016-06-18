from adaptivenv import CompError
import copy

class NamedSet:
    def __init__(self, a):
        self.nset = None
        self.value = None

        if isinstance(a, int):
            self.value = a
            return

        if not isinstance(a, list):
            raise CompError("This is not named set")
        for elem in a:
            if not isinstance(elem, tuple):
                raise CompError("Bad element of named set")
            if not isinstance(elem[0], str):
                raise CompError("Bad name of element of named set")
            if not isinstance(elem[1], int):
                raise CompError("Bad value of element of named set")
        self.nset = copy.copy(a)


    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return "{" + ", ".join(list(map(lambda x: "(" + x[0] + ", " + str(x[1]) + ")", self.nset))) + "}"

