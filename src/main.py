"""Модуль конфигурации CLI для визуализатора графа зависимостей (Этап 3)."""

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
        help="Имя выходного файла с изображением графа graph.png",
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
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Режим вывода на экран обратных зависимостей для заданного пакета.",
    )
    return parser


def validate_args(args):
    """Проверяет корректность всех введенных пользователем параметров."""
    if not args.package.strip():
        raise ValueError("Имя пакета не может быть пустым.")

    if not args.version.strip():
        raise ValueError("Версия пакета не может быть пустой")

    if not args.repo.strip():
        raise ValueError("URL или путь к репозиторию не может быть пустым")

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
    """Извлекает прямые зависимости пакета Cargo по URL репозитория в словарь."""
    base_url = repo_url.rstrip("/")
    api_url = f"{base_url}/api/v1/crates/{package}/{version}/dependencies"
    headers = {'User-Agent': 'ConfigManagementLab/1.0 (zzz@gmail.com)'}
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
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
        if dep.get("kind") == "normal" and not dep.get("optional"):
            crate_id = dep.get("crate_id")
            if crate_id and crate_id not in dependencies:
                dependencies.append(crate_id)

    return dependencies

def print_config(args):
    """Вывод параметров в формате ключ-значение."""
    for key, value in vars(args).items():
        print(f"{key} = {value}")

def get_latest_version(repo_url, package):
    """Узнает последнюю стабильную версию пакета в репозитории Cargo."""
    base_url = repo_url.rstrip("/")
    info_url = f"{base_url}/api/v1/crates/{package}"
    headers = {'User-Agent': 'ConfigManagementLab/1.0 (zzz@gmail.com)'}
    req = urllib.request.Request(info_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            version = data["crate"]["max_stable_version"]
            return version
    except urllib.error.HTTPError as err:
        raise RuntimeError(
            f"Не удалось узнать версию пакета '{package}' (код {err.code})."
        ) from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Ошибка сети при обращении к {info_url}") from err


def load_test_repo(file_path):
    """Читает граф тестового репозитория из локального JSON-файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def build_graph_dfs(package, args, test_data, visited, graph):
    """Рекурсивно строит граф зависимостей алгоритмом DFS."""
    if package in visited:
        return
    visited.add(package)
    if args.test_mode:
        raw_deps = test_data.get(package, [])
    else:
        if package == args.package:
            pkg_version = args.version
        else:
            pkg_version = get_latest_version(args.repo, package)
        raw_deps = fetch_cargo_dependencies(args.repo, package, pkg_version)
    filtered_deps = []
    for dep in raw_deps:
        if args.filter and args.filter in dep:
            continue
        filtered_deps.append(dep)
    graph[package] = filtered_deps
    for dep in filtered_deps:
        if dep not in visited:
            build_graph_dfs(dep, args, test_data, visited, graph)


def print_graph(graph):
    """Выводит построенный граф зависимостей на экран."""
    print("Построенный граф зависимостей (DFS):")
    for pkg, deps in graph.items():
        deps_output = ", ".join(deps) if deps else "нет зависимостей"
        print(f"  {pkg} -> {deps_output}")


def find_reverse_dependencies(target_pkg, args, test_data):
    """Находит все пакеты, которые зависят от target_pkg, используя обход DFS."""
    reverse_deps = []
    for candidate in test_data:
        if candidate == target_pkg:
            continue
        if args.filter and args.filter in candidate:
            continue
        visited = set()
        temp_graph = {}
        build_graph_dfs(candidate, args, test_data, visited, temp_graph)
        if target_pkg in visited:
            reverse_deps.append(candidate)
    return reverse_deps

def print_reverse_dependencies(target_pkg, reverse_deps):
    """Выводит список обратных зависимостей для заданного пакета."""
    print(f"Обратные зависимости для пакета '{target_pkg}' (что зависит от него):")
    if reverse_deps:
        print(f"  {', '.join(reverse_deps)}")
    else:
        print("  нет обратных зависимостей")

def main():
    """Точка входа в программу."""
    parser = create_parser()
    try:
        args = parser.parse_args()
        validate_args(args)
        test_data = load_test_repo(args.repo) if args.test_mode else {}
        if args.reverse:
            rev_deps = find_reverse_dependencies(args.package, args, test_data)
            print_reverse_dependencies(args.package, rev_deps)
        else:
            visited = set()
            graph = {}
            build_graph_dfs(args.package, args, test_data, visited, graph)
            print_graph(graph)
    except Exception as err:
        print(f"Ошибка конфигурации: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()