from txt_database import JsonDatabase, printd
import random
import json

def load_game_items(filename='game_items.json'):
    with open(filename, 'r') as f:
        return json.load(f)

game_items = load_game_items()
SHOP = game_items['SHOP']
HEALTH_ITEMS = game_items['HEALTH_ITEMS']
DAMAGE_ITEMS = game_items['DAMAGE_ITEMS']
TREASURES = game_items['TREASURES']
MONSTERS = game_items.get('MONSTERS', {})  # Загружаем монстров

db = JsonDatabase()
db.load()

print("Список игроков:")
for pid, username in db.list_players().items():
    print(f"ID: {pid}, Username: {username}")

player_id = input("Введите ID игрока или 'new' для создания: ")
if player_id == 'new':
    username = input("Имя нового игрока: ")
    new_id = str(len(db.data) + 1)
    db.create_player(new_id, {
        'username': username,
        'gold': 10,
        'damage': 10,
        'lvl': 1,
        'health': 100,
        'inventory': []
    })
    db.set_current_player(new_id)
else:
    db.set_current_player(player_id)

player = db.get_current_player()
if not player:
    print("Игрок не найден!")
    exit()

def save_player(db, player):
    db.update_current_player(player)
    printd(f'[Данные игрока сохранены: {player["username"]}]')

def shop(db, player):
    print('В магазине есть:')
    for item, price in SHOP.items():
        print(f'{item} - {price} золота')
    while True:
        print(f'У тебя {player["gold"]} золота.')
        buy = input('Что купить? (или "выйти"): ').title()
        if buy == 'Выйти' or buy == '':
            break
        elif buy in SHOP:
            if player["gold"] >= SHOP[buy]:
                player["gold"] -= SHOP[buy]
                print(f'Ты купил {buy}! Осталось {player["gold"]} золота.')
                if buy in HEALTH_ITEMS:
                    player["health"] += HEALTH_ITEMS[buy]
                    print(f'Здоровье +{HEALTH_ITEMS[buy]} → {player["health"]}')
                elif buy in DAMAGE_ITEMS:
                    player["damage"] += DAMAGE_ITEMS[buy]
                    print(f'Урон +{DAMAGE_ITEMS[buy]} → {player["damage"]}')
                else:
                    player["inventory"].append(buy)
                save_player(db, player)
            else:
                print('Недостаточно золота!')
        else:
            print('Нет такого товара!')
    return player

def show_character(player):
    print('\n↓↓↓↓↓↓↓')
    print(player["username"])
    print(f'ЗДОРОВЬЕ: {player["health"]}')
    print(f'УРОВЕНЬ: {player["lvl"]}')
    print(f'ЗОЛОТО: {player["gold"]}')
    print(f'УРОН: {player["damage"]}')
    print('↑↑↑↑↑↑↑')

def show_inventory(db, player):
    print('Инвентарь:')
    for item in player["inventory"]:
        print(item)
    while True:
        do = input("Что использовать? (или 'выйти'): ").title()
        if do == 'Выйти' or do == '':
            break
        elif do in player["inventory"]:
            if do in HEALTH_ITEMS:
                print(f'Использовано {do}, здоровье +{HEALTH_ITEMS[do]}')
                player["health"] += HEALTH_ITEMS[do]
                player["inventory"].remove(do)
                save_player(db, player)
            elif do in DAMAGE_ITEMS:
                print(f'Использовано {do}, урон +{DAMAGE_ITEMS[do]}')
                player["damage"] += DAMAGE_ITEMS[do]
                player["inventory"].remove(do)
                save_player(db, player)
            elif do == 'Кейс':
                case_open(db, player)
            else:
                print(f'Ты держишь {do}, но ничего не происходит.')
        else:
            print('Нет такого предмета!')

def case_open(db, player):
    if 'Кейс' in player["inventory"]:
        print('\nТы открываешь кейс...')
        case_items = list(TREASURES.keys()) + list(HEALTH_ITEMS.keys()) + list(DAMAGE_ITEMS.keys()) + ['Кейс'] + ["Мусор"]*7
        item = random.choice(case_items)
        print(f'Выпало: {item}!')
        player["inventory"].remove('Кейс')
        if item != "Мусор":
            player["inventory"].append(item)
        save_player(db, player)
    else:
        print('Нет кейса!')

def battle(db, player):
    LVL = player["lvl"]
    GOLD = player["gold"]
    DAMAGE = player["damage"]
    HEALTH = player["health"]
    max_health = HEALTH

    # Выбираем случайного монстра
    if not MONSTERS:
        print("Монстры не найдены в game_items.json!")
        return player
    monster_name = random.choice(list(MONSTERS.keys()))
    monster = MONSTERS[monster_name]
    
    # Масштабируем характеристики монстра на основе уровня игрока
    monster_health = monster["base_health"] + (LVL * 10)  # Увеличиваем здоровье на 10 за уровень
    monster_damage = monster["base_damage"] + (LVL * 2)   # Увеличиваем урон на 2 за уровень
    max_monster_health = monster_health
    
    print(f'\n{monster["description"]}')
    print(f'Твоё здоровье: {HEALTH} Твой урон: {DAMAGE}')
    print(f'Здоровье {monster_name}: {monster_health} Урон: {monster_damage}')
    
    while True:
        monster_health -= DAMAGE
        if monster_health <= 0 or HEALTH <= 0:
            if monster_health <= 0:
                print(f'\nТы победил {monster_name}!')
                if HEALTH <= 0:
                    HEALTH = 0
                HEALTH += monster_damage + 2
                LVL += (max_monster_health - monster_damage) // 10
                GOLD += monster["gold_reward"]
                
                # Выпадение предметов
                drop = random.choices(
                    [d["item"] for d in monster["item_drops"]],
                    weights=[d["chance"] for d in monster["item_drops"]],
                    k=1
                )[0]
                if drop != "Мусор":
                    player["inventory"].append(drop)
                    print(f'Ты получил: {drop}!')
                print(f'Получено {monster["gold_reward"]} золота.')
                break
            elif HEALTH <= 0:
                print(f'\n{monster_name} победил тебя!')
                input('Ты пытаешься сбежать...')
                if random.randint(1, 100) <= 50:
                    print('Сбежал!')
                    HEALTH = random.randint(1, max_health)
                    GOLD += random.randint(1, 7)
                else:
                    HEALTH = 0
                    print('Не удалось сбежать.')
                break
        input(f'Ты бьёшь {monster_name}, у него осталось {monster_health} здоровья.')
        HEALTH -= monster_damage
    
    player["lvl"] = LVL
    player["gold"] = GOLD
    player["damage"] = DAMAGE
    player["health"] = HEALTH
    save_player(db, player)
    return player

def get_next_marketplace_id(db):
    marketplace = db.get_marketplace()
    if not marketplace:
        return 1
    return max(slot["slot_id"] for slot in marketplace) + 1

def show_marketplace(db):
    marketplace = db.get_marketplace()
    if not marketplace:
        print("Маркетплейс пуст.")
        return
    print("Слоты маркетплейса:")
    for slot in marketplace:
        buyer = slot.get("buyer_id")
        seller_username = db.data.get(slot["seller_id"], {}).get("username", "Неизвестный")
        status = "Продано" if buyer else "В продаже"
        print(f"ID: {slot['slot_id']} | {slot['item']} | Цена: {slot['price']} | Продавец: {seller_username}, ID: {slot['seller_id']} | Статус: {status}")

def add_item_to_marketplace(db, player, item, price):
    if item not in player["inventory"]:
        print("У тебя нет такого предмета!")
        return
    slot_id = get_next_marketplace_id(db)
    slot = {
        "slot_id": slot_id,
        "item": item,
        "seller_id": db.current_id,
        "price": price,
        "buyer_id": None
    }
    db.add_marketplace_slot(slot)
    player["inventory"].remove(item)
    save_player(db, player)
    print(f"Предмет {item} выставлен на продажу за {price} золота (ID слота: {slot_id})")

def buy_item_from_marketplace(db, player, slot_id):
    marketplace = db.get_marketplace()
    slot = next((s for s in marketplace if s["slot_id"] == slot_id and s["buyer_id"] is None), None)
    if not slot:
        print("Нет такого слота или предмет уже куплен!")
        return
    if player["gold"] < slot["price"]:
        print("Недостаточно золота!")
        return
    player["gold"] -= slot["price"]
    player["inventory"].append(slot["item"])
    slot["buyer_id"] = db.current_id
    db.update_marketplace([s if s["slot_id"] != slot_id else slot for s in marketplace])
    save_player(db, player)
    print(f"Ты купил {slot['item']} за {slot['price']} золота!")

def remove_my_marketplace_slot(db, player, slot_id):
    marketplace = db.get_marketplace()
    slot = next((s for s in marketplace if s["slot_id"] == slot_id and s["seller_id"] == db.current_id and s["buyer_id"] is None), None)
    if not slot:
        print("Нет такого слота или предмет уже куплен!")
        return
    player["inventory"].append(slot["item"])
    db.remove_marketplace_slot(slot_id)
    save_player(db, player)
    print(f"Ты снял с продажи предмет {slot['item']} (ID слота: {slot_id})")

def marketplace_menu(db, player):
    while True:
        print("\n--- Маркетплейс ---")
        print("1. Посмотреть слоты")
        print("2. Выставить предмет")
        print("3. Купить предмет")
        print("4. Снять свой предмет с продажи")
        print("0. Назад")
        choice = input("Выбор: ")
        if choice == "1":
            show_marketplace(db)
        elif choice == "2":
            print("Ваш инвентарь:", player["inventory"])
            item = input("Что выставить? ").title()
            if item not in player["inventory"]:
                print("Нет такого предмета!")
                continue
            price = input("Цена: ")
            try:
                price = int(price)
            except ValueError:
                print("Некорректная цена!")
                continue
            add_item_to_marketplace(db, player, item, price)
        elif choice == "3":
            slot_id = input("ID слота для покупки: ")
            try:
                slot_id = int(slot_id)
            except ValueError:
                print("Некорректный ID!")
                continue
            buy_item_from_marketplace(db, player, slot_id)
        elif choice == "4":
            slot_id = input("ID слота для снятия: ")
            try:
                slot_id = int(slot_id)
            except ValueError:
                print("Некорректный ID!")
                continue
            remove_my_marketplace_slot(db, player, slot_id)
        elif choice == "0":
            break
        else:
            print("Нет такого варианта!")

while True:
    print("\nЧто ты хочешь? 1.В бой! 2.Магазин 3.Персонаж 4.Инвентарь. 5. Торговая площадка 0.Выход")
    smth = input("Выбор: ")
    if smth == '1':
        player = battle(db, player)
    elif smth == '2':
        player = shop(db, player)
    elif smth == '3':
        show_character(player)
    elif smth == '4':
        show_inventory(db, player)
    elif smth == '5':
        marketplace_menu(db, player)
    elif smth == '0':
        print("Выход из игры.")
        break
    else:
        print('Нет такого варианта!')
    if player["health"] <= 0:
        print('\nТы умер! Начинаешь сначала.')
        player["lvl"] = 1
        player["gold"] = 10
        player["damage"] = 10
        player["health"] = 100
        player["inventory"] = []
        save_player(db, player)