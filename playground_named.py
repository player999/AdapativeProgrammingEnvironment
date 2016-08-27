from namedset import NamedSet
from namedalgebra import NMDAApplication, NMDASuperposition, NMDAIf, NMDAWhile
from metacompositions import MetaSuperposition
from bfimpl.namedfunc import compile
import namedfunctions

f1 = namedfunctions.name("C")
f2 = namedfunctions.unname("A")
f3 = namedfunctions.overlap()

f4 = NMDASuperposition(f1, f2).function()
f5 = namedfunctions.cons("A", 5)
f6 = namedfunctions.modd("A", "B", "E")
f7 = namedfunctions.div("A", "B", "F")
f8 = namedfunctions.equal("Q")

f9 = NMDASuperposition(f8, namedfunctions.cons("Q", 2), namedfunctions.cons("Q", 2)).function()
a = NamedSet([("A", 1071),("B", 462)])

#Euclid
rename = NMDASuperposition(namedfunctions.overlap(),
                  NMDASuperposition(namedfunctions.name("R1"),namedfunctions.unname("A")).function(),
                  NMDASuperposition(namedfunctions.name("R2"),namedfunctions.unname("B")).function()
                ).function()

b = rename(a)
body = NMDAApplication(namedfunctions.div("R1", "R2", "Q"),
                       namedfunctions.modd("R1", "R2", "R"),
                       NMDASuperposition(namedfunctions.name("R1"),namedfunctions.unname("R2")).function(),
                       NMDASuperposition(namedfunctions.name("R2"),namedfunctions.unname("R")).function()
    ).function()
true = NMDASuperposition(namedfunctions.equal("R"), namedfunctions.cons("R", 0), namedfunctions.cons("R", 0)).function()
false = NMDASuperposition(namedfunctions.equal("R"), namedfunctions.cons("R", 1), namedfunctions.cons("R", 0)).function()
idd = namedfunctions.idfun(0)
predicate = NMDAIf(NMDASuperposition(namedfunctions.equal("R"), idd, namedfunctions.cons("R", 0)).function(), false, true).function()
euclid =    NMDASuperposition(
                NMDASuperposition(
                    namedfunctions.name("Q"),
                    NMDASuperposition(
                        namedfunctions.unname("Q"),
                        NMDAWhile(predicate, body).function()
                    ).function()
                ).function(),
                rename
            ).function()
print(a, "->", euclid(a))
#End of euclid

# print(a)
# print(f4(a))
# print(f5(33,33,333))
# print(f6(a))
# print(f7(a))
# print(f9())