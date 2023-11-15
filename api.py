#Autors - Aleksis Pocs
# Programma - Laika konvertacija

#1. Laika noteiksana latvija
import requests
import json
import os
response1 = requests.get("http://worldtimeapi.org/api/timezone/Europe/Riga")
response2 = requests.get("http://worldtimeapi.org/api/timezone/Australia/Sydney")

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
    starpiba = int((getTimezone(timezone2))) - int(getTimezone(timezone1))
    return starpiba

def DataPreparation(obj1,obj2):
    dati = {
        f"Laiks {getLocation(obj1)}": getTime(obj1),
        f"Laiks {getLocation(obj2)}": getTime(obj2),
        f"Laika_Zona {getLocation(obj1)}": getTimezone(obj1),
        f"Laika_Zona {getLocation(obj2)}": getTimezone(obj2),
        f"Laika_Starpiba {getLocation(obj1),getLocation(obj2)}": f"{laikaStarpiba(obj1,obj2)} h"
    }
    return dati

if not os.path.exists("laiksAPI.json"):
    with open("laiksAPI.json", "w") as file:
        data1 = [DataPreparation(response1,response2)]
        json_object = json.dumps(data1, indent=4)
        file.write(json_object)
else:
    oldData = []
    with open("laiksAPI.json", "r+") as file:
        oldData = json.load(file)
        newData = json.loads(json.dumps(DataPreparation(response1,response2), indent=4))
        oldData.append(newData)
    with open("laiksAPI.json", "w") as file:
        file.write(json.dumps(oldData, indent=4))
        
    