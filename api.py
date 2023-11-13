# 1. Izveidots vienkāršs servera puses pieprasījums.
# 2. Izveidota tukša atbilde no servera.
# 3. Atbilde no servera ir izveidots kā tukšs JSON objekts tā formātā.
# 4. Atbilde no servera tiek izveidota JSON formātā, iekļaujot reāllaika izdruku.
# 5. Tiek iestrādāti laika zonas starpības parametri pieprasījumā.
# 6. Serveris atbild ar kļūdu, izmantojot dažādas datu struktūras kļūdas definēšanā, ja līdzi
# nav padoti laika zonas starpības parametri.
# 7. Serveris atbild ar izmainītu laika un datuma izdruku atbilstoši iedotajai stundu nobīdei.

#Autors - Aleksis Pocs
# Programma - Laika konvertacija

#1. Laika noteiksana latvija
import requests
import json
responseASV = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")
responseRiga = requests.get("http://worldtimeapi.org/api/timezone/Europe/Riga")

def getLocation(obj):
    location = obj.json()["timezone"]
    return location

def getTimezone(obj):
    laikazona = obj.json()['utc_offset'][:3]
    return laikazona

def getTime(obj):
    laiks = obj.json()['datetime'][11:16]
    return laiks

def laikaStarpiba(timezone1,timezone2):
    starpiba = abs(int((getTimezone(timezone1))) - int(getTimezone(timezone2)))
    return starpiba

def DataPreparation(obj1,obj2):
    dati = {
        f"Laiks {getLocation(obj1)}": getTime(obj1),
        f"Laiks {getLocation(obj2)}": getTime(obj2),
        f"Laika_Zona {getLocation(obj1)}": getTimezone(obj1),
        f"Laiks_Zona {getLocation(obj2)}": getTimezone(obj2),
        f"Laika_Starpiba {getLocation(obj1),getLocation(obj2)}": f"{laikaStarpiba(obj1,obj2)} h"
    }
    return dati

json_object = json.dumps(DataPreparation(responseASV,responseRiga), indent=4)

with open("laiksAPI.json", "w") as file:
    file.write(json_object)