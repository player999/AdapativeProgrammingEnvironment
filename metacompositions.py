from adaptivenv import CompError, Composition, Metacomposition
import random
import hashlib
import re

def generate_id():
    randline = str(random.random()).encode('ASCII')
    identification = hashlib.sha256(randline).hexdigest()[1:10]
    return identification


class MetaSuperposition(Metacomposition):
    def __init__(self, *args):
        if len(args) < 2:
            raise CompError("Too few functions for metasuperposition")
        Metacomposition.__init__(self, args, "MetaSuperposition")
        self.composition_id = generate_id()

    def composition(self):
        def initializer(self, *args):
            Composition.__init__(self, args)
            self.functions = args

        def stringifier(self):
            line = self.__class__.__name__ + " of: \n"
            for f in self.functions:
                line += str(f)
            return line

        compositions = self.compositions[1:]
        main_composition = self.compositions[0]

        def function(self):
            # Apply compositions
            functions = list(map(lambda x: x(*self.functions).function(), compositions))
            the_function = main_composition(*functions).function()
            return the_function

        new_composition = type("composition_" + self.composition_id, (Composition,), {"__init__": initializer,
                                                                                      "__str__": stringifier,
                                                                                      "function": function})
        return new_composition


# Meta table
table = [
    {"pattern": "MS", "f": MetaSuperposition}
]


def getMetacomp(fname):
    for entry in table:
        res = re.findall(entry["pattern"], fname)
        if len(res) > 0:
            f = entry["f"]
            return f
    return None
