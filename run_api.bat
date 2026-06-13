@echo off
echo Iniciando servidor Backend en Python (FastAPI)...
python -m uvicorn api:app --reload
pause
