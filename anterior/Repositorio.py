import json
import os
from datetime import datetime


class Repositorio:
    """
    Clase de persistencia en archivos JSON.
    Prepara la estructura de datos lista para migrar a PostgreSQL.
    """

    BASE_DIR = "data"

    def __init__(self, nombre_coleccion: str):
        self.nombre_coleccion = nombre_coleccion
        self.filepath = os.path.join(self.BASE_DIR, f"{nombre_coleccion}.json")
        self._asegurar_directorio()

    def _asegurar_directorio(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)

    def _cargar(self) -> list:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, datos: list):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

    def guardar(self, registro: dict) -> dict:
        """Inserta un nuevo registro. Añade id y timestamp automáticamente."""
        datos = self._cargar()
        registro["id"] = len(datos) + 1
        registro["creado_en"] = datetime.now().isoformat()
        datos.append(registro)
        self._guardar(datos)
        return registro

    def obtener_todos(self) -> list:
        """Retorna todos los registros de la colección."""
        return self._cargar()

    def obtener_por_id(self, id: int) -> dict | None:
        """Busca un registro por su ID."""
        for registro in self._cargar():
            if registro.get("id") == id:
                return registro
        return None

    def eliminar_por_id(self, id: int) -> bool:
        """Elimina un registro por su ID."""
        datos = self._cargar()
        nuevos = [r for r in datos if r.get("id") != id]
        if len(nuevos) == len(datos):
            return False  # No se encontró
        self._guardar(nuevos)
        return True

    def total(self) -> int:
        """Cuenta los registros de la colección."""
        return len(self._cargar())


# --- Repositorios específicos del dominio universitario ---

class RepositorioMatriculas(Repositorio):
    def __init__(self):
        super().__init__("matriculas")

class RepositorioEstudiantes(Repositorio):
    def __init__(self):
        super().__init__("estudiantes")

class RepositorioProfesores(Repositorio):
    def __init__(self):
        super().__init__("profesores")
