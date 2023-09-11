from tabulate import tabulate
from tkinter import *

class Sastavdalas():
    def __init__(self,Veids,Modelis,Cena):
        self.Veids = Veids
        self.Modelis = Modelis
        self.Cena = Cena 

    def Apskate(self):
        return [self.Veids,self.Modelis,self.Cena]
    
iesniegumi = 0
dators = []

root = Tk()
root.title = "Datora Sastavdalas.exe"

mainFrame = Frame(root)
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)

def show_frame(frame):
    # Hide all frames
    for f in frames:
        f.pack_forget()
    
    # Show the selected frame
    frame.pack()

frames = [mainFrame,frame1,frame2,frame3]

def Ievade():
    show_frame(frame1)
    root.geometry()

    veidi1=Label(frame1,text="Ievadi Komponentes Veidu:",font=('Arial',15))
    veidi1.grid(row=1,column=0,pady=5)
    veidi2=Entry(frame1,font=('Arial',15))
    veidi2.grid(row=1,column=1)

    modelis1=Label(frame1,text="Ievadi Komponentes Modeli:",font=('Arial',15))
    modelis1.grid(row=2,column=0,pady=5)
    modelis2=Entry(frame1,font=('Arial',15))
    modelis2.grid(row=2,column=1)

    cena1=Label(frame1,text="Ievadi Komponentes Cenu:",font=('Arial',15))
    cena1.grid(row=3,column=0,pady=5)
    cena2=Entry(frame1,font=('Arial',15))
    cena2.grid(row=3,column=1)


    def Iesniegsana():
        global iesniegumi
        iesniegumi += 1
        data = [veidi2.get().upper(),modelis2.get(),cena2.get()]

        def parbaude(data1,data2):
            for i in data2:
                if i == data1:
                    return True
                
        if iesniegumi <= 1:
            dators.append([veidi2.get().upper(),modelis2.get(),cena2.get()])
            print('iesniegts!')
        elif iesniegumi > 1 and not parbaude(data,dators):
            print('iesniegumu vairak par 1, Iesniegumi atskiras, iesniegts!')
            dators.append([veidi2.get().upper(),modelis2.get(),cena2.get()])
        elif iesniegumi > 1 and parbaude(data,dators):
            print('iesniegsana neizdevas!')
        # output.config(text=(tabulate(dators, headers=['Veids', 'Modelis', 'Cena'])))
        
    def back():
        show_frame(mainFrame)
        Sakums()

    

    iesniegt=Button(frame1,text="Iesniegt",font=('Arial Black',10),command=Iesniegsana)
    iesniegt.grid(row=5,column=0,pady=5)

    atpakal=Button(frame1,text="Atpakal",font=('Arial Black',10),command=back)
    atpakal.grid(row=5,column=1,pady=5)

    # outputFrame=LabelFrame(frame1,text='Tabula')
    # outputFrame.grid(row=5,column=0)

    # output=Label(outputFrame,text=(tabulate(dators, headers=['Veids', 'Modelis', 'Cena'])))
    # output.pack()
    root.mainloop()



def Sakums():
    show_frame(mainFrame)
    root.geometry("500x200")

    ievadi=Button(mainFrame,text="ievadi",font=('Arial',15),command=lambda:window(1))
    ievadi.grid(row=1,column=0,pady=10)


    edit=Button(mainFrame,text="rediģē",font=('Arial',15),command=lambda:window(2))
    edit.grid(row=2,column=0,pady=10)

    def window(windowNum):
        if windowNum == 1:
            show_frame(frame1)
            Ievade()
        if windowNum == 3:
            show_frame(frame3)
            Inspect()
        # if windowNum == 2:
        #     show_frame(frame2)

    inspect=Button(mainFrame,text="apskati",font=('Arial',15),command=lambda:window(3))
    inspect.grid(row=3,column=0,pady=10)

    root.mainloop()


def Inspect():
    show_frame(frame3)
    root.geometry("800x600")
    outputFrame=LabelFrame(frame3,text='Tabula')
    outputFrame.grid(row=1,column=1)

    output=Label(outputFrame,text=(tabulate(dators, headers=['Veids', 'Modelis', 'Cena'])))
    output.pack()
    # root.mainloop()




Sakums()
# Inspect()
# print(tabulate(dators, headers=['Veids', 'Modelis', 'Cena']))