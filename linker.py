import config


def find_function(fname):
    modlist = config.getConfig()["functions"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getFunction'])
        f = getattr(mod, 'getFunction')
        if f(fname):
            return f(fname)
        return None


def find_composition(fname):
    modlist = config.getConfig()["compositions"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getComposition'])
        f = getattr(mod, 'getComposition')
        if f(fname):
            return f(fname)
        return None


def find_metacomp(fname):
    modlist = config.getConfig()["metacomps"]
    for mod in modlist:
        mod = __import__(mod, fromlist=['getMetacomp'])
        f = getattr(mod, 'getMetacomp')
        if f(fname):
            return f(fname)
        return None