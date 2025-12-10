"""
графика для игры
класс Graphics отвечающий за всю визуальную составляющую игры:
отрисовку интерфейса игровых объектов  экранов состояний (пауза, game over)
и вспомогательных элементов (сетка, счет)
"""

import pygame
from .config import *


class Graphics:
    """
    отвечает за всю графику в игре
    рисует интерфейс паузу game over
    """

    def __init__(self, width, height):
        """
        создает графику
        width height - размер экрана
        """
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.textures = {}
        self.load_textures()

    def load_textures(self):
        """
        загружает текстуры
        сейчас просто цветные квадраты
        """
        try:
            self.create_texture('snake_head', GREEN)
            self.create_texture('snake_body', (0, 200, 0))
            self.create_texture('apple', RED)
        except Exception as e:
            print(f"ошибка загрузки текстур: {e}")

    def create_texture(self, name, color):
        """
        создает текстуру по цвету
        name - имя текстуры
        color - какой цвет
        """
        texture = pygame.Surface((CELL_SIZE, CELL_SIZE))
        texture.fill(color)
        pygame.draw.rect(texture, (color[0] // 2, color[1] // 2, color[2] // 2),
                         texture.get_rect(), 2)
        self.textures[name] = texture

    def draw_score(self, screen, score, high_score, player_name):
        """
        рисует панель счета
        screen - куда рисовать
        score - текущий счет
        high_score - рекорд
        player_name - имя игрока
        """
        info_bg = pygame.Rect(0, 0, self.width, 40)
        pygame.draw.rect(screen, (50, 50, 50), info_bg)

        score_text = self.font_medium.render(f'счёт: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        high_score_text = self.font_medium.render(f'рекорд: {high_score}', True, YELLOW)
        screen.blit(high_score_text, (self.width // 2 - 70, 10))

        name_text = self.font_medium.render(f'игрок: {player_name}', True, WHITE)
        screen.blit(name_text, (self.width - 200, 10))

    def draw_game_over(self, screen, score, player_name):
        """
        рисует экран game over
        screen - куда рисовать
        score - финальный счет
        player_name - имя игрока
        """
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render('игра окончена!', True, RED)
        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(game_over_text, text_rect)

        score_text = self.font_medium.render(f'финальный счёт: {score}', True, WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(score_text, score_rect)

        name_text = self.font_medium.render(f'игрок: {player_name}', True, WHITE)
        name_rect = name_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
        screen.blit(name_text, name_rect)

        instruction_text = self.font_small.render('жми R для рестарта или Q для выхода', True, YELLOW)
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
        screen.blit(instruction_text, instruction_rect)

    def draw_pause(self, screen):
        """
        рисует экран паузы
        screen - куда рисовать
        """
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(120)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render('пауза', True, YELLOW)
        text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        screen.blit(pause_text, text_rect)

        instruction_text = self.font_medium.render('жми P для продолжения', True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        screen.blit(instruction_text, instruction_rect)

    def draw_grid(self, screen):
        """
        рисует сетку поля
        screen - куда рисовать
        сетка от y=40
        """
        for x in range(0, self.width, CELL_SIZE):
            pygame.draw.line(screen, DARK_GREEN,
                             (x, 40), (x, self.height), 1)
        for y in range(40, self.height, CELL_SIZE):
            pygame.draw.line(screen, DARK_GREEN,
                             (0, y), (self.width, y), 1)

    def draw_snake(self, screen, snake_body):
        """
        рисует змейку с глазами
        screen - куда рисовать
        snake_body - тело змейки
        голова с глазами
        """
        for i, segment in enumerate(snake_body):
            if i == len(snake_body) - 1:  # голова
                pygame.draw.rect(screen, (0, 200, 0), segment)
                eye_size = segment.width // 5
                left_eye = pygame.Rect(
                    segment.x + segment.width // 4 - eye_size // 2,
                    segment.y + segment.height // 3 - eye_size // 2,
                    eye_size, eye_size
                )
                right_eye = pygame.Rect(
                    segment.x + 3 * segment.width // 4 - eye_size // 2,
                    segment.y + segment.height // 3 - eye_size // 2,
                    eye_size, eye_size
                )
                pygame.draw.rect(screen, WHITE, left_eye)
                pygame.draw.rect(screen, WHITE, right_eye)
            else:
                pygame.draw.rect(screen, GREEN, segment)
                pygame.draw.rect(screen, (0, 150, 0), segment, 1)