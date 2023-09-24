from tabulate import tabulate
from tkinter import *
import os
from datetime import *

# Klases izveide ar grafiskās saskarnes īpašībām un vajadzīgajiem datiem tālākajām darbībām
class Noma():
    def __init__(self):
        self.root = Tk()
        self.root.title('Instrumentu un tehnikas uzskaites sistēma')

        self.produkti = []
        self.nomnieki = []
        self.Produkta_kategorija = ""
        self.Produkta_nosaukums = ""
        self.Tehniskie_raksturojumi = ""
        self.Nomas_cena_dienā = ""
        self.Produkts_pieejams = True
        self.Nomnieks_vārds = ""
        self.Nomnieks_uzvārds = ""
        self.Nomnieks_pers_kods = ""
        self.Nomnieks_tel_numurs = ""
        self.Nomas_sākuma_datums = ""
        self.Nomas_beigu_datums = ""
        self.mainFrame = Frame(self.root)
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)
        self.frames = [self.mainFrame,self.frame1,self.frame2,self.frame3]
    

    def Nomas_atlikusais_laiks(self,nomasBeiguDatums):
        nomasBeigas = nomasBeiguDatums.split(".")
        sodiena = str(datetime.now())[0:10].split("-")
        Gadi = int(nomasBeigas[2])-int(sodiena[0])
        Menesi = int(nomasBeigas[1])-int(sodiena[1])
        Dienas = int(nomasBeigas[0])-int(sodiena[2])
        MONTH_STATIC = 31
        YEAR_STATIC = 365
        Palika = (Gadi*YEAR_STATIC) + Menesi * MONTH_STATIC + Dienas
        Palika = str(Palika)

        if int(Palika) > 0:
            print(f"Līdz nomas beigām atlikušas aptuveni {Palika} dienas")
        else:
            print(f"Noma beidzās aptuveni {Palika[1:]} dienas atpakaļ")
        
        return int(Palika)

    def cena_Kopa(self,nomasSakums,nomasBeigas,nomasCena):
        nomasSakums = nomasSakums.split(".")
        nomasBeigas = nomasBeigas.split(".")
        Gadi = int(nomasBeigas[2])-int(nomasSakums[2])
        Menesi = int(nomasBeigas[1])-int(nomasSakums[1])
        Dienas = int(nomasBeigas[0])-int(nomasSakums[0])
        MONTH_STATIC = 31
        YEAR_STATIC = 365
        DienasKopa = (Gadi*YEAR_STATIC) + Menesi * MONTH_STATIC + Dienas

        cena = nomasCena*DienasKopa
        print("Nomas Cena Kopā:",cena)
        return cena
    
    
    def Iesniegsana(self,data,IesniegumaVeids):

        if IesniegumaVeids == "Produktu_Iesniegumi":
            IesniegumaVeids = self.produkti
        elif IesniegumaVeids == "Nomnieku_Iesniegumi":
            IesniegumaVeids = self.nomnieki
        # Iesniegto datu pārbaudes funkcija
        def parbaude(data1,data2):
            # 1. parbaude
            for v in data1:
                if v == "": return True
            # 2. parbaude
            for i in data2:
                if i == data1:
                    return True
            
        if parbaude(data,IesniegumaVeids):
            print('iesniegsana neizdevas!')
        elif not parbaude(data,IesniegumaVeids):
            IesniegumaVeids.append(data)
            print('iesniegts!')

    # Sākuma metodes izveide, kurai jābūt izsauktai katru reizi, kad ir izveidots objekts

    def ShowFrame(self,izvele):
        if izvele == "nomnieks":
            for f in self.frame1.winfo_children():
                f.destroy()
            self.IevadeNomnieks()
        elif izvele == "produkts":
            for f in self.frame1.winfo_children():
                f.destroy()
            self.IevadeProdukts()
        elif izvele == "Datu_Ievade":
            for f in self.frame1.winfo_children():
                f.destroy()
            self.DarbibasIzvele(izvele)
        elif izvele == "Datu_Izvade":
            for f in self.frame1.winfo_children():
                f.destroy()
            self.DarbibasIzvele(izvele)
        elif izvele == "nomnieks_Izvade":
            for f in self.frame1.winfo_children():
                f.destroy()
            self.Nomnieks_info()

    def sakums(self):
        if not self.Produkts_pieejams: return
        self.show_frame(self.frame1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("400x250")

        title = Label(self.frame1,text="Sveiki!\nIzvēlies Darbību:",font=('Arial Black',20))
        title.grid(pady=10)

        nomnieks=Button(self.frame1,text="Datu Ievade",font=('Arial',15),command= lambda:self.ShowFrame("Datu_Ievade"))
        nomnieks.grid(pady=10)

        if self.produkti != [] and self.produkti != []:
            nomnieks=Button(self.frame1,text="Datu Izvade",font=('Arial',15),command= lambda:self.ShowFrame("Datu_Izvade"))
            nomnieks.grid(pady=10)

        self.root.mainloop()

    def DarbibasIzvele(self,darbiba):
        self.show_frame(self.frame1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("400x300")

        title = Label(self.frame1,text="Sveiki!\nIzvēlies Darbību:",font=('Arial Black',20))
        title.grid(pady=10)

        if darbiba == "Datu_Ievade":
            nomnieks=Button(self.frame1,text="Ievadīt Nomnieku",font=('Arial',15),command= lambda:self.ShowFrame("nomnieks"))
            nomnieks.grid(pady=10)

            produkts=Button(self.frame1,text="Ievadīt Produktu",font=('Arial',15),command= lambda:self.ShowFrame("produkts"))
            produkts.grid(pady=10,padx = 10)
        elif darbiba == "Datu_Izvade":
            nomnieks=Button(self.frame1,text="Izvadīt Nomnieku",font=('Arial',15),command= lambda:self.ShowFrame("nomnieks_Izvade"))
            nomnieks.grid(pady=10)

            produkts=Button(self.frame1,text="Izvadīt Produktu",font=('Arial',15),command= lambda:self.ShowFrame("produkts"))
            produkts.grid(pady=10,padx = 10)
            
        atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
        atpakal.grid(pady=5)


    # Metode logu/rāmju aizvēršanai un tad vajadzīga loga atvēršanai
    def show_frame(self,frame):
 
        for f in self.frames:
            f.pack_forget()

        frame.pack()

    # Metode sākuma, jeb galvenā loga atvēršanai
    def back(self,frame):
        for f in frame.winfo_children():
            f.destroy()
        self.show_frame(self.mainFrame)
        self.sakums()

    # Metode ievadīto datu apskatei

    def Nomnieks_info(self):
        self.show_frame(self.frame1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("")

        def generate_Nomnieks_info(index):
            for f in self.frame1.winfo_children():
                f.destroy()
            index = int(index)
            nomnieks = self.nomnieki[index]
            NomnieksLabel = Label(self.frame1,text=(f"Nomnieka Vārds/Uzvārds: {nomnieks[0]} {nomnieks[1]}\nNomnieka Personas Kods: {nomnieks[2]}\nNomnieka Telefona Numurs: {nomnieks[3]}\nNomas Sākuma Datums: {nomnieks[4]}\nNomas Beigu Datums: {nomnieks[5]}"),font=('Arial',15))
            NomnieksLabel.grid(row=0,padx=10,pady=10)

            atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: generate_Nomnieki())
            atpakal.grid(row=1,column=1,pady=5)
            print=Button(self.frame1,text="Izprintēt Datus",font=('Arial Black',10))
            print.grid(row=1,column=0,pady=5)

        def generate_Nomnieki():
            for f in self.frame1.winfo_children():
                f.destroy()

            title = Label(self.frame1,text="Izvēlies Interesējošo Nomnieku:",font=('Arial Black',20))
            title.grid(row=0, pady=10)
            for i,nomnieks in enumerate(self.nomnieki):
                i = i + 1
                NomnieksButton = Button(self.frame1,text=(f"{str(i)}.",nomnieks[0],nomnieks[1]),font=('Arial',15),command=lambda:generate_Nomnieks_info(int(NomnieksButton.cget("text")[0:1])-1))
                NomnieksButton.grid(row=i,padx=10,pady=10)
            atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
            atpakal.grid(pady=5)

        generate_Nomnieki()

        self.root.mainloop()

    def Produkts_info(self):
        self.show_frame(self.frame1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("")

        def generate_Produkts_info(index):
            for f in self.frame1.winfo_children():
                f.destroy()
            index = int(index)
            produkts = self.produkti[index]
            ProduktsLabel = Label(self.frame1,text=(f"Nomnieka Vārds/Uzvārds: {nomnieks[0]} {nomnieks[1]}\nNomnieka Personas Kods: {nomnieks[2]}\nNomnieka Telefona Numurs: {nomnieks[3]}\nNomas Sākuma Datums: {nomnieks[4]}\nNomas Beigu Datums: {nomnieks[5]}"),font=('Arial',15))
            ProduktsLabel.grid(padx=10,pady=10)

            atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: generate_Produkti())
            atpakal.grid(pady=5)

        def generate_Produkti():
            for f in self.frame1.winfo_children():
                f.destroy()

            title = Label(self.frame1,text="Izvēlies Interesējošo Produktu:",font=('Arial Black',20))
            title.grid(row=0, pady=10)
            for i,nomnieks in enumerate(self.nomnieki):
                NomnieksButton = Button(self.frame1,text=(f"{str(i)}.",nomnieks[0],nomnieks[1]),font=('Arial',15),command=lambda:generate_Produkts_info(NomnieksButton.cget("text")[0:1]))
                i = i + 1
                NomnieksButton.grid(row=i,padx=10,pady=10)
            atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
            atpakal.grid(pady=5)

        generate_Produkti()

        self.root.mainloop()



    def Apskate(self):
        self.show_frame(self.frame3)
        self.root.geometry("")

        nomnieks=Button(self.frame1,text="Apskatīt Informāciju Par Nomnieku",font=('Arial',15))
        nomnieks.grid(pady=10)

        produkts=Button(self.frame1,text="Apskatīt Informāciju Par Produktu",font=('Arial',15))
        produkts.grid(pady=10,padx = 10)

        atpakal=Button(self.frame3,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame3))
        atpakal.grid(row=100,column=1,pady=5)
        self.root.mainloop()

    # Metode datu ievadīšanai
    def IevadeProdukts(self):
        self.show_frame(self.frame1) 
        self.root.geometry("")

        kategorija1=Label(self.frame1,text="Ievadi Produkta Kategoriju:",font=('Arial',15))
        kategorija1.grid(row=1,column=0,pady=5)
        kategorija2=Entry(self.frame1,font=('Arial',15))
        kategorija2.grid(row=1,column=1)

        nosaukums1=Label(self.frame1,text="Ievadi Produkta Nosaukumu:",font=('Arial',15))
        nosaukums1.grid(row=2,column=0,pady=5)
        nosaukums2=Entry(self.frame1,font=('Arial',15))
        nosaukums2.grid(row=2,column=1)

        raksturojums1=Label(self.frame1,text="Ievadi Produkta Tehnisko Raksturojumu:",font=('Arial',15))
        raksturojums1.grid(row=3,column=0,pady=5)
        raksturojums2=Entry(self.frame1,font=('Arial',15))
        raksturojums2.grid(row=3,column=1)

        cena1=Label(self.frame1,text="Ievadi Nomas Cenu:",font=('Arial',15))
        cena1.grid(row=4,column=0,pady=5)
        cena2=Entry(self.frame1,font=('Arial',15))
        cena2.grid(row=4,column=1)

        iesniegt=Button(self.frame1,text="Iesniegt",font=('Arial Black',10),command=lambda:self.Iesniegsana([kategorija2.get(),nosaukums2.get(),raksturojums2.get(),cena2.get()],"Produktu_Iesniegumi"))
        iesniegt.grid(row=100,column=0,pady=5)

        atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
        atpakal.grid(row=100,column=1,pady=5)

        self.root.mainloop()

    def IevadeNomnieks(self):
        self.show_frame(self.frame1) 
        self.root.geometry("")

        vards1=Label(self.frame1,text="Ievadi Nomnieka Vārdu:",font=('Arial',15))
        vards1.grid(row=2,column=0,pady=5)
        vards2=Entry(self.frame1,font=('Arial',15))
        vards2.grid(row=2,column=1)

        uzvards1=Label(self.frame1,text="Ievadi Nomnieka Uzvārdu:",font=('Arial',15))
        uzvards1.grid(row=3,column=0,pady=5)
        uzvards2=Entry(self.frame1,font=('Arial',15))
        uzvards2.grid(row=3,column=1)

        personasKods1=Label(self.frame1,text="Ievadi Nomnieka Personas kodu:",font=('Arial',15))
        personasKods1.grid(row=4,column=0,pady=5)
        personasKods2=Entry(self.frame1,font=('Arial',15))
        personasKods2.grid(row=4,column=1)

        telefonaNumurs1=Label(self.frame1,text="Ievadi Nomnieka Telefona Numuru:",font=('Arial',15))
        telefonaNumurs1.grid(row=5,column=0,pady=5)
        telefonaNumurs2=Entry(self.frame1,font=('Arial',15))
        telefonaNumurs2.grid(row=5,column=1)

        NomaSakums1=Label(self.frame1,text="Ievadi Nomas Sākuma Datumu:",font=('Arial',15))
        NomaSakums1.grid(row=6,column=0,pady=5)
        NomaSakums2=Entry(self.frame1,font=('Arial',15))
        NomaSakums2.grid(row=6,column=1)

        NomaBeigas1=Label(self.frame1,text="Ievadi Nomas Beigu Datumu:",font=('Arial',15))
        NomaBeigas1.grid(row=7,column=0,pady=5)
        NomaBeigas2=Entry(self.frame1,font=('Arial',15))
        NomaBeigas2.grid(row=7,column=1)

        iesniegt=Button(self.frame1,text="Iesniegt",font=('Arial Black',10),command=lambda:self.Iesniegsana([vards2.get(),uzvards2.get(),personasKods2.get(),telefonaNumurs2.get(),NomaSakums2.get(),NomaBeigas2.get()],"Nomnieku_Iesniegumi"))
        iesniegt.grid(row=100,column=0,pady=5)

        atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
        atpakal.grid(row=100,column=1,pady=5)

        self.root.mainloop()


    def saving(self):
        sastavdala = ""
        if os.path.isfile("Nomnieki.txt"):
            savingData2 = f"\n-Personālā datora sastāvdaļa-\nVeids: {sastavdala[0]}\nModelis: {sastavdala[1]}\nCena: {sastavdala[2]} EUR\n"
            f = open("sastavdalas.txt", "a",encoding="utf8")
            f.write(savingData2)
            f.close()
        else:
            savingData1 = f"-Personālā datora sastāvdaļa-\nVeids: {sastavdala[0]}\nModelis: {sastavdala[1]}\nCena: {sastavdala[2]} EUR\n"
            f = open("sastavdalas.txt", "w",encoding="utf8")
            f.write(savingData1)
            f.close()

#Izveidojam objektu un izsaucam sākuma metodi.

Nomnieks1 = Noma().sakums()