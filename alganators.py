# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

import os
import mysql.connector # Tiek nodrošināts savienojums ar bibliotēku "mysql.connector", kura nodrošinās iespēju savienoties ar datu bāzi
import customtkinter
from cryptography.fernet import Fernet
import pyotp
import qrcode

key = 'XGT2BDNVJBTU2JFQCRAVCQPYNFZI2RVI'
totp = pyotp.TOTP(key)
# uri = totp.provisioning_uri(name="Admin",issuer_name="Algas aprēķina programma")
# qrcode.make(uri).save("qrcode.png")

class Alganators(): # Definē klasi Alganators
    def __init__(self,darbinieks_alga,darbinieks_berni,darbinieks_vards,darbinieks_uzvards,darbinieks_pk,uznemums,darba_devejs_vards,darba_devejs_uzvards): # Klases sākuma uzstādīšana

        self.SN_LIKME = 0.105 # Konstanta Sociālā nodokļa likme 10.5%
        self.IIN_LIKME = 0.2 # Konstanta Iedzīvotāja ienākuma nodokļa likme 20%
        self.IIN_LIKME2 = 0.23 # Konstanta Iedzīvotāja ienākuma nodokļa likme 23%
        self.DD_SN_LIKME = 0.2359 # Konstanta Darba devēja sociālā nodokļa likme 23.59%
        self.APGADAJAMO_LIKME = 250 # Likme par katru apgādājamo personu 250 eiro
        self.ALGAS_LIKME = 1667 # Likme pēc kuras pienākas papildus nodoklis

        self.darbinieks_vards = darbinieks_vards # Vienkārši definē tukšu mainīgo
        self.darbinieks_uzvards = darbinieks_uzvards # Vienkārši definē tukšu mainīgo
        self.darbinieks_pk = darbinieks_pk # Vienkārši definē tukšu mainīgo
        self.darbinieks_alga = float(darbinieks_alga) # definē mainīgo, kura vērtība tiek pielīdzināta objekta ievadītiem datiem "darbinieks_alga"
        self.darbinieks_berni = int(darbinieks_berni) # definē mainīgo, kura vērtība tiek pielīdzināta objekta ievadītiem datiem "darbinieks_berni"
        self.darba_devejs_vards = darba_devejs_vards # Vienkārši definē tukšu mainīgo
        self.darba_devejs_uzvards = darba_devejs_uzvards # Vienkārši definē tukšu mainīgo
        self.uznemums = uznemums # Vienkārši definē tukšu mainīgo

        self.data = {"Darbinieks": {"Vards":darbinieks_vards,"Uzvards":darbinieks_uzvards,"Personas_kods":darbinieks_pk,"Berni":darbinieks_berni,"Alga":darbinieks_alga},"darba_Devejs":{"Vards":darba_devejs_vards,"Uzvards":darba_devejs_uzvards},"Uznemums":uznemums} # vārdnīcas izveide, kurā tiks glabāti ievadītie dati

        self.db = mysql.connector.connect(host="localhost",database="algaprekins",user="root",password="password") # Programma tiek savienota ar datu bāzi, kuras nosaukums ir "algaprekins"
        self.cursor = self.db.cursor() # Kursora definēšana, ar kura palīdzību var pārvietoties pa datu bāzi

        self.veids = ["darbinieks","darba_devejs","alga"]
        self.db_dati = {"darbinieks":[],"darba_devejs":[],"alga":[]}
        
        for v in self.veids:
            self.cursor.execute(f"SELECT * FROM {v}")
            self.db_dati[v] = self.cursor.fetchall()

    def algas_formula(self): # Definēta funkcija, kura saņems 2 datus, bruto algu un bērnu skaitu
        atvieglojums = self.darbinieks_berni * self.APGADAJAMO_LIKME # atvieglojuma aprēķināšana (bērnu skaits pareizināts ar likmi, kura ir 250 eiro par vienu bērnu)
        if self.darbinieks_alga <= self.ALGAS_LIKME: # Pārbauda, vai bruto alga nav lielāka par algas likmi, kura ir 1667 eiro
            sn = self.darbinieks_alga * self.SN_LIKME # 1. darbība ir sociālā nodokļa aprēķins (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            iin_baze = self.darbinieks_alga - sn - atvieglojums # 2. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no bruto algas tiek atņemts sociālais nodoklis un atvieglojums)
            if iin_baze > 0:
                pass
            else:
                iin_baze = 0
            iin = iin_baze * self.IIN_LIKME # 3. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            neto_alga = self.darbinieks_alga - sn - iin # 4. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodoklis)
            return neto_alga # Atgriež neto algas vērtību
        else: # Ja bruto alga ir lielāka par algas likmi, kura ir 1667 eiro, tad:
            sn = self.darbinieks_alga * self.SN_LIKME # 1. sociālā nodokļa aprēķināšana (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            iin_baze = self.ALGAS_LIKME - sn - atvieglojums # 2. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no algas likmes (1667 eiro) tiek atņemts sociālais nodoklis un atvieglojums)
            if iin_baze > 0:
                pass
            else:
                iin_baze = 0
            iin = iin_baze * self.IIN_LIKME # 3. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            parpalikums = self.darbinieks_alga - self.ALGAS_LIKME # 4. Pārpalikuma aprēķināšana, kuru var izrēķināt, atņemot algas likmi (1667) no bruto algas
            iin2 = parpalikums * self.IIN_LIKME2 # 5. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, šoreiz pareizinot pārpalikumu ar IIN likmi, kad bruto alga pārsniedz 1667 eiro, tas ir 23%
            neto_alga = self.darbinieks_alga - sn - iin - iin2 # 6. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodokļi)
            return neto_alga # Atgriež neto algas vērtību
    
    def index_parbaude(self,idx):
        if idx == None or idx == []:
            idx = 0
        elif idx != None:
            idx = int(idx[-1][0]) + 1
        return idx
    
    def pieskir_index(self,struktura,indeksi):
        for i in struktura:
            i.insert(0,indeksi[struktura.index(i)])
            if i == struktura[2]:
                i.insert(3,indeksi[0])
                i.insert(4,indeksi[1])
        return struktura
    
    def datu_parbaude(self,data):
        count = 0
        for v in self.veids:
            self.cursor.execute(f"SELECT * FROM {v}")
            self.db_dati[v] = self.cursor.fetchall()
        sakritosie_dati = {"darbinieks":[False,0],"darba_devejs":[False,0],"alga":[False,0]}
        for v in self.db_dati:
            if self.db_dati[v] != []:
                for i in self.db_dati[v]:
                    for j in i:
                        if v == "darbinieks":
                            if i.index(j) == 1 or i.index(j) == 2 or i.index(j) == 3:
                                if j == data[count][i.index(j)]:
                                    sakritosie_dati["darbinieks"][1]+=1
                        elif v == "darba_devejs":
                            if i.index(j) == 1 or i.index(j) == 2:
                                if j == data[count][i.index(j)]:
                                    sakritosie_dati["darba_devejs"][1]+=1
                        else:
                            if i.index(j) == 1:
                                if j == data[count][i.index(j)]:
                                    sakritosie_dati["alga"][1]+=1
            count+=1
        for i in sakritosie_dati:
            if i == "darba_devejs":
                if sakritosie_dati[i][1] == 2:
                    sakritosie_dati[i][0] = True
                    return sakritosie_dati[i][0]
            elif i == "darbinieks":
                if sakritosie_dati[i][1] >= 1:
                    sakritosie_dati[i][0] = True
                    return sakritosie_dati[i][0]
            else:
                if sakritosie_dati[i][1] == 1:
                    sakritosie_dati[i][0] = True
                    return sakritosie_dati[i][0]
        return False

    def saglabasana(self):
        alga_data_structure = [self.data["Uznemums"],self.algas_formula()]
        darbinieks_data_structure = [self.data["Darbinieks"]["Vards"],self.data["Darbinieks"]["Uzvards"],self.data["Darbinieks"]["Personas_kods"],self.data["Darbinieks"]["Berni"],self.data["Darbinieks"]["Alga"]]
        darba_devejs_data_structure = [self.data["darba_Devejs"]["Vards"],self.data["darba_Devejs"]["Uzvards"]]

        sql = {
            "Darbinieks":("""insert into darbinieks (ID_darbinieks, darbinieks_vards, darbinieks_uzvards, darbinieks_pk, darbinieks_berni, darbinieks_alga) values (%s, %s, %s, %s,%s, %s);"""),
            "Darba Devejs":("""insert into darba_devejs (ID_darba_devejs, darba_devejs_vards, darba_devejs_uzvards) values (%s,%s, %s);"""),
            "Alga":("""insert into alga (ID_alga, uznemums, neto_alga, darbinieks_ID, darba_devejs_ID) values (%s, %s, %s, %s,%s);""")
            }

        indeksi = []

        for v in self.veids:
            self.cursor.execute(f"SELECT * FROM {v}")
            indeksi.append(self.index_parbaude(self.cursor.fetchall()))

        structures = [darbinieks_data_structure,darba_devejs_data_structure,alga_data_structure,]
        structures = self.pieskir_index(structures,indeksi)
        parbaude = self.datu_parbaude(structures)
        count=0
        if not parbaude:
            if os.path.isfile(f"./alganators_save/alga_{darbinieks_data_structure[3]}.txt"):
                savingData = f"\n-Algas aprēķināšanas kopsavilkums-\nVārds/Uzvārds: {darbinieks_data_structure[1]} {darbinieks_data_structure[2]}\nPersonas kods: {darbinieks_data_structure[3]}\nBērnu skaits {darbinieks_data_structure[4]}\nBruto alga: {darbinieks_data_structure[5]}\n\nDarba devējs (Vārds/Uzvārds): {darba_devejs_data_structure[1]} {darba_devejs_data_structure[2]}\nUzņēmums: {alga_data_structure[1]}\n\nNETO ALGA: {alga_data_structure[2]}\n"
                f = open(f"./alganators_save/alga_{darbinieks_data_structure[3]}.txt", "a",encoding="utf8")
                f.write(savingData)
                f.close()
            else:
                savingData = f"-Algas aprēķināšanas kopsavilkums-\nVārds/Uzvārds: {darbinieks_data_structure[1]} {darbinieks_data_structure[2]}\nPersonas kods: {darbinieks_data_structure[3]}\nBērnu skaits {darbinieks_data_structure[4]}\nBruto alga: {darbinieks_data_structure[5]}\n\nDarba devējs (Vārds/Uzvārds): {darba_devejs_data_structure[1]} {darba_devejs_data_structure[2]}\nUzņēmums: {alga_data_structure[1]}\n\nNETO ALGA: {alga_data_structure[2]}\n"
                f = open(f"./alganators_save/alga_{darbinieks_data_structure[3]}.txt", "w",encoding="utf8")
                f.write(savingData)
                f.close()
            count = 0
            for i in sql:
                self.cursor.execute(sql[i],structures[count])
                self.db.commit()
                count += 1
            return True
        else:
            return False
    
    def db_dati_return(self):
        return self.db_dati
            

def mainApp():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("Algas aprēķina programma")
    root.resizable(False,False)
    root.grid_columnconfigure((0,1),weight=1)
    root.grid_rowconfigure(0,weight=1)

    def errorFrame(text):
        frame = customtkinter.CTkToplevel(master=root)
        frame.geometry("1000x200")
        frame.resizable(False,False)
        frame.title("Uzmanību!")
        frame.attributes('-topmost', 'true')

        errorMSG = customtkinter.CTkLabel(master=frame, text=(f"Uzmanību! {text}"), font=("Roboto",32), anchor="center")
        errorMSG.pack(padx=50, pady=50)

    def editFrame(dbDati):
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Speciālais datu piekļuves centrs", font=("Roboto",22))
        label.pack(pady=12,padx=10)

        entry = customtkinter.CTkEntry(master=frame, placeholder_text="Ievadiet meklējamā informāciju...")
        entry.pack(pady=12,padx=10)

        optionmenu = customtkinter.CTkOptionMenu(frame, values=["Darbinieks", "Darba Devējs", "Alga"])
        optionmenu.pack(pady=12,padx=10)

        ID_searchButton = customtkinter.CTkButton(master=frame,text="Meklēt pēc ID",font=("Roboto",14),command=lambda: editFrame(searchResults(entry.get(),optionmenu.get(),"ID")))
        PK_searchButton = customtkinter.CTkButton(master=frame,text="Meklēt pēc personas koda",font=("Roboto",14),command=lambda: editFrame(searchResults(entry.get(),optionmenu.get(),"PK")))

        ID_searchButton.pack(pady=12)
        PK_searchButton.pack(pady=12)

        def searchResults(searchInfo,optionChoice,searchMode):
            options = ["darbinieks","darba_devejs","alga"]

            if optionChoice == "Darbinieks":
                optionChoice = options[0]
            elif optionChoice == "Darba Devējs":
                optionChoice = options[1]
            else:
                optionChoice = options[2]

            if searchMode == "ID":
                if searchInfo.isdigit():
                    found = False
                    for i in dbDati[optionChoice]:
                        if int(searchInfo) == i[0]:
                            found = True
                            return [optionChoice,i]
                    if not found:
                        errorFrame("Dati ar šādu ID neeksistē!")
                else:
                    errorFrame("Nepareizi ievadīts ID")
            elif searchMode == "PK":
                if optionChoice == "darbinieks":
                    found = False
                    for i in dbDati[optionChoice]:
                        if searchInfo == i[3]:
                            found = True
                            return [optionChoice,i]
                    if not found:
                        errorFrame("Datu ar šādu Personas kodu neeksistē!")
                else:
                    errorFrame("Meklēšana TIKAI DARBINIEKA DATIEM!")


        def datu_parbaude(data):
            count = 0
            sakritosie_dati = {"darbinieks":[False,0],"darba_devejs":[False,0],"alga":[False,0]}
            print(dbDati,data)

        def editFrame(EditData):
            frame = customtkinter.CTkToplevel(master=root)
            frame.geometry("700x450")
            frame.resizable(False,False)
            frame.title("Algas aprēķina programma")
            frame.attributes('-topmost', 'true')

            innerFrame = customtkinter.CTkFrame(master=frame)
            innerFrame.pack(pady=10, padx=20, fill="both", expand=True)

            label = customtkinter.CTkLabel(master=innerFrame, text="Datu Rediģēšana", font=("Roboto",22))
            label.pack(pady=12)


            optionList = {"darbinieks":["Vārds","Uzvārds","Personas Kods","Bērnu Skaits","Bruto Alga"],"darba_devejs":["Vārds","Uzvārds"],"alga":["Neto Alga"]}

            idx = 0
            for v in EditData[1][1:]:
                dataLabel = customtkinter.CTkLabel(master=innerFrame, text=f"{optionList[idx]}: {str(v)}", font=("Roboto",18))
                dataLabel.pack(pady=12)
                idx+=1

            optionmenu = customtkinter.CTkOptionMenu(frame, values=optionList[EditData[0]])
            optionmenu.pack(pady=12)

            EditBtn = customtkinter.CTkButton(master=frame,text="Rediģēt Izvēlētos Datus",font=("Roboto",14),command=lambda: popupEdit(optionmenu.get(),EditData))
            EditBtn.pack(pady=12)

            def destroyEditFrameContents():
                for f in innerFrame.winfo_children():
                    f.destroy()
                optionmenu.destroy()
                EditBtn.destroy()

            def popupEdit(data_to_edit,editData):
                destroyEditFrameContents()

                label = customtkinter.CTkLabel(master=innerFrame, text=f"Datu Rediģēšana ({data_to_edit})", font=("Roboto",22))
                label.pack(pady=12)

                entry = customtkinter.CTkEntry(master=innerFrame, placeholder_text="Ievadiet vērtību aizstāšanai",width=600)
                entry.pack(pady=12)

                btn = customtkinter.CTkButton(master=innerFrame, text="Rediģēt/Aizstāt",width=400,command=lambda:check(editData[1],editData[0],data_to_edit))
                btn.pack(pady=12)

            def check(data,option,optionOption):
                for i in data:
                        if i=='':
                            errorFrame(f"lauciņš palika tukšs!")
                            return False
                if option == "darbinieks":
                    for i in data:
                        if optionOption == "Vārds" or optionOption == "Uzvārds":
                            if i.isdigit():
                                errorFrame(f"lauciņš netika aizpildīts korekti!")
                                return False
                        if optionOption == "Personas Kods":
                            if len(i) < 12:
                                errorFrame(f"lauciņš netika aizpildīts korekti!")
                                return False
                            if not i[:6].isdigit() or not i[7:].isdigit() or i[6] != "-":
                                errorFrame(f"lauciņš netika aizpildīts korekti!")
                                return False
                        if optionOption == "Bruto alga" or optionOption == "Bērnu skaits":
                            if not i.isdigit():
                                errorFrame(f"lauciņš netika aizpildīts korekti!")
                                return False
                if option == "darba_devejs":
                    for i in data:
                        if optionOption == "Vārds" or optionOption == "Uzvārds":
                            if i.isdigit():
                                errorFrame(f"lauciņš netika aizpildīts korekti!")
                                return False                        





    def stepsFrame(data,obj_alga):
        frame = customtkinter.CTkToplevel(master=root)
        frame.geometry("700x400")
        frame.resizable(False,False)
        frame.title("Algas aprēķina programma")
        frame.attributes('-topmost', 'true')

        innerFrame = customtkinter.CTkFrame(master=frame)
        innerFrame.pack(pady=10, padx=20, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=innerFrame, text="Aprēķina soļi", font=("Roboto",22))
        label.grid(row=0, column=0, padx=20, pady=10,sticky="nsew")

        if int(data["Bruto alga"]) < 1667:
            step1 = customtkinter.CTkLabel (master=innerFrame, text=f"1. Solis [SN]: Bruto alga * 10.5% = {int(data['Bruto alga']) * 0.105}")
            iin_baze = (int(data['Bruto alga']) - (int(data['Bruto alga']) * 0.105) - (int(data['Bērnu skaits'])*250))
            step2 = customtkinter.CTkLabel (master=innerFrame, text=f"2. Solis [Atvieglojums]: Bērnu skaits * 250 = {(int(data['Bērnu skaits'])*250)}")
            if iin_baze > 0:
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: Bruto alga - SN - Atvieglojums = {iin_baze}")
            else:
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: Bruto alga - SN - Atvieglojums = {iin_baze}, jeb IIN bāze = 0")
                iin_baze = 0
            step4 = customtkinter.CTkLabel (master=innerFrame, text=f"4. Solis [IIN]: IIN bāze * 20% = {iin_baze * 0.2}")
            step5 = customtkinter.CTkLabel (master=innerFrame, text=f"5. Solis [Neto alga]: Bruto alga - SN - IIN = {obj_alga}")
            step1.grid(pady=5,padx=10,sticky="nsew",row=1,column=0)
            step2.grid(pady=5,padx=10,sticky="nsew",row=2,column=0)
            step3.grid(pady=5,padx=10,sticky="nsew",row=3,column=0)
            step4.grid(pady=5,padx=10,sticky="nsew",row=4,column=0)
            step5.grid(pady=5,padx=10,sticky="nsew",row=5,column=0)
        else:
            step1 = customtkinter.CTkLabel (master=innerFrame, text=f"1. Solis [SN]: Bruto alga * 10.5% = {int(data['Bruto alga']) * 0.105}")
            iin_baze = (1667 - (int(data['Bruto alga']) * 0.105) - (int(data['Bērnu skaits'])*250))
            step2 = customtkinter.CTkLabel (master=innerFrame, text=f"2. Solis [Atvieglojums]: Bērnu skaits * 250 = {(int(data['Bērnu skaits'])*250)}")
            if iin_baze > 0:
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: 1667 - SN - Atvieglojums = {iin_baze}")
            else:
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: 1667 - SN - Atvieglojums = {iin_baze}, jeb IIN bāze = 0")
                iin_baze = 0
            parpalikums = int(data['Bruto alga']) - 1667
            step4 = customtkinter.CTkLabel (master=innerFrame, text=f"4. Solis [IIN]: IIN bāze - 10.5% = {iin_baze * 0.105}")
            step5 = customtkinter.CTkLabel (master=innerFrame, text=f"5. Solis [Pārpalikums]: Bruto alga - 1667 = {parpalikums}")
            step6 = customtkinter.CTkLabel (master=innerFrame, text=f"6. Solis [IIN 2]: Pārpalikums * 23% = {parpalikums * 0.23}")
            step7 = customtkinter.CTkLabel (master=innerFrame, text=f"7. Solis [Neto alga]: Bruto alga - SN - IIN - IIN 2 = {obj_alga}")
            step1.grid(pady=5,padx=10,sticky="nsew",row=1,column=0)
            step2.grid(pady=5,padx=10,sticky="nsew",row=2,column=0)
            step3.grid(pady=5,padx=10,sticky="nsew",row=3,column=0)
            step4.grid(pady=5,padx=10,sticky="nsew",row=4,column=0)
            step5.grid(pady=5,padx=10,sticky="nsew",row=5,column=0)
            step6.grid(pady=5,padx=10,sticky="nsew",row=6,column=0)
            step7.grid(pady=5,padx=10,sticky="nsew",row=7,column=0)


        netoLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Neto Alga: {'{:.2f}'.format(obj_alga)}", font=("Roboto",20),justify="center",wraplength=150)
        netoLabel.grid(row=3, column=1, padx=20, pady=10,sticky="nsew")

        author = customtkinter.CTkLabel(master=frame,text="© Aleksis Počs 2024")
        author.pack()

    def savingGUI(bool):
        if bool:
            print("saved")
        else:
            print("fail")

    def outputFrame(data):
        frame = customtkinter.CTkToplevel(master=root)
        frame.geometry("700x350")
        frame.resizable(False,False)
        frame.title("Algas aprēķina programma")
        frame.attributes('-topmost', 'true')
        
        name=data["Vārds/Uzvārds"].split(" ")
        ddName=data["Darba devējs"].split(" ")

        obj = Alganators(data["Bruto alga"],data["Bērnu skaits"],name[0],name[1],data["Personas Kods"],data["Uzņēmums"],ddName[0],ddName[1])
        obj_alga = obj.algas_formula()

        innerFrame = customtkinter.CTkFrame(master=frame)
        innerFrame.pack(pady=10, padx=20, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=innerFrame, text="Algas aprēķina programma", font=("Roboto",22))
        label.grid(row=0, column=0, padx=20, pady=10,sticky="nsew")

        nameLabel = customtkinter.CTkLabel (master=innerFrame, text=f"Vārds/Uzvārds: {data['Vārds/Uzvārds']}")
        pkLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Personas Kods: {data['Personas Kods']}")
        brutoLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Bruto Alga: {data['Bruto alga']}")
        childLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Bērnu Skaits: {data['Bērnu skaits']}")
        ddLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Darba Devējs (Vārds/Uzvārds): {data['Darba devējs']}")
        companyLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Uzņēmums: {data['Uzņēmums']}")
            
        nameLabel.grid(pady=5,padx=10,sticky="nsew",row=1,column=0)
        pkLabel.grid(pady=5,padx=10,sticky="nsew",row=2)
        brutoLabel.grid(pady=5,padx=10,sticky="nsew",row=3)
        childLabel.grid(pady=5,padx=10,sticky="nsew",row=4)
        ddLabel.grid(pady=5,padx=10,sticky="nsew",row=5)
        companyLabel.grid(pady=5,padx=10,sticky="nsew",row=6)

        netoLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Neto Alga: {'{:.2f}'.format(obj_alga)}", font=("Roboto",20),justify="center",wraplength=150)
        netoLabel.grid(row=3, column=1, padx=20, pady=10,sticky="nsew")

        calculationBtn = customtkinter.CTkButton(master=innerFrame,text="Aprēķina Soļi",font=("Roboto",14),command=lambda: stepsFrame(data,obj_alga))
        saveBtn = customtkinter.CTkButton(master=innerFrame,text="Saglabāt .txt",font=("Roboto",14), command=lambda: savingGUI(obj.saglabasana()))
        calculationBtn.grid(pady=5,padx=10,sticky="nsew",row=6,column=1)
        saveBtn.grid(pady=5,padx=10,sticky="nsew",row=6,column=2)

        author = customtkinter.CTkLabel(master=frame,text="© Aleksis Počs 2024")
        author.pack()

    def inputFrame():
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        def check():
            data = {"Vārds/Uzvārds":nameEntry.get(),"Personas Kods":pkEntry.get(),"Bruto alga":brutoEntry.get(),"Bērnu skaits":childEntry.get(),"Darba devējs":ddEntry.get(),"Uzņēmums":companyEntry.get()}
            for i in data:
                if data[i]=='':
                    errorFrame(f"{i} lauciņš palika tukšs!")
                    return False
                if i == "Vārds/Uzvārds" or i == "Darba devējs" or i == "Uzņēmums":
                    if data[i].isdigit():
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!")
                        return False
                    if i == "Vārds/Uzvārds" or i == "Darba devējs":
                        if len(data[i].split(" ")) != 2:
                            print(len(data[i].split(" ")))
                            errorFrame(f"{i} lauciņš netika aizpildīts korekti!")
                            return False
                if i == "Personas Kods":
                    if len(data[i]) < 12:
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!")
                        return False
                    if not data[i][:6].isdigit() or not data[i][7:].isdigit() or data[i][6] != "-":
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!")
                        return False
                if i == "Bruto alga" or i == "Bērnu skaits":
                    if not data[i].isdigit():
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!")
                        return False
            outputFrame(data)


        label = customtkinter.CTkLabel(master=frame, text="Algas aprēķina programma", font=("Roboto",22))
        label.grid(row=0, column=0, padx=20, pady=10,sticky="nsew")
        nameEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Vārds/Uzvārds")
        pkEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Personas Kods")
        brutoEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Bruto Alga")
        childEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Bērnu Skaits")
        ddEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Darba Devējs (Vārds/Uzvārds)")
        companyEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Uzņēmums")
        aprekinatButton = customtkinter.CTkButton(master=frame, text="Aprēķināt", command=check)

        nameEntry.grid(pady=5,padx=10,sticky="nsew",row=1)
        pkEntry.grid(pady=5,padx=10,sticky="nsew",row=2)
        brutoEntry.grid(pady=5,padx=10,sticky="nsew",row=3)
        childEntry.grid(pady=5,padx=10,sticky="nsew",row=4)
        ddEntry.grid(pady=5,padx=10,sticky="nsew",row=5)
        companyEntry.grid(pady=5,padx=10,sticky="nsew",row=6)
        aprekinatButton.grid(pady=5,padx=5,row=6,column=1)

        author = customtkinter.CTkLabel(master=root,text="© Aleksis Počs 2024")
        author.pack()

    def loginFrame():   
        def login():
            credentials = {"Login_Input":loginEntry.get(),"Password_Input":passwordEntry.get()}
            if credentials["Login_Input"] != "Admin" or not totp.verify(credentials["Password_Input"]):
                errorFrame("Lietotājvārds vai parole tika ievadīta nepareizi!")
            elif credentials["Login_Input"] == "Admin" or totp.verify(credentials["Password_Input"]):
                loginframe.destroy()
                editFrame(Alganators(0,0,0,0,0,0,0,0).db_dati_return())

        def guest():
            loginframe.destroy()
            inputFrame()
            
        loginframe = customtkinter.CTkFrame(master=root)
        loginframe.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=loginframe, text="Sveicināti, Lietotāj!", font=("Roboto",22))
        label.pack(pady=12,padx=10)

        loginEntry = customtkinter.CTkEntry(master=loginframe, placeholder_text="Lietotājvārds")
        loginEntry.pack(pady=12,padx=10)

        passwordEntry = customtkinter.CTkEntry(master=loginframe, placeholder_text="Key", show="*")
        passwordEntry.pack(pady=12,padx=10)

        loginbutton = customtkinter.CTkButton(master=loginframe, text="Pieslēgties", command=login)
        loginbutton.pack(pady=12,padx=10)

        guestButton = customtkinter.CTkButton(master=loginframe, text="Viesa režīms", command=guest)
        guestButton.pack(pady=12,padx=10)

    loginFrame()

    root.mainloop()

mainApp()