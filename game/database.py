import psycopg2
from psycopg2.extras import RealDictCursor


class GameDatabase:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Подключиться к PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="snake_game_db",
                user="postgres",
                password="admin",
                port="5432"
            )
            print(" PostgreSQL подключена")

        except Exception as e:
            print(f" Ошибка подключения к БД: {e}")
            print("Проверь пароль в строке 16!")
            self.conn = None

    def save_game_result(self, player_name, score, snake_length, difficulty,
                         apples_eaten=0):
        """Сохранить результат игры"""
        if not self.conn:
            print(" БД не подключена, игра не сохранена")
            return False

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO game_results 
                    (player_name, score, snake_length, apples_eaten)
                    VALUES (%s, %s, %s, %s)
                """, (player_name, score, snake_length, apples_eaten))

                self.conn.commit()
                print(f" Сохранено: {player_name} - {score}")
                return True

        except Exception as e:
            print(f" Ошибка: {e}")
            return False

    def get_top_scores(self, limit=10):
        """Получить топ рекордов"""
        if not self.conn:
            return []

        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT player_name, score, snake_length,
                           TO_CHAR(created_at, 'DD.MM HH24:MI') as time
                    FROM game_results 
                    ORDER BY score DESC 
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()
        except:
            return []

    def close(self):
        if self.conn:
            self.conn.close()


db = GameDatabase()