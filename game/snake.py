import pygame
from .config import *

class Snake:
    def __init__(self, x, y, size):
        """Инициализация змейки"""
        self.size = size
        self.direction = RIGHT
        self.length = INITIAL_LENGTH

        #тело змейки как список прямоугольников
        self.body = []
        for i in range(self.length):
            segment = pygame.Rect(
                x - i * size,  # следующий сегмент левее
                y,
                size,
                size
            )
            self.body.append(segment)

        self.grow_next_move = False
        self.color = GREEN
        self.head_color = (0, 200, 0)

    def move(self):
        """Движение змейки вперед"""

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
        """Изменение направления движения"""
        opposite_x = -self.direction[0]
        opposite_y = -self.direction[1]

        if new_direction[0] != opposite_x or new_direction[1] != opposite_y:
            self.direction = new_direction

    def grow(self):
        """Команда роста на следующем ходу"""
        self.grow_next_move = True

    def check_collision(self, width, height):
        head = self.body[0]

        # Стены (верхняя граница теперь 40, не 0)
        if (head.x < 0 or head.x >= width or
                head.y < 40 or head.y >= height):  # ИЗМЕНИЛОСЬ: head.y < 40
            return True

        # Сама с собой
        for segment in self.body[1:]:
            if head.colliderect(segment):
                return True

        return False

    def check_apple_collision(self, apple_rect):
        """Проверка столкновения с яблоком"""
        head = self.body[-1]
        return head.colliderect(apple_rect)

    def get_head_position(self):
        """Получение позиции головы"""
        return (self.body[-1].x, self.body[-1].y)

    def get_positions(self):
        """Получение всех позиций змейки (для отрисовки)"""
        return [(seg.x, seg.y) for seg in self.body]

    def draw(self, screen):
        """Отрисовка змейки"""
        for i, segment in enumerate(self.body):
            if i == len(self.body) - 1:
                pygame.draw.rect(screen, self.head_color, segment)
            else:
                pygame.draw.rect(screen, self.color, segment)
            pygame.draw.rect(screen, DARK_GREEN, segment, 1)

    def reset(self, x, y):
        """Сброс змейки в начальное состояние"""
        self.__init__(x, y, self.size)