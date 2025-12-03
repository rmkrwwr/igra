import pygame
import sys
import argparse
from game.snake import Snake
from game.config import *

class TemporaryApple:
    def __init__(self, size, width, height):
        self.rect = pygame.Rect(100, 100, size, size)
        self.color = RED

    def respawn(self, snake_body):
        """Временный метод - потом заменит второй участник"""
        self.rect.x = 300
        self.rect.y = 300

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Game:
    def __init__(self, player_name="Player", speed=10, difficulty="medium"):
        """Инициализация игры"""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Змейка - Участник 1')
        self.clock = pygame.time.Clock()
        self.player_name = player_name
        self.game_speed = speed
        self.difficulty = difficulty
        self.score = 0
        self.game_over = False
        self.paused = False
        self.snake = Snake(WIDTH // 2, HEIGHT // 2, CELL_SIZE)
        self.apple = TemporaryApple(CELL_SIZE, WIDTH, HEIGHT)  #проверка яблока временное
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.frame_count = 0

    def handle_events(self):
        """Обработка всех событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    print("Пауза:", self.paused)
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
        """Обновление игровой логики"""
        if self.paused or self.game_over:
            return
        self.snake.move()
        if self.snake.check_apple_collision(self.apple.rect):
            self.snake.grow()
            self.score += 10
            self.apple.respawn(self.snake.body)
            print(f"скушал яблочко! счёт: {self.score}")

        if self.snake.check_collision(WIDTH, HEIGHT):
            self.game_over = True
            print(f"игра все твой финальный счёт: {self.score}")

    def draw_grid(self):
        """Отрисовка сетки"""
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREEN, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREEN, (0, y), (WIDTH, y), 1)

    def draw_ui(self):
        """Отрисовка интерфейса"""
        info_panel = pygame.Rect(0, 0, WIDTH, 40)
        pygame.draw.rect(self.screen, GRAY, info_panel)
        score_text = self.font.render(f'счёт: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
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
            score_rect = score_display.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(score_display, score_rect)
            restart_text = self.font.render('жми R для рестарта', True, YELLOW)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

    def render(self):
        """Отрисовка всей игры"""
        self.screen.fill(BLACK)
        self.draw_grid()
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        self.draw_ui()
        pygame.display.flip()

    def restart_game(self):
        """Перезапуск игры"""
        self.snake = Snake(WIDTH // 2, HEIGHT // 2, CELL_SIZE)
        self.apple = TemporaryApple(CELL_SIZE, WIDTH, HEIGHT)
        self.score = 0
        self.game_over = False
        self.paused = False
        print("перезапуск игры)")

    def quit_game(self):
        """Корректный выход из игры"""
        pygame.quit()
        sys.exit()

    def run(self):
        """Главный игровой цикл"""
        print("Змейка")
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
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='игра крутая Змейка',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python main.py
  python main.py --name "санк" --speed 15 --difficulty hard
        '''
    )

    parser.add_argument('--name', type=str, default='Игрок',
                        help='Имя игрока (по умолчанию: "Игрок")')

    parser.add_argument('--speed', type=int, default=10,
                        help='Скорость игры в FPS (по умолчанию: 10)')

    parser.add_argument('--difficulty', type=str, default='medium',
                        choices=['easy', 'medium', 'hard'],
                        help='Уровень сложности (по умолчанию: medium)')

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