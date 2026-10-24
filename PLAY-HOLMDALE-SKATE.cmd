@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\open-pharmacie-skate.ps1" -Location Holmdale
if errorlevel 1 pause
