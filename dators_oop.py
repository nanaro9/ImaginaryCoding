from tabulate import tabulate
from tkinter import *
import os

# Klases izveide ar grafiskās saskarnes īpašībām un vajadzīgajiem datiem tālākajām darbībām
class Sastavdalas():
    def __init__(self,Iesniegumi,Dators):
        self.root = Tk()

        self.mainFrame = Frame(self.root)
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)
        self.iesniegumi = Iesniegumi
        self.dators = Dators
        self.frames = [self.mainFrame,self.frame1,self.frame2,self.frame3]
    

    # Sākuma metodes izveide, kurai jābūt izsauktai katru reizi, kad ir izveidots objekts
    def sakums(self):
        self.show_frame(self.mainFrame)
        self.root.geometry("400x200")

        ievadi=Button(self.mainFrame,text="Ievadi",font=('Arial',15),command=lambda:window(1))
        ievadi.grid(row=1,column=0,pady=10)


        edit=Button(self.mainFrame,text="Rediģē / Saglabā",font=('Arial',15),command=lambda:window(2))
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

        inspect=Button(self.mainFrame,text="Apskati",font=('Arial',15),command=lambda:window(3))
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
        outputFrame=LabelFrame(self.frame3,text='Tabula')
        outputFrame.grid(row=1,column=1)

        output=Label(outputFrame,text=(tabulate(self.dators, headers=['Veids', 'Modelis', 'Cena'])),font="Arial,20")
        output.pack()

        atpakal=Button(self.frame3,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame3))
        atpakal.grid(row=2,column=1,pady=5)
        self.root.mainloop()

    # Metode datu ievadīšanai
    def Ievade(self):
        self.show_frame(self.frame1) 
        self.root.geometry("")

        veidi1=Label(self.frame1,text="Ievadi Komponentes Veidu:",font=('Arial',15))
        veidi1.grid(row=1,column=0,pady=5)
        veidi2=Entry(self.frame1,font=('Arial',15))
        veidi2.grid(row=1,column=1)

        modelis1=Label(self.frame1,text="Ievadi Komponentes Modeli:",font=('Arial',15))
        modelis1.grid(row=2,column=0,pady=5)
        modelis2=Entry(self.frame1,font=('Arial',15))
        modelis2.grid(row=2,column=1)

        cena1=Label(self.frame1,text="Ievadi Komponentes Cenu:",font=('Arial',15))
        cena1.grid(row=3,column=0,pady=5)
        cena2=Entry(self.frame1,font=('Arial',15))
        cena2.grid(row=3,column=1)

        # Datu iesniegšanas funkcija
        def Iesniegsana():
            self.iesniegumi += 1
            data = [veidi2.get().upper(),modelis2.get(),cena2.get()]

            # Iesniegto datu pārbaudes funkcija
            def parbaude(data1,data2):
                for i in data2:
                    if i == data1:
                        return True
                    
            if self.iesniegumi <= 1:
                self.dators.append([veidi2.get().upper(),modelis2.get(),cena2.get()])
                print('iesniegts!')
            elif self.iesniegumi > 1 and not parbaude(data,self.dators):
                print('iesniegumu vairak par 1, Iesniegumi atskiras, iesniegts!')
                self.dators.append([veidi2.get().upper(),modelis2.get(),cena2.get()])
            elif self.iesniegumi > 1 and parbaude(data,self.dators):
                print('iesniegsana neizdevas!')
            
        iesniegt=Button(self.frame1,text="Iesniegt",font=('Arial Black',10),command=Iesniegsana)
        iesniegt.grid(row=5,column=0,pady=5)

        atpakal=Button(self.frame1,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame1))
        atpakal.grid(row=5,column=1,pady=5)

        self.root.mainloop()

    # Metode datu rediģēšanai
    def Edit(self):
        self.show_frame(self.frame2)
        self.root.geometry("")

        # Funkcija, kura attīra atmiņu, kura tika izmantota ar nevajadzīgiem papildu rīkiem (widgetiem - pogām, ievades laukiem)
        def editValue(index):
            for i in self.frame2.winfo_children():
                i.destroy()

            veidi1=Label(self.frame2,text="Ievadi Komponentes Veidu:",font=('Arial',15))
            veidi1.grid(row=index+1,column=0,pady=5)
            veidi2=Entry(self.frame2,font=('Arial',15))
            veidi2.grid(row=index+1,column=1)

            modelis1=Label(self.frame2,text="Ievadi Komponentes Modeli:",font=('Arial',15))
            modelis1.grid(row=index+2,column=0,pady=5)
            modelis2=Entry(self.frame2,font=('Arial',15))
            modelis2.grid(row=index+2,column=1)

            cena1=Label(self.frame2,text="Ievadi Komponentes Cenu:",font=('Arial',15))
            cena1.grid(row=index+3,column=0,pady=5)
            cena2=Entry(self.frame2,font=('Arial',15))
            cena2.grid(row=index+3,column=1)

            # Iesniegšanas funkcija, kurā tiek pārbaudīti dati, kuriem ir jābūt rediģētiem.
            def submit():
                data = [veidi2.get().upper(),modelis2.get(),cena2.get()]
                if data != ["","",""]:
                    # Pārbaudes funkcija
                    def parbaude(data1,data2):
                        for i in data2:
                            if i == data1:
                                return True
                    if not parbaude(data,self.dators):
                        # Ja tādu datu nebija, ja jaunie dati ir jauni, tad tiek vecie dati tiek aizstāti.
                        self.dators[index] = data

                        frames = [veidi1,veidi2,modelis1,modelis2,cena1,cena2,iesniegt]
                        # pēc visām mahinācijām visi logi attīras, lai neizmantotu lieki atmiņu (sava veida optimizācija)
                        for f in frames:
                            f.destroy()
                        # Atkal izveidojas vajadzīgie rīki pēc rediģēšanas.
                        generate_Values()

            iesniegt=Button(self.frame2,text="Iesniegt",font=('Arial Black',10),command=submit)
            iesniegt.grid(row=10,column=0,pady=5)

        # Funkcija, kura saglabā tieši tos datus, pie kuriem bija uzspiesta poga.
        def saving(index):
            sastavdala = self.dators[index]
            if os.path.isfile("sastavdalas.txt"):
                savingData2 = f"\n-Personālā datora sastāvdaļa-\nVeids: {sastavdala[0]}\nModelis: {sastavdala[1]}\nCena: {sastavdala[2]} EUR\n"
                f = open("sastavdalas.txt", "a",encoding="utf8")
                f.write(savingData2)
                f.close()
            else:
                savingData1 = f"-Personālā datora sastāvdaļa-\nVeids: {sastavdala[0]}\nModelis: {sastavdala[1]}\nCena: {sastavdala[2]} EUR\n"
                f = open("sastavdalas.txt", "w",encoding="utf8")
                f.write(savingData1)
                f.close()

        # Funkcija, izveido ievietoto datu rīkus. Katriem datiem savs rīks.
        def generate_Values():
            for i,v in enumerate(self.dators):
                    output=Label(self.frame2,text=("Veids:",v[0],"Modelis:",v[1],"Cena:",v[2]),font="Arial,20")
                    outputBtn=Button(self.frame2,text="Rediģēt:",font=("Arial Black",12))
                    saveBtn=Button(self.frame2,text="Saglabāt",font=("Arial Black",10))
                    outputBtn.configure(command=lambda button=outputBtn:editValue(button.grid_info()['row']))
                    saveBtn.configure(command=lambda button=saveBtn:saving(button.grid_info()['row']))
                    output.grid(row=i,column=1,padx=5)
                    outputBtn.grid(row=i,column=0,padx=5)
                    saveBtn.grid(row=i,column=2,padx=5)

            atpakal=Button(self.frame2,text="Atpakal",font=('Arial Black',10),command=lambda: self.back(self.frame2))
            atpakal.grid(row=10,column=1,pady=5)

        generate_Values()
        self.root.mainloop()

#Izveidojam objektu un izsaucam sākuma metodi.
MyPc = Sastavdalas(0,[]).sakums()