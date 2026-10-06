@echo off
REM Запуск эмулятора со всеми параметрами: VFS и скрипт.
python "%~dp0..\src\shell_emulator.py" ^
    --vfs "%~dp0..\vfs" ^
    --script "%~dp0startup.cmds"