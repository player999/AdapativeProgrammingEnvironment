from config import getImplementation
import random
import hashlib


def loadImplementation(funcname):
    g = __import__("compimpl.%s.%s" % (getImplementation(), funcname), fromlist=['generate'])
    f = getattr(g, 'generate')
    return f


def generateId():
    randline = str(random.random()).encode('ASCII')
    identification = hashlib.sha256(randline).hexdigest()[1:10]
    return identification
