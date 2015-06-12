import json
from adaptivenv import CompError

configuration = {}

def getConfig():
    try:
        conf = json.load(open("config.cfg","r"))
    except:
        raise CompError("Can not find or load configuration file")
    if type(conf) is not dict:
        raise ("Configuration is not JSON dictionary")
    conf.update(configuration)
    return conf

def getImplementation():
    conf = getConfig()
    if "implementation" in conf.keys():
        if type(conf["implementation"]) == str:
            return conf["implementation"]
        else:
            raise ("Worong type for \"implementation\" field")
    else:
        raise Exception("\"Implementation\" in configuration does not exist")