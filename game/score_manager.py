import os
from datetime import datetime


class ScoreManager:
    def __init__(self, filename='scores.txt'):
        self.filename = filename
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Загрузка результатов из файла"""
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
            print(f"Ошибка загрузки результатов: {e}")

    def save_score(self, name, score, difficulty):
        """Сохранение нового результата"""
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
            print(f"Ошибка сохранения результата: {e}")

    def get_high_score(self, difficulty=None):
        """Получение рекорда"""
        if not self.scores:
            return 0

        if difficulty:
            filtered_scores = [s for s in self.scores if s['difficulty'] == difficulty]
            return max([s['score'] for s in filtered_scores]) if filtered_scores else 0
        else:
            return max([s['score'] for s in self.scores])

    def get_top_scores(self, count=10, difficulty=None):
        """Получение топ-N результатов"""
        if difficulty:
            filtered = [s for s in self.scores if s['difficulty'] == difficulty]
            return sorted(filtered, key=lambda x: x['score'], reverse=True)[:count]
        else:
            return self.scores[:count]

    def get_player_stats(self, player_name):
        """Получение статистики игрока"""
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