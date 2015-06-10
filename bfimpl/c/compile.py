from config import getConfig


def extractDeclarations(code):
    lines = code.split("\n")
    decls = []
    declf = 0
    for line in lines:
        if line == "//Stop:Declarations":
            break
        if declf == 1:
            decls.append(line)
        if line == "//Start:Declarations":
            declf = 1
    code = "\n".join(decls)
    return code


def extractDefinitions(code):
    lines = code.split("\n")
    decls = []
    declf = 0
    for line in lines:
        if line == "//Stop:Definitions":
            break
        if declf == 1:
            decls.append(line)
        if line == "//Start:Definitions":
            declf = 1
    code = "\n".join(decls)
    return code


def compile(function):
    cfg = getConfig()
    path = cfg["output_folder"]
    main_decl = ""
    main_defs = ""
    for file in function.src:
        main_decl += extractDeclarations(file[1])
        main_defs += extractDefinitions(file[1])
    f = open(path + "/" + "main.c", "w")
    f.write(main_decl + main_defs)
    f.close()
