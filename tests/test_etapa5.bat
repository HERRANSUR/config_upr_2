echo Тест 24: PNG граф зависимостей и ASCII-дерево пакета (тестовый режим для локального JSON)
python src/main.py --package A --repo tests/test_repository.json --test-mode --version 1.0.0 --output graph1.png --ascii-tree
echo.

echo Тест 25: PNG граф зависимостей и ASCII-дерево пакета (тестовый режим для локального JSON) с фильтром
python src/main.py --package A --repo tests/test_repository.json --test-mode --version 1.0.0 --filter B --output graph2.png --ascii-tree
echo.

echo Тест 26: PNG граф зависимостей и ASCII-дерево пакета time (версия 0.1.45)
python src/main.py --package time --version 0.1.45 --repo https://crates.io --output graph3.png --ascii-tree
echo.