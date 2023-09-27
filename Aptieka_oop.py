# Tēma - Aptiekas uzskaites sistēma
# Programmas izstrādātājs - Aleksis Počs

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
        
        self.DarbibasIzvele(izvele[0])
        self.frame.pack()


    def Main(self):
        self.LoguMaina()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)   
        self.root.geometry("500x250")

        title = Label(self.frame,text="Sveicināti Aptiekas Sistēmā!\nIzvēlies Darbību:",font=('Arial Black',20))
        title.grid(pady=10)

        datu_Ievade=Button(self.frame,text="Datu Ievade",font=('Arial',15),command=lambda: self.LoguMaina("ievade"))
        datu_Ievade.grid(pady=10)

        datu_Izvade=Button(self.frame,text="Datu Izvade",font=('Arial',15),command=lambda:izvadesParbaude())
        datu_Izvade.grid(pady=10)

        def izvadesParbaude():
            if self.pirceji != [] and self.antibiotikas != []:
                self.LoguMaina("izvade")
            else:
                datu_Izvade.configure(text="Nav Pircēju un Antibiotiku Datu!")
                

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

    

SystemAptieka = Aptieka().Main()