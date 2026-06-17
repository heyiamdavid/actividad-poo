import os
from dotenv import load_dotenv
from supabase import create_client, Client
from RepositorioBase import RepositorioBase

class RepositorioSupabase(RepositorioBase):
    def __init__(self):
        load_dotenv()
        url = os.environ.get("SUPABASE_URL")
        # Usamos la clave secreta en el backend para evitar RLS
        key = os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get("SUPABASE_KEY")
        if not url or not key:
            print("ADVERTENCIA: SUPABASE_URL o SUPABASE_SECRET_KEY no están configuradas en el archivo .env")
        self.supabase: Client = create_client(url, key)

    def crear_estructura(self):
        pass

    def guardar_estudiante(self, estudiante):
        try:
            data, count = self.supabase.table('usuarios').insert({
                "nombre": estudiante.nombre,
                "telefono": estudiante.telefono,
                "email": estudiante.email,
                "identificacion": estudiante.identificacion,
                "contrasena": estudiante.contrasena,
                "promedio_ingreso": estudiante.promedio_ingreso,
                "promedio_graduacion": estudiante.promedio_graduacion,
                "estado": estudiante.estado,
                "modalidad": estudiante.modalidad,
                "rol": "estudiante"
            }).execute()
            print("Estudiante guardado correctamente en Supabase")
        except Exception as e:
            print(f"Error al guardar estudiante: {e}")

    def guardar_profesor(self, profesor):
        try:
            data, count = self.supabase.table('usuarios').insert({
                "nombre": profesor.nombre,
                "telefono": profesor.telefono,
                "email": profesor.email,
                "identificacion": profesor.identificacion,
                "contrasena": profesor.contrasena,
                "materia": profesor.materia,
                "titulo": profesor.titulo,
                "rol": "profesor"
            }).execute()
            print("Profesor guardado correctamente en Supabase")
        except Exception as e:
            print(f"Error al guardar profesor: {e}")

    def buscar_estudiante(self, identificacion):
        response = self.supabase.table('usuarios').select("*").eq("identificacion", identificacion).eq("rol", "estudiante").execute()
        if response.data:
            return response.data[0]
        return None

    def buscar_profesor(self, identificacion):
        response = self.supabase.table('usuarios').select("*").eq("identificacion", identificacion).eq("rol", "profesor").execute()
        if response.data:
            return response.data[0]
        return None

    def validar_login(self, identificacion, contrasena):
        response = self.supabase.table('usuarios').select("*").eq("identificacion", identificacion).eq("contrasena", contrasena).execute()
        if response.data:
            return response.data[0]
        return None

    def validar_login_estudiante(self, identificacion, contrasena):
        return self.validar_login(identificacion, contrasena)

    def validar_login_profesor(self, identificacion, contrasena):
        return self.validar_login(identificacion, contrasena)

    def listar_estudiantes(self):
        response = self.supabase.table('usuarios').select("*").eq("rol", "estudiante").execute()
        return response.data

    def listar_profesores(self):
        response = self.supabase.table('usuarios').select("*").eq("rol", "profesor").execute()
        return response.data

    def eliminar_estudiante(self, identificacion):
        self.supabase.table('usuarios').delete().eq("identificacion", identificacion).eq("rol", "estudiante").execute()

    def eliminar_profesor(self, identificacion):
        self.supabase.table('usuarios').delete().eq("identificacion", identificacion).eq("rol", "profesor").execute()

    def total_estudiantes(self):
        # Para conteos exactos en Supabase
        response = self.supabase.table('usuarios').select("id", count="exact").eq("rol", "estudiante").execute()
        return response.count if response.count else 0

    def total_profesores(self):
        response = self.supabase.table('usuarios').select("id", count="exact").eq("rol", "profesor").execute()
        return response.count if response.count else 0
