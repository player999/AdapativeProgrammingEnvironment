from pyparsing import *
from linker import find_function, find_composition, find_metacomp


funcStack = []
compStack = []
valueStack = []
symbolStack = {}


def assignVar( str, loc, toks ):
    toks = toks.asList()
    symbolStack[toks[0]] = toks[1]


def applyFunction( str, loc, toks ):
    valueStack.append(toks.asList())


def applyComposition( str, loc, toks ):
    funcStack.append(toks.asList())


def applyMeta( str, loc, toks ):
    compStack.append(toks.asList())


lFapply  = Literal( "(" )
rFapply  = Literal( ")" )

lCapply  = Literal( "[" )
rCapply  = Literal( "]" )

lMapply  = Literal( "<" )
rMapply  = Literal( ">" )

assign = Literal( "=" )

integer = Word(nums)
name = Regex("[a-zA-Z]+[0-9a-zA-Z_]*")

Capply = Forward()
Mapply = Forward()

function_arguments = delimitedList(integer)
composition_arguments = delimitedList(Group(Capply) | name )
metacomp_arguments = delimitedList(Group(Mapply) | name )

Fapply = (name + Group(lFapply.suppress() + function_arguments + rFapply.suppress())).setParseAction(applyFunction)
Capply << (name + Group(lCapply.suppress() + composition_arguments + rCapply.suppress())).setParseAction(applyComposition)
Mapply << (name + Group(lMapply.suppress() + metacomp_arguments + rMapply.suppress())).setParseAction(applyMeta)

expression = Fapply | Capply | Mapply
assignment = (name + assign.suppress() + Group(expression)).setParseAction(assignVar)

application = OneOrMore(Group(expression) | Group(assignment))

pattern = application

source = "cmp1 = MS<If, S, For>\n" \
         "main = cmp1[I_2_3, add3, sub3]\n"

if __name__ == "__main__":
    program = pattern.parseString(source)
    print(funcStack)
    print(find_function("I_3_5")(1,2,3,4,5))
    print(find_composition("CI_3_5"))
    print(find_metacomp("MS"))
