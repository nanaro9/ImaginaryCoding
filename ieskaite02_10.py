# Programmesanas valoda Python
class Klients():
    def __init__(self,vards):
        self.vards = vards

# Programmesanas valoda Python
class Prece():
    def __init__(self,cena):
        self.cena = cena

Ziepes=Prece(1.99)

from random import randrange
class Lietotajs:
    def __init__(self,vards,parole,kartasNumurs = randrange(1,15)):
        self.vards = vards
        self.parole = parole
        self.kartasNumurs = kartasNumurs

    def drukaVardu(self):
        print("Lietotāja vārds:",self.vards,"| Lietotāja kārtas numurs:",self.kartasNumurs)


class Darbinieks(Lietotajs):
    def drukaVardu(self):
        print("Pierakstījies Darbinieks!\nDarbinieka vārds:",self.vards,"| Darbinieka kārtas numurs:",self.kartasNumurs)

Lietotajs("Andris","Parole1",0).drukaVardu()

Darbinieks("Jaroslavs","Parole2",1).drukaVardu()

class Viesis(Lietotajs):
    def __init__(self, vards, kartasNumurs=randrange(1, 15)):
        super().__init__(vards, kartasNumurs)

    def drukaVardu(self):
        print("Viesa vārds:",self.vards,"| Viesa kārtas numurs:",self.kartasNumurs)

Viesis("Valdis",10).drukaVardu()

