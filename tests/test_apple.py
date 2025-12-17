import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygame
from game.apple import Apple

pygame.init()


def test_apple_initialization():
    """Тест инициализации яблока"""
    apple = Apple(20, 800, 600)
    assert apple.rect.width == 20
    assert apple.rect.height == 20
    assert apple.color == (255, 0, 0)
    print("✓ Тест инициализации яблока пройден")


def test_apple_respawn():
    """Тест перемещения яблока"""
    apple = Apple(20, 800, 600)
    original_pos = apple.get_position()

    snake_body = [pygame.Rect(0, 0, 20, 20)]

    apple.respawn(snake_body)
    new_pos = apple.get_position()

    assert original_pos != new_pos
    print("✓ Тест перемещения яблока пройден")


def test_apple_position_constraints():
    """Тест ограничений позиции яблока"""
    apple = Apple(20, 800, 600)

    assert apple.rect.x % 20 == 0
    assert apple.rect.y % 20 == 0
    print("✓ Тест ограничений позиции пройден")


def test_apple_collision_avoidance():
    """Тест избегания столкновения со змейкой"""
    apple = Apple(20, 800, 600)

    snake_body = [pygame.Rect(x, 0, 20, 20) for x in range(0, 800, 20)]

    apple.respawn(snake_body)

    for segment in snake_body:
        class TempObject:
            def __init__(self, rect):
                self.rect = rect

        temp_obj = TempObject(segment)
        assert not apple.collides_with(temp_obj)
    print("✓ Тест избегания столкновений пройден")


def run_all_tests():
    """Запуск всех тестов для яблока"""
    print("Запуск тестов для модуля Apple...")
    test_apple_initialization()
    test_apple_respawn()
    test_apple_position_constraints()
    test_apple_collision_avoidance()
    print("Все тесты для Apple пройдены успешно!")


if __name__ == '__main__':
    run_all_tests()