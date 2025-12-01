import pygame
import random
from .base import GameObject
from .config import *


class Apple(GameObject):
    def __init__(self, size, width, height):
        x = random.randrange(0, width, size)
        y = random.randrange(0, height, size)
        super().__init__(x, y, size, size, RED)
        self.size = size
        self.width = width
        self.height = height

    def respawn(self, snake_body):
        """Перемещение яблока в случайную позицию, не занятую змейкой"""
        while True:
            self.rect.x = random.randrange(0, self.width, self.size)
            self.rect.y = random.randrange(0, self.height, self.size)

            # Проверяем, не попадает ли яблоко на змейку
            if not any(segment.colliderect(self.rect) for segment in snake_body):
                break

    def draw(self, screen):
        """Отрисовка яблока с эффектом объема"""
        # Основной круг
        pygame.draw.rect(screen, self.color, self.rect)

        # Блики для объема
        highlight_rect = pygame.Rect(
            self.rect.x + self.size // 4,
            self.rect.y + self.size // 4,
            self.size // 4,
            self.size // 4
        )
        pygame.draw.rect(screen, (255, 150, 150), highlight_rect)

        # Хвостик яблока
        stem_rect = pygame.Rect(
            self.rect.x + self.size // 2 - 1,
            self.rect.y - 3,
            2,
            4
        )
        pygame.draw.rect(screen, (139, 69, 19), stem_rect)
