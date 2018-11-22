@echo off
REG ADD    "\\.\HKEY_CURRENT_USER\Console\%SystemRoot%_System32_cmd.exe" /v WindowPosition /t REG_DWORD /d 0
