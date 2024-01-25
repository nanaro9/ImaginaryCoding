# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

import mysql.connector # Tiek nodrošināts savienojums ar bibliotēku "mysql.connector", kura nodrošinās iespēju savienoties ar datu bāzi
import customtkinter

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
        self.darbinieks_alga = darbinieks_alga # definē mainīgo, kura vērtība tiek pielīdzināta objekta ievadītiem datiem "darbinieks_alga"
        self.darbinieks_berni = darbinieks_berni # definē mainīgo, kura vērtība tiek pielīdzināta objekta ievadītiem datiem "darbinieks_berni"
        self.darba_devejs_vards = darba_devejs_vards # Vienkārši definē tukšu mainīgo
        self.darba_devejs_uzvards = darba_devejs_uzvards # Vienkārši definē tukšu mainīgo
        self.uznemums = uznemums # Vienkārši definē tukšu mainīgo

        self.data = {"Darbinieks": {"Vards":darbinieks_vards,"Uzvards":darbinieks_uzvards,"Personas_kods":darbinieks_pk,"Berni":darbinieks_berni,"Alga":darbinieks_alga},"darba_Devejs":{"Vards":darba_devejs_vards,"Uzvards":darba_devejs_uzvards},"Uznemums":uznemums} # vārdnīcas izveide, kurā tiks glabāti ievadītie dati

        self.db = mysql.connector.connect(host="localhost",database="algaprekins",user="root",password="password") # Programma tiek savienota ar datu bāzi, kuras nosaukums ir "algaprekins"
        self.cursor = self.db.cursor() # Kursora definēšana, ar kura palīdzību var pārvietoties pa datu bāzi

        self.veids = ["darbinieks","darba_devejs","alga"]
        self.db_dati = {"darbinieks":[],"darba_deveji":[],"alga":[]}
        
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

        
    def saglabasana(self,veids):
        if veids == "txt":
            pass
        elif veids == "db":

            sql = {
                "Darbinieks":("""insert into darbinieks (ID_darbinieks, darbinieks_vards, darbinieks_uzvards, darbinieks_pk, darbinieks_berni, darbinieks_alga) values (%s, %s, %s, %s,%s, %s);"""),
                "Darba Devejs":("""insert into darba_devejs (ID_darba_devejs, darba_devejs_vards, darba_devejs_uzvards) values (%s,%s, %s);"""),
                "Alga":("""insert into alga (ID_alga, uznemums, neto_alga, darbinieks_ID, darba_devejs_ID) values (%s, %s, %s, %s,%s);""")
                }
            
            alga_data_structure = [self.data["Uznemums"],self.algas_formula()]
            darbinieks_data_structure = [self.data["Darbinieks"]["Vards"],self.data["Darbinieks"]["Uzvards"],self.data["Darbinieks"]["Personas_kods"],self.data["Darbinieks"]["Berni"],self.data["Darbinieks"]["Alga"]]
            darba_devejs_data_structure = [self.data["darba_Devejs"]["Vards"],self.data["darba_Devejs"]["Uzvards"]]

            indeksi = []

            for v in self.veids:
                self.cursor.execute(f"SELECT * FROM {v}")
                indeksi.append(self.index_parbaude(self.cursor.fetchall()))

            structures = [darbinieks_data_structure,darba_devejs_data_structure,alga_data_structure,]
            structures = self.pieskir_index(structures,indeksi)

            count = 0
            for i in sql:
                self.cursor.execute(sql[i],structures[count])
                self.db.commit()
                count += 1

stradnieks = Alganators(2000,0,"Guntars","Tutins","040400-0404","SIA PLEĶĪŠI","Aleksandrs","Sātīgais") # Objekta izveide
# print(stradnieks.algas_formula()) # metodes izvade
# stradnieks.saglabasana("db")

def mainApp():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("Algas aprēķina programma")
    root.resizable(False,False)

    def loginFrame():   
        def login():
            Input_credentials = {"Login_Input":loginEntry.get(),"Password_Input":passwordEntry.get()}
            if Input_credentials["Login_Input"] != "Admin" and Input_credentials["Password_Input"] != "Password":
                frame = customtkinter.CTkToplevel(master=loginframe)
                frame.geometry("1000x200")
                frame.resizable(False,False)
                frame.title("Uzmanību!")

                errorMSG = customtkinter.CTkLabel(master=frame, text=("Uzmanību! Lietotājvārds vai parole tika ievadīta nepareizi!"), font=("Roboto",32), anchor="center")
                errorMSG.pack(padx=50, pady=50)
            else:
                loginframe.destroy()
        def guest():
            loginframe.destroy()
        loginframe = customtkinter.CTkFrame(master=root)
        loginframe.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=loginframe, text="Sveicināti, Lietotāj!", font=("Roboto",22))
        label.pack(pady=12,padx=10)

        loginEntry = customtkinter.CTkEntry(master=loginframe, placeholder_text="Lietotājvārds")
        loginEntry.pack(pady=12,padx=10)

        passwordEntry = customtkinter.CTkEntry(master=loginframe, placeholder_text="Parole", show="*")
        passwordEntry.pack(pady=12,padx=10)

        loginbutton = customtkinter.CTkButton(master=loginframe, text="Pieslēgties", command=login)
        loginbutton.pack(pady=12,padx=10)

        guestButton = customtkinter.CTkButton(master=loginframe, text="Viesa režīms", command=guest)
        guestButton.pack(pady=12,padx=10)
        
        


    def guest():
        pass

    loginFrame()

    root.mainloop()


mainApp()