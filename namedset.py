from adaptivenv import CompError
import copy
import pyparsing

class NamedSet:
    def __init__(self, a):
        self.nset = None
        self.value = None

        if isinstance(a, int):
            self.value = a
            return
        if isinstance(a, str):
            a = parse_set(a)[0]

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

def parse_set(string):
   leftSet = pyparsing.Literal("{")
   rightSet = pyparsing.Literal("}")
   leftPair = pyparsing.Literal("(")
   rightPair = pyparsing.Literal(")")
   integer = pyparsing.Word(pyparsing.nums)
   name = pyparsing.Regex("[a-zA-Z]+[0-9a-zA-Z_]*")
   namedsets = []

   def parse_pairlist(str, loc, toks):
       nset = []
       for p in toks:
           element = (p[0], int(p[1]))
           nset.append(element)
       namedsets.append(nset)

   pair = pyparsing.Group(leftPair.suppress() + name + pyparsing.Literal(",").suppress() + integer + rightPair.suppress())
   nset = (leftSet.suppress() + pyparsing.delimitedList(pair) + rightSet.suppress()).setParseAction(parse_pairlist)
   nsets = pyparsing.OneOrMore(nset)
   nsets.parseString(string)
   return namedsets