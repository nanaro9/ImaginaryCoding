import datetime
import os

def registracija():
    vards_uzvards = input("Ievadi savu vārdu un uzvārdu: ")
    return vards_uzvards

vardsUNuzvards = registracija()
rezultati = []

def saving():
    lastData = str(vardsUNuzvards)+" | Rezultāti: "+str(rezultati)+" | Datums: "+str(datetime.datetime.now())[:19]+"\n"
    if os.path.isfile("lietotaji.txt"):
        print("Fails Jau Eksistē!")
        f = open("lietotaji.txt", "a",encoding="utf8")
        f.write(lastData)
        f.close()
    else:
        f = open("lietotaji.txt", "w",encoding="utf8")
        f.write(lastData)
        f.close()



    return lastData

def darbiba(action):
    a = int(input("Ievadi pirmo skaitli: "))
    b = int(input("Ievadi otro skaitli: "))

    if action == "1":
        print("Rezultāts:",a + b)
        return a+b
    elif action == "2":
        print("Rezultāts:",a - b)
        return a-b
    elif action == "3":
        print("Rezultāts:",a / b)
        return a/b
    elif action == "4":
        print("Rezultāts:",a * b)
        return a*b
    



while True:
    # print("Rezultati list -", rezultati)
    print('Izvelies darbibu: ')
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