@echo off
:loop
if exist "D:\001DIY\005lib\01AIcadence\ai_bridge\exchange\command.flag" echo RUN
ping -n 1 -w 250 198.51.100.254 >nul
goto loop
