from pyparsing import *

funcStack = []
compStack = []
valueStack = []
valueSymList = {}
funcSymList = {}
compSymList = {}


def get_func_symlist():
    return funcSymList


def assignValue( str, loc, toks ):
    toks = toks.asList()
    valueSymList[toks[0]] = toks[1]


def assignFunction( str, loc, toks ):
    toks = toks.asList()
    funcSymList[toks[0]] = toks[1]


def assignComposition( str, loc, toks ):
    toks = toks.asList()
    compSymList[toks[0]] = toks[1]


def applyFunction( str, loc, toks ):
    valueStack.append(toks.asList())


def applyComposition( str, loc, toks ):
    funcStack.append(toks.asList())


def applyMeta( str, loc, toks ):
    compStack.append(toks.asList())

def parse_source(src):
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

    valueAssignment = (name + assign.suppress() + Group(Fapply)).setParseAction(assignValue)
    funcAssignment = (name + assign.suppress() + Group(Capply)).setParseAction(assignFunction)
    compAssignment = (name + assign.suppress() + Group(Mapply)).setParseAction(assignComposition)

    assignment = (valueAssignment | funcAssignment | compAssignment)

    application = OneOrMore(Group(expression) | Group(assignment))

    pattern = application

    program = pattern.parseString(src)

    return program

