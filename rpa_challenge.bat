@echo off
cd /d "C:\Users\Shadow\Documents\Projets\RPAaas\code_source\rpaaas-robots"
if not exist logs mkdir logs
C:\Users\Shadow\AppData\Local\Programs\Python\Python311\python.exe robots\robot_rpa_challenge\processes\main.py >> logs\execution.log 2>&1
pause