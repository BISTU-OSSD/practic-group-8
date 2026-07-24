@echo off
chcp 65001 >nul
:: 两种方案自动适配，优先系统py命令，不行再走完整路径
py main.py || "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" main.py
pause