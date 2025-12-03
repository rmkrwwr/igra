

# базовая версия
python main.py

# с параметрами
python main.py --name "Игрок" --speed 12 --difficulty medium

--name        Имя игрока (по умолчанию: "Игрок")
--speed       Скорость игры в FPS (по умолчанию: 10)
--difficulty  Уровень сложности: easy/medium/hard (по умолчанию: medium)

Примеры запуска
# легкий уровень
python main.py --name "Новичок" --difficulty easy

# сложный уровень с высокой скоростью
python main.py --name "Профи" --speed 15 --difficulty hard

# кастомная скорость
python main.py --name "Тестер" --speed 8

     каждое яблоко: +10 очков

    сохраняются в файл scores.txt

    формат: Имя,Счёт,Сложность,Дата



# мой тест (змея)
python tests/test_snake.py

# тест саши (яблоко и графика)
python tests/test_apple.py
python tests/test_graphics.py
