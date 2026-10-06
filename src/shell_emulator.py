"""Эмулятор командной оболочки ОС. Этап 1: REPL.

Реализует минимальный прототип: приглашение на основе данных ОС,
простой парсер, команды-заглушки ls и cd, команда exit.
"""

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
    """Разобрать строку ввода на команду и аргументы.

    Args:
        line: Строка, введённая пользователем.

    Returns:
        Кортеж (command, args). Если строка пустая — (None, []).
    """
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def cmd_ls(args):
    """Заглушка команды ls: выводит своё имя и аргументы."""
    print(f"ls: args={args}")


def cmd_cd(args):
    """Заглушка команды cd: выводит своё имя и аргументы."""
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
    """Выполнить команду с обработкой ошибок.

    Args:
        command: Имя команды.
        args: Список аргументов.
    """
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"{command}: command not found")
        return
    try:
        handler(args)
    except Exception as exc:  # noqa: BLE001
        print(f"{command}: error: {exc}")


def repl():
    """Основной цикл REPL: чтение — разбор — выполнение."""
    print("Shell emulator (stage 1). Type 'exit' to quit.")
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


if __name__ == "__main__":
    repl()