from adaptivenv import CompError


class Reduction:
    def __init__(self, *args):
        self.arguments = list(args)

    def __str__(self):
        line = self.name + "of: "
        for arg in self.arguments:
            line += str(arg) + ", "
        line = line[:-2]
        return line


class ReduceCycle(Reduction):
    @staticmethod
    def getName():
        return "Cycle"

    @staticmethod
    def getFields():
        fields = [{"name": "Predicate", "count": 1},
                  {"name": "Body", "count": -1}]
        return fields

    def __init__(self, *args):
        Reduction.__init__(self, *args)


class ReduceBranch(Reduction):
    @staticmethod
    def getFields():
        fields = [{"name": "If", "count": 1},
                  {"name": "Then", "count": 1},
                  {"name": "Else", "count": 1}]
        return fields

    @staticmethod
    def getName():
        return "Branch"

    def __init__(self, *args):
        Reduction.__init__(self, *args)


class ReduceSequential(Reduction):
    @staticmethod
    def getFields():
        fields = [{"name": "Function", "count": -1}]
        return fields

    @staticmethod
    def getName():
        return "Seq"

    def __init__(self, *args):
        Reduction.__init__(self, *args)
        self.name = "Seq"

table = [{"name": ReduceCycle.getName(), "reduction": ReduceCycle},
         {"name": ReduceBranch.getName(), "reduction": ReduceBranch},
         {"name": ReduceSequential.getName(), "reduction": ReduceSequential}
        ]

def getReduction(rname):
    for entry in table:
        if entry["name"] == rname:
            return entry["reduction"]
    return None
