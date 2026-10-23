@echo off
chcp 65001 > nul

echo Тест 8: Прямые зависимости пакета serde (версия 1.0.210)
python src/main.py --package serde --version 1.0.210 --repo https://crates.io
echo.

echo Тест 9: Прямые зависимости пакета rand (версия 0.8.5)
python src/main.py --package rand --version 0.8.5 --repo https://crates.io
echo.

echo Тест 10: Прямые зависимости пакета itoa (версия 1.0.11)
python src/main.py --package itoa --version 1.0.11 --repo https://crates.io
echo.

echo Тест 11: Ошибка - несуществующая версия пакета
python src/main.py --package serde --version 999.999.999 --repo https://crates.io

echo Тест 12: Ошибка - несуществующий пакет
python src/main.py --package ser --version 1.0 --repo https://crates.io