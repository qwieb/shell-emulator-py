@echo off
REM Запуск эмулятора со стартовым скриптом.
python "%~dp0..\src\shell_emulator.py" ^
    --script "%~dp0startup.cmds"