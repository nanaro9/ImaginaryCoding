class kubs:
    objekti = []
    def __init__(self,malas_garums,krasa):
        kubs.objekti.append(self)
        if int(malas_garums) >= 2 and int(malas_garums) <= 10:
            self.malas_garums = int(malas_garums)
        else:
            print(malas_garums,"Malas garums neatbilst nosacījumiem!")
            self.malas_garums = 2

        if str(krasa).isdigit():
            print("Krāsa tika ievadīta nepareizi!")
        else:
            self.krasa = krasa

    def aprekinat_tilpumu(self):
        return self.malas_garums**3
    
    def objekta_likvidacija(self,obj):
        print(f"Objekts ar krāsu {self.krasa} tika likvidēts!")
        for i in globals():
            if obj == globals()[i]:
                del globals()[i]
                return
        
        
kubg = kubs(10,"Zaļa")
kubr = kubs(1,"Sarkana")
kubb = kubs(4,"Zila")
kubw = kubs(5,"Balta")

print(kubg.krasa, kubg.aprekinat_tilpumu(), "cm3")

print(kubr.malas_garums,"cm")
    
kubr.objekta_likvidacija(kubr)

try:    
    print(kubr.krasa)
except:
    print("Šis objekts vairs nav pieejams!")

print(kubg.malas_garums,"centimetri")

class bloks(kubs):

    __kubu_skaits = None

    def __init__(self, malas_garums, krasa, forma, derigums=0):
        super().__init__(malas_garums,krasa)

        for i in kubs.objekti:
            if bloks.__instancecheck__(i):
                kubs.objekti.pop(kubs.objekti.index(i))

        self.__kubu_skaits = len(kubs.objekti)

        if self.__kubu_skaits > 4 or self.__kubu_skaits < 1:
            print("Kubu skaits blokā neatbilst noteikumiem")

        self.nosaukums = (f"{self.krasa}{self.__kubu_skaits}")

        forma_vertibas = [11,12,13,14,22]

        self.forma = forma
        self.derigums = derigums

        for i in forma_vertibas:
            if forma != i:
                self.derigums = 1
            else:
                self.derigums = 0
                return
        if self.derigums == 1:
            print('Parametrs "forma" neatbilst noteikumiem')
    
    def tilpums(self):
        proporcijas = [int(i) for i in str(self.forma)]
        Laukums_pam = proporcijas[0] ** 2 * self.malas_garums
        augstums = proporcijas[1] * self.malas_garums
        return Laukums_pam*augstums