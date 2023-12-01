#Aleksis Pocs 12a
#01/12/2023

# 1 uzdevums

import requests

LatvianUniversitiesJson = requests.get("http://universities.hipolabs.com/search?country=Latvia").json() # Saņem datus no api domēna par visām universitātēm Latvijas valstī un pārveido par json datiem

LatvijasUniversitates = [] # Izveido tukšu sarakstu, kurā tiks glabātas latvijas universitātes

for v in LatvianUniversitiesJson: # Notiek iterācija cauri visiem Latvijas universitāšu json datiem
    LatvijasUniversitates.append(v['name']) # Visi dati pie atslēgas "name", jeb vārds tiek pievienoti sarakstam "LatvijasUniversitates"

LatvijasUniversitates = sorted(LatvijasUniversitates) # Ar funkciju "sorted()" tiek sakārtoti saraksta "LatvijasUniversitates" dati alfabētiskā secībā

# for universitate in LatvijasUniversitates: # Iterē cauri sakārtotam Latvijas universitāšu sarakstam
#     print(universitate) #Izvada Latvijas universitātes nosaukumus

# 2 uzdevums

with open("teksts.txt",mode='r',encoding="UTF-8") as teksts:
    content = teksts.read()
    content = content.split(" ")
    
def iznemtPieturzimes(text):
    iteration = 0
    for word in text:
        if word[-1] == "." or word[-1] == "," or word[-1] == "?" or word[-1] == "!":
            correctedWord = word[0:-1]
            text[iteration] = correctedWord
        iteration += 1
    return text
        
    
content = iznemtPieturzimes(content)

def izlasitAtkartotusVardus(list):
    atkartotiVardi = set()
    for vards in list:
        if len(vards) >= 5:
            atkartotiVardi.add(vards)
    return atkartotiVardi

biezakieVardi = dict()
for vards in izlasitAtkartotusVardus(content):
    biezums = content.count(vards)
    biezakieVardi[vards] = biezums

sorted_dict = sorted(biezakieVardi.items(), key = lambda x:x[1], reverse=True)

def cetriBiezakie(sakartotaVardnica):
    iteration = 0
    for i in sakartotaVardnica:
        if iteration <= 3:
            print(i[0],"ir minets",i[1],'reizes')
        else:
            break
        iteration +=1


cetriBiezakie(sorted_dict)