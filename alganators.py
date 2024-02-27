# Programmas autors - Aleksis Počs
# Izstrādāta 5. tēmas ietvaros

import os # Sistēmas bibliotēka, ar kuras palīdzību šajā programmā tiks pārbaudīta faila esamība
import mysql.connector # Tiek nodrošināts savienojums ar bibliotēku "mysql.connector", kura nodrošinās iespēju savienoties ar datu bāzi
import customtkinter # Lietotāja ievades bibliotēka, ērta bibliotēka moderna lietotāja interfeisa izveidei
import pyotp # "Python one-time password" bibliotēka, jeb bibliotēka pagaidu paroļu izveidei
import qrcode # Šī bibliotēka tika izmantota vienu reizi, lai izveidot qr kodu, ar kura palīdzību varēja savienot pyotp ar mobilo autentifikatoru, jeb laika paroļu ģeneratoru

key = 'XGT2BDNVJBTU2JFQCRAVCQPYNFZI2RVI' # base32 atslēgas izveide pyotp bibliotēkai
totp = pyotp.TOTP(key) # totp izveide, jeb "Pagaidu" paroles izveide, kura balstāz uz laiku. Tā atjaunojas katras 30 sekundes bezgalīgi (Time-Based One Time Password)
# uri = totp.provisioning_uri(name="Admin",issuer_name="Algas aprēķina programma") # Tika izveidots speciāls URI - Uniform Resource Identifier ar kura palīdzību varēja izveidot qr kodu, kurš savienos mobilo autentifikatoru ar šīm pagaidu, laika parolēm
# qrcode.make(uri).save("qrcode.png") # qr koda izveide

class Alganators(): # Definē klasi Alganators
    def __init__(self,darbinieks_alga,darbinieks_berni,darbinieks_vards,darbinieks_uzvards,darbinieks_pk,uznemums,darba_devejs_vards,darba_devejs_uzvards): # Klases sākuma uzstādīšana

        self.SN_LIKME = 0.105 # Konstanta Sociālā nodokļa likme 10.5%
        self.IIN_LIKME = 0.2 # Konstanta Iedzīvotāja ienākuma nodokļa likme 20%
        self.IIN_LIKME2 = 0.23 # Konstanta Iedzīvotāja ienākuma nodokļa likme 23%
        self.DD_SN_LIKME = 0.2359 # Konstanta Darba devēja sociālā nodokļa likme 23.59%
        self.APGADAJAMO_LIKME = 250 # Likme par katru apgādājamo personu 250 eiro
        self.ALGAS_LIKME = 1667 # Likme pēc kuras pienākas papildus nodoklis

        self.darbinieks_vards = darbinieks_vards # Pielīdzina klases mainīgo ievadītajam parametram
        self.darbinieks_uzvards = darbinieks_uzvards # Pielīdzina klases mainīgo ievadītajam parametram
        self.darbinieks_pk = darbinieks_pk # Pielīdzina klases mainīgo ievadītajam parametram
        self.darbinieks_alga = float(darbinieks_alga) # definē mainīgo, kura vērtība tiek pielīdzināta objektā ievadītam parametram "darbinieks_alga"
        self.darbinieks_berni = int(darbinieks_berni) # definē mainīgo, kura vērtība tiek pielīdzināta objektā ievadītam parametram "darbinieks_berni"
        self.darba_devejs_vards = darba_devejs_vards # Pielīdzina klases mainīgo ievadītajam parametram
        self.darba_devejs_uzvards = darba_devejs_uzvards # Pielīdzina klases mainīgo ievadītajam parametram
        self.uznemums = uznemums # Pielīdzina klases mainīgo ievadītajam parametram

        self.data = {"Darbinieks": {"Vards":darbinieks_vards,"Uzvards":darbinieks_uzvards,"Personas_kods":darbinieks_pk,"Berni":darbinieks_berni,"Alga":darbinieks_alga},"darba_Devejs":{"Vards":darba_devejs_vards,"Uzvards":darba_devejs_uzvards},"Uznemums":uznemums} # vārdnīcas izveide, kurā tiks glabāti ievadītie dati

        self.db = mysql.connector.connect(host="localhost",database="algaprekins",user="root",password="password") # Programma tiek savienota ar datu bāzi, kuras nosaukums ir "algaprekins"
        self.cursor = self.db.cursor() # Kursora definēšana, ar kura palīdzību var pārvietoties pa datu bāzi

        self.veids = ["darbinieks","darba_devejs","alga"] # saraksta izveide, kurā tiek glabāti MySQL tabulu nosaukumi, ērtai piekļuvei
        self.db_dati = {"darbinieks":[],"darba_devejs":[],"alga":[]} # Vārdnīcas izveide, kas glabās sevī datus no katras MySQL tabulas
        
        for v in self.veids: # For cikla izveide, kura iterēs cauri "self.veids" vārdnīcai pielīdzinot datus mainīgajam "v"
            self.cursor.execute(f"SELECT * FROM {v}") # datu bāzes kursors izpilda komandu "SELECT * FROM {v}", kas nozīmē atlasīt VISUS datus no v, jeb no tabulām - "darbinieks", "darba_devejs" un "alga"
            self.db_dati[v] = self.cursor.fetchall() # iepriekš atlasītos datus ievieto "self.db_dati" vārdnīcā pie "v" atslēgas

    def algas_formula(self): # Definēta funkcija, kura saņems 2 datus, bruto algu un bērnu skaitu
        atvieglojums = self.darbinieks_berni * self.APGADAJAMO_LIKME # atvieglojuma aprēķināšana (bērnu skaits pareizināts ar likmi, kura ir 250 eiro par vienu bērnu)
        if self.darbinieks_alga <= self.ALGAS_LIKME: # Pārbauda, vai bruto alga nav lielāka par algas likmi, kura ir 1667 eiro
            sn = self.darbinieks_alga * self.SN_LIKME # 1. darbība ir sociālā nodokļa aprēķins (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            iin_baze = self.darbinieks_alga - sn - atvieglojums # 2. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no bruto algas tiek atņemts sociālais nodoklis un atvieglojums)
            if iin_baze > 0: # ja mainīgā iin_baze vērtība ir lielāka par nulli
                pass # neko nedara, vienkārši izlaiž šo rindiņu un iziet no if nosacījumiem
            else: # citādi
                iin_baze = 0 # pielīdzina mainīgo iin_baze nullei, sakarā ar to, ka iin_bāze nevar būt negatīva. (citādi darbiniekam no algas, kurai jābūt 700, viņa var izaugt līdz 1000 un tas nav iespējams dzīvē, jo sanāks ka valsts viņam vēl parādā būs +300 eiro)
            iin = iin_baze * self.IIN_LIKME # 3. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            neto_alga = self.darbinieks_alga - sn - iin # 4. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodoklis)
            return neto_alga # Atgriež neto algas vērtību
        else: # Ja bruto alga ir lielāka par algas likmi, kura ir 1667 eiro, tad:
            sn = self.darbinieks_alga * self.SN_LIKME # 1. sociālā nodokļa aprēķināšana (bruto alga pareizināta ar sociālā nodokļa likmi (10.5%))
            iin_baze = self.ALGAS_LIKME - sn - atvieglojums # 2. IIN (iedzīvotāja ienākuma nodokļa) bāzes aprēķināšana (no algas likmes (1667 eiro) tiek atņemts sociālais nodoklis un atvieglojums)
            if iin_baze > 0: # ja mainīgā iin_baze vērtība ir lielāka par nulli
                pass # neko nedara, vienkārši izlaiž šo rindiņu un iziet no if nosacījumiem
            else: # citādi
                iin_baze = 0 # pielīdzina mainīgo iin_baze nullei, sakarā ar to, ka iin_bāze nevar būt negatīva. (citādi darbiniekam no algas, kurai jābūt 700, viņa var izaugt līdz 1000 un tas nav iespējams dzīvē, jo sanāks ka valsts viņam vēl parādā būs +300 eiro)
            iin = iin_baze * self.IIN_LIKME # 3. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, IIN bāze tiek pareizināta ar IIN likmi, kura ir 20%
            parpalikums = self.darbinieks_alga - self.ALGAS_LIKME # 4. Pārpalikuma aprēķināšana, kuru var izrēķināt, atņemot algas likmi (1667) no bruto algas
            iin2 = parpalikums * self.IIN_LIKME2 # 5. IIN (iedzīvotāja ienākuma nodokļa) aprēķināšana, šoreiz pareizinot pārpalikumu ar IIN likmi, kad bruto alga pārsniedz 1667 eiro, tas ir 23%
            neto_alga = self.darbinieks_alga - sn - iin - iin2 # 6. Neto algas (tīrās algas) aprēķināšana, no bruto algas tiek atņemti visi nodokļi (sociālais nodoklis un iedzīvotāja ienākuma nodokļi)
            return neto_alga # Atgriež neto algas vērtību
    
    def index_parbaude(self,idx): # definē metodi "index_parbaude", kas saņems parametru "self", jo tā ir savas klases "Alganators" metode, un "idx", kas nākotnē kļūs par indeksa mainīgo
        if idx == None or idx == []: # Pārbauda vai indekss ir nekas (None), vai tukšs saraksts ([])
            idx = 0 # Šādā situācijā pielīdzina indeksu nullei
        elif idx != None: # citādi, ja indekss tomēr nav nekas (None)
            idx = int(idx[-1][0]) + 1 # Tad pielīdzināt mainīgo "idx" - pēdājai pirmajai indeksa vērtībai pārveidotai par cipariem, sakarā ar to, ka idx vērtība šobrīd ir vienas rindas saraksts no visiem MySQL tabulu sarakstiem, jeb tur ir vairāki saraksti, kuri izskatās aptuveni šādi [ [0,'vards','uzvards','bla-bla'], [0,'alga','nauda','banknotes'], [0,'sia logi',1024,0,0] ] un tiek ņemts pēdējā iekšējā sarakta pirmais, jeb 0 elements, kurš parasti ir (un arī tālāk būs) datu indekss (P.S. es nemāku paskaidrot..)
        return idx # atgriež mainīgo "idx"
    
    def pieskir_index(self,struktura,indeksi): # definē citu metodi "pieskir_index", kura saņems prametrus "self","struktura" un "indeksi"
        for i in struktura: # Ar for cikla palīdzību notiks iterācija cauri saraksta "struktura" elementiem, kurš sastāv no citiem sarakstiem
            i.insert(0,indeksi[struktura.index(i)]) # katrā saraksta "struktura" iekšējā sarakstā ievieto indeksu, kurš izvilkts no cita indeksa, no saraksta "sturktura" no saraksta "indeksi", pašā sākumā, jeb pirms 0. elementa (P.S. es tiešām nevaru izskaidrot.)
            if i == struktura[2]: # Pārbauda vai "struktura" saraksta elements, jeb for cikla mainīgais "i" ir vienāds ar trešo (skaitot no viens) "struktura" saraksta elementu
                i.insert(3,indeksi[0]) # ievieto šajā, mainīgā "i", sarakstā indeksu no 0. "indeksi" saraksta elementa pirms 3. mainīgā "i" saraksta elementa (saraksts "struktura" sastāv no citiem sarakstiem)
                i.insert(4,indeksi[1]) # ievieto šajā, mainīgā "i", sarakstā indeksu no 1. "indeksi" saraksta elementa pirms 4. mainīgā "i" saraksta elementa (saraksts "struktura" sastāv no citiem sarakstiem)
        return struktura # atgriež sarakstu "struktura"
    
    def datu_parbaude(self,data): # definē metodi "datu_parbaude", kura saņems prametrus "self" un "data"
        count = 0 # mainīgais, lai sekot līdzi iterāciju skaitam
        for v in self.veids: # for cikla iterācija cauri "self.veids" sarakstam
            self.cursor.execute(f"SELECT * FROM {v}") # atlasa VISU no "v" mainīgā, jeb mysql tabulu nosaukumiem, sakarā ar to, ka "self.veids" saraksts glabāja sevī mysql tabulu nosaukumus
            self.db_dati[v] = self.cursor.fetchall() # ievieto "self.db_dati" vārdnīcā pie [v] atslēgas (jeb "darbinieks","darba_devejs", "alga") augstāk atlasītos datus
        sakritosie_dati = {"darbinieks":[False,0,False],"darba_devejs":[False,0],"alga":[False,0]} # sakrītošo datu vārdnīcas izveide
        for v in self.db_dati: # iterācija cauri "self.db_dati" vārdnīcai, jeb izvelk šīs vārdnīcas atslēgas
            if self.db_dati[v] != []: # Pārbauda vai "self.db_dati" vārdnīcas saraksts pie [v] atslēgas nav tukšs.
                for i in self.db_dati[v]: # iterē cauri datiem pie atslēgām. notiks 3 ārējās iterācijas, kurās notiks vēl iekšējās - angliski to sauc par "nested loops"
                    for j in i: # iterē cauri elementiem, kurus ieguva no sarakstiem, kurus ieguva no "self.db_dati" vārdnīcas
                        if v == "darbinieks": # skatās vai šīs iterācijas atslēgas nosaukums ir "darbinieks"
                            if i.index(j) == 1 or i.index(j) == 2 or i.index(j) == 3: # Pārbauda vai saraksts, kuram iterē cauri atrodas uz viena no indeksiem
                                if j == data[count][i.index(j)]: # ja datu bāzes datu vārdnīcas saraksta elements pie atslēgas "darbinieks" ir vienāds ar datiem, kuri tika ievadīti "data" sarakstā un pie šī paša elementa indeksa
                                    sakritosie_dati["darbinieks"][1]+=1 # Palielina sakrītošo datu skaitu pie atslēgas "darbinieks" par vienu
                                    if i.index(j) == 3: # Ja tiek iterēts cauri 3 elementam
                                        sakritosie_dati["darbinieks"][2] = True # Apstiprina sakrītošos datus pie atslēgas "darbinieks" (šeit tika pārbaudīts, vai  ievadītais darbinieka personas kods sakrita ar jebkuru no personas kodiem datu bāzē, ja tā, tad to apstiprināja)
                        elif v == "darba_devejs": # skatās vai šīs iterācijas atslēgas nosaukums ir "darba_devejs"
                            if i.index(j) == 1 or i.index(j) == 2: # Pārbauda vai saraksts, kuram iterē cauri atrodas uz viena no indeksiem
                                if j == data[count][i.index(j)]: # ja datu bāzes datu vārdnīcas saraksta elements pie atslēgas "darba_devejs" ir vienāds ar datiem, kuri tika ievadīti "data" sarakstā un pie šī paša elementa indeksa
                                    sakritosie_dati["darba_devejs"][1]+=1 # Palielina sakrītošo datu skaitu pie atslēgas "darba_devejs" par vienu
                        else: # skatās vai šīs iterācijas atslēgas nosaukums ir kāds cits, jeb "alga"
                            if i.index(j) == 1: # Ja tiek iterēts cauri 3 elementam
                                if j == data[count][i.index(j)]: # ja datu bāzes datu vārdnīcas saraksta elements pie atslēgas "alga" ir vienāds ar datiem, kuri tika ievadīti "data" sarakstā un pie šī paša elementa indeksa
                                    sakritosie_dati["alga"][1]+=1 # Palielina sakrītošo datu skaitu pie atslēgas "alga" par vienu
            count+=1 # palielina mainīgā vērtību, lai varētu sekot līdzi iterācijām
        for i in sakritosie_dati: # iterācija cauri "sakritosie_dati" vārdnīcai, jeb izvelk šīs vārdnīcas atslēgas
            if i == "darba_devejs": # skatās vai šīs iterācijas atslēgas nosaukums ir "darba_devejs"
                if sakritosie_dati[i][1] == 1: # ja ir tieši vieni sakrītoši dati
                    sakritosie_dati[i][0] = True # apstiprina to, padarot vienu vērtību pie šīs atslēgas par True
                    return sakritosie_dati[i][0] # atgriež True
            elif i == "darbinieks": # skatās vai šīs iterācijas atslēgas nosaukums ir "darbinieks"
                if sakritosie_dati[i][2]: # Vispirms pārbauda vai "Personas Koda" vērtība pie darbinieka atslēgas saraksta ir patiesa (True)
                    if sakritosie_dati[i][1] > 1: # ja ir vairāk par vienu sakrītošu datu
                        sakritosie_dati[i][0] = True # apstiprina to, padarot vienu vērtību pie šīs atslēgas par True
                        return sakritosie_dati[i][0] # atgriež True
                else:
                    if sakritosie_dati[i][1] >= 2: # ja ir divi vai vairāk sakrītošu datu
                        sakritosie_dati[i][0] = True  # apstiprina to, padarot vienu vērtību pie šīs atslēgas par True
                        return sakritosie_dati[i][0] # atgriež True
            else: # citādi (ja atslēga ir "alga")
                if sakritosie_dati[i][1] == 1: # ja ir tieši vieni sakrītoši dati
                    sakritosie_dati[i][0] = True # apstiprina to, padarot vienu vērtību pie šīs atslēgas par True
                    return sakritosie_dati[i][0] # atgriež True
        return False # ja nevieni dati nesakrita atgriež False

    def saglabasana(self): # definē metodi "saglabasana", kura saņems prametru "self"
        alga_data_structure = [self.data["Uznemums"],self.algas_formula()] # algas datu struktūras izveide (tā ir struktūra, pēc kuras tiks saglabāti dati MySQL datu bāzes tabulā "alga")
        darbinieks_data_structure = [self.data["Darbinieks"]["Vards"],self.data["Darbinieks"]["Uzvards"],self.data["Darbinieks"]["Personas_kods"],self.data["Darbinieks"]["Berni"],self.data["Darbinieks"]["Alga"]] # Darbinieka datu struktūras izveide (tā ir struktūra, pēc kuras tiks saglabāti dati MySQL datu bāzes tabulā "darbinieks")
        darba_devejs_data_structure = [self.data["darba_Devejs"]["Vards"],self.data["darba_Devejs"]["Uzvards"]] # darba devēja datu struktūras izveide (tā ir struktūra, pēc kuras tiks saglabāti dati MySQL datu bāzes tabulā "darba_devejs")

        sql = {
            "Darbinieks":("""insert into darbinieks (ID_darbinieks, darbinieks_vards, darbinieks_uzvards, darbinieks_pk, darbinieks_berni, darbinieks_alga) values (%s, %s, %s, %s,%s, %s);"""),
            "Darba Devejs":("""insert into darba_devejs (ID_darba_devejs, darba_devejs_vards, darba_devejs_uzvards) values (%s,%s, %s);"""),
            "Alga":("""insert into alga (ID_alga, uznemums, neto_alga, darbinieks_ID, darba_devejs_ID) values (%s, %s, %s, %s,%s);""")
            }
        # 4 augšējās rindiņās tika izveidots tā saucamais "query", jeb pieprasījums sql datu bāzei vai kam citam, īsumā - sql pieprasījuma izveide katrai tabulai, tāpēc viss ir tik ērti, smuki, kompakti sakārtots vienā vārdnīcā

        indeksi = [] # tukša indeksu saraksta izveide

        for v in self.veids: # for cikla iterācija cauri "self.veids" sarakstam
            self.cursor.execute(f"SELECT * FROM {v}") # atlasa VISU no "v" mainīgā, jeb mysql tabulu nosaukumiem, sakarā ar to, ka "self.veids" saraksts glabāja sevī mysql tabulu nosaukumus
            indeksi.append(self.index_parbaude(self.cursor.fetchall())) # pievieno visus atlasītos datus, kurus pirms tam pārbauda, izmantojot metodi "self.index_parbaude", indeksu sarakstam

        structures = [darbinieks_data_structure,darba_devejs_data_structure,alga_data_structure] # apvieno visus struktūru sarakstus vienā, kopīgā sarakstā "structures"
        structures = self.pieskir_index(structures,indeksi) # pielīdzina structures mainīgā vērtību - metodes "pieskir_index" atgrieztajiem datiem
        parbaude = self.datu_parbaude(structures) # izveido mainīgo "parbaude", lai pārbaudīt "structures" sarakstā esošo sarakstu datu unikalitāti
        if not parbaude: # pārbaudes laikā netika atrasti dati, kas atkārtojas
            if os.path.isfile(f"C:/Users/Aleks/Documents/alga_{darbinieks_data_structure[3]}.txt"): # pārbauda vai šajā ceļā atrodas sekojošais fails
                savingData = f"\n-Algas aprēķināšanas kopsavilkums-\nVārds/Uzvārds: {darbinieks_data_structure[1]} {darbinieks_data_structure[2]}\nPersonas kods: {darbinieks_data_structure[3]}\nBērnu skaits {darbinieks_data_structure[4]}\nBruto alga: {darbinieks_data_structure[5]}\n\nDarba devējs (Vārds/Uzvārds): {darba_devejs_data_structure[1]} {darba_devejs_data_structure[2]}\nUzņēmums: {alga_data_structure[1]}\n\nNETO ALGA: {alga_data_structure[2]}\n" # izskatīgi sakārto un ievieto datus cilvēkam ērti lasāmā formā
                f = open(f"C:/Users/Aleks/Documents/alga_{darbinieks_data_structure[3]}.txt", "a",encoding="utf8") # atver failu sekojošajā ceļā pievienošanas režīmā (ja tāda nav, viņš to vienkārši izveido)
                f.write(savingData) # ieraksta teksta failā datus no "savingData" mainīgā
                f.close() # pēc darba aizver failu
            else: # ja šajā ceļā NEatrodas šāds fails
                savingData = f"-Algas aprēķināšanas kopsavilkums-\nVārds/Uzvārds: {darbinieks_data_structure[1]} {darbinieks_data_structure[2]}\nPersonas kods: {darbinieks_data_structure[3]}\nBērnu skaits {darbinieks_data_structure[4]}\nBruto alga: {darbinieks_data_structure[5]}\n\nDarba devējs (Vārds/Uzvārds): {darba_devejs_data_structure[1]} {darba_devejs_data_structure[2]}\nUzņēmums: {alga_data_structure[1]}\n\nNETO ALGA: {alga_data_structure[2]}\n" # izskatīgi sakārto un ievieto datus cilvēkam ērti lasāmā formā
                f = open(f"C:/Users/Aleks/Documents/alga_{darbinieks_data_structure[3]}.txt", "w",encoding="utf8") # atver failu sekojošajā ceļā rakstīšanas režīmā (ja tāda nav, viņš to vienkārši izveido)
                f.write(savingData) # ieraksta teksta failā datus no "savingData" mainīgā
                f.close() # pēc darba aizver failu
            count=0 # mainīgais, lai sekot līdzi iterāciju skaitam
            for i in sql: # iterācija, izmantojot for ciklu cauri "sql" vārdnīcas atslēgām
                self.cursor.execute(sql[i],structures[count]) # datu bāzes kursors izpilda katru vaicājumu, kuri tika ierakstīti "sql" vārdnīcā pie katras atslēgas, kurā ievieto datus no "structures" saraksta pie elementa, kurš atbilst iterāciju skaitam
                self.db.commit() # apstiprina pieprasījumu datu bāzei
                count += 1 # palielina izpildīto iterāciju skaitu
            return True # atgriež True, ja dati tika veiksmīgi saglabāti
        else: # citādi
            return False # atgriež False, ja dati netika veiksmīgi saglabāti
        
    def db_upd(self): # definē metodi "db_upd", kura saņems prametru "self"
        for v in self.veids: # iterācija cauri "self.veids" vārdnīcas atslēgām
            self.cursor.execute(f"SELECT * FROM {v}") # atlasa VISU no "v" mainīgā, jeb mysql tabulu nosaukumiem, sakarā ar to, ka "self.veids" saraksts glabāja sevī mysql tabulu nosaukumus
            self.db_dati[v] = self.cursor.fetchall() # iepriekš atlasītos datus ievieto "self.db_dati" vārdnīcā pie "v" atslēgas
    
    def db_dati_return(self): # definē metodi "db_dati_return", kura saņems prametru "self"
        self.db_upd() # izsauc metodi datu "atsvaidzināšanai"
        return self.db_dati # atgriež "atsvaidzinātos" datus
    
    def editDb(self,sql): # definē metodi "editDb", kura saņems prametru "self" un "sql"
        self.db_upd() # izsauc metodi datu "atsvaidzināšanai"
        self.cursor.execute(sql) # izpilda datu rediģēšanu pēc parametra "sql" pieprasījuma
        self.db.commit() # apstiprina izmaiņas datu bāzē
            

def mainApp(): # definē funkciju "mainApp"
    customtkinter.set_appearance_mode("System") # uzstāda galveno aplikācijas tēmu (melno,balto vai sistēmas - tāda, kāda stāv lietotājam uz šo brīdi)
    customtkinter.set_default_color_theme("blue") # uzstāda galveno krāsu aplikācijai

    root = customtkinter.CTk() # izveido galveno logu, jeb sakni
    root.geometry("500x350") # uzstāda loga izmērus
    root.title("Algas aprēķina programma") # uzstāda loga nosaukumu
    root.resizable(False,False) # aizliedz mainīt loga izmēru
    root.grid_columnconfigure((0,1),weight=1) # neesmu pārliecināts, bet varētu būt, ka konfigurē kolonnu elementu izkārtojumu, to svaru
    root.grid_rowconfigure(0,weight=1) # neesmu pārliecināts, bet varētu būt, ka konfigurē rindu elementu izkārtojumu, to svaru

    def errorFrame(text): # funkcijas "errorFrame" izveide, kura pieņem parametru "text"
        frame = customtkinter.CTkToplevel(master=root) # uznirstošā lodziņa izveide
        frame.geometry("1000x200") # uzstāda loga izmērus
        frame.resizable(False,False) # aizliedz mainīt loga izmēru
        frame.title("Uzmanību!") # uzstāda loga nosaukumu
        frame.attributes('-topmost', 'true') # liek lodziņam parādīties virspusē, virs pārējiem logiem

        errorMSG = customtkinter.CTkLabel(master=frame, text=(f"Uzmanību! {text}"), font=("Roboto",32), anchor="center") # teksta elementa izveide
        errorMSG.pack(padx=50, pady=50) # teksta elementa izvietošana lodziņā

    def editFrame(dbDati): # funkcijas "editFrame" izveide, kura pieņem parametru "dbDati"
        frame = customtkinter.CTkFrame(master=root) # rāmja izveide galvenajā logā
        frame.pack(pady=10, padx=20, fill="both", expand=True) # rāmja "pakošana"

        label = customtkinter.CTkLabel(master=frame, text="Speciālais datu piekļuves centrs", font=("Roboto",22)) # teksta elementa izveide
        label.pack(pady=12,padx=10) # teksta elementa izvietošana lodziņā

        entry = customtkinter.CTkEntry(master=frame, placeholder_text="Ievadiet meklējamā informāciju...") # teksta ievades elementa izveide
        entry.pack(pady=12,padx=10) # teksta ievades elementa izvietošana lodziņā

        optionmenu = customtkinter.CTkOptionMenu(frame, values=["Darbinieks", "Darba Devējs", "Alga"]) # Izvēles elementa izveide
        optionmenu.pack(pady=12,padx=10) # izvēles elementa izvietošana lodziņā

        ID_searchButton = customtkinter.CTkButton(master=frame,text="Meklēt pēc ID",font=("Roboto",14),command=lambda: searchResults(entry.get(),optionmenu.get(),"ID")) # pogas izveide meklēšanai pēc ID, kura pēc uzspiešanas izsauc funkciju "searchResults", kura pieņem ievades un izvēles elementu izvēli un "ID" identifikatoru
        PK_searchButton = customtkinter.CTkButton(master=frame,text="Meklēt pēc personas koda",font=("Roboto",14),command=lambda: searchResults(entry.get(),optionmenu.get(),"PK")) # pogas izveide meklēšanai pēc PK, kura pēc uzspiešanas izsauc funkciju "searchResults", kura pieņem ievades un izvēles elementu izvēli un "PK" identifikatoru

        ID_searchButton.pack(pady=12) # meklēšanas podziņas izvietošana lodziņā
        PK_searchButton.pack(pady=12) # meklēšanas podziņas izvietošana lodziņā

        def searchResults(searchInfo,optionChoice,searchMode): # funkcijas "searchResults" izveide, kura pieņem parametru "searchInfo,optionChoice,searchMode"
            dbDati = Alganators(0,0,0,0,0,0,0,0).db_dati_return() # dbDati mainīgā atkārtota izveide, kas izsauc klases "Alganators" "db_dati_return" metodi, atgriežot datu bāzē esošos datus
            options = ["darbinieks","darba_devejs","alga"] # mainīgā "options" izveide, kurā glabāsies visi iespējamie izvēles varianti meklēšanai

            if optionChoice == "Darbinieks": # Pārbauda vai izvēles variants ir "Darbinieks"
                optionChoice = options[0] # piešķir mainīgajam "optionChoice" "options" saraksta pirmo elementu
            elif optionChoice == "Darba Devējs": # Pārbauda vai izvēles variants ir "Darba Devējs"
                optionChoice = options[1] # piešķir mainīgajam "optionChoice" "options" saraksta otro elementu
            else: # citādi
                optionChoice = options[2] # piešķir mainīgajam "optionChoice" "options" saraksta trešo elementu

            if searchMode == "ID": # Ja mainīgais "searchMode" atbilst vērtībai "ID"
                if searchInfo.isdigit(): # pārbauda vai mainīgais "searchInfo" satur ciparus
                    found = False # izveido mainīgo "found", kura vērtība ir False, jeb nepatiess
                    for i in dbDati[optionChoice]: # iterācija cauri datu bāzes vārdnīcas datiem, pie atslēgas "optionChoice", jeb viens no trijiem variantiem: "darbinieks";"darba_devejs";"alga"
                        if int(searchInfo) == i[0]: # pārbauda vai pirmais iterācijas elements atbilst meklētajam "ID"
                            found = True # sakritības gadījumā pārveido mainīgo "found" par True, jeb patiesu
                            editFrame([optionChoice,i]) # izsauc funkciju "editFrame", kurā pārnes parametrus "optionChoice" un "i", jeb tekošās iterācijas elementu no datu bāzes, kas ir saraksts
                    if not found: # pārbauda, ja tomēr mainīgā "found" vērtība netika mainīta
                        errorFrame("Dati ar šādu ID neeksistē!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                else: # pārbauda vai mainīgais "searchInfo" nesatur ciparus 
                    errorFrame("Nepareizi ievadīts ID") # izsauc funkciju "errorFrame" ar sekojošu tekstu
            elif searchMode == "PK": # Ja mainīgais "searchMode" atbilst vērtībai "PK"
                if optionChoice == "darbinieks": # Pārbauda vai izvēles variants ir "darbinieks"
                    found = False # izveido mainīgo "found", kura vērtība ir False, jeb nepatiess
                    for i in dbDati[optionChoice]: # iterācija cauri datu bāzes vārdnīcas datiem, pie atslēgas "optionChoice", jeb viens no trijiem variantiem: "darbinieks";"darba_devejs";"alga"
                        if searchInfo == i[3]: # pārbauda vai ceturtais iterācijas elements atbilst meklētajam "ID"
                            found = True # sakritības gadījumā pārveido mainīgo "found" par True, jeb patiesu
                            editFrame([optionChoice,i]) # izsauc funkciju "editFrame", kurā pārnes parametrus "optionChoice" un "i", jeb tekošās iterācijas elementu no datu bāzes, kas ir saraksts
                    if not found: # pārbauda, ja tomēr mainīgā "found" vērtība netika mainīta
                        errorFrame("Datu ar šādu Personas kodu neeksistē!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                else: # ja mainīgais "optionChoice" nav "darbinieks"
                    errorFrame("Meklēšana TIKAI DARBINIEKA DATIEM!") # izsauc funkciju "errorFrame" ar sekojošu tekstu


        def datu_parbaude(data): # definē funkciju "datu_parbaude", kura saņems parametru "data"
            count = 0 # definē mainīgo iterāciju skaita sekošanai
            sakritosie_dati = {"darbinieks":[False,0],"darba_devejs":[False,0],"alga":[False,0]} # izveido vārdnīcu, kuros tiks glabāti sakrītošo datu esamība un to skaits

        def editFrame(EditData): # definē funkciju "editFrame", kas pieņems parametru "EditData"
            frame = customtkinter.CTkToplevel(master=root) # iznirstošā rāmja izveide galvenajā logā
            frame.geometry("700x450") # rāmja izmēra maiņa
            frame.resizable(False,False) # rāmja izmēru lietotājs mainīt nevarēs
            frame.title("Algas aprēķina programma") # rāmja nosaukuma maiņa
            frame.attributes('-topmost', 'true') # rāmja izvietošana pa priekšu citiem logiem

            innerFrame = customtkinter.CTkFrame(master=frame) # iekšējā rāmja izveide
            innerFrame.pack(pady=10, padx=20, fill="both", expand=True) # iekšējā rāmja izvietošana un konfigurēšana

            label = customtkinter.CTkLabel(master=innerFrame, text="Datu Rediģēšana", font=("Roboto",22)) # teksta elementa izveide
            label.pack(pady=12) # teksta elementa izvietošana


            optionList = {"darbinieks":["Vārds","Uzvārds","Personas Kods","Bērnu Skaits","Bruto Alga"],"darba_devejs":["Vārds","Uzvārds"],"alga":["Uzņēmums","Neto Alga"]} # vārdnīcas izveide ar datu bāzes tabulu atslēgām un aptuvenie tabulu datu kolonnu nosaukumi

            idx = 0 # mainīgā "idx" definēšana iterāciju skaita sekošana
            for v in EditData[1][1:]: # iterācija cauri "EditData" sarakstam
                if idx < len(optionList[EditData[0]]):
                    dataLabel = customtkinter.CTkLabel(master=innerFrame, text=f"{optionList[EditData[0]][idx]}: {str(v)}", font=("Roboto",18)) # teksta elementa izveide, kam piešķir vēlamo rediģējamo datu nosaukumus un to vērtības
                    dataLabel.pack(pady=12) # izvieto datus uz ekrāna
                    idx+=1 # palielina "idx" mainīgā vērtību par vienu

            optionmenu = customtkinter.CTkOptionMenu(frame, values=optionList[EditData[0]]) # "izvēlnes" izveide
            optionmenu.pack(pady=12) # izvieto "izvēlnes" elementu uz lodziņa

            EditBtn = customtkinter.CTkButton(master=frame,text="Rediģēt Izvēlētos Datus",font=("Roboto",14),command=lambda: popupEdit(optionmenu.get(),EditData)) # izveido podziņu
            EditBtn.pack(pady=12) # izvieto podziņu uz ekrāna

            def destroyEditFrameContents(): # definē funkciju "destroyEditFrameContents"
                for f in innerFrame.winfo_children(): # iterācija cauri visiem rediģēšanas lodziņa elementiem
                    f.destroy() # tekošās iterācijas elementu iznīcina, izposta, izārda un sagrauj 😡
                optionmenu.destroy() # iznīcina "izvēlnes" elementu
                EditBtn.destroy() # iznīcina podziņu

            def popupEdit(data_to_edit,editData): # izveido funkciju "popupEdit" ar parametriem "data_to_edit" un "editData"
                destroyEditFrameContents() # izsauc funkciju, kura iznīcina lodziņa elementus

                label = customtkinter.CTkLabel(master=innerFrame, text=f"Datu Rediģēšana ({data_to_edit})", font=("Roboto",22)) # izveido teksta elementu
                label.pack(pady=12) # izvieto teksta elementu

                entry = customtkinter.CTkEntry(master=innerFrame, placeholder_text="Ievadiet vērtību aizstāšanai",width=600) # izveido ievades elementu
                entry.pack(pady=12) # izvieto ievades elementu

                btn = customtkinter.CTkButton(master=innerFrame, text="Rediģēt/Aizstāt",width=400,command=lambda:check(entry.get(),editData[1],editData[0],data_to_edit)) # izveido podziņu
                btn.pack(pady=12) # izvieto podziņu lodziņā

            def check(entryData,data,option,optionOption): # definē funkciju "check" ar parametriem "entryData", "data", "option", "optionOption"
                if entryData == '': # pārbauda vai "entryData" mainīgā vērtība ir tukšs teksts
                    errorFrame(f"lauciņš palika tukšs!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                    return False # atgriež False
                if optionOption == "Uzņēmums": # pārbauda vai mainīgais "optionOption" ir "Uzņēmums"
                    if entryData.isdigit(): # pārbauda vai "entryData" mainīgais satur ciparus
                        errorFrame(f"lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                if option == "darbinieks" or option == "darba_devejs": # pārbauda vai mainīgā "option" vērtība ir "darbinieks" vai "darba_devejs"
                    if optionOption == "Vārds" or optionOption == "Uzvārds": # pārbauda vai "optionOption" ir "Vārds" vai "Uzvārds"
                            if entryData.isdigit(): # pārbauda vai "entryData" mainīgais satur ciparus
                                errorFrame(f"lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                                return False # atgriež False
                if optionOption == "Personas Kods": # ja "optionOption" ir "Personas Kods"
                    if len(entryData) < 12: # pārbauda vai "entryData" mainīgā vērtības garums ir mazāks par 12
                        errorFrame(f"lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                    if not entryData[:6].isdigit() or not entryData[7:].isdigit() or entryData[6] != "-": # pārbauda vai "entryData" mainīgā vērtība līdz 7. simbolam nav cipars vai vērtība no 8. simbola nav cipars, vai 7. simbols nav "-"
                        errorFrame(f"lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                if optionOption == "Bruto Alga" or optionOption == "Bērnu Skaits" or optionOption == "Neto Alga": # pārbauda vai mainīgā "optionOption" ir "Bruto Alga" vai "BĒrnu Skaits", vai "Neto Alga"
                    if not entryData.isdigit(): # pārbauda vai "entryData" mainīgais NEsatur ciparus
                        errorFrame(f"lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                    
                valIdx = {"darbinieks":{"Vārds":1,"Uzvārds":2,"Personas Kods":3,"Bērnu Skaits":4,"Bruto Alga":5},"darba_devejs":{"Vārds":1,"Uzvārds":2},"alga":{"Uzņēmums":1,"Neto Alga":2}} # indeksu numerācija katrā no strukturētiem datu sarakstiem
                
                if entryData == data[valIdx[option][optionOption]]: # pārbaude vai "entryData" mainīgā vērtība atbilst saraksta "data" elementam pie specifiskā elementa indeksa, kuru nosaka no "valIdx" vārdnīca
                    errorFrame("Ievadiet JAUNUS datus!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                    return False # atgriež False
                
                if option == "darbinieks" or "darba_devejs": # ja mainīgā "option" vērtība ir "darbinieks" vai "darba_devejs"
                    if optionOption == "Vārds": # ja mainīgā "optionOption" vērtība ir "Vārds"
                        for i in dbDati[option]: # iterācija cauri "dbDati" vārdnīcai pie atslēgas "option"
                            if entryData == i[valIdx[option][optionOption]] and data[valIdx[option]["Uzvārds"]] == i[valIdx[option]["Uzvārds"]]: # pārbaude vai "entryData" mainīgā vērtība atbilst tekošās iterācijas vērtības elementam pie konkrēta indeksa un, vai "data" vārdnīcas elements "Uzvārds" pie konkrētas atslēgas sakrīt ar tekošās iterācijas vērtības elementu pie konkrēta indeksa 
                                errorFrame("Šādi dati jau iekļauti datu bāzē!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                                return False # atgriež False
                    elif optionOption == "Uzvārds": # citādi ja "optionOption" vērtība ir "Uzvārds"
                        for i in dbDati[option]: # iterācija cauri "dbDati" vārdnīcai pie atslēgas "option"
                            if entryData == i[valIdx[option][optionOption]] and data[valIdx[option]["Vārds"]] == i[valIdx[option]["Vārds"]]: # pārbaude vai "entryData" mainīgā vērtība atbilst tekošās iterācijas vērtības elementam pie konkrēta indeksa un, vai "data" vārdnīcas elements "Vārds" pie konkrētas atslēgas sakrīt ar tekošās iterācijas vērtības elementu pie konkrēta indeksa 
                                errorFrame("Šādi dati jau iekļauti datu bāzē!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                                return False # atgriež False
                            
                if optionOption == "Personas Kods" or "Uzņēmums": # ja "optionOption" vērtība ir "Uzņēmums" vai "Personas Kods"
                    for i in dbDati[option]: # iterācija cauri "dbDati" vārdnīcai pie atslēgas "option"
                        if entryData == i[valIdx[option][optionOption]]: # pārbaude vai "entryData" mainīgā vērtība atbilst tekošās iterācijas vērtības elementam pie konkrēta indeksa
                            errorFrame("Šādi dati jau iekļauti datu bāzē!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                            return False # atgriež False

                tableNames = {"darbinieks":{"Vārds":"darbinieks_vards","Uzvārds":"darbinieks_uzvards","Personas Kods":"darbinieks_pk","Bērnu Skaits":"darbinieks_berni","Bruto Alga":"darbinieks_alga"},"darba_devejs":{"Vārds":"darba_devejs_vards","Uzvārds":"darba_devejs_uzvards"},"alga":{"Uzņēmums":"uznemums","Neto Alga":"neto_alga"}} # vārdnīcas izveide ar tabulu nosaukumiem un tabulu kolonnu nosaukumiem, vieglai piekļuvei
                sqlQuery = ("UPDATE %s SET %s = '%s' WHERE ID_%s ='%s' " % (option,tableNames[option][optionOption],entryData,option,data[0])) # sql pieprasījuma izveide ar konkrētiem datiem
                Alganators(0,0,0,0,0,0,0,0).editDb(sqlQuery) # klases "Alganators" "editDb" metodes izsaukšana ar parametru "sqlQuery"

    def stepsFrame(data,obj_alga): # "stepsFrame" funkcijas definēšana ar parametriem "data", "obj_alga"
        frame = customtkinter.CTkToplevel(master=root) # iznirstošā rāmja izveide galvenajā logā
        frame.geometry("700x400") # rāmja izmēra maiņa
        frame.resizable(False,False) # rāmja izmēru lietotājs mainīt nevarēs
        frame.title("Algas aprēķina programma") # rāmja nosaukuma maiņa
        frame.attributes('-topmost', 'true') # rāmja izvietošana pa priekšu citiem logiem

        innerFrame = customtkinter.CTkFrame(master=frame) # iekšējā rāmja izveide
        innerFrame.pack(pady=10, padx=20, fill="both", expand=True) # iekšējā rāmja izvietošana un konfigurēšana

        label = customtkinter.CTkLabel(master=innerFrame, text="Aprēķina soļi", font=("Roboto",22)) # teksta elementa izveide
        label.grid(row=0, column=0, padx=20, pady=10,sticky="nsew") # teksta elementa izvietošana režģa veidā

        if int(data["Bruto alga"]) < 1667: # pārbauda vai skaitlis no "data" vārdnīcas pie atslēgas "Bruto alga" ir mazāks par 1667
            step1 = customtkinter.CTkLabel (master=innerFrame, text=f"1. Solis [SN]: Bruto alga * 10.5% = {int(data['Bruto alga']) * 0.105}") # teksta elementa izveide
            iin_baze = (int(data['Bruto alga']) - (int(data['Bruto alga']) * 0.105) - (int(data['Bērnu skaits'])*250)) # mainīgā iin_baze izveide, kas aprēķina iin bāzi pēc klasē "Alganators" dotās formulas
            step2 = customtkinter.CTkLabel (master=innerFrame, text=f"2. Solis [Atvieglojums]: Bērnu skaits * 250 = {(int(data['Bērnu skaits'])*250)}") # teksta elementa izveide
            if iin_baze > 0: # pārbaude vai iin_baze mainīgā vērtība ir lielāka par 0
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: Bruto alga - SN - Atvieglojums = {iin_baze}") # teksta elementa izveide
            else: # ja iin_baze mainīgā vērtība ir mazāka par 0
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: Bruto alga - SN - Atvieglojums = {iin_baze}, jeb IIN bāze = 0") # teksta elementa izveide
                iin_baze = 0 # iin_baze mainīgo pielīdzina 0
            step4 = customtkinter.CTkLabel (master=innerFrame, text=f"4. Solis [IIN]: IIN bāze * 20% = {iin_baze * 0.2}") # teksta elementa izveide
            step5 = customtkinter.CTkLabel (master=innerFrame, text=f"5. Solis [Neto alga]: Bruto alga - SN - IIN = {obj_alga}") # teksta elementa izveide
            step1.grid(pady=5,padx=10,sticky="nsew",row=1,column=0) # teksta elementa izvietošana logā 1. rindā
            step2.grid(pady=5,padx=10,sticky="nsew",row=2,column=0) # teksta elementa izvietošana logā 2. rindā
            step3.grid(pady=5,padx=10,sticky="nsew",row=3,column=0) # teksta elementa izvietošana logā 3. rindā
            step4.grid(pady=5,padx=10,sticky="nsew",row=4,column=0) # teksta elementa izvietošana logā 4. rindā
            step5.grid(pady=5,padx=10,sticky="nsew",row=5,column=0) # teksta elementa izvietošana logā 5. rindā
        else: # citādi, ja skaitlis no "data" vārdnīcas pie atslēgas "Bruto alga" ir lielāks par 1667
            step1 = customtkinter.CTkLabel (master=innerFrame, text=f"1. Solis [SN]: Bruto alga * 10.5% = {int(data['Bruto alga']) * 0.105}") # teksta elementa izveide
            iin_baze = (1667 - (int(data['Bruto alga']) * 0.105) - (int(data['Bērnu skaits'])*250)) # mainīgā iin_baze izveide, kas aprēķina iin bāzi pēc klasē "Alganators" dotās formulas
            step2 = customtkinter.CTkLabel (master=innerFrame, text=f"2. Solis [Atvieglojums]: Bērnu skaits * 250 = {(int(data['Bērnu skaits'])*250)}") # teksta elementa izveide
            if iin_baze > 0: # pārbaude vai iin_baze mainīgā vērtība ir lielāka par 0
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: 1667 - SN - Atvieglojums = {iin_baze}") # teksta elementa izveide
            else: # citādi
                step3 = customtkinter.CTkLabel (master=innerFrame, text=f"3. Solis [IIN bāze]: 1667 - SN - Atvieglojums = {iin_baze}, jeb IIN bāze = 0") # teksta elementa izveide
                iin_baze = 0 # iin_baze mainīgā vērtība pielīdzināta 0
            parpalikums = int(data['Bruto alga']) - 1667 # pārpalikuma aprēķins pēc formulas no "Alganators" klases aprēķina metodes
            step4 = customtkinter.CTkLabel (master=innerFrame, text=f"4. Solis [IIN]: IIN bāze - 10.5% = {iin_baze * 0.105}") # teksta elementa izveide
            step5 = customtkinter.CTkLabel (master=innerFrame, text=f"5. Solis [Pārpalikums]: Bruto alga - 1667 = {parpalikums}") # teksta elementa izveide
            step6 = customtkinter.CTkLabel (master=innerFrame, text=f"6. Solis [IIN 2]: Pārpalikums * 23% = {parpalikums * 0.23}") # teksta elementa izveide
            step7 = customtkinter.CTkLabel (master=innerFrame, text=f"7. Solis [Neto alga]: Bruto alga - SN - IIN - IIN 2 = {obj_alga}") # teksta elementa izveide
            step1.grid(pady=5,padx=10,sticky="nsew",row=1,column=0) # teksta elementa izvietošana logā 1. rindā
            step2.grid(pady=5,padx=10,sticky="nsew",row=2,column=0) # teksta elementa izvietošana logā 2. rindā
            step3.grid(pady=5,padx=10,sticky="nsew",row=3,column=0) # teksta elementa izvietošana logā 3. rindā
            step4.grid(pady=5,padx=10,sticky="nsew",row=4,column=0) # teksta elementa izvietošana logā 4. rindā
            step5.grid(pady=5,padx=10,sticky="nsew",row=5,column=0) # teksta elementa izvietošana logā 5. rindā
            step6.grid(pady=5,padx=10,sticky="nsew",row=6,column=0) # teksta elementa izvietošana logā 6. rindā
            step7.grid(pady=5,padx=10,sticky="nsew",row=7,column=0) # teksta elementa izvietošana logā 7. rindā


        netoLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Neto Alga: {'{:.2f}'.format(obj_alga)}", font=("Roboto",20),justify="center",wraplength=150) # teksta gabala izveide
        netoLabel.grid(row=3, column=1, padx=20, pady=10,sticky="nsew") # teksta elementa izvietošana logā 3. rindā 1. kolonnā

        author = customtkinter.CTkLabel(master=frame,text="© Aleksis Počs 2024") # autortiesības teksta elements
        author.pack() # autortiesību teksta elementa iepakošana

    def savingGUI(bool): # funkcijas "savingGUI" definēšana ar parametru "bool"
        if bool: # ja "bool" parametrs ir patiess
            print("saved") # izvada tekstu "saved"
        else: # ja "bool" parametrs NAV patiess
            print("fail") # izvada tekstu "fail"

    def outputFrame(data): # definē funkciju "outputFrame" ar parametru data
        frame = customtkinter.CTkToplevel(master=root) # iznirstošā rāmja izveide galvenajā logā
        frame.geometry("900x350") # rāmja izmēra maiņa
        frame.resizable(False,False) # rāmja izmēru lietotājs mainīt nevarēs
        frame.title("Algas aprēķina programma") # rāmja nosaukuma maiņa
        frame.attributes('-topmost', 'true') # rāmja izvietošana pa priekšu citiem logiem
        
        name=data["Vārds/Uzvārds"].split(" ") # izveido mainīgo name un piešķir tam sadalīto "data" vārdnīcas vērtību pie atslēgas "Vārds/Uzvārds"
        ddName=data["Darba devējs"].split(" ") # izveido mainīgo ddName un piešķir tam sadalīto "data" vārdnīcas vērtību pie atslēgas "Darba devējs"

        obj = Alganators(data["Bruto alga"],data["Bērnu skaits"],name[0],name[1],data["Personas Kods"],data["Uzņēmums"],ddName[0],ddName[1]) # objekta izveide klasei "Alganators"
        obj_alga = obj.algas_formula() # tikko izveidotajam objektam izsauc metodi "algas_formula" un tās vērtību piešķir mainīgajam "obj_alga"

        innerFrame = customtkinter.CTkFrame(master=frame) # izveido iekšējo lodziņu
        innerFrame.pack(pady=10, padx=20, fill="both", expand=True) # izvieto iekšējo lodziņu

        label = customtkinter.CTkLabel(master=innerFrame, text="Algas aprēķina programma", font=("Roboto",22)) # izveido teksta elementu
        label.grid(row=0, column=0, padx=20, pady=10,sticky="nsew") # izvieto teksta elementu

        nameLabel = customtkinter.CTkLabel (master=innerFrame, text=f"Vārds/Uzvārds: {data['Vārds/Uzvārds']}") #izveido teksta elementu vārdam
        pkLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Personas Kods: {data['Personas Kods']}") #izveido teksta elementu personas kodam
        brutoLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Bruto Alga: {data['Bruto alga']}") #izveido teksta elementu bruto algai
        childLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Bērnu Skaits: {data['Bērnu skaits']}") #izveido teksta elementu bērnu skaitam
        ddLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Darba Devējs (Vārds/Uzvārds): {data['Darba devējs']}") #izveido teksta elementu darba devējam
        companyLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Uzņēmums: {data['Uzņēmums']}") #izveido teksta elementu uzņēmumam
            
        nameLabel.grid(pady=5,padx=10,sticky="nsew",row=1,column=0) #teksta elementa izviedošana režģī, 1. rindā
        pkLabel.grid(pady=5,padx=10,sticky="nsew",row=2) #teksta elementa izviedošana režģī, 2. rindā
        brutoLabel.grid(pady=5,padx=10,sticky="nsew",row=3) #teksta elementa izviedošana režģī, 3. rindā
        childLabel.grid(pady=5,padx=10,sticky="nsew",row=4) #teksta elementa izviedošana režģī, 4. rindā
        ddLabel.grid(pady=5,padx=10,sticky="nsew",row=5) #teksta elementa izviedošana režģī, 5. rindā
        companyLabel.grid(pady=5,padx=10,sticky="nsew",row=6) #teksta elementa izviedošana režģī, 6. rindā

        netoLabel = customtkinter.CTkLabel(master=innerFrame, text=f"Neto Alga: {'{:.2f}'.format(obj_alga)}", font=("Roboto",20),justify="center",wraplength=150) # teksta elementa izveide
        netoLabel.grid(row=3, column=1, padx=20, pady=10,sticky="nsew") # teksta elementa izvietošana

        check_var = customtkinter.StringVar(value="off") # lietotāja piekrišanas vērtības izveide

        def userAgreementCheck(val): # funkcijas izveide, kura pārbauda lietotāja piekrišanu nosacījumiem
            if val == "off": # pārbauda vai vērtība ir "off"
                errorFrame("Jūs nepiekritāt datu saglabāšanas nosacījumiem!") # izsauc kļūdu, parāda lietotājam, ka viņš nepiekrita nosacījumiem
            elif val == "on": # ja vērtība ir "on"
                savingGUI(obj.saglabasana()) # izsauc saglabāšanas funkciju

        calculationBtn = customtkinter.CTkButton(master=innerFrame,text="Aprēķina Soļi",font=("Roboto",14),command=lambda: stepsFrame(data,obj_alga)) # aprēķina podziņas izveidošana
        saveBtn = customtkinter.CTkButton(master=innerFrame,text="Saglabāt datus",font=("Roboto",14), command=lambda: userAgreementCheck(check_var.get())) # saglabāšanas podziņas izveide
        checkbox = customtkinter.CTkCheckBox(innerFrame, text="Es piekrītu, ka mani dati tiks saglabāti datu bāzē", variable=check_var, onvalue="on", offvalue="off") # lietotāja pierkišanas (user agreement) izveide

        calculationBtn.grid(pady=5,padx=10,sticky="nsew",row=6,column=1) # aprēķina podziņas izvietošana
        checkbox.grid(pady=5,padx=10,sticky="nsew",row=5,column=1) # lietotāja piekrišanas izvietošana
        saveBtn.grid(pady=5,padx=10,sticky="nsew",row=6,column=2) # saglabāšanas podziņas izvietošana

        author = customtkinter.CTkLabel(master=frame,text="© Aleksis Počs 2024") # teksta elementa izveide
        author.pack() # teksta elementa izvietošana

    def inputFrame(): # "inputFrame" funkcijas definēšana
        frame = customtkinter.CTkFrame(master=root) # lodziņa izveide
        frame.pack(pady=10, padx=20, fill="both", expand=True) # lodziņa izvietošana

        def check(): # funkcijas "check" definēšana
            data = {"Vārds/Uzvārds":nameEntry.get(),"Personas Kods":pkEntry.get(),"Bruto alga":brutoEntry.get(),"Bērnu skaits":childEntry.get(),"Darba devējs":ddEntry.get(),"Uzņēmums":companyEntry.get()} # mainīgā "data" izveidošana, kas ir vārdnīca ar visiem lietotāja ievadītiem datiem iekšā
            for i in data: # iterācija cauri "data" vārdnīcas atslēgām
                if data[i]=='': # ja vērtība pie "i" atslēgas vārdnīcā "data" ir tukša
                    errorFrame(f"{i} lauciņš palika tukšs!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                    return False # atgriež False
                if i == "Vārds/Uzvārds" or i == "Darba devējs" or i == "Uzņēmums": # pārbaude vai atslēga ir "Vārds/Uzvārds" vai "Darba devējs", vai "Uzņēmums"
                    if data[i].isdigit(): # pārbaude vai "data" vērtība pie atslēgas "i" ir skaitlis
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                    if i == "Vārds/Uzvārds" or i == "Darba devējs": # pārbaude vai atslēga ir "Vārds/Uzvārds" vai "Darba devējs", vai "Uzņēmums"
                        if len(data[i].split(" ")) != 2: # pārbauda vai sadalītas vārdnīcas "data" pie atslēgas "i" vērtības, jeb saraksta garums nav 2
                            errorFrame(f"{i} lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                            return False # atgriež False
                if i == "Personas Kods": # pārbaude vai atslēga ir "Vārds/Uzvārds" vai "Darba devējs", vai "Uzņēmums"
                    if len(data[i]) < 12: # pārbauda vai vārdnīcas "data" pie atslēgas "i" vērtības garums ir mazāks par 12
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                    if not data[i][:6].isdigit() or not data[i][7:].isdigit() or data[i][6] != "-": # pārbauda vai vārdnīcas "data" vērtība pie atslēgas "i" nav cipars līdz 7. simbolam vai no 8. simbola, vai vārdnīcas "data" vērtība pie atslēgas "i" tieši 6 simbola vietā nav "-"
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
                if i == "Bruto alga" or i == "Bērnu skaits": # pārbaude vai atslēga ir "Bruto alga" vai "Bērnu skaits"
                    if not data[i].isdigit(): # pārbaude vai "data" vērtība pie atslēgas "i" nav skaitlis
                        errorFrame(f"{i} lauciņš netika aizpildīts korekti!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
                        return False # atgriež False
            outputFrame(data) # izsauc funkciju "outputFrame" ar parametru "data", jo tas izgāja pārbaudi


        label = customtkinter.CTkLabel(master=frame, text="Algas aprēķina programma", font=("Roboto",22)) # teksta elementa izveide (tituls, galvenais teksts)
        label.grid(row=0, column=0, padx=20, pady=10,sticky="nsew") # teksta elementa izvietošana režģī
        nameEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Vārds/Uzvārds") # ievades elementa izveide
        pkEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Personas Kods") # ievades elementa izveide
        brutoEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Bruto Alga") # ievades elementa izveide
        childEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Bērnu Skaits") # ievades elementa izveide
        ddEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Darba Devējs (Vārds/Uzvārds)") # ievades elementa izveide
        companyEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Uzņēmums") # ievades elementa izveide
        aprekinatButton = customtkinter.CTkButton(master=frame, text="Aprēķināt", command=check) # pogas elementa izveide

        nameEntry.grid(pady=5,padx=10,sticky="nsew",row=1) # ievades elementa izvietošana režģī 1. rindā
        pkEntry.grid(pady=5,padx=10,sticky="nsew",row=2) # ievades elementa izvietošana režģī 2. rindā
        brutoEntry.grid(pady=5,padx=10,sticky="nsew",row=3) # ievades elementa izvietošana režģī 3. rindā
        childEntry.grid(pady=5,padx=10,sticky="nsew",row=4) # ievades elementa izvietošana režģī 4. rindā
        ddEntry.grid(pady=5,padx=10,sticky="nsew",row=5) # ievades elementa izvietošana režģī 5. rindā
        companyEntry.grid(pady=5,padx=10,sticky="nsew",row=6) # ievades elementa izvietošana režģī 6. rindā
        aprekinatButton.grid(pady=5,padx=5,row=6,column=1) # pogas elementa izvietošana režģī 6. rindas 1. kolonnā

        author = customtkinter.CTkLabel(master=root,text="© Aleksis Počs 2024") # programmas autora teksta elementa izveide
        author.pack() # programmas autora teksta elementa izvietošana

    def loginFrame(): # "loginFrame" funkcijas izveide
        def login(): # "login" funkcijas izveide
            credentials = {"Login_Input":loginEntry.get(),"Password_Input":passwordEntry.get()} # pieejas datu vārdnīcas izveide, vieglai piekļuvei
            if credentials["Login_Input"] != "Admin" or not totp.verify(credentials["Password_Input"]): # pārbaude vai dati no vārdnīcas "credentials" nav pareizi ievadīti, nav pārbaudīti (verify)
                errorFrame("Lietotājvārds vai parole tika ievadīta nepareizi!") # izsauc funkciju "errorFrame" ar sekojošu tekstu
            elif credentials["Login_Input"] == "Admin" or totp.verify(credentials["Password_Input"]): # citādi, ja visi dati tika ievadīti pareizi
                loginframe.destroy() # iznīcināt "loginframe" rāmi/logu
                editFrame(Alganators(0,0,0,0,0,0,0,0).db_dati_return()) # izsauc "editFrame" funkciju, jeb datu piekļuves/rediģēšanas režīma uzsākšana

        def guest(): # funkcija "guest" izveide
            loginframe.destroy() # "loginframe" loga iznīcināšana
            inputFrame() # ievades loga/rāmja izsaukšana
            
        loginframe = customtkinter.CTkFrame(master=root) # rāmja izveide
        loginframe.pack(pady=20, padx=60, fill="both", expand=True) # rāmja izvietošana logā

        label = customtkinter.CTkLabel(master=loginframe, text="Sveicināti, Lietotāj!", font=("Roboto",22)) # teksta elementa izveide, virsraksts
        label.pack(pady=12,padx=10) # teksta elementa, virsraksta izvietošana

        loginEntry = customtkinter.CTkEntry(master=loginframe, placeholder_text="Lietotājvārds") # lietotājvārda ievades izveide
        loginEntry.pack(pady=12,padx=10)  # lietotājvārda ievades izvietošana rāmī

        passwordEntry = customtkinter.CTkEntry(master=loginframe, placeholder_text="Key", show="*") # paroles ievades izveide
        passwordEntry.pack(pady=12,padx=10) # paroles ievades izvietošana rāmī

        loginbutton = customtkinter.CTkButton(master=loginframe, text="Pieslēgties", command=login) # administratora ieejas pogas izveide
        loginbutton.pack(pady=12,padx=10) # administratora ieejas pogas izvietošana rāmī

        guestButton = customtkinter.CTkButton(master=loginframe, text="Viesa režīms", command=guest) # viesa pogas izveide
        guestButton.pack(pady=12,padx=10) # viesa pogas izvietošana rāmī

    loginFrame() # izsauc funkciju "loginFrame"

    root.mainloop() # uzsāk galveno ciklu. nezinu ko tas dara, bet domāju, ka ar šī cikla palīdzību notiek aplikācijas darbināšana, cikls maina kadrus.

mainApp() # izsauc "mainApp" funkciju, jeb startē aplikāciju! :)