# init python:
#     from my_python_api.main import main as main_api
#
# # Вы можете расположить сценарий своей игры в этом файле.
#
# # Определение персонажей игры.
# define e = Character('Эйлин', color="#c8ffc8")
#
# # Вместо использования оператора image можете просто
# # складывать все ваши файлы изображений в папку images.
# # Например, сцену bg room можно вызвать файлом "bg room.png",
# # а eileen happy — "eileen happy.webp", и тогда они появятся в игре.
#
# # Игра начинается здесь:
# label start:
#     python:
#         random_int = main_api()
#
#     scene bg room
#
#     show eileen happy
#
#     e "Вы создали новую игру Ren'Py."
#
#     e "Результат работы функции main_api: [random_int]."  # Используем [random_int] для вставки значения
#
#     e "Добавьте сюжет, изображения и музыку и отправьте её в мир!"
#
#     return

image bg out1 = Transform("out.png", fit="contain")

init python:
    import os  # Модуль для взаимодействия с операционной системой, установка не требуется.

    from PIL import Image as PILImage  # Переименовываем PIL.Image
    from PIL import ImageDraw

    # Путь к файлу через config.basedir
    # По умолчанию путь идет в корень RenPy, а не проекта.
    game_path = os.path.join(config.basedir, "game")

    def create_custom_image():
        img = PILImage.new('RGBA', (800, 600), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 300, 300], fill="blue")
        img.save(f"{game_path}/new_images/custom_image.png")  # Сохраняем изображение в папку game

    # Инициализация переменных
    status_game = {
        "day": 1
    }

    resources = {
        "wood": 0,
        "stone": 0,
        "gold": 0,
        "food": 0
    }

    buildings = {
        "sawmill": 1,
        "quarry": 0,
        "farm": 0
    }

    # Функция для сбора ресурсов
    def gather_resources():
        resources["wood"] += buildings["sawmill"]
        resources["stone"] += buildings["quarry"]
        resources["food"] += buildings["farm"]

    # Функция для строительства зданий
    def build(building):
        if building == "sawmill" and resources["wood"] >= 10 and resources["stone"] >= 5:
            resources["wood"] -= 10
            resources["stone"] -= 5
            buildings["sawmill"] += 1
            return True
        elif building == "quarry" and resources["wood"] >= 15 and resources["stone"] >= 10:
            resources["wood"] -= 15
            resources["stone"] -= 10
            buildings["quarry"] += 1
            return True
        elif building == "farm" and resources["wood"] >= 20 and resources["stone"] >= 15:
            resources["wood"] -= 20
            resources["stone"] -= 15
            buildings["farm"] += 1
            return True
        else:
            return False

    def end_day():
        status_game['day'] += 1
        gather_resources()

    # Создаем изображение при запуске игры
    create_custom_image()

# Загружаем изображение в Ren'Py
image custom_bg = "new_images/custom_image.png"

# Начало игры
label start:
    scene bg out1
    show custom_bg  # Показываем изображение, созданное с помощью PIL
    show screen status_display
    show screen resource_display
    show screen buildings_display
    "Добро пожаловать в ваше поселение!"
    jump main_menu

label main_menu:
    show custom_bg  # Показываем изображение, созданное с помощью PIL
    scene bg out1
    show screen status_display
    show screen resource_display
    show screen buildings_display
    "Вы можете собирать ресурсы и строить здания."
    # Меню выбора действий
    menu:
        "Что вы хотите сделать?"
        "Собрать ресурсы":
            $ gather_resources()
            "Вы собрали немного ресурсов."
        "Построить здание":
            "Вы построили здание."
#             call screen build_menu
#             jump main_menu
        "Закончить день":
            "Вы решили закончить день."
            $ end_day()
            return


# label main_menu:
#     # Показываем экран с ресурсами
#     show screen resource_display
#
#     # Меню выбора действий
#     menu:
#         "Что вы хотите сделать?"
#         "Собрать ресурсы":
#             $ gather_resources()
#             "Вы собрали немного ресурсов."
#             jump main_menu
#         "Построить здание":
#             call screen build_menu
#             jump main_menu
#         "Закончить день":
#             "Вы решили закончить день."
#             return
#

# Экран для отображения статуса игры
screen status_display():
    frame:
        xalign 0.5
        yalign 0
        vbox:
            text "День: [status_game['day']]"

# Экран для отображения ресурсов
screen resource_display():
    frame:
        xalign 0
        yalign 0
        vbox:
            text "Дерево: [resources['wood']]"
            text "Камень: [resources['stone']]"
            text "Золото: [resources['gold']]"
            text "Еда: [resources['food']]"

# Экран для отображения построек
screen buildings_display():
    frame:
        xalign 1.0
        yalign 0
        vbox:
            text "Лесопилки: [buildings['sawmill']]"
            text "Каменоломни: [buildings['quarry']]"
            text "Фермы: [buildings['farm']]"


# # Экран для строительства зданий
# screen build_menu():
#     frame:
#         xalign 0.5
#         yalign 0.5
#         vbox:
#             text "Выберите здание для постройки:"
#             textbutton "Лесопилка (10 дерева, 5 камня)" action [Function(build, "sawmill"), Return()]
#             textbutton "Каменоломня (15 дерева, 10 камня)" action [Function(build, "quarry"), Return()]
#             textbutton "Ферма (20 дерева, 15 камня)" action [Function(build, "farm"), Return()]

