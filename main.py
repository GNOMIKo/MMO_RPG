import txt_database
import random
from txt_database import printd
data = txt_database.txt_database()
###########
health_price = 10
damage_price = 30
EFFECT = 0
INVENTORY_MASS = []
TREASURES = {
    'Сокровище_1':200,
    'Сокровище_2':150,
    'Сокровище_3':100,
    'Сокровище_4':50,
}
SHOP = {
    'Лекарство': 20,
    'Бинт': 10,
    'Чистка_Оружия': 10,
    'Автомат_Ак-47': 50,
    'Кейс': 100
}
HEALTH_ITEMS = {
    'Лекарство': 10,
    'Бинт': 5,
}
DAMAGE_ITEMS = {
    'Чистка_Оружия': 3,
    'Автомат_Ак-47': 15
}
ITEMS = {
    'Лекарство': HEALTH_ITEMS,
    'Чистка_Оружия': DAMAGE_ITEMS,
    'Автомат_Ак-47': DAMAGE_ITEMS,
    'Бинт': HEALTH_ITEMS,
}
TRANSLATE_ITEMS = {
    'Лекарство':'small_heal',
    'Чистка_Оружия':'weapon_cleaning'
}
#############
# Functions #
#############
def battle(LVL, GOLD, DAMAGE, HEALTH):
    max_health = HEALTH
    monster_health = random.randint(DAMAGE * 5, DAMAGE * 10)
    monster_damage = random.randint(HEALTH // 20, HEALTH // 8)
    max_monster_health = monster_health
    if monster_damage <= 0:
        monster_damage = HEALTH
    print(f'\nТвоё здоровье:{HEALTH} Твой урон: {DAMAGE}')
    print(f'Здоровье монстра:{monster_health} Урон монстра: {monster_damage}')
    while True:
        monster_health -= DAMAGE

        if monster_health <= 0 or HEALTH <= 0:
            if monster_health <= 0:
                print('\nТы победил!')
                if HEALTH <= 0:
                    HEALTH = 0
                HEALTH += monster_damage + 2
                print(f'Твой уровень: {LVL}')
                LVL += (max_monster_health - monster_damage) // 10
                print(f'Твой НОВЫЙ уровень: {LVL}')
                print(f'У монстра было {monster_damage} золота.')
                GOLD += monster_damage + 10
                break
            elif HEALTH <= 0:
                print('\nКажется ты проигрываешь монстру!')
                input('Ты пытаешься сбежать и...')
                if random.randint(1, 100) <= 50:
                    print('У тебя получается')
                    HEALTH = random.randint(1, max_health)
                    GOLD += random.randint(1, 7)
                    print(f'Но у тебя остаётся лишь:{HEALTH} здоровья. Зато ты украл у монстра немного золота)')
                else:
                    HEALTH = 0
                    print(f'У тебя не получается(')
                break
        input(f'Ты бьёшь монстра и у него остаётся {monster_health} здоровья.')
        HEALTH -= monster_damage
        if monster_health <= 0 or HEALTH <= 0:
            if monster_health <= 0:
                print('\nТы победил!')
                if HEALTH <= 0:
                    HEALTH = 0
                HEALTH += monster_damage + 2
                print(f'Твой уровень: {LVL}')
                LVL += (max_monster_health - monster_damage) // 10
                print(f'Твой НОВЫЙ уровень: {LVL}')
                print(f'У монстра было {monster_damage} золота.')
                GOLD += monster_damage + 10
                break
            elif HEALTH <= 0:
                print('\nКажется ты проигрываешь монстру!')
                input('Ты пытаешься сбежать и...')
                if random.randint(1, 100) <= 50:
                    print('У тебя получается')
                    HEALTH = random.randint(1, max_health)
                    GOLD += random.randint(1, 7)
                    print(f'Но у тебя остаётся лишь:{HEALTH} здоровья. Зато ты украл у монстра неного золота)')
                else:
                    HEALTH = 0
                    print(f'У тебя не получается(')
                break
        input(f'Монстр бьёт тебя и у тебя остаётся {HEALTH} здоровья.')
    return LVL, GOLD, DAMAGE, HEALTH

def save_inventory(inventory, filename='inventory.txt'):
    """Сохраняет инвентарь в файл и выводит сообщение об успешном сохранении."""
    try:
        with open(filename, 'w') as txt:
            txt.write(' '.join(inventory))
        printd(f'[Инвентарь сохранён: {len(inventory)} предмет(ов)]')
    except Exception as e:
        printd(f'Ошибка при сохранении инвентаря: {e}')

def shop(GOLD, HEALTH, DAMAGE, INVENTORY_MASS):
    input('В магазине есть разные товраы...')
    print("#" * 20)
    for i in SHOP:
        print(i, '-', SHOP[i], 'золота')
    print("#" * 20)
    while True:
        print(f'У тебя {GOLD} золота.')
        buy = input('Что ты хочешь купить? (или "выйти" для выхода из магазина): ').title()
        printd(buy)
        if buy == 'Выйти' or buy == '':
            break
        elif buy == 'Список':
            print('Список товаров:')
            print("#" * 20)
            for item in SHOP:
                print(f'{item} - {SHOP[item]} золота')
            print("#" * 20)
        elif buy in SHOP:
            if GOLD >= SHOP[buy]:
                GOLD -= SHOP[buy]
                print(f'Ты купил {buy}! \nУ тебя осталось {GOLD} золота.')
                if buy in HEALTH_ITEMS:
                    HEALTH += HEALTH_ITEMS[buy]
                    print(f'Твое здоровье увеличилось на {HEALTH_ITEMS[buy]} едениц. \nУ тебя теперь {HEALTH} здоровья.')
                elif buy in DAMAGE_ITEMS:
                    DAMAGE += DAMAGE_ITEMS[buy]
                    print(f'Твой урон увеличился на {DAMAGE_ITEMS[buy]} едениц. \nУ тебя теперь {DAMAGE} урона.')
                else:
                    INVENTORY_MASS.append(buy)
                printd(INVENTORY_MASS)
                save_inventory(INVENTORY_MASS)
            else:
                print('У тебя недостаточно золота!')
        else:
            print('Такого товара нет в магазине!')
    return GOLD, HEALTH, DAMAGE, INVENTORY_MASS

def show_character(USERNAME, HEALTH, LVL, GOLD, DAMAGE):
    print('\n↓↓↓↓↓↓↓')
    print(USERNAME)
    print(f'ЗДОРОВЬЕ: {HEALTH}')
    print(f'УРОВЕНЬ: {LVL}')
    print(f'ЗОЛОТО: {GOLD}')
    print(f'УРОН: {DAMAGE}')
    print('↑↑↑↑↑↑↑')

def show_inventory(INVENTORY_MASS):
    input('Ты открываешь рюкзак и...')
    for item in INVENTORY_MASS: print(item)
    while True:
        do = input("Что ты хочешь использовать? (или 'выйти' для выхода из инвентаря): ").title()
        if do == 'Выйти' or do == '':
            break
        elif do == 'Список':
            print('Список предметов в инвентаре:')
            for item in INVENTORY_MASS: print(item)
        elif do in INVENTORY_MASS:
            if do in HEALTH_ITEMS:
                print(f'Ты используешь {do} и восстанавливаешь {HEALTH_ITEMS[do]} здоровья!')
                INVENTORY_MASS.remove(do)
                save_inventory(INVENTORY_MASS)
            elif do in DAMAGE_ITEMS:
                print(f'Ты используешь {do} и увеличиваешь урон на {DAMAGE_ITEMS[do]} едениц!')
                INVENTORY_MASS.remove(do)
                save_inventory(INVENTORY_MASS)
            elif do == 'Кейс':
                case_open(INVENTORY_MASS)
                save_inventory(INVENTORY_MASS)
            else:
                print(f'Ты держишь в руках {do}! Какой-то бесполезный предмет...')

def case_open(INVENTORY_MASS):
    if 'Кейс' in INVENTORY_MASS:
        print('\nТы открываешь кейс и...')
        case_items = [
            'Сокровище_1', 'Сокровище_2', 'Сокровище_3', 'Сокровище_4',
            'Бинт', 'Лекарство', 'Чистка_Оружия', 'Автомат_Ак-47', 'Кейс',
            "Мусор", "Мусор", "Мусор", "Мусор", "Мусор", "Мусор", "Мусор"
        ]
        item = random.choice(case_items)
        print(f'Тебе выпало: {item}!')
        INVENTORY_MASS.remove('Кейс')
        if item != "Мусор":
            INVENTORY_MASS.append(item)
        save_inventory(INVENTORY_MASS)
        return item
    else:
        print('У тебя нет кейса!')
        return None

#################
# END FUNCTIONS #
#################


###########################
# Начальная инициализация #
###########################
while True:
    with open('inventory.txt', 'r') as txt:
        for i in txt:
            INVENTORY_MASS = i.split()
    EFFECT = 0
    data.read()
    ############
    USERNAME = data.username
    LVL = data.lvl
    GOLD = data.gold
    DAMAGE = data.damage
    HEALTH = data.health
    ###########
    smth = input('\nЧто ты хoчешь? 1.В бой! 2.Магазин 3.Персонаж 4.Инвентарь. :')
    if smth == '1':
        LVL, GOLD, DAMAGE, HEALTH = battle(LVL, GOLD, DAMAGE, HEALTH)
    elif smth == '2':
        GOLD, HEALTH, DAMAGE, INVENTORY_MASS = shop(GOLD, HEALTH, DAMAGE, INVENTORY_MASS)
    elif smth == '3':
        show_character(USERNAME, HEALTH, LVL, GOLD, DAMAGE)
    elif smth == '4':
        show_inventory(INVENTORY_MASS)
    else:
        print('\nТакого в свписке нету(')
        pass
    if HEALTH <= 0:
        print('\nВот твой путь и закончился... Но ведь можно начать сначала!')
        LVL = 1
        GOLD = 10
        DAMAGE = 10
        HEALTH = 100
    ###########
    data.username = USERNAME
    data.lvl = LVL
    data.gold = GOLD
    data.damage = DAMAGE
    data.health = HEALTH
    ###########
    data.write()
    # Сохраняем инвентарь в файл
    save_inventory(INVENTORY_MASS) 