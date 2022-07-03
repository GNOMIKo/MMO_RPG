import txt_database
import random
data = txt_database.txt_database()
###########
health_price = 10
damage_price = 30
EFFECT = 0
INVENTORY_MASS = []
SHOP = {
    'Лекарство': health_price,
    'Читска_Оружия': damage_price,
    'Кейс': 100
}
HEALTH_ITEMS = {
    'Лекарство': 10,
    'Бинт': 5,
}
DAMAGE_ITEMS = {
    'Чистка_Оружия': 3,
    'Автомат_АК-47': 15
}
ITEMS = {
    'Лекарство': HEALTH_ITEMS,
    'Чистка_Оружия': DAMAGE_ITEMS,
    'Автомат_АК-47': DAMAGE_ITEMS,
    'Бинт': HEALTH_ITEMS,
}
TRANSLATE_ITEMS = {
    'Лекарство':'small_heal',
    'Чистка_Оружия':'weapon_cleaning'
}
###########
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
        max_health = HEALTH
        monster_health = random.randint(DAMAGE * 5, DAMAGE * 10)
        monster_damage = random.randint(HEALTH // 20, HEALTH // 8)
        max_monster_health = monster_health
        if monster_damage <= 0:monster_damage = HEALTH
        print(f'\nТвоё здоровье:{HEALTH} Твой урон: {DAMAGE}')
        print(f'Здоровье монстра:{monster_health} Урон монстра: {monster_damage}')
        while True:
            monster_health -= DAMAGE

            if monster_health <= 0 or HEALTH <= 0:
                if monster_health <= 0:
                    print('\nТы победил!')
                    if HEALTH <= 0:
                        HEALTH = 0
                    HEALTH += monster_damage+2
                    print(f'Твой уровень: {LVL}')
                    LVL += (max_monster_health-monster_damage)//10
                    print(f'Твой НОВЫЙ уровень: {LVL}')
                    print(f'У монстра было {monster_damage} золота.')
                    GOLD += monster_damage+10
                    break
                elif HEALTH <= 0:
                    print('\nКажется ты проигрываешь монстру!')
                    input('Ты пытаешься сбежать и...')
                    if random.randint(1,100) <= 50:
                        print('У тебя получается')
                        HEALTH = random.randint(1,max_health)
                        GOLD += random.randint(1,7)
                        print(f'Но у тебя остаётся лишь:{HEALTH} здоровья. Зато ты украл у монстра неного золота)')
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
                    HEALTH += monster_damage+2
                    print(f'Твой уровень: {LVL}')
                    LVL += (max_monster_health-monster_damage)//10
                    print(f'Твой НОВЫЙ уровень: {LVL}')
                    print(f'У монстра было {monster_damage} золота.')
                    GOLD += monster_damage+10
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
    elif smth == '2':
        input('В магазине есть разные товраы...')
        for i in SHOP:
            print(i,'-',SHOP[i],'золота')
        while True:
            break
    elif smth == '3':
        print('\n↓↓↓↓↓↓↓')
        print(USERNAME)
        print(f'ЗДОРОВЬЕ: {HEALTH}')
        print(f'УРОВЕНЬ: {LVL}')
        print(f'ЗОЛОТО: {GOLD}')
        print(f'УРОН: {DAMAGE}')
        print('↑↑↑↑↑↑↑')
    elif smth == '4':
        input('Ты открываешь рюкзак и...')
        print(*INVENTORY_MASS)
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