class CSDD_Auto:
    def __init__(self, zimols, modelis, reg_datums, pilna_masa, degvielas_veids):
        self.zimols = zimols
        self.modelis = modelis
        self.reg_datums = reg_datums
        self.pilna_masa = pilna_masa
        self.degvielas_veids = degvielas_veids
    
    def Info(self):
        print("Zīmols:",self.zimols)
        print("Modelis:",self.modelis)
        print("Reģistrācijas Datums:",self.reg_datums)
        print("Pilna masa:",self.pilna_masa)
        print("Degvielas Veids:",self.degvielas_veids)


Objekts = CSDD_Auto("Audi","A4","22.10.2019",1800,"BG")
Objekts.Info()