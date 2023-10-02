# Tēma - Aptiekas uzskaites sistēma
# Programmas izstrādātājs - Aleksis Počs

import os
from tkinter import *

class Aptieka():
    # Konstruktora izveide
    def __init__(self):
        self.Antibiotiku_kategorija = ""
        self.Antibiotiku_nosaukums = ""
        self.Antibiotiku_raksturojums = ""
        self.Antibiotiku_cena = ""
        self.Pirceja_vārds= ""
        self.Pirceja_uzvārds = ""
        self.Priceja_pk = ""
        self.Pirceja_mobilais = ""

        # Grafiskai saskarnei nepieciešamās funkcijas, metodes, dati
        self.root = Tk()
        self.root.title('Antibiotiku un klientu uzskaites sistēma.exe')

        self.frame = Frame(self.root)

        self.antibiotikas = []
        self.pirceji = []

    def LoguMaina(self,*izvele):
        # Neizmantojamo logrīku iznīcināšana labākai veiktspējai

        for f in self.frame.winfo_children():
            f.destroy()  
        self.frame.pack_forget()

        if not izvele:
            self.frame.pack()
            return
        
        if izvele[0] == "antibiotikas_izvade":
            self.Antibiotikas_info()
        elif izvele[0] == "pircejs_izvade":
            self.Pircejs_info()
        elif izvele[0] == "printesana":
            self.pirkums_info_print()
        else:
            self.DarbibasIzvele(izvele[0])
        self.frame.pack()


    def Main(self):
        self.LoguMaina()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("500x325")

        title = Label(self.frame,text="Sveicināti Aptiekas Sistēmā!\nIzvēlies Darbību:",font=('Arial Black',20))
        title.grid(pady=10)

        datu_Ievade=Button(self.frame,text="Datu Ievade",font=('Arial',15),command=lambda: self.LoguMaina("ievade"))
        datu_Ievade.grid(pady=10)

        datu_Izvade=Button(self.frame,text="Datu Izvade",font=('Arial',15),command=lambda:izvadesParbaude(datu_Izvade))
        datu_Izvade.grid(pady=10)

        datu_Printesana=Button(self.frame,text="Datu Printēšana",font=('Arial',15),command=lambda:izvadesParbaude(datu_Printesana))
        datu_Printesana.grid(pady=10)

        def izvadesParbaude(widget):
            if self.pirceji != [] and self.antibiotikas != []:
                if widget.cget("text") == "Datu Izvade": 
                    self.LoguMaina("izvade")
                elif widget.cget("text") == "Datu Printēšana":
                    self.LoguMaina("printesana")
            else:
                widget.configure(text="Nav Pircēju un Antibiotiku Datu!")


        self.root.mainloop()

    def back(self):
            for f in self.frame.winfo_children():
                f.destroy()
            self.LoguMaina()
            self.Main()

    def DarbibasIzvele(self,darbiba):
        self.LoguMaina()
        self.root.geometry("500x300")

        title = Label(self.frame,text="Sveicināti Aptiekas Sistēmā!\nIzvēlies Darbību:",font=('Arial Black',20))
        title.grid(pady=10)

        atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=self.back)
        atpakal.grid(row=100,column=0,pady=5)
        if darbiba == "ievade":

            pircejs=Button(self.frame,text="Ievadīt Pircēju",font=('Arial',15),command= lambda:self.LoguMaina("pircejs"))
            pircejs.grid(row=1,pady=10)

            antibiotikas=Button(self.frame,text="Ievadīt Antibiotikas",font=('Arial',15),command= lambda:self.LoguMaina("antibiotikas"))
            antibiotikas.grid(row=2,pady=10,padx = 10)

        elif darbiba == "izvade":
            pircejs=Button(self.frame,text="Izvadīt Pircēju",font=('Arial',15),command= lambda:self.LoguMaina("pircejs_izvade"))
            pircejs.grid(row=1,pady=10)

            antibiotikas=Button(self.frame,text="Izvadīt Antibiotikas",font=('Arial',15),command= lambda:self.LoguMaina("antibiotikas_izvade"))
            antibiotikas.grid(row=2,pady=10,padx = 10)

        elif darbiba == "pircejs":
            self.LoguMaina()
            self.root.geometry("")
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)   
            frame = self.frame

            vards1=Label(frame,text="Ievadi Pricēja Vārdu:",font=('Arial',15))
            vards1.grid(row=1,column=0,pady=5)
            vards2=Entry(self.frame,font=('Arial',15))
            vards2.grid(row=1,column=1)

            uzvards1=Label(frame,text="Ievadi Pricēja Uzvārdu:",font=('Arial',15))
            uzvards1.grid(row=2,column=0,pady=5)
            uzvards2=Entry(frame,font=('Arial',15))
            uzvards2.grid(row=2,column=1)

            personas_kods1=Label(frame,text="Ievadi Pricēja Personas Kodu:",font=('Arial',15))
            personas_kods1.grid(row=3,column=0,pady=5)
            personas_kods2=Entry(frame,font=('Arial',15))
            personas_kods2.grid(row=3,column=1)

            mobilais1=Label(frame,text="Ievadi Pricēja Tālruni:",font=('Arial',15))
            mobilais1.grid(row=4,column=0,pady=5)
            mobilais2=Entry(frame,font=('Arial',15))
            mobilais2.grid(row=4,column=1)

            iesniegt=Button(frame,text="Iesniegt",font=('Arial Black',10),command=lambda:self.Iesniegsana([vards2.get(),uzvards2.get(),personas_kods2.get(),mobilais2.get()],"pircejs_iesniegt"))
            iesniegt.grid(row=100,column=0,pady=5)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=self.back)
            atpakal.grid(row=100,column=1,pady=5)

        elif darbiba == "antibiotikas":
            self.LoguMaina()
            self.root.geometry("")
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)   
            frame = self.frame

            kategorija1=Label(frame,text="Ievadi Antibiotiku Kategoriju:",font=('Arial',15))
            kategorija1.grid(row=1,column=0,pady=5)
            kategorija2=Entry(frame,font=('Arial',15))
            kategorija2.grid(row=1,column=1)

            nosaukums1=Label(frame,text="Ievadi Antibiotiku Nosaukumu:",font=('Arial',15))
            nosaukums1.grid(row=2,column=0,pady=5)
            nosaukums2=Entry(frame,font=('Arial',15))
            nosaukums2.grid(row=2,column=1)

            raksturojums1=Label(frame,text="Ievadi Antibiotika Raksturojumu:",font=('Arial',15))
            raksturojums1.grid(row=3,column=0,pady=5)
            raksturojums2=Entry(frame,font=('Arial',15))
            raksturojums2.grid(row=3,column=1)

            cena1=Label(frame,text="Ievadi Antibiotiku Cenu:",font=('Arial',15))
            cena1.grid(row=4,column=0,pady=5)
            cena2=Entry(frame,font=('Arial',15))
            cena2.grid(row=4,column=1)

            iesniegt=Button(frame,text="Iesniegt",font=('Arial Black',10),command=lambda:self.Iesniegsana([kategorija2.get(),nosaukums2.get(),raksturojums2.get(),cena2.get()],"antibiotikas_iesniegt"))
            iesniegt.grid(row=100,column=0,pady=5)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=self.back)
            atpakal.grid(row=100,column=1,pady=5)


    def Iesniegsana(self,data,IesniegumaVeids):
        if IesniegumaVeids == "antibiotikas_iesniegt":
            IesniegumaVeids = self.antibiotikas
        elif IesniegumaVeids == "pircejs_iesniegt":
            IesniegumaVeids = self.pirceji

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


    def Antibiotikas_info(self):
        self.LoguMaina()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("")

        def generate_Antibiotikas_info(index):
            for f in self.frame.winfo_children():
                f.destroy()
            index = int(index)
            antibiotika = self.antibiotikas[index]
            ProduktsLabel = Label(self.frame,text=(f"Antibiotiku nosaukums: {antibiotika[0]}\nAntibiotiku kategorija: {antibiotika[1]}\nAntibiotiku raksturojums: {antibiotika[2]}\nAntibiotiku Cena: {antibiotika[3]} EUR"),font=('Arial',15))
            ProduktsLabel.grid(padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
            atpakal.grid(row=100,pady=5)

        def generate_Antibiotikas():
            for f in self.frame.winfo_children():
                f.destroy()

            title = Label(self.frame,text="Izvēlies Interesējošās Antibiotikas:",font=('Arial Black',20))
            title.grid(row=0, pady=10)

            for i,antibiotikas in enumerate(self.antibiotikas):
                i = i + 1
                antibiotikasButton = Button(self.frame,text=(f"{str(i)}.",antibiotikas[0],antibiotikas[1]),font=('Arial',15),command=lambda:generate_Antibiotikas_info(int(antibiotikasButton.cget("text")[0:1])-1))
                antibiotikasButton.grid(row=i,padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
            atpakal.grid(row=100,pady=5)

        generate_Antibiotikas()



    
    def Pircejs_info(self):
        self.LoguMaina()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("")

        def generate_Pircejs_info(index):
            for f in self.frame.winfo_children():
                f.destroy()
            index = int(index)
            pircejs = self.pirceji[index]
            pircejsLabel = Label(self.frame,text=(f"Pircēja Vārds/Uzvārds: {pircejs[0]} {pircejs[1]}\nPircēja Personas Kods: {pircejs[2]}\nPircēja Tālruņa Numurs: {pircejs[3]}"),font=('Arial',15))
            pircejsLabel.grid(padx=10,pady=10)
            
            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
            atpakal.grid(row=100,pady=5)

        def generate_Pircejs():
            for f in self.frame.winfo_children():
                f.destroy()

            title = Label(self.frame,text="Izvēlies Interesējošo Pircēju:",font=('Arial Black',20))
            title.grid(row=0, pady=10)

            for i,pircejs in enumerate(self.pirceji):
                i = i + 1
                pircejsButton = Button(self.frame,text=(f"{str(i)}.",pircejs[0],pircejs[1]),font=('Arial',15),command=lambda:generate_Pircejs_info(int(pircejsButton.cget("text")[0:1])-1))
                pircejsButton.grid(row=i,padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
            atpakal.grid(row=100,pady=5)

        generate_Pircejs()

    def pirkums_info_print(self):
        def generate_Pircejs():
            for f in self.frame.winfo_children():
                f.destroy()

            title = Label(self.frame,text="Izvēlies Interesējošo Pircēju:",font=('Arial Black',20))
            title.grid(row=0, pady=10)

            for i,pircejs in enumerate(self.pirceji):
                i = i + 1
                pircejsButton = Button(self.frame,text=(f"{str(i)}.",pircejs[0],pircejs[1]),font=('Arial',15),command=lambda:print(int(pircejsButton.cget("text")[0:1])-1))
                pircejsButton.grid(row=i,padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
            atpakal.grid(row=100,pady=5)

        generate_Pircejs()

        def print(index):
            index = int(index)
            pircejs = self.pirceji[index]
            antibiotikas = self.antibiotikas[index]
            if os.path.isfile("pirkumi.txt"):
                savingData2 = f"\n-Pirkuma Čeks-\n\nPircēja Vārds/Uzvārds: {pircejs[0]} {pircejs[1]}\nPircēja Personas Kods: {pircejs[2]}\nPircēja Tālruņa Numurs: {pircejs[3]}\n\nAntibiotiku Nosaukums: {antibiotikas[0]}\nAntibiotiku Kategorija: {antibiotikas[1]}\nAntibiotiku raksturojums: {antibiotikas[2]}\nAntibiotiku Cena: {antibiotikas[3]} EUR\n\nPaldies Par Pirkumu!"
                f = open("pirkumi.txt", "a",encoding="utf8")
                f.write(savingData2)
                f.close()
            else:
                savingData1 = f"-Pirkuma Čeks-\n\nPircēja Vārds/Uzvārds: {pircejs[0]} {pircejs[1]}\nPircēja Personas Kods: {pircejs[2]}\nPircēja Tālruņa Numurs: {pircejs[3]}\n\nAntibiotiku Nosaukums: {antibiotikas[0]}\nAntibiotiku Kategorija: {antibiotikas[1]}\nAntibiotiku raksturojums: {antibiotikas[2]}\nAntibiotiku Cena: {antibiotikas[3]} EUR\n\nPaldies Par Pirkumu!"
                f = open("pirkumi.txt", "w",encoding="utf8")
                f.write(savingData1)
                f.close()
        

SystemAptieka = Aptieka().Main()