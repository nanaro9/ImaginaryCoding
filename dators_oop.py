from tabulate import tabulate
from tkinter import *

class Sastavdalas():
    def __init__(self,Veids,Modelis,Cena):
        self.Veids = Veids
        self.Modelis = Modelis
        self.Cena = Cena 

    def Apskate(self):
        return [self.Veids,self.Modelis,self.Cena]

dators = []

# print(tabulate([dators1.Apskate(),dators2.Apskate()], headers=['Veids', 'Modelis', 'Cena']))

def Sakums():
    logs = Tk()
    logs.title = "Datora Sastavdalas.exe"
    logs.geometry('800x600')
    logs.configure(bg="#6699ff")
    logs.resizable(False, False)

    Title = Label(logs, text="Ievadiet Datora Sastavdalas Datus!",width=100,height=4,font="Arial")
    Title.pack()

    def submit():
        return Label(logs, text="Submitted!").pack()

    nameTf = Entry(logs)
    nameTf.pack()

    submitBtn = Button(logs, text="submit", command=submit)
    submitBtn.pack()

    logs.mainloop()



Sakums()

