import csv

csv1FileName = "./faili/csv1.csv"
csv2FileName = "./faili/csv2.csv"

def csvGetData(csv1,csv2):
    csv1Data = []
    csv2Data = []
    with open(csv1, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            csv1Data = row
        with open(csv2, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                csv2Data = row
    return csv1Data, csv2Data

csv1Data, csv2Data = csvGetData(csv1FileName,csv2FileName)

csv1Garums = len(csv1Data)
csv2Garums = len(csv2Data)

if csv1Garums == csv2Garums:
    print("Ir vienadi!")
elif csv2Garums > csv1Garums:
    print("Saraksts csv2 ir garaks neka csv1 par",csv2Garums-csv1Garums,"elementiem")
elif csv2Garums < csv1Garums:
    print("Saraksts csv1 ir garaks neka csv2 par",csv1Garums-csv2Garums,"elementiem")

import json

JSON1FileName = "./faili/JsonViens.json"
JSON2FileName = "./faili/JsonDivi.json"

def JSONGetData(json1,json2):
    jsonData1 = {}
    jsonData2 = {}
    with open(json1, 'r', encoding="utf-8") as file:
        jsonData1 = json.load(file)
    with open(json2, 'r', encoding="utf-8") as file:
        jsonData2 = json.load(file)
    result = dict(list(jsonData1.items()) + list(jsonData2.items()))
    with open("./faili/JsonTris.json",'w',encoding="utf-8") as file:
        json.dump(result,file,indent=4)
    json1Keys = []
    json2Keys = []
    diffKeys = []
    for i in jsonData1.keys():
        json1Keys.append(i)
    for i in jsonData2.keys():
        json2Keys.append(i)
    for i in range(7):
        if json1Keys[i] != json2Keys[i]:
            diffKeys.insert(i,json1Keys[i])
            diffKeys.insert(i,json2Keys[i])
    
    return jsonData1, jsonData2, result
    
jsonData1, jsonData2, result = JSONGetData(JSON1FileName,JSON2FileName)