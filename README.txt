MMO_RPG Game — README
=====================

Описание
--------
Это консольная RPG-игра с системой сохранения прогресса и инвентаря для каждого игрока. Все игровые данные хранятся в формате JSON, что облегчает редактирование и расширение игры. Поддерживается несколько игроков, магазин, инвентарь, кейсы, предметы, сражения с монстрами.

Структура проекта
-----------------
- main.py — основной игровой цикл, логика игры, взаимодействие с игроком.
- txt_database.py — класс JsonDatabase для работы с файлом сохранения игроков (base.json).
- game_items.json — список игровых предметов, их цены и эффекты.
- base.json — база данных всех игроков и их прогресса.
- README.txt — этот файл.

Запуск игры
-----------
1. Убедитесь, что у вас установлен Python 3.
2. Проверьте наличие файлов base.json и game_items.json в папке с игрой.
3. Запустите main.py:
   ```
   python3 main.py
   ```
4. Следуйте инструкциям в консоли.

Формат хранения данных
----------------------
**base.json**  
Содержит словарь игроков. Каждый игрок — отдельный ключ (ID), значение — словарь с параметрами:
- username — имя игрока
- gold — количество золота
- damage — урон
- lvl — уровень
- health — здоровье
- inventory — список предметов

**game_items.json**  
Содержит словари с предметами:
- SHOP — предметы, доступные для покупки и их цены
- HEALTH_ITEMS — предметы, восстанавливающие здоровье
- DAMAGE_ITEMS — предметы, увеличивающие урон
- TREASURES — ценные предметы (например, из кейсов)

Основные возможности
--------------------
- Создание нового игрока или выбор существующего.
- Покупка предметов в магазине.
- Использование предметов из инвентаря.
- Открытие кейсов с случайными наградами.
- Сражения с монстрами.
- Автоматическое сохранение прогресса после каждого действия.

Редактирование предметов
------------------------
Для добавления/изменения предметов откройте файл game_items.json и отредактируйте нужные разделы.  
Например, чтобы добавить новый предмет в магазин:
```json
"SHOP": {
    "Лекарство": 20,
    "Бинт": 10,
    "Меч": 100
}
```
Чтобы добавить новый предмет, восстанавливающий здоровье:
```json
"HEALTH_ITEMS": {
    "Лекарство": 10,
    "Бинт": 5,
    "Зелье": 50
}
```

Советы
------
- Не редактируйте base.json вручную, если не уверены в формате.
- Для тестирования можно добавить новых игроков или предметы через соответствующие JSON-файлы.
- Если игра не запускается, проверьте, что все файлы существуют и корректны.

Контакты
--------
Разработчик: GNOMIK  
Для обратной связи используйте GitHub Issues или email.