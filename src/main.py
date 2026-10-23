"""Модуль конфигурации CLI для визуализатора графа зависимостей (Этап 1)."""

import argparse
import os
import sys
import urllib.error
import urllib.request
import json


def create_parser():
    """Создает и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей пакетов Rust (Cargo)."
    )
    parser.add_argument(
        "--package", required=True, help="Имя анализируемого пакета."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="URL репозитория или путь к файлу тестового репозитория.",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым репозиторием, работа с тестовым файлом.",
    )
    parser.add_argument(
        "--version", required=True, help="Версия анализируемого пакета."
    )
    parser.add_argument(
        "--output",
        default="graph.png",
        help="Имя сгенерированного файла с изображением графа, имя по умолчанию graph.png",
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Режим вывода зависимостей в формате ASCII-дерева.",
    )
    parser.add_argument(
        "--filter",
        default="",
        help="Подстрока для фильтрации пакетов.",
    )
    return parser


def validate_args(args):
    """Проверяет корректность всех введенных пользователем параметров."""
    if not args.package.strip():
        raise ValueError("Имя пакета не может быть пустым, обязательное значение.")

    if not args.version.strip():
        raise ValueError("Версия пакета не может быть пустой, обязательное значение.")

    if not args.repo.strip():
        raise ValueError("URL или путь к репозиторию не может быть пустым, обязательное значение.")

    if args.test_mode:
        if not os.path.isfile(args.repo):
            raise FileNotFoundError(
                f"Файл тестового репозитория не найден: {args.repo}"
            )
    else:
        if not (
            args.repo.startswith("http://")
            or args.repo.startswith("https://")
        ):
            raise ValueError(
                "Адрес должен начинаться с http или https"
            )

    if not args.output.endswith(".png"):
        raise ValueError("Имя выходного файла должно заканчиваться на .png")

def fetch_cargo_dependencies(repo_url, package, version):
    """Извлекает прямые зависимости пакета Cargo по URL репозитория."""
    base_url = repo_url.rstrip("/")
    api_url = f"{base_url}/api/v1/crates/{package}/{version}/dependencies"
    headers = {"User-Agent": "ConfigManagementLab/1.0"}
    req = urllib.request.Request(api_url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            raw_data = response.read().decode("utf-8")
            parsed_json = json.loads(raw_data)
    except urllib.error.HTTPError as err:
        raise RuntimeError(
            f"Пакет '{package}' версии '{version}' не найден (код {err.code})."
        ) from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Ошибка сети при обращении к {api_url}") from err
    dependencies = []
    for dep in parsed_json.get("dependencies", []):
        if dep.get("kind") == "normal":
            crate_id = dep.get("crate_id")
            if crate_id and crate_id not in dependencies:
                dependencies.append(crate_id)

    return dependencies

def print_config(args):
    """Вывод параметров в формате ключ-значение."""
    for key, value in vars(args).items():
        print(f"{key} = {value}")


def main():
    """Точка входа в программу."""
    parser = create_parser()
    try:
        args = parser.parse_args()
        validate_args(args)
        deps = fetch_cargo_dependencies(args.repo, args.package, args.version)
        print(f"Прямые зависимости пакета {args.package} ({args.version}):")
        if deps:
            for dep in deps:
                print(f"- {dep}")
        else:
            print("Зависимости отсутствуют.")
    except Exception as err:
        print(f"Ошибка конфигурации: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()