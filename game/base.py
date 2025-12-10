"""
базовый класс для всех объектов игры
"""

import pygame


class GameObject:
    """
    базовый объект игры
    умеет рисоваться и проверять столкновения
    """

    def __init__(self, x, y, width, height, color):
        """
        создает объект
        x y - координаты
        width height - размер
        color - цвет
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        """
        рисует объект на экране
        screen - куда рисовать
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def get_position(self):
        """
        возвращает позицию
        """
        return (self.rect.x, self.rect.y)

    def set_position(self, x, y):
        """
        ставит новую позицию
        x y - куда поставить
        """
        self.rect.x = x
        self.rect.y = y

    def collides_with(self, other):
        """
        проверяет столкновение с другим объектом
        other - другой объект
        возвращает True если столкнулись
        """
        return self.rect.colliderect(other.rect)