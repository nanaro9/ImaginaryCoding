from tabulate import tabulate
from tkinter import *
import os
from datetime import *

# Klases izveide ar grafiskās saskarnes īpašībām un vajadzīgajiem datiem tālākajām darbībām
class Noma():
    def __init__(self):
        self.root = Tk()

        self.iesniegumi = 0
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

    # Sākuma metodes izveide, kurai jābūt izsauktai katru reizi, kad ir izveidots objekts
    def sakums(self):
        if not self.Produkts_pieejams: return
        self.show_frame(self.mainFrame)
        self.root.geometry("400x200")

        ievadi=Button(self.mainFrame,text="Datu ievade",font=('Arial',15),command=lambda:window(1))
        ievadi.grid(row=1,column=0,pady=10)


        edit=Button(self.mainFrame,text="Datu Izvade",font=('Arial',15),command=lambda:window(2))
        edit.grid(row=2,column=0,pady=10)

        # Citu logu atvēršana pēc sekojošas pogas uzspiezšanas
        def window(windowNum):
            if windowNum == 1:
                self.show_frame(self.frame1)
                self.Ievade()
            if windowNum == 3:
                self.show_frame(self.frame3)
                self.Apskate()
            if windowNum == 2:
                self.show_frame(self.frame2)
                self.Edit()

        inspect=Button(self.mainFrame,text="Datu Printēšana",font=('Arial',15),command=lambda:window(3))
        inspect.grid(row=3,column=0,pady=10)

        self.root.mainloop()

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
    def Apskate(self):
        self.show_frame(self.frame3)
        self.root.geometry("")
        # outputFrame=LabelFrame(self.frame3,text='Tabula')
        # outputFrame.grid(row=1,column=1)

        # output=Label(outputFrame,text=(tabulate(self.dators, headers=['Veids', 'Modelis', 'Cena'])),font="Arial,20")
        # output.pack()

        # atpakal=Button(self.frame3,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame3))
        # atpakal.grid(row=2,column=1,pady=5)
        self.root.mainloop()


    def Ievade(self):
        self.show_frame(self.frame1) 
        self.root.geometry("400x100")

        def ShowNomnieksIevade(izvele):
            if izvele == "nomnieks":
                for f in self.frame1.winfo_children():
                    f.destroy()
                self.IevadeNomnieks()
            elif izvele == "produkts":
                for f in self.frame1.winfo_children():
                    f.destroy()
                self.IevadeProdukts()

        nomnieks=Button(self.frame1,text="Ievadīt Nomnieku",font=('Arial',15),command= lambda:ShowNomnieksIevade("nomnieks"))
        nomnieks.grid(row=1,column=0,pady=10)

        produkts=Button(self.frame1,text="Ievadīt Produktu",font=('Arial',15),command= lambda:ShowNomnieksIevade("produkts"))
        produkts.grid(row=1,column=1,pady=10,padx = 10)


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

        def Iesniegsana():
            self.iesniegumi += 1
            data = [kategorija2.get(),nosaukums2.get(),raksturojums2.get(),cena2.get()]

            # Iesniegto datu pārbaudes funkcija
            def parbaude(data1,data2):
                for i in data2:
                    if i == data1:
                        return True
                    
            if self.iesniegumi <= 1:
                self.produkti.append(data)
                print('iesniegts!')
            elif self.iesniegumi > 1 and not parbaude(data,self.produkti):
                print('iesniegumu vairak par 1, Iesniegumi atskiras, iesniegts!')
                self.produkti.append(data)
            elif self.iesniegumi > 1 and parbaude(data,self.produkti):
                print('iesniegsana neizdevas!')

        iesniegt=Button(self.frame1,text="Iesniegt",font=('Arial Black',10))
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



        # Datu iesniegšanas funkcija
        def Iesniegsana():
            self.iesniegumi += 1
            data = [vards2.get().upper(),uzvards2.get(),personasKods2.get(),telefonaNumurs2.get(),NomaSakums2.get(),NomaBeigas2.get()]

            # Iesniegto datu pārbaudes funkcija
            def parbaude(data1,data2):
                for i in data2:
                    if i == data1:
                        return True
                    
            if self.iesniegumi <= 1:
                self.nomnieki.append(data)
                print('iesniegts!')
            elif self.iesniegumi > 1 and not parbaude(data,self.nomnieki):
                print('iesniegumu vairak par 1, Iesniegumi atskiras, iesniegts!')
                self.nomnieki.append(data)
            elif self.iesniegumi > 1 and parbaude(data,self.nomnieki):
                print('iesniegsana neizdevas!')
            
        iesniegt=Button(self.frame1,text="Iesniegt",font=('Arial Black',10),command=Iesniegsana)
        iesniegt.grid(row=100,column=0,pady=5)

        atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
        atpakal.grid(row=100,column=1,pady=5)

        self.root.mainloop()

    # Funkcija, kura saglabā tieši tos datus, pie kuriem bija uzspiesta poga.
    # def saving(index):
    #     sastavdala = self.dators[index]
    #     if os.path.isfile("sastavdalas.txt"):
    #         savingData2 = f"\n-Personālā datora sastāvdaļa-\nVeids: {sastavdala[0]}\nModelis: {sastavdala[1]}\nCena: {sastavdala[2]} EUR\n"
    #         f = open("sastavdalas.txt", "a",encoding="utf8")
    #         f.write(savingData2)
    #         f.close()
    #     else:
    #         savingData1 = f"-Personālā datora sastāvdaļa-\nVeids: {sastavdala[0]}\nModelis: {sastavdala[1]}\nCena: {sastavdala[2]} EUR\n"
    #         f = open("sastavdalas.txt", "w",encoding="utf8")
    #         f.write(savingData1)
    #         f.close()

    # Funkcija, izveido ievietoto datu rīkus. Katriem datiem savs rīks.
    # def generate_Values():
    #     for i,v in enumerate(self.dators):
    #             output=Label(self.frame2,text=("Veids:",v[0],"Modelis:",v[1],"Cena:",v[2]),font="Arial,20")
    #             outputBtn=Button(self.frame2,text="Rediģēt:",font=("Arial Black",12))
    #             saveBtn=Button(self.frame2,text="Saglabāt",font=("Arial Black",10))
    #             outputBtn.configure(command=lambda button=outputBtn:editValue(button.grid_info()['row']))
    #             saveBtn.configure(command=lambda button=saveBtn:saving(button.grid_info()['row']))
    #             output.grid(row=i,column=1,padx=5)
    #             outputBtn.grid(row=i,column=0,padx=5)
    #             saveBtn.grid(row=i,column=2,padx=5)

    #     atpakal=Button(self.frame2,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame2))
    #     atpakal.grid(row=10,column=1,pady=5)

#Izveidojam objektu un izsaucam sākuma metodi.

Nomnieks1 = Noma().sakums()