
def make_arguments(arr, idxs=None):
    line = "["
    if idxs is None:
        idxs = list(range(0, len(arr)))
    for i in idxs:
        line += arr[i] + ", "
    line = line[:-2] + "]"
    return line


def reduction2ppa(red_stack):
    source = ""
    for name in red_stack.keys():
        app = red_stack[name]
        red = app[0]
        ars = app[1]
        line = name + " = "

        if red == "Cycle":
            line += "For" + make_arguments(ars)
        elif red == "Branch":
            line += "If" + make_arguments(ars)
        elif red == "Seq":
            arg = ars.copy()
            right = ""
            subst = arg[0]
            for ar in arg[1:]:
                right = "S" + make_arguments([ar, subst])
                subst = right
            line += right + "\n"
        else:
            return None

        source += line
    return source
