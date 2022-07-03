import random
mass = []
with open('inventory.txt','r') as txt:
    for i in txt:
        mass = i.split()
print(mass)
mass.append('bandage')
try:
    mass.remove('vodka')
except:
    print('ERROR: This item is not in this list. Try to append it at first.')
with open('inventory.txt','w') as txt:
    for i in mass:
        txt.write(i+' ')
print(random.choice(mass))