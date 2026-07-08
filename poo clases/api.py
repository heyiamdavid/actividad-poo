from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from RepositorioSQLite import RepositorioSQLite

app = FastAPI(title="Sistema Universitario con SQLite", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo_sqlite = RepositorioSQLite()

class LoginRequest(BaseModel):
    identificacion: str
    contrasena: str

@app.get("/")
def root():
    return {"message": "API del Sistema Universitario conectada a SQLite"}

@app.post("/api/login")
def login(request: LoginRequest):
    # Verificar si es el administrador (credenciales de Administrador.py)
    if request.identificacion == "12346776" and request.contrasena == "Sigma67":
        return {
            "status": "success",
            "data": {
                "id": 0,
                "nombre": "Administrador",
                "rol": "admin"
            }
        }
    

    # Si no es admin, intentar como estudiante
    usuario = repo_sqlite.validar_login_estudiante(request.identificacion, request.contrasena)
    rol = "estudiante"
    
    if not usuario:
        usuario = repo_sqlite.validar_login_profesor(request.identificacion, request.contrasena)
        rol = "profesor"

    if usuario:
        # usuario es una tupla en SQLite: (id, nombre, telefono, email, identificacion, contrasena, ...)
        return {
            "status": "success",
            "data": {
                "id": usuario[0],
                "nombre": usuario[1],
                "rol": rol
            }
        }
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.get("/api/admin/estadisticas")
def estadisticas_admin():
    total_estudiantes = repo_sqlite.total_estudiantes()
    total_profesores = repo_sqlite.total_profesores()
    return {
        "status": "success",
        "data": {
            "total_estudiantes": total_estudiantes,
            "total_profesores": total_profesores,
            "total_cursos": 0 # TODO: Implementar conteo de cursos en SQLite
        }
    }
