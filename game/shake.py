import pygame
from .base import GameObject
class Snake(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, (0, 255, 0))
        self.direction = (1, 0)
        self.body = [self.rect.copy()]
        self.grow = False
        self.size = size

    def move(self):
        """Движение змейки"""
        head = self.body[-1].copy()
        head.move_ip(self.direction[0] * self.size, self.direction[1] * self.size)
        self.body.append(head)
        if not self.grow:
            self.body.pop(0)

        self.grow = False
        self.rect = self.body[-1]

    def change_direction(self, dx, dy):
        """Изменение направления движения"""

        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def check_collision(self, width, height):
        """Проверка столкновений с границами и собой"""
        head = self.body[-1]


        if (head.left < 0 or head.right > width or
                head.top < 0 or head.bottom > height):
            return True


        for segment in self.body[:-1]:
            if head.colliderect(segment):
                return True

        return False

    def draw(self, screen):
        """Отрисовка змейки"""
        for segment in self.body:
            pygame.draw.rect(screen, self.color, segment)
            pygame.draw.rect(screen, (0, 200, 0), segment, 1)

    def get_head_position(self):
        """Получение позиции головы"""
        return self.body[-1].center if self.body else (0, 0)

    def get_length(self):
        """Получение длины змейки"""
        return len(self.body)