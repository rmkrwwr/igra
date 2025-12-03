import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygame
from game.graphics import Graphics

pygame.init()


def test_graphics_initialization():
    """Тест инициализации графики"""
    graphics = Graphics(800, 600)
    assert graphics.width == 800
    assert graphics.height == 600
    assert hasattr(graphics, 'font_large')
    assert hasattr(graphics, 'font_medium')
    assert hasattr(graphics, 'font_small')
    print("✓ Тест инициализации графики пройден")


def test_texture_loading():
    """Тест загрузки текстур"""
    graphics = Graphics(800, 600)
    assert 'snake_head' in graphics.textures
    assert 'snake_body' in graphics.textures
    assert 'apple' in graphics.textures
    print("✓ Тест загрузки текстур пройден")


def test_score_manager():
    """Тест менеджера результатов"""
    from game.score_manager import ScoreManager

    manager = ScoreManager('test_scores.txt')

    manager.save_score('TestPlayer', 100, 'medium')

    high_score = manager.get_high_score()
    assert high_score == 100

    if os.path.exists('test_scores.txt'):
        os.remove('test_scores.txt')
    print("✓ Тест менеджера результатов пройден")


def run_all_graphics_tests():
    """Запуск всех тестов графики"""
    print("Запуск тестов для графических модулей...")
    test_graphics_initialization()
    test_texture_loading()
    test_score_manager()
    print("Все графические тесты пройдены успешно!")


if __name__ == '__main__':
    run_all_graphics_tests()