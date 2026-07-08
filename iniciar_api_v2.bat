@echo off
echo Iniciando servidor Backend en Python (FastAPI) usando api_v2.py en POOproyecto...
cd "POOproyecto"
python -m uvicorn api_v2:app --host 0.0.0.0 --port 8000 --reload
pause
