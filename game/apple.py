"""
класс яблока
представляющий съедобный объект в игре
Яблоко случайным образом появляется на игровом поле и увеличивает
длину змейки при поедании. Класс обеспечивает корректное размещение
яблока без пересечения с телом змейки.
"""

import pygame
import random
from .base import GameObject
from .config import *


class Apple(GameObject):
    """
    яблоко которое ест змейка
    появляется в свободных клетках
    """

    def __init__(self, size, width, height):
        """
        создает яблоко
        size - размер
        width height - размер поля
        появляется ниже панели (y от 40)
        Яблоко всегда размещается на координатах, кратных size
        """
        # яблоко ниже панели
        max_x = width - size
        max_y = height - size

        # x как обычно y от 40
        x = random.randrange(0, max_x + 1, size)
        y = random.randrange(40, max_y + 1, size)

        super().__init__(x, y, size, size, RED)
        self.size = size
        self.width = width
        self.height = height
        self.max_x = max_x
        self.max_y = max_y

    def respawn(self, snake_body):
        """
        перемещает яблоко в новое место
        snake_body - тело змейки чтобы не пересекаться
        пытается 1000 раз найти свободное место
        возвращает True если нашел
        """
        max_attempts = 1000

        for attempt in range(max_attempts):
            x = random.randrange(0, self.max_x + 1, self.size)
            y = random.randrange(40, self.max_y + 1, self.size)

            new_rect = pygame.Rect(x, y, self.size, self.size)

            collision = False
            for segment in snake_body:
                if new_rect.colliderect(segment):
                    collision = True
                    break

            if not collision:
                self.rect.x = x
                self.rect.y = y
                return True

        return False

    def draw(self, screen):
        """
        рисует яблоко с бликами
        screen - куда рисовать
        """
        # основной квадрат
        pygame.draw.rect(screen, self.color, self.rect)

        # блик для объема
        highlight_rect = pygame.Rect(
            self.rect.x + self.size // 4,
            self.rect.y + self.size // 4,
            self.size // 4,
            self.size // 4
        )
        pygame.draw.rect(screen, (255, 150, 150), highlight_rect)

        # хвостик
        stem_rect = pygame.Rect(
            self.rect.x + self.size // 2 - 1,
            self.rect.y - 3,
            2,
            4
        )
        pygame.draw.rect(screen, (139, 69, 19), stem_rect)