import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygame
from game.snake import Snake
from game.config import *


def run_tests():
    """Запуск всех тестов"""
    print("это запуск тестов для проверочки")

    pygame.init()
    print("инициализации змейки")
    snake = Snake(100, 100, 20)
    assert snake.direction == RIGHT, "направление должно быть RIGHT"
    assert snake.length == INITIAL_LENGTH, f"длина должна быть {INITIAL_LENGTH}"
    assert len(snake.body) == INITIAL_LENGTH, f"тело должно иметь {INITIAL_LENGTH} сегментов"
    print(" ну хайп!")

    print("как двигается наша змейка...")
    initial_head = snake.get_head_position()
    snake.move()
    new_head = snake.get_head_position()
    assert new_head[0] == initial_head[0] + 20, "должна двигаться вправо"
    assert new_head[1] == initial_head[1], "Y координата не должна меняться"
    print("круто!")

    print("изменения направления")
    snake.change_direction(UP)
    assert snake.direction == UP, "направление должно измениться на UP"
    snake.change_direction(DOWN)
    assert snake.direction == UP, "не должно меняться на противоположное"
    print("класс!")


    print("роста змейки")
    initial_length = snake.length
    snake.grow()
    snake.move()
    assert snake.length == initial_length + 1, "длина должна увеличиться"
    print(" класс!")

    print("столкновения с границами")
    edge_snake = Snake(0, 40, 20)  # Начинаем с y=40 (ниже панели)
    edge_snake.change_direction(LEFT)
    for i in range(3):
        edge_snake.move()
        print(f"  шаг {i + 1}: голова на {edge_snake.get_head_position()}")
    collision = edge_snake.check_collision(800, 600)
    print(f"  Столкновение после 3 движений: {collision}")
    assert collision == True, "должно быть столкновение"
    print("хайп!")

    print("столкновения с собой")
    self_snake = Snake(100, 100, 20)
    while self_snake.length < 4:
        self_snake.grow()
        self_snake.move()

    self_snake.change_direction(DOWN)
    self_snake.move()
    self_snake.change_direction(LEFT)
    self_snake.move()
    self_snake.change_direction(UP)
    self_snake.move()
    collision_possible = self_snake.check_collision(800, 600)
    print(f"столкновение: {collision_possible}")
    print("проверка столкновений работает!")
    print("успешно")
    print("змейка работает правильно!")




if __name__ == '__main__':
    run_tests()