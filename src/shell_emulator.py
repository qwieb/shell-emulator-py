"""Эмулятор командной оболочки ОС. Этап 2: конфигурация.

Добавлены параметры командной строки (путь к VFS, путь к стартовому
скрипту), поддержка стартового скрипта с комментариями и отладочный
вывод всех параметров при запуске.
"""

import argparse
import getpass
import os
import socket
import sys


def build_prompt() -> str:
    """Сформировать приглашение вида username@hostname:~$."""
    user = os.environ.get("USER") or os.environ.get("USERNAME") or "user"
    host = socket.gethostname() or "localhost"
    cwd = os.getcwd().replace("\\", "/")
    home = os.path.expanduser("~").replace("\\", "/")

    if cwd == home:
        short_cwd = "~"
    elif cwd.startswith(home + "/"):
        short_cwd = "~" + cwd[len(home):]
    else:
        short_cwd = cwd

    return f"{user}@{host}:{short_cwd}$ "


def parse_command(line: str):
    """Разобрать строку ввода на команду и аргументы."""
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def cmd_ls(args):
    """Заглушка команды ls."""
    print(f"ls: args={args}")


def cmd_cd(args):
    """Заглушка команды cd."""
    print(f"cd: args={args}")


def cmd_exit(_args):
    """Завершить работу эмулятора."""
    print("Bye!")
    sys.exit(0)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}


def execute(command: str, args):
    """Выполнить команду с обработкой ошибок."""
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"{command}: command not found")
        return
    try:
        handler(args)
    except SystemExit:
        raise
    except Exception as exc:  
        print(f"{command}: error: {exc}")


def parse_args(argv=None):
    """Разобрать аргументы командной строки эмулятора.

    Args:
        argv: Список аргументов (по умолчанию — sys.argv[1:]).

    Returns:
        Объект с полями vfs и script.
    """
    parser = argparse.ArgumentParser(
        prog="shell-emulator",
        description="Эмулятор командной оболочки ОС (этап 2).",
    )
    parser.add_argument(
        "--vfs",
        default=None,
        help="Путь к физическому расположению VFS.",
    )
    parser.add_argument(
        "--script",
        default=None,
        help="Путь к стартовому скрипту для выполнения команд.",
    )
    return parser.parse_args(argv)


def dump_config(args):
    """Вывести отладочную информацию о параметрах запуска."""
    print("=== Shell emulator configuration ===")
    print(f"vfs    = {args.vfs!r}")
    print(f"script = {args.script!r}")
    print("====================================")


def run_script(path: str):
    """Выполнить стартовый скрипт с поддержкой комментариев.

    Каждая строка скрипта интерпретируется как команда эмулятора.
    Строки, начинающиеся с '#', игнорируются. Пустые строки также
    пропускаются. На экран выводится как ввод, так и вывод, имитируя
    диалог с пользователем.

    Args:
        path: Путь к файлу скрипта.
    """
    with open(path, encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.rstrip("\n")
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            print(f"{build_prompt()}{stripped}")

            command, args = parse_command(stripped)
            if command is None:
                continue

            try:
                execute(command, args)
            except SystemExit:
                return


def repl():
    """Основной цикл REPL."""
    while True:
        try:
            line = input(build_prompt())
        except (EOFError, KeyboardInterrupt):
            print()
            break
        command, args = parse_command(line)
        if command is None:
            continue
        execute(command, args)


def main(argv=None) -> int:
    """Точка входа эмулятора."""
    args = parse_args(argv)
    dump_config(args)

    if args.script:
        if not os.path.isfile(args.script):
            print(f"shell-emulator: script not found: {args.script}",
                  file=sys.stderr)
            return 1
        try:
            run_script(args.script)
        except OSError as exc:
            print(f"shell-emulator: script error: {exc}",
                  file=sys.stderr)
            return 1

    print("Shell emulator (stage 2). Type 'exit' to quit.")
    repl()
    return 0


if __name__ == "__main__":
    sys.exit(main())