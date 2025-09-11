szoveg = "autórendszám"
szam = 15
logaikai = True

print(szoveg)
print(szam)

szam *= 2

print(szam)
print(not logaikai)
print(20 > szam)

print(szoveg[1])
print(szoveg[-4])

szotar = {"név:": "Béla", "kor": 43}
print(szotar)
lista = ["habos", "kakaó"]
print(lista[0] + lista[1])
lista += ["tejszínes"]
print(lista)

eletkor = input("Add meg hány éves vagy: ")
print(eletkor)
print(szotar["név:"], "kora: \n", eletkor, sep="_", end="\n")

print("valami".center(__width=40, __fillchar="-"))