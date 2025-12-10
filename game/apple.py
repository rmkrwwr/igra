"""
ТОЧКА ВХОДА В ИГРУ
Запуск: python main.py
Управление: стрелки или WASD
Цель: съедать яблоки, не врезаться
"""

import pygame
import random
from .base import GameObject
from .config import *


class Apple(GameObject):
    def __init__(self, size, width, height):
        max_x = width - size
        max_y = height - size

        x = random.randrange(0, max_x + 1, size)
        y = random.randrange(0, max_y + 1, size)

        super().__init__(x, y, size, size, RED)
        self.size = size
        self.width = width
        self.height = height
        self.max_x = max_x
        self.max_y = max_y

    def respawn(self, snake_body):
        max_attempts = 1000

        for attempt in range(max_attempts):
            x = random.randrange(0, self.max_x + 1, self.size)
            y = random.randrange(0, self.max_y + 1, self.size)

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

        for x in range(0, self.max_x + 1, self.size):
            for y in range(0, self.max_y + 1, self.size):
                test_rect = pygame.Rect(x, y, self.size, self.size)
                free = True
                for segment in snake_body:
                    if test_rect.colliderect(segment):
                        free = False
                        break
                if free:
                    self.rect.x = x
                    self.rect.y = y
                    return True

        self.rect.x = -100
        self.rect.y = -100
        return False

    def draw(self, screen):
        if self.rect.right > self.width:
            self.rect.x = self.width - self.size
        if self.rect.bottom > self.height:
            self.rect.y = self.height - self.size
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.top < 0:
            self.rect.y = 0

        pygame.draw.rect(screen, self.color, self.rect)

        highlight_rect = pygame.Rect(
            self.rect.x + self.size // 4,
            self.rect.y + self.size // 4,
            self.size // 4,
            self.size // 4
        )
        pygame.draw.rect(screen, (255, 150, 150), highlight_rect)

        stem_rect = pygame.Rect(
            self.rect.x + self.size // 2 - 1,
            self.rect.y - 3,
            2,
            4
        )
        pygame.draw.rect(screen, (139, 69, 19), stem_rect)