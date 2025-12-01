import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygame
from game.snake import Snake

# Инициализация Pygame для тестов
pygame.init()


def test_snake_initialization():
    """Тест инициализации змейки"""
    snake = Snake(100, 100, 20)
    assert snake.get_length() == 1
    assert snake.direction == (1, 0)
    assert snake.rect.width == 20
    assert snake.rect.height == 20
    print("✓ Тест инициализации пройден")


def test_snake_movement():
    """Тест движения змейки"""
    snake = Snake(100, 100, 20)

    initial_length = snake.get_length()
    snake.move()
    assert snake.get_length() == initial_length
    assert snake.rect.x == 120  # 100 + 20

    snake.grow = True
    snake.move()
    assert snake.get_length() == initial_length + 1
    print("✓ Тест движения пройден")


def test_direction_change():
    """Тест изменения направления"""
    snake = Snake(100, 100, 20)

    snake.change_direction(0, 1)
    assert snake.direction == (0, 1)

    #запрещаем противоположное
    snake.change_direction(0, -1)
    assert snake.direction == (0, 1)
    print("Тест изменения направления")


def test_collision_detection():
    """Тест обнаружения столкновений"""
    snake = Snake(0, 0, 20)  #это если у границы врод потом лево и центр


    snake.change_direction(-1, 0)
    snake.move()
    assert snake.check_collision(800, 600) == True

    snake = Snake(400, 300, 20)
    assert snake.check_collision(800, 600) == False
    print("тест на столкновения")


def run_all_tests():
    """Запуск всех тестов"""
    print("запуск тестов для змейки")
    test_snake_initialization()
    test_snake_movement()
    test_direction_change()
    test_collision_detection()
    print("все тесты пройдены успешно!")


if __name__ == '__main__':
    run_all_tests()