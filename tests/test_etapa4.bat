echo Тест 20: Обратные зависимости для пакета D
python src/main.py --package D --version 1.0 --repo tests/test_repository.json --test-mode --reverse
echo.

echo Тест 21: Обратные зависимости для пакета B
python src/main.py --package B --version 1.0 --repo tests/test_repository.json --test-mode --reverse
echo.

echo Тест 22: Обратные зависимости для пакета D с фильтром
python src/main.py --package D --version 1.0 --repo tests/test_repository.json --test-mode --reverse --filter B
echo.

echo Тест 23: Обратные зависимости для пакета C
python src/main.py --package C --version 1.0 --repo tests/test_repository.json --test-mode --reverse
echo.