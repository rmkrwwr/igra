"""
главный файл игры
запускает игру обрабатывает ввод
"""

from game.database import db
import pygame
import sys
import argparse
from game.snake import Snake
from game.config import *
from game.apple import Apple
from game.score_manager import ScoreManager


class Game:
    """
    главный класс игры
    управляет всем игровым процессом
    """

    def __init__(self, player_name="Player", speed=10, difficulty="medium"):
        """
        создает игру
        player_name - имя игрока
        speed - скорость игры
        difficulty - сложность
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('змейка')
        start_x = (SCREEN_WIDTH // 2) // CELL_SIZE * CELL_SIZE
        start_y = ((SCREEN_HEIGHT // 2) // CELL_SIZE * CELL_SIZE) + 40
        self.snake = Snake(start_x, start_y, CELL_SIZE)
        self.apple = Apple(CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.clock = pygame.time.Clock()
        self.player_name = player_name
        self.game_speed = speed
        self.difficulty = difficulty
        self.score = 0
        self.game_over = False
        self.paused = False
        #self.snake = Snake(WIDTH // 2, HEIGHT // 2, CELL_SIZE)
        self.apple = Apple(CELL_SIZE, WIDTH, HEIGHT)
        self.score_manager = ScoreManager()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.frame_count = 0
        self.player_name = "Player"
        self.apples_eaten = 0
        self.game_start_time = 0

    def handle_events(self):
        """
        обрабатывает события игры
        клавиши закрытие окна и тд
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    print("пауза:", self.paused)
                if self.game_over and event.key == pygame.K_r:
                    self.restart_game()
                if event.key == pygame.K_q:
                    self.quit_game()
                if not self.paused and not self.game_over:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)

    def update(self):
        """
        обновляет игровую логику
        движение змейки проверка столкновений
        """
        if self.paused or self.game_over:
            return
        self.snake.move()
        if self.snake.check_apple_collision(self.apple.rect):
            self.snake.grow()
            self.score += 10
            self.apples_eaten += 1
            self.apple.respawn(self.snake.body)
            print(f"скушал яблочко! счёт: {self.score}")

        if self.snake.check_collision(WIDTH, HEIGHT):
            self.game_over = True
            print(f"💀 Игра окончена! Финальный счёт: {self.score}")

            # Сохраняем в PostgreSQL БД
            db.save_game_result(
                player_name=self.player_name,
                score=self.score,
                snake_length=self.snake.length,
                difficulty=self.difficulty,
                apples_eaten=self.apples_eaten
            )

            # Сохраняем в файл (старая система)
            self.score_manager.save_score(
                self.player_name,
                self.score,
                self.difficulty
            )
            print(f"💾 Сохранено в файл")

    def draw_grid(self):
        """
        рисует сетку поля
        """
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREEN, (x, 40), (x, HEIGHT), 1)
        for y in range(40, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREEN, (0, y), (WIDTH, y), 1)

    def draw_ui(self):
        """
        рисует интерфейс игры
        счет панель паузу game over
        """
        info_panel = pygame.Rect(0, 0, WIDTH, 40)
        pygame.draw.rect(self.screen, GRAY, info_panel)
        score_text = self.font.render(f'счёт: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        high_score = self.score_manager.get_high_score(self.difficulty)
        high_text = self.font.render(f'рекорд: {high_score}', True, YELLOW)
        self.screen.blit(high_text, (WIDTH // 40, 40))
        name_text = self.font.render(f'игрок: {self.player_name}', True, WHITE)
        self.screen.blit(name_text, (WIDTH - 200, 10))
        length_text = self.font.render(f'длина: {self.snake.length}', True, WHITE)
        self.screen.blit(length_text, (WIDTH // 2 - 50, 10))

        if self.paused:
            pause_text = self.big_font.render('пауза', True, YELLOW)
            text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)

            hint_text = self.font.render('жми P для продолжения', True, WHITE)
            hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(hint_text, hint_rect)

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            game_over_text = self.big_font.render('game over xd', True, RED)
            go_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, go_rect)
            score_display = self.font.render(f'счёт: {self.score}', True, WHITE)
            #time_display = self.font.render(f'Время: {self.game_duration} сек', True, CYAN)
            #time_rect = time_display.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            #self.screen.blit(time_display, time_rect)
            score_rect = score_display.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(score_display, score_rect)
            restart_text = self.font.render('жми R для рестарта', True, YELLOW)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

    def render(self):
        """
        рисует всю игру
        фон сетку яблоко змейку интерфейс
        """
        self.screen.fill(BLACK)
        self.draw_grid()
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        self.draw_ui()
        pygame.display.flip()

    def restart_game(self):
        """
        перезапускает игру
        сбрасывает все параметры
        """
        self.game_start_time = pygame.time.get_ticks()
        self.snake = Snake(WIDTH // 2, HEIGHT // 2, CELL_SIZE)
        self.apple = Apple(CELL_SIZE, WIDTH, HEIGHT)
        self.score = 0
        self.game_over = False
        self.paused = False
        print("перезапуск игры)")
        top_scores = self.score_manager.get_top_scores(5, self.difficulty)
        if top_scores:
            print("топ 5")
            for i, score_data in enumerate(top_scores, 1):
                print(f"  {i}. {score_data['name']}: {score_data['score']} ({score_data['date']})")

    def quit_game(self):
        """
        выходит из игры
        закрывает pygame
        """
        db.close()
        pygame.quit()
        sys.exit()

    def run(self):
        """
        главный игровой цикл
        крутится пока игра не закончится
        """
        print("змейка")
        print(f"игрок: {self.player_name}")
        print(f"скорость: {self.game_speed} FPS")
        print(f"сложность: {self.difficulty}")
        print("управление: WASD/стрелки, P - пауза, R - рестарт, Q - выход")
        print("=" * 30)

        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.game_speed)
            self.frame_count += 1


def parse_arguments():
    """
    парсит аргументы командной строки
    имя скорость сложность
    """
    parser = argparse.ArgumentParser(
        description='игра крутая змейка',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
примеры использования:
  python main.py
  python main.py --name "санк" --speed 15 --difficulty hard
        '''
    )

    parser.add_argument('--name', type=str, default='игрок',
                        help='имя игрока (по умолчанию: "игрок")')

    parser.add_argument('--speed', type=int, default=10,
                        help='скорость игры в FPS (по умолчанию: 10)')

    parser.add_argument('--difficulty', type=str, default='medium',
                        choices=['easy', 'medium', 'hard'],
                        help='уровень сложности (по умолчанию: medium)')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    speed_map = {
        'easy': 8,
        'medium': 12,
        'hard': 16
    }
    final_speed = speed_map.get(args.difficulty, args.speed)

    game = Game(
        player_name=args.name,
        speed=final_speed,
        difficulty=args.difficulty
    )
    game.run()