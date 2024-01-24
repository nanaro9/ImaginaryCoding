# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

import mysql.connector # Tiek nodrošināts savienojums ar bibliotēku "mysql.connector", kura nodrošinās iespēju savienoties ar datu bāzi

class Alganators(): # Definē klasi Alganators
    def __init__(self,darbinieks_alga,darbinieks_berni): # Klases sākuma uzstādīšana

        self.SN_LIKME = 0.105 # Konstanta Sociālā nodokļa likme 10.5%
        self.IIN_LIKME = 0.2 # Konstanta Iedzīvotāja ienākuma nodokļa likme 20%
        self.IIN_LIKME2 = 0.23 # Konstanta Iedzīvotāja ienākuma nodokļa likme 23%
        self.DD_SN_LIKME = 0.2359 # Konstanta Darba devēja sociālā nodokļa likme 23.59%
        self.APGADAJAMO_LIKME = 250 # Likme par katru apgādājamo personu 250 eiro
        self.ALGAS_LIKME = 1667 # Likme pēc kuras pienākas papildus nodoklis

        self.darbinieks_vards = None # Vienkārši definē tukšu mainīgo
        self.darbinieks_uzvards = None # Vienkārši definē tukšu mainīgo
        self.darbinieks_pk = None # Vienkārši definē tukšu mainīgo
        self.darbinieks_alga = darbinieks_alga # definē mainīgo, kura vērtība tiek pielīdzināta objekta ievadītiem datiem "darbinieks_alga"
        self.darbinieks_berni = darbinieks_berni # definē mainīgo, kura vērtība tiek pielīdzināta objekta ievadītiem datiem "darbinieks_berni"
        self.darba_devejs_vards = None # Vienkārši definē tukšu mainīgo
        self.darba_devejs_uzvards = None # Vienkārši definē tukšu mainīgo
        self.uznemums = None # Vienkārši definē tukšu mainīgo

        self.db = mysql.connector.connect(host="localhost",database="algaprekins",user="root",password="password") # Programma tiek savienota ar datu bāzi, kuras nosaukums ir "algaprekins"
        self.cursor = self.db.cursor() # Kursora definēšana, ar kura palīdzību var pārvietoties pa datu bāzi

        self.cursor.execute("SELECT * FROM darbinieks") # izvēlas visus datus no tabulas "darbinieks"
        self.darbinieki = self.cursor.fetchall() # Saņem augstāk izvēlētos datus un pielīdzina tos mainīgajam "darbinieki"

        self.cursor.execute("SELECT * FROM darba_devejs") # izvēlas visus datus no tabulas "darba_devejs"
        self.darba_deveji = self.cursor.fetchall() # Saņem augstāk izvēlētos datus un pielīdzina tos mainīgajam "darba_deveji"

    def algas_formula(self): # Definēta funkcija, kura saņems 2 datus, bruto algu un bērnu skaitu
        if self.darbinieks_alga <= self.ALGAS_LIKME: # Pārbauda, vai bruto alga nav lielāka par algas likmi, kura ir 1667 eiro
            sn = self.darbinieks_alga * self.SN_LIKME # 1. darbība ir sociālā nodokļa aprēķins (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            atvieglojums = self.darbinieks_berni * self.APGADAJAMO_LIKME # 2. atvieglojuma aprēķināšana (bērnu skaits pareizināts ar likmi, kura ir 250 eiro par vienu bērnu)
            iin_baze = self.darbinieks_alga - sn - atvieglojums # 3. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no bruto algas tiek atņemts sociālais nodoklis un atvieglojums)
            iin = iin_baze * self.IIN_LIKME # 4. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            neto_alga = self.darbinieks_alga - sn - iin # 5. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodoklis)
            return neto_alga # Atgriež neto algas vērtību
        else: # Ja bruto alga ir lielāka par algas likmi, kura ir 1667 eiro, tad:
            sn = self.darbinieks_alga * self.SN_LIKME # 1. sociālā nodokļa aprēķināšana (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            atvieglojums = self.darbinieks_berni * self.APGADAJAMO_LIKME # 2. atvieglojuma aprēķināšana (bērnu skaits pareizināts ar likmi, kura ir 250 eiro par vienu bērnu)
            iin_baze = self.ALGAS_LIKME - sn - atvieglojums # 3. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no algas likmes (1667 eiro) tiek atņemts sociālais nodoklis un atvieglojums)
            iin = iin_baze * self.IIN_LIKME # 4. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            parpalikums = self.darbinieks_alga - self.ALGAS_LIKME # 5. Pārpalikuma aprēķināšana, kuru var izrēķināt, atņemot algas likmi (1667) no bruto algas
            iin2 = parpalikums * self.IIN_LIKME2 # 6. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, šoreiz pareizinot pārpalikumu ar IIN likmi, kad bruto alga pārsniedz 1667 eiro, tas ir 23%
            neto_alga = self.darbinieks_alga - sn - iin - iin2 # 7. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodokļi)
            return neto_alga # Atgriež neto algas vērtību
    
a = Alganators(900,2) # Objekta izveide
print(a.algas_formula()) # metodes izvade