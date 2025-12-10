"""
класс змейки
реализует всю логику поведения
змейки: движение, управление, рост, столкновения и отрисовку.
Класс управляет телом змейки как списком сегментов и обеспечивает
все необходимые взаимодействия с игровым миром
"""

import pygame
from .config import *


class Snake:
    """
    змейка в игре
    двигается ест яблоки и все дела
    """

    def __init__(self, x, y, size):
        """
        создает змейку
        x y - где голова
        size - размер клетки
        """
        self.size = size
        self.direction = RIGHT
        self.length = INITIAL_LENGTH

        # тело как список прямоугольников
        self.body = []
        for i in range(self.length):
            segment = pygame.Rect(
                x - i * size,
                y,
                size,
                size
            )
            self.body.append(segment)

        self.grow_next_move = False
        self.color = GREEN
        self.head_color = (0, 200, 0)

    def move(self):
        """
        двигает змейку вперед
        если должен расти - добавляет сегмент
        """
        # голова - последний элемент
        head = self.body[-1].copy()
        head.x += self.direction[0] * self.size
        head.y += self.direction[1] * self.size

        self.body.append(head)
        if not self.grow_next_move:
            self.body.pop(0)
        else:
            self.grow_next_move = False
            self.length += 1

    def change_direction(self, new_direction):
        """
        меняет направление
        new_direction - куда повернуть
        нельзя повернуть на 180 градусов
        """
        opposite_x = -self.direction[0]
        opposite_y = -self.direction[1]

        if new_direction[0] != opposite_x or new_direction[1] != opposite_y:
            self.direction = new_direction

    def grow(self):
        """
        говорит что на следующем ходу нужно вырасти
        Подготавливает змейку к росту на следующем шаге движения.

        флаг grow_next_move в True что приведет к увеличению
        длины змейки на 1 сегмент при следующем вызове метода move()
        """

        self.grow_next_move = True

    def check_collision(self, width, height):
        """
        проверяет столкновения
        с границами и с собой
        width height - размер поля
        возвращает True если врезался
        """
        head = self.body[-1]
        if (head.x < 0 or head.x >= width or
                head.y < 40 or head.y >= height):
            return True
        for segment in self.body[:-1]:
            if head.colliderect(segment):
                return True

        return False

    def check_apple_collision(self, apple_rect):
        """
        проверяет съел ли яблоко
        apple_rect - прямоугольник яблока
        возвращает True если съел
        """
        head = self.body[-1]
        return head.colliderect(apple_rect)

    def get_head_position(self):
        """
        возвращает где голова
        """
        return (self.body[-1].x, self.body[-1].y)

    def get_positions(self):
        """
        возвращает все позиции змейки
        для отрисовки или еще чего
        """
        return [(seg.x, seg.y) for seg in self.body]

    def draw(self, screen):
        """
        рисует змейку
        screen - куда рисовать
        голова другого цвета
        """
        for i, segment in enumerate(self.body):
            if i == len(self.body) - 1:
                pygame.draw.rect(screen, self.head_color, segment)
            else:
                pygame.draw.rect(screen, self.color, segment)
            pygame.draw.rect(screen, DARK_GREEN, segment, 1)

    def reset(self, x, y):
        """
        сбрасывает змейку в начальное состояние
        x y - новая позиция
        """
        self.__init__(x, y, self.size)