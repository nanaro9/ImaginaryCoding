# Vardnica = Objekts klasei Dictionary
dict = {1:"viens",2:"divi"}

print(dict.keys())

# Saraksts - List
# Sakartotu, mainamu, dublejamu, indeksetu elementu kopa (masivam lidzigas strukturas)
list = [1,2,3,4,5]

print(list)

from collections import deque

queue = deque() # Divvirzienu rindas izveide

list = ["Kakis","Suns","Kamis"] # Saraksts

queue.append(list) # Pieliek sarakstu pie "deque"

print(queue)

queue.append("Zurka") # Pievieno elementu no labas puses
queue.appendleft("Pertikis") # Pievieno elementu no kreisas puses

print(queue)

queue.pop() # Nonem elementu no labas puses
queue.popleft() # Nonem elementu no kreisas puses

print(queue)

#tuple - kortežs
#Set - kopa

tuple = (1,2,3) # Nesakārtotu nemaināmu, dublējamu viena veida neindeksētu elementu kopa

set = {1,2,3} # Unikālu nesakārtotu elementu kolekcija

print(type(tuple),type(set))