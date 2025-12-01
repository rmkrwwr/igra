import pygame


class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        """Базовый метод отрисовки - переопределяется в наследниках"""
        pygame.draw.rect(screen, self.color, self.rect)

    def get_position(self):
        """Получение позиции объекта"""
        return (self.rect.x, self.rect.y)

    def set_position(self, x, y):
        """Установка позиции объекта"""
        self.rect.x = x
        self.rect.y = y

    def collides_with(self, other):
        """Проверка столкновения с другим объектом"""
        return self.rect.colliderect(other.rect)
