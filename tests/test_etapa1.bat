@echo off
chcp 65001 > nul

echo Тест 1: Корректный запуск (обычный режим)
python src/main.py --package serde --repo https://crates.io --version 1.0.0 --output graph.png --ascii-tree --filter win
echo.

echo Тест 2: Корректный запуск (тестовый режим с JSON-файлом)
python src/main.py --package A --repo tests/test_repository.json --test-mode --version 1.0.0
echo.

echo Тест 3: Ошибка - пустое имя пакета
python src/main.py --package "" --repo https://crates.io --version 1.0.0
echo.

echo Тест 4: Ошибка - пустая версия пакета
python src/main.py --package serde --repo https://crates.io --version ""
echo.

echo Тест 5: Ошибка - неправильный URL репозитория
python src/main.py --package serde --repo htp://crates.io --version 1.0.0
echo.

echo Тест 6: Ошибка - файл тестового репозитория не существует
python src/main.py --package A --repo tests/no.json --test-mode --version 1.0.0
echo.

echo Тест 7: Ошибка - выходной файл не в формате .png
python src/main.py --package serde --repo https://crates.io --version 1.0.0 --output im.jpg