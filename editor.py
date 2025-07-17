import json

def load_game_items(filename='game_items.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "SHOP": {},
            "HEALTH_ITEMS": {},
            "DAMAGE_ITEMS": {},
            "TREASURES": {},
            "MONSTERS": {},
            "QUESTS": {}
        }

def save_game_items(data, filename='game_items.json'):
    confirm = input("Сохранить изменения в game_items.json? (да/нет): ").lower()
    if confirm == 'да':
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Данные сохранены в {filename}")
    else:
        print("Сохранение отменено.")

def show_items(data, category):
    if not data.get(category, {}):
        print(f"Категория {category} пуста.")
        return
    print(f"\nТекущие элементы в {category}:")
    for item, value in data[category].items():
        print(f"- {item}: {value}")

def add_item(data, category):
    show_items(data, category)
    item_name = input(f"\nВведите название предмета: ").title()
    if not item_name:
        print("Ошибка: название не может быть пустым!")
        return
    if item_name in data[category]:
        print(f"Ошибка: предмет {item_name} уже существует в {category}!")
        return
    try:
        if category == "SHOP":
            price = input("Введите цену (положительное целое число): ")
            price = int(price)
            if price <= 0:
                raise ValueError("Цена должна быть больше 0!")
            data[category][item_name] = price
        elif category in ["HEALTH_ITEMS", "DAMAGE_ITEMS"]:
            effect = input("Введите эффект (положительное целое число): ")
            effect = int(effect)
            if effect <= 0:
                raise ValueError("Эффект должен быть больше 0!")
            data[category][item_name] = effect
        elif category == "TREASURES":
            value = input("Введите ценность (положительное целое число): ")
            value = int(value)
            if value <= 0:
                raise ValueError("Ценность должна быть больше 0!")
            data[category][item_name] = value
        print(f"Предмет {item_name} добавлен в {category}")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")

def edit_item(data, category):
    show_items(data, category)
    item_name = input(f"\nВведите название предмета для редактирования: ").title()
    if item_name not in data.get(category, {}):
        print(f"Ошибка: предмет {item_name} не найден в {category}!")
        return
    try:
        if category == "SHOP":
            price = input("Введите новую цену (положительное целое число): ")
            price = int(price)
            if price <= 0:
                raise ValueError("Цена должна быть больше 0!")
            data[category][item_name] = price
        elif category in ["HEALTH_ITEMS", "DAMAGE_ITEMS"]:
            effect = input("Введите новый эффект (положительное целое число): ")
            effect = int(effect)
            if effect <= 0:
                raise ValueError("Эффект должен быть больше 0!")
            data[category][item_name] = effect
        elif category == "TREASURES":
            value = input("Введите новую ценность (положительное целое число): ")
            value = int(value)
            if value <= 0:
                raise ValueError("Ценность должна быть больше 0!")
            data[category][item_name] = value
        print(f"Предмет {item_name} в {category} обновлён")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")

def add_monster(data):
    print("\nТекущие монстры:")
    show_items(data, "MONSTERS")
    monster_name = input("\nВведите название монстра: ").title()
    if not monster_name:
        print("Ошибка: название не может быть пустым!")
        return
    if monster_name in data["MONSTERS"]:
        print(f"Ошибка: монстр {monster_name} уже существует!")
        return
    try:
        base_health = input("Введите базовое здоровье (положительное целое число): ")
        base_health = int(base_health)
        if base_health <= 0:
            raise ValueError("Здоровье должно быть больше 0!")
        base_damage = input("Введите базовый урон (положительное целое число): ")
        base_damage = int(base_damage)
        if base_damage <= 0:
            raise ValueError("Урон должен быть больше 0!")
        gold_reward = input("Введите награду в золоте (положительное целое число): ")
        gold_reward = int(gold_reward)
        if gold_reward <= 0:
            raise ValueError("Награда должна быть больше 0!")
        description = input("Введите описание монстра: ")
        if not description:
            print("Ошибка: описание не может быть пустым!")
            return
        item_drops = []
        total_chance = 0
        while True:
            add_drop = input("Добавить предмет в дроп? (да/нет): ").lower()
            if add_drop != 'да':
                break
            item = input("Название предмета: ").title()
            if not item:
                print("Ошибка: название предмета не может быть пустым!")
                continue
            chance = input("Вероятность выпадения (0.0-1.0): ")
            chance = float(chance)
            if not (0 <= chance <= 1):
                print("Ошибка: вероятность должна быть от 0 до 1!")
                continue
            item_drops.append({"item": item, "chance": chance})
            total_chance += chance
        if item_drops and abs(total_chance - 1.0) > 0.01:
            print("Ошибка: сумма вероятностей дропа должна быть равна 1!")
            return
        data["MONSTERS"][monster_name] = {
            "base_health": base_health,
            "base_damage": base_damage,
            "gold_reward": gold_reward,
            "item_drops": item_drops,
            "description": description
        }
        print(f"Монстр {monster_name} добавлен")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")

def edit_monster(data):
    print("\nТекущие монстры:")
    show_items(data, "MONSTERS")
    monster_name = input("\nВведите название монстра для редактирования: ").title()
    if monster_name not in data["MONSTERS"]:
        print(f"Ошибка: монстр {monster_name} не найден!")
        return
    try:
        base_health = input("Введите новое базовое здоровье (положительное целое число): ")
        base_health = int(base_health)
        if base_health <= 0:
            raise ValueError("Здоровье должно быть больше 0!")
        base_damage = input("Введите новый базовый урон (положительное целое число): ")
        base_damage = int(base_damage)
        if base_damage <= 0:
            raise ValueError("Урон должен быть больше 0!")
        gold_reward = input("Введите новую награду в золоте (положительное целое число): ")
        gold_reward = int(gold_reward)
        if gold_reward <= 0:
            raise ValueError("Награда должна быть больше 0!")
        description = input("Введите новое описание монстра: ")
        if not description:
            print("Ошибка: описание не может быть пустым!")
            return
        item_drops = []
        total_chance = 0
        while True:
            add_drop = input("Добавить предмет в дроп? (да/нет): ").lower()
            if add_drop != 'да':
                break
            item = input("Название предмета: ").title()
            if not item:
                print("Ошибка: название предмета не может быть пустым!")
                continue
            chance = input("Вероятность выпадения (0.0-1.0): ")
            chance = float(chance)
            if not (0 <= chance <= 1):
                print("Ошибка: вероятность должна быть от 0 до 1!")
                continue
            item_drops.append({"item": item, "chance": chance})
            total_chance += chance
        if item_drops and abs(total_chance - 1.0) > 0.01:
            print("Ошибка: сумма вероятностей дропа должна быть равна 1!")
            return
        data["MONSTERS"][monster_name] = {
            "base_health": base_health,
            "base_damage": base_damage,
            "gold_reward": gold_reward,
            "item_drops": item_drops,
            "description": description
        }
        print(f"Монстр {monster_name} обновлён")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")

def add_quest(data):
    print("\nТекущие квесты:")
    show_items(data, "QUESTS")
    quest_id = input("\nВведите ID квеста (например, quest4): ")
    if not quest_id:
        print("Ошибка: ID квеста не может быть пустым!")
        return
    if quest_id in data["QUESTS"]:
        print(f"Ошибка: квест с ID {quest_id} уже существует!")
        return
    description = input("Введите описание квеста: ")
    if not description:
        print("Ошибка: описание не может быть пустым!")
        return
    quest_type = input("Введите тип квеста (kill_monster/collect_item): ")
    if quest_type not in ["kill_monster", "collect_item"]:
        print("Ошибка: неподдерживаемый тип квеста!")
        return
    target = input("Введите цель (например, Гоблин или Лекарство): ").title()
    if not target:
        print("Ошибка: цель не может быть пустой!")
        return
    try:
        amount = input("Введите количество (положительное целое число): ")
        amount = int(amount)
        if amount <= 0:
            raise ValueError("Количество должно быть больше 0!")
        gold_reward = input("Введите награду в золоте (положительное целое число, 0 если нет): ")
        gold_reward = int(gold_reward)
        if gold_reward < 0:
            raise ValueError("Награда не может быть отрицательной!")
        items_reward = []
        while True:
            add_item = input("Добавить предмет в награду? (да/нет): ").lower()
            if add_item != 'да':
                break
            item = input("Название предмета: ").title()
            if not item:
                print("Ошибка: название предмета не может быть пустым!")
                continue
            items_reward.append(item)
        data["QUESTS"][quest_id] = {
            "description": description,
            "type": quest_type,
            "target": target,
            "amount": amount,
            "rewards": {
                "gold": gold_reward,
                "items": items_reward
            }
        }
        print(f"Квест {quest_id} добавлен")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")

def edit_quest(data):
    print("\nТекущие квесты:")
    show_items(data, "QUESTS")
    quest_id = input("\nВведите ID квеста для редактирования: ")
    if quest_id not in data["QUESTS"]:
        print(f"Ошибка: квест с ID {quest_id} не найден!")
        return
    description = input("Введите новое описание квеста: ")
    if not description:
        print("Ошибка: описание не может быть пустым!")
        return
    quest_type = input("Введите новый тип квеста (kill_monster/collect_item): ")
    if quest_type not in ["kill_monster", "collect_item"]:
        print("Ошибка: неподдерживаемый тип квеста!")
        return
    target = input("Введите новую цель (например, Гоблин или Лекарство): ").title()
    if not target:
        print("Ошибка: цель не может быть пустой!")
        return
    try:
        amount = input("Введите новое количество (положительное целое число): ")
        amount = int(amount)
        if amount <= 0:
            raise ValueError("Количество должно быть больше 0!")
        gold_reward = input("Введите новую награду в золоте (положительное целое число, 0 если нет): ")
        gold_reward = int(gold_reward)
        if gold_reward < 0:
            raise ValueError("Награда не может быть отрицательной!")
        items_reward = []
        while True:
            add_item = input("Добавить предмет в награду? (да/нет): ").lower()
            if add_item != 'да':
                break
            item = input("Название предмета: ").title()
            if not item:
                print("Ошибка: название предмета не может быть пустым!")
                continue
            items_reward.append(item)
        data["QUESTS"][quest_id] = {
            "description": description,
            "type": quest_type,
            "target": target,
            "amount": amount,
            "rewards": {
                "gold": gold_reward,
                "items": items_reward
            }
        }
        print(f"Квест {quest_id} обновлён")
    except ValueError as e:
        print(f"Ошибка: {str(e)}")

def add_category(data):
    category = input("Введите название новой категории (например, LOCATIONS): ").upper()
    if not category:
        print("Ошибка: название категории не может быть пустым!")
        return
    if category in data:
        print(f"Ошибка: категория {category} уже существует!")
        return
    data[category] = {}
    print(f"Категория {category} создана")

def add_to_category(data, category):
    if category not in data:
        print(f"Ошибка: категория {category} не существует!")
        return
    print(f"\nТекущие элементы в {category}:")
    show_items(data, category)
    key = input("\nВведите ключ (например, название локации): ").title()
    if not key:
        print("Ошибка: ключ не может быть пустым!")
        return
    if key in data[category]:
        print(f"Ошибка: ключ {key} уже существует в {category}!")
        return
    value = input("Введите данные в формате JSON (например, {\"description\": \"Темный лес\"}): ")
    try:
        value = json.loads(value)
        data[category][key] = value
        print(f"Данные для {key} добавлены в {category}")
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON-формат!")

def edit_category_item(data, category):
    if category not in data:
        print(f"Ошибка: категория {category} не существует!")
        return
    print(f"\nТекущие элементы в {category}:")
    show_items(data, category)
    key = input("\nВведите ключ для редактирования: ").title()
    if key not in data[category]:
        print(f"Ошибка: ключ {key} не найден в {category}!")
        return
    value = input("Введите новые данные в формате JSON: ")
    try:
        value = json.loads(value)
        data[category][key] = value
        print(f"Данные для {key} в {category} обновлены")
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON-формат!")

def show_all_data(data):
    print("\nВсе данные в game_items.json:")
    for category, items in data.items():
        print(f"\n{category}:")
        if not items:
            print("  Пусто")
        else:
            for key, value in items.items():
                print(f"  - {key}: {value}")

def main():
    data = load_game_items()
    print("\nТекущие категории в game_items.json:", ", ".join(data.keys()))
    while True:
        print("\n--- Редактор данных MMO_RPG ---")
        print("1. Добавить предмет (SHOP, HEALTH_ITEMS, DAMAGE_ITEMS, TREASURES)")
        print("2. Редактировать предмет")
        print("3. Добавить монстра")
        print("4. Редактировать монстра")
        print("5. Добавить квест")
        print("6. Редактировать квест")
        print("7. Создать новую категорию")
        print("8. Добавить данные в существующую категорию")
        print("9. Редактировать данные в категории")
        print("10. Показать все данные")
        print("0. Сохранить и выйти")
        choice = input("Выбор: ")
        if choice == "1":
            category = input("Выберите категорию (SHOP/HEALTH_ITEMS/DAMAGE_ITEMS/TREASURES): ").upper()
            if category in ["SHOP", "HEALTH_ITEMS", "DAMAGE_ITEMS", "TREASURES"]:
                add_item(data, category)
            else:
                print("Ошибка: неподдерживаемая категория!")
        elif choice == "2":
            category = input("Выберите категорию (SHOP/HEALTH_ITEMS/DAMAGE_ITEMS/TREASURES): ").upper()
            if category in ["SHOP", "HEALTH_ITEMS", "DAMAGE_ITEMS", "TREASURES"]:
                edit_item(data, category)
            else:
                print("Ошибка: неподдерживаемая категория!")
        elif choice == "3":
            add_monster(data)
        elif choice == "4":
            edit_monster(data)
        elif choice == "5":
            add_quest(data)
        elif choice == "6":
            edit_quest(data)
        elif choice == "7":
            add_category(data)
        elif choice == "8":
            category = input("Введите категорию: ").upper()
            add_to_category(data, category)
        elif choice == "9":
            category = input("Введите категорию: ").upper()
            edit_category_item(data, category)
        elif choice == "10":
            show_all_data(data)
        elif choice == "0":
            save_game_items(data)
            break
        else:
            print("Ошибка: нет такого варианта!")

if __name__ == "__main__":
    main()