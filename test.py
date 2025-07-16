import txt_database
from txt_database import printd
import json
data = txt_database.txt_database()
data.read('base.txt')

with open('inventory.txt', 'r') as txt:
        for i in txt:
            inventory_mass = i.split()

dic = {'username':data.username,
       'gold':data.gold,
       'damage':data.damage,
       'lvl':data.lvl,
       'health':data.health,
       'inventory':inventory_mass
       }


users = {"1":dic,
            "2": {"username": "PLAYER", "gold": 1000, "damage": 10, "lvl": 1, "health": 100, "inventory": []},
            "3": {"username": "ERROR", "gold": 0, "damage": 0, "lvl": 0, "health": 0, "inventory": []},
            
         }

with open('base.json', 'w') as f:
      json.dump(users, f)


with open('base.json', 'r') as f:
    data = json.load(f)

for i in data:
    printd(f"ID: {i}, Username: {data[i]['username']}, Gold: {data[i]['gold']}, Damage: {data[i]['damage']}, Level: {data[i]['lvl']}, Health: {data[i]['health']}, Inventory: {data[i]['inventory']}")

player = input('ID:')
