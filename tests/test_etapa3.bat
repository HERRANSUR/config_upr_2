echo Тест 13: Граф зависимостей пакета (тестовый режим для локального JSON)
python src/main.py --package A --repo tests/test_repository.json --test-mode --version 1.0.0
echo.

echo Тест 14: Граф зависимостей пакета (тестовый режим для локального JSON) с фильтром
python src/main.py --package A --repo tests/test_repository.json --test-mode --version 1.0.0 --filter B
echo.

echo Тест 15: Граф зависимостей пакета itoa (версия 1.0.11)
python src/main.py --package itoa --version 1.0.11 --repo https://crates.io
echo.

echo Тест 16: Граф зависимостей пакета time с исключением (фильтром) (версия 0.8.5)
python src/main.py --package time --version 0.1.45 --repo https://crates.io --filter winapi
echo.

echo Тест 17: Граф зависимостей пакета serde (версия 1.0.210)
python src/main.py --package serde --version 1.0.210 --repo https://crates.io
echo.

echo Тест 18: Граф зависимостей пакета time (версия 0.1.45)
python src/main.py --package time --version 0.1.45 --repo https://crates.io
echo.

echo Тест 19: Граф зависимостей пакета rand (версия 0.8.5)
python src/main.py --package rand --version 0.8.5 --repo https://crates.io
echo.
