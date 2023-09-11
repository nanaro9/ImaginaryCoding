#Klase
class Mobile():
    # konstruktors
    # self <-- vienmēr būs
    # Pēc self iet īpašības
    def __init__(self,modelis,kamera):
        self.modelis,self.kamera = modelis,kamera

apple = Mobile("Iphone X","16mp")

print(apple.modelis,apple.kamera)