"""
Конфигурационный модуль игры "Змейка".

Содержит все константы и настройки, используемые в игре:
- Размеры окна и игрового поля
- Цвета для различных элементов
- Направления движения змейки
- Начальные параметры игры

Constants:
    WIDTH (int): ширина игрового окна в пикселях
    HEIGHT (int): высота игрового окна в пикселях
    CELL_SIZE (int): размер одной клетки игровой сетки
    FIELD_OFFSET_Y (int): отступ сверху для игрового поля

    BLACK (tuple): цвет черный в формате RGB
    WHITE (tuple): цвет белый в формате RGB
    RED (tuple): цвет красный в формате RGB
    GREEN (tuple): цвет зеленый в формате RGB
    BLUE (tuple): цвет синий в формате RGB
    YELLOW (tuple): цвет желтый в формате RGB
    DARK_GREEN (tuple): цвет темно-зеленый в формате RGB
    GRAY (tuple): цвет серый в формате RGB

    UP (tuple): направление вверх (dx=0, dy=-1)
    DOWN (tuple): направление вниз (dx=0, dy=1)
    LEFT (tuple): направление влево (dx=-1, dy=0)
    RIGHT (tuple): направление вправо (dx=1, dy=0)

    INITIAL_SPEED (int): начальная скорость игры (кадров в секунду)
    INITIAL_LENGTH (int): начальная длина змейки
"""

WIDTH = 800
HEIGHT = 600

FIELD_OFFSET_Y = 60
CELL_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (50, 50, 50)

#направ
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#константа для игры добавление
INITIAL_SPEED = 10
INITIAL_LENGTH = 1