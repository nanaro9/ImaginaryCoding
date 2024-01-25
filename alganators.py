# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

import mysql.connector # Tiek nodrošināts savienojums ar bibliotēku "mysql.connector", kura nodrošinās iespēju savienoties ar datu bāzi

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

        self.data = {"Darbinieks": {"Vards":darbinieks_vards,"Uzvards":darbinieks_uzvards,"Personas_kods":darbinieks_pk,"Berni":darbinieks_berni,"Alga":darbinieks_alga},"Darba_Devejs":{"Vards":darba_devejs_vards,"Uzvards":darba_devejs_uzvards},"Uznemums":uznemums} # vārdnīcas izveide, kurā tiks glabāti ievadītie dati

        self.db = mysql.connector.connect(host="localhost",database="algaprekins",user="root",password="password") # Programma tiek savienota ar datu bāzi, kuras nosaukums ir "algaprekins"
        self.cursor = self.db.cursor() # Kursora definēšana, ar kura palīdzību var pārvietoties pa datu bāzi

        self.cursor.execute("SELECT * FROM darbinieks") # izvēlas visus datus no tabulas "darbinieks"
        self.darbinieki = self.cursor.fetchall() # Saņem augstāk izvēlētos datus un pielīdzina tos mainīgajam "darbinieki"

        self.cursor.execute("SELECT * FROM darba_devejs") # izvēlas visus datus no tabulas "darba_devejs"
        self.darba_deveji = self.cursor.fetchall() # Saņem augstāk izvēlētos datus un pielīdzina tos mainīgajam "darba_deveji"

    def algas_formula(self): # Definēta funkcija, kura saņems 2 datus, bruto algu un bērnu skaitu
        atvieglojums = self.darbinieks_berni * self.APGADAJAMO_LIKME # atvieglojuma aprēķināšana (bērnu skaits pareizināts ar likmi, kura ir 250 eiro par vienu bērnu)
        if self.darbinieks_alga <= self.ALGAS_LIKME: # Pārbauda, vai bruto alga nav lielāka par algas likmi, kura ir 1667 eiro
            sn = self.darbinieks_alga * self.SN_LIKME # 1. darbība ir sociālā nodokļa aprēķins (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            iin_baze = self.darbinieks_alga - sn - atvieglojums # 2. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no bruto algas tiek atņemts sociālais nodoklis un atvieglojums)
            iin = iin_baze * self.IIN_LIKME # 3. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            neto_alga = self.darbinieks_alga - sn - iin # 4. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodoklis)
            return neto_alga # Atgriež neto algas vērtību
        else: # Ja bruto alga ir lielāka par algas likmi, kura ir 1667 eiro, tad:
            sn = self.darbinieks_alga * self.SN_LIKME # 1. sociālā nodokļa aprēķināšana (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            iin_baze = self.ALGAS_LIKME - sn - atvieglojums # 2. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no algas likmes (1667 eiro) tiek atņemts sociālais nodoklis un atvieglojums)
            iin = iin_baze * self.IIN_LIKME # 3. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            parpalikums = self.darbinieks_alga - self.ALGAS_LIKME # 4. Pārpalikuma aprēķināšana, kuru var izrēķināt, atņemot algas likmi (1667) no bruto algas
            iin2 = parpalikums * self.IIN_LIKME2 # 5. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, šoreiz pareizinot pārpalikumu ar IIN likmi, kad bruto alga pārsniedz 1667 eiro, tas ir 23%
            neto_alga = self.darbinieks_alga - sn - iin - iin2 # 6. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodokļi)
            return neto_alga # Atgriež neto algas vērtību
    
    def index_parbaude(self,idx):
        if idx == []:
            idx = 0
        else:
            idx = int(idx[-1][0])

        if idx != None and idx > 0:
            idx += 1 
        elif idx == None and idx == []:
            idx = 0
        return idx

        
    def saglabasana(self,veids):
        if veids == "txt":
            pass
        elif veids == "db":
            sql_alga = ("""
                    insert into alga (ID_alga, uznemums, neto_alga, darbinieks_ID, darba_devejs_ID) values (%s, %s, %s, %s,%s);
                """)
            sql_darbinieks = ("""
                    insert into darbinieks (ID_darbinieks, darbinieks_vards, darbinieks_uzvards, darbinieks_pk, darbinieks_berni, darbinieks_alga) values (%s, %s, %s, %s,%s, %s);
                """)
            sql_darba_devejs = ("""
                    insert into darba_devejs (ID_darba_devejs, darba_devejs_vards, darba_devejs_uzvards) values (%s, %s);
                """)
            
            self.cursor.execute("SELECT * FROM alga")
            idx = self.cursor.fetchall()
            print(self.index_parbaude(idx))
            alga_data_structure = [self.data["Uznemums"],self.algas_formula()]
            
            # self.data["alga"].insert(0,idx)
            # self.cursor.execute(sql,data)
            # self.db.commit()
            # print('iesniegts!')
        
        


    
stradnieks = Alganators(900,2,"Jaroslavs","Belovs","010100-0101","SIA KLUCĪŠI","Pēteris","Lielais") # Objekta izveide
print(stradnieks.algas_formula()) # metodes izvade
stradnieks.saglabasana("db")