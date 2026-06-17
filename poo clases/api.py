from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from RepositorioSupabase import RepositorioSupabase

app = FastAPI(title="Sistema Universitario con Supabase", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo_supabase = RepositorioSupabase()

class LoginRequest(BaseModel):
    identificacion: str
    contrasena: str

@app.get("/")
def root():
    return {"message": "API del Sistema Universitario conectada a Supabase"}

@app.post("/api/login")
def login(request: LoginRequest):
    # En Supabase la contraseña idealmente debería estar hasheada.
    # Por simplicidad ahora lo validamos directo.
    usuario = repo_supabase.validar_login(request.identificacion, request.contrasena)
    if usuario:
        # usuario es un dict devuelto por Supabase
        return {
            "status": "success",
            "data": {
                "id": usuario.get("id"),
                "nombre": usuario.get("nombre"),
                "rol": usuario.get("rol")
            }
        }
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.get("/api/admin/estadisticas")
def estadisticas_admin():
    total_estudiantes = repo_supabase.total_estudiantes()
    total_profesores = repo_supabase.total_profesores()
    return {
        "status": "success",
        "data": {
            "total_estudiantes": total_estudiantes,
            "total_profesores": total_profesores,
            "total_cursos": 0 # TODO: Implementar conteo de cursos en Supabase
        }
    }
