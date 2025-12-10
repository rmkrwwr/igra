"""
менеджер результатов
сохраняет и загружает счета
"""

import os
from datetime import datetime


class ScoreManager:
    """
    управляет счетами игроков
    сохраняет в файл загружает из файла
    """

    def __init__(self, filename='scores.txt'):
        """
        создает менеджер
        filename - файл для сохранения
        """
        self.filename = filename
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """
        загружает результаты из файла
        если файла нет - ничего не делает
        """
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        name, score, difficulty = parts[:3]
                        date = parts[3] if len(parts) > 3 else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        self.scores.append({
                            'name': name,
                            'score': int(score),
                            'difficulty': difficulty,
                            'date': date
                        })
        except Exception as e:
            print(f"ошибка загрузки результатов: {e}")

    def save_score(self, name, score, difficulty):
        """
        сохраняет новый результат
        name - имя игрока
        score - счет
        difficulty - сложность
        добавляет дату и время
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(f'{name},{score},{difficulty},{timestamp}\n')

            self.scores.append({
                'name': name,
                'score': score,
                'difficulty': difficulty,
                'date': timestamp
            })

            self.scores.sort(key=lambda x: x['score'], reverse=True)

        except Exception as e:
            print(f"ошибка сохранения результата: {e}")

    def get_high_score(self, difficulty=None):
        """
        возвращает рекорд
        difficulty - если указана то для этой сложности
        иначе для всех
        """
        if not self.scores:
            return 0

        if difficulty:
            filtered_scores = [s for s in self.scores if s['difficulty'] == difficulty]
            return max([s['score'] for s in filtered_scores]) if filtered_scores else 0
        else:
            return max([s['score'] for s in self.scores])

    def get_top_scores(self, count=10, difficulty=None):
        """
        возвращает топ-N результатов
        count - сколько результатов
        difficulty - если указана то для этой сложности
        """
        if difficulty:
            filtered = [s for s in self.scores if s['difficulty'] == difficulty]
            return sorted(filtered, key=lambda x: x['score'], reverse=True)[:count]
        else:
            return self.scores[:count]

    def get_player_stats(self, player_name):
        """
        возвращает статистику игрока
        player_name - имя игрока
        возвращает словарь с лучшим счетом общим числом игр и средним счетом
        """
        player_scores = [s for s in self.scores if s['name'] == player_name]
        if not player_scores:
            return None

        best_score = max([s['score'] for s in player_scores])
        total_games = len(player_scores)
        avg_score = sum([s['score'] for s in player_scores]) // total_games

        return {
            'best_score': best_score,
            'total_games': total_games,
            'avg_score': avg_score
        }