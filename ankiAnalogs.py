import random
apguves_Baze = {}

def menu():
    print("-----Sveicināti vārdu apguves programmā!-----\n")

    print("Izvēlies darbību:")
    print("1. Pievienot vārdu\n2. Sākt testu\n3. Aizvērt programmu\n")
    UserInput = input("Izvēle: ")
    return UserInput

def addWord():
    print("\n-----Vārda pievienošana-----\n")
    word = input("Ievadi vārdu: ")
    if word in apguves_Baze:
        print("\nŠāds vārds jau eksistē!")
    else:
        meaning = input("Ievadi vārda nozīmi: ")
        apguves_Baze[word] = meaning
    print()

def StartTest():
    print("\n-----Tests-----")
    score = 0

    temp = list(apguves_Baze.items())
    random.shuffle(temp)
    testa_jautjumi = dict(temp)

    for i in testa_jautjumi:  
        print("\nKo nozīmē vārds -", i)
        userInput = input("\nVārda nozīme: ")
        if userInput == testa_jautjumi[i]:
            print("\nPareizi!")
            score+=1
        else:
            print("\nNepareizi! Šī vārda nozīme ir -", testa_jautjumi[i])
    print(f"\nApsveicam! Jūs pabeidzāt testu ar {score} pareziām atbildēm no {len(apguves_Baze.keys())}\n")

while True:
    start = menu()
    if start == "1" or start == "2" or start == "3":
        if start == "1":
            addWord()
            continue
        if start == "2" and apguves_Baze:
            StartTest()
            continue
        elif start == "2" and not apguves_Baze:
            print("\nNevar sākt testu ar tukšu vārdu sarakstu!\n")
            continue
        if start == "3":
            print("\n-----Paldies par darbu!-----\n")
            break
    else:
        continue