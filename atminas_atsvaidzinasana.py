#// 1. Uzdevums

def ievade():
    ievade1 = int(input("Ievadi pirmo skaitli: "))
    ievade2 = int(input("Ievadi otro skaitli: "))

    print(ievade1,"+",ievade2,"=",(ievade1+ievade2))
    print(ievade1,"-",ievade2,"=",(ievade1-ievade2))
    print(ievade1,"x",ievade2,"=",(ievade1*ievade2))
    print(ievade1,"/",ievade2,"=",int(round((ievade1/ievade2),0)))

# ievade()

#// 2. Uzdevums

def uzMetriem():
    InchIevade = float(input('Ievadi inchus: '))
    m = (InchIevade * 0.0254)
    print(int(InchIevade),"inči ir",m,"metri")
    
# uzMetriem()

#// 3. Uzdevums

def laukums():
    baze = float(input("Ievadi trijstūra bāzes malu: "))
    augstums = float(input("Ievadi trijstūra augstumu: "))
    S = 1/2*baze*augstums
    print('Trijstūra laukums ir:',int(S))

# laukums()

#// 4. Uzdevums

def XY(x,y):
    x = int(x)
    y = int(y)

    if x == y:
        print(1)
    elif x > y:
        print(2)
    elif x < y:
        print(3)

# XY(86,86)
# XY(86,43)
# XY(27,43)

#// 5. Uzdevums

def lidz10():
    x = 1
    while x <= 10:
        print(x)
        if x == 10:
            break
        elif x < 10:
            x += 1

# lidz10()

#// 6. Uzdevums

def produktuNosaukumi():
    produkti = ["Piens","Maize","Olas"]

    for i in produkti:
        print(i)

# produktuNosaukumi()

#// 7. Uzdevums

def tests(teksts):
    if len(teksts) % 2 == 0:
        print(teksts.upper())
    elif len(teksts) % 1 == 0:
        print(teksts.lower())

# tests("Ola")
# tests("Suns")

