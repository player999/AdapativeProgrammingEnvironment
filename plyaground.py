import bfunctions
from ppa import PPASuperposition, PPABranch, PPALoop, COMP_Inm
from metacompositions import MetaSuperposition
from bfimpl.bfunc import compile
from adaptivenv import Composition


if __name__ == "__main__":
    f1 = bfunctions.select(2, 5)
    print(f1(1, 2, 3, 4, 5))
    print(f1.src)
    print(f1)

    f2 = bfunctions.add(5)
    print(f2(1, 2, 3, 4, 5))
    print(f2.src)
    print(f2)

    f3 = bfunctions.sub(5)
    print(f3(100, 2, 3, 4, 5))
    print(f3.src)
    print(f3)

    f4 = bfunctions.zero(5)
    print(f4(1, 2, 3, 4, 5))
    print(f4.src)
    print(f4)

    f5 = bfunctions.equal(5)
    print(f5(0, 0, 0, 0, 1))
    print(f5.src)
    print(f5)

    print("Superposition")
    c = PPASuperposition(bfunctions.select(1, 2), f2, f3)
    ff1 = c.function()
    print(ff1(1, 2, 3, 4, 5))

    print("Branch")
    predicate = PPASuperposition(bfunctions.equal(2), bfunctions.select(1, 5), bfunctions.select(2, 5)).function()
    c = PPABranch(predicate, f2, f3)
    ff2 = c.function()
    print(ff2(1, 2, 3, 4, 5))

    print("Loop")
    notequal = PPABranch(bfunctions.equal(2), bfunctions.zero(2), bfunctions.one(2)).function()
    predicate = PPASuperposition(notequal, bfunctions.select(2, 2), bfunctions.zero(2)).function()
    decrement = PPASuperposition(bfunctions.sub(2), bfunctions.select(2,2), bfunctions.one(2)).function()
    increment = PPASuperposition(bfunctions.add(2), bfunctions.select(1,2), bfunctions.one(2)).function()
    c = PPALoop(predicate, increment, decrement)
    ff3 = c.function()
    print(ff3(1, 2))
    #compile(ff3)

    I31 = COMP_Inm(1, 3)
    ms = MetaSuperposition(PPABranch, I31, PPALoop, PPASuperposition)
    nt = ms.composition()
    created_composition = nt(bfunctions.equal(2), bfunctions.zero(2), bfunctions.zero(2))
    ff4 = created_composition.function()
    print("aa")
    print(ff4(6,4))
    compile(ff4)
