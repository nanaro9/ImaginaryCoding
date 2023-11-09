# Tēma - Aptiekas uzskaites sistēma
# Programmas izstrādātājs - Aleksis Počs

import os
from tkinter import *
import mysql.connector
import datetime
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
        self.db = mysql.connector.connect(host="localhost",database="aptieka",user="root",password="password")
        self.cursor = self.db.cursor()

        self.atslega = b'IeIXGVbK5fzVXI7N6n2g6heIg8Vtmby2uCZ8wneC3XY='
        self.objekts = Fernet(self.atslega)

        # Grafiskai saskarnei nepieciešamās funkcijas, metodes, dati
        self.root = Tk()
        self.root.title('Antibiotiku un klientu uzskaites sistēma.exe')

        self.frame = Frame(self.root)

        self.cursor.execute("SELECT * FROM antibiotikas_info")
        self.antibiotikas = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM pircejs_info")
        self.pirceji = self.cursor.fetchall()

        # print(self.antibiotikas,self.pirceji)

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
            self.pirkums_pircejs()
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
            # print(self.pirceji)
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

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda:self.DarbibasIzvele("ievade"))
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

            def cenaValueReplacement():
                cenaValue = ""
                if "," in cena2.get():
                    cenaValue = cena2.get().replace(",",".")
                else:
                    cenaValue = cena2.get()

                self.Iesniegsana([kategorija2.get(),nosaukums2.get(),raksturojums2.get(),float(cenaValue)],"antibiotikas_iesniegt")

            iesniegt=Button(frame,text="Iesniegt",font=('Arial Black',10),command=lambda:cenaValueReplacement())
            iesniegt.grid(row=100,column=0,pady=5)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda:self.DarbibasIzvele("ievade"))
            atpakal.grid(row=100,column=1,pady=5)


    def Iesniegsana(self,data,IesniegumaVeids):
        if IesniegumaVeids == "antibiotikas_iesniegt":
            IesniegumaVeids = self.antibiotikas
            sql = ("""
                insert into antibiotikas_info (antibiotikas_ID, antibiotikas_kategorija, antibiotikas_nosaukums, antibiotikas_raksturojums, antibiotikas_cena)
                values (%s, %s, %s, %s,%s);
                """)
            self.cursor.execute("SELECT * FROM antibiotikas_info")
        elif IesniegumaVeids == "pircejs_iesniegt":
            IesniegumaVeids = self.pirceji
            sql = ("""
                insert into pircejs_info (pircejs_ID, pircejs_vards, pircejs_uzvards, pircejs_pk, pircejs_mobilais)
                values (%s, %s, %s, %s,%s);
                """)
            self.cursor.execute("SELECT * FROM pircejs_info")

        # Iesniegto datu pārbaudes funkcija
        def parbaude(data1):
            # 1. parbaude
            for v in data1:
                if v == "": return True
            # 2. parbaude
            for i in self.cursor.fetchall():
                if list(i[1:]) == data1:
                    return True
                
        if parbaude(data):
            print('iesniegsana neizdevas!')
        elif not parbaude(data):
            IesniegumaVeids.append(data)
            if IesniegumaVeids == self.pirceji:
                self.cursor.execute("SELECT * FROM pircejs_info")
            elif IesniegumaVeids == self.antibiotikas:
                self.cursor.execute("SELECT * FROM antibiotikas_info")
            idx = self.cursor.fetchall()
            if idx == []:
                idx = 0
            else:
                idx = int(idx[-1][0])


            if idx != NONE or idx > 0:
                idx += 1 
            elif idx == NONE or idx == []:
                idx = 0

            def cryptDati(datuTabula,indekss):
                teksts = str(datuTabula[indekss])
                bTeksts = bytes(teksts,'UTF-8')
                kriptDati = self.objekts.encrypt(bTeksts)
                datuTabula[indekss] = kriptDati

            # cryptDati(data,2)
            # cryptDati(data,3)
            data.insert(0,idx)
            self.cursor.execute(sql,data)
            self.db.commit()
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
            ProduktsLabel = Label(self.frame,text=(f"Antibiotiku nosaukums: {antibiotika[1]}\nAntibiotiku kategorija: {antibiotika[2]}\nAntibiotiku raksturojums: {antibiotika[3]}\nAntibiotiku Cena: {antibiotika[4]} EUR"),font=('Arial',15))
            ProduktsLabel.grid(padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.Antibiotikas_info())
            atpakal.grid(row=100,pady=5)

        def generate_Antibiotikas():
            for f in self.frame.winfo_children():
                f.destroy()

            title = Label(self.frame,text="Izvēlies Interesējošās Antibiotikas:",font=('Arial Black',20))
            title.grid(row=0, pady=10)

            self.cursor.execute("SELECT * FROM antibiotikas_info")
            for antibiotikas in self.cursor.fetchall():
                antibiotikasButton = Button(self.frame,text=(f"{antibiotikas[0]+1}.",antibiotikas[2]),font=('Arial',15),command=lambda id=antibiotikas[0]:generate_Antibiotikas_info(id))
                antibiotikasButton.grid(row=(antibiotikas[0])+1,padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.DarbibasIzvele("izvade"))
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
            self.cursor.execute("SELECT * FROM pircejs_info")
            pircejs = self.cursor.fetchall()[index]
            # print(pircejs,index)
            pircejsLabel = Label(self.frame,text=(f"Pircēja Vārds/Uzvārds: {pircejs[1]} {pircejs[2]}\nPircēja Personas Kods: {pircejs[3]}\nPircēja Tālruņa Numurs: {pircejs[4]}"),font=('Arial',15))
            pircejsLabel.grid(padx=10,pady=10)
            
            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.Pircejs_info())
            atpakal.grid(row=100,pady=5)

        def generate_Pircejs():
            for f in self.frame.winfo_children():
                f.destroy()

            title = Label(self.frame,text="Izvēlies Interesējošo Pircēju:",font=('Arial Black',20))
            title.grid(row=0, pady=10)

            self.cursor.execute("SELECT * FROM pircejs_info")
            for pirceji in self.cursor.fetchall():
                pircejsButton = Button(self.frame,text=(f"{str(pirceji[0])}.",pirceji[1],pirceji[2]),font=('Arial',15),command=lambda id=pirceji[0]:generate_Pircejs_info(id))
                pircejsButton.grid(row=(pirceji[0])+1,padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.DarbibasIzvele("izvade"))
            atpakal.grid(row=100,pady=5)

        generate_Pircejs()

    def pirkums_pircejs(self):
        def generate_Pircejs():
            for f in self.frame.winfo_children():
                f.destroy()

            title = Label(self.frame,text="Izvēlies Interesējošo Pircēju:",font=('Arial Black',20))
            title.grid(row=0, pady=10)

            self.cursor.execute("SELECT * FROM pircejs_info")
            for pirceji in self.cursor.fetchall():
                pircejsButton = Button(self.frame,text=(f"{str(pirceji[0])}.",pirceji[1],pirceji[2]),font=('Arial',15),command=lambda id=pirceji[0]:self.pirkums_antibiotikas(id))
                pircejsButton.grid(row=(pirceji[0])+1,padx=10,pady=10)

            atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
            atpakal.grid(row=100,pady=5)

        generate_Pircejs()

    def pirkums_antibiotikas(self,indexPircejs):
        self.root.geometry("")
        for f in self.frame.winfo_children():
            f.destroy()

        title = Label(self.frame,text="Izvēlies Antibiotikas, Kuras Tika Iegādātas:",font=('Arial Black',20))
        title.grid(row=0, pady=10)

        self.cursor.execute("SELECT * FROM antibiotikas_info")
        for antibiotikas in self.cursor.fetchall():
            pircejsButton = Button(self.frame,text=(f"{str(antibiotikas[0])}.",antibiotikas[2]),font=('Arial',15),command=lambda id=antibiotikas[0]:self.pirkums(indexPircejs,id))
            pircejsButton.grid(row=(antibiotikas[0])+1,padx=10,pady=10)

        atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.pirkums_pircejs())
        atpakal.grid(row=100,pady=5)



    def pirkums(self,indexPircejs,indexAntibiotikas):
        self.root.geometry("700x150")
        for f in self.frame.winfo_children():
            f.destroy()

        pircejs = self.pirceji[indexPircejs]
        antibiotikas = self.antibiotikas[indexAntibiotikas]
        datums = str(datetime.datetime.now())[:-7]

        sql = ("""
        insert into pirkums_info (pirkums_ID, pircejs_ID, antibiotikas_ID, pirkums_Datums)
        values (%s, %s, %s, %s);
            """)
        
        data = [indexPircejs,indexAntibiotikas,datums]
        self.cursor.execute("SELECT * FROM pirkums_info")
        indexPirkums = self.cursor.fetchall()
        if indexPirkums == NONE or indexPirkums == []:
            indexPirkums = 0
        else:
            if indexPirkums[-1][0] > 0 or indexPirkums [-1][0] != NONE:
                indexPirkums = indexPirkums[-1][0]
                indexPirkums += 1

        data.insert(0,indexPirkums)
        self.cursor.execute(sql,data)
        self.db.commit()

        title = Label(self.frame,text="Pirkums Tika Veiksmīgi Ierakstīts Datubāzē!",font=('Arial Black',20))
        title.grid(row=0, pady=10)

        atpakal=Button(self.frame,text="Atpakal",font=('Arial Black',10),command=lambda: self.back())
        atpakal.grid(row=100,pady=5)
        

SystemAptieka = Aptieka().Main()