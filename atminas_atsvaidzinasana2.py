import json
import datetime

x = datetime.datetime.now()
print()

def registracija():
    vards_uzvards = input("Ievadi savu vārdu un uzvārdu:\n")
    return vards_uzvards

vardsUNuzvards = registracija()
rezultati = []

def darbiba(action):
    a = int(input("Ievadi pirmo skaitli: "))
    b = int(input("Ievadi otro skaitli: "))

    if action == "1":
        print("Rezultāts:",a + b)
        return a+b
    elif action == "2":
        print("Rezultāts:",a - b)
    elif action == "3":
        print("Rezultāts:",a / b)
        return a/b
    elif action == "4":
        print("Rezultāts:",a * b)
        return a*b
    

def saving():
    lastData = vardsUNuzvards,"| Rezultāti",rezultati,"| Datums:",str(x)[:19]


while True:
    # print("Rezultati list -", rezultati)
    print('\nIzvelies darbibu: ')
    print(' 1 - Saskaitīt \n 2 - Atņemt \n 3 - Dalīt \n 4 - Reizināt \n 5 - Iziet un Saglabāt')
    izvele = input(" ")
    if izvele == '1' or izvele == '2' or izvele == '3' or izvele == '4':
        rezultati.append(str(darbiba(izvele)))
    elif izvele == '5':
        saving()
        break
    else:
        print('\nIzvelies darbibu velreiz!')


print('Lietotājs ir veiksmīgi pievienots!\nPaldies par programmas izmantošanu!')