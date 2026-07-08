# Módulos base de Python para crear Clases Abstractas (Interfaces)
from abc import ABC, abstractmethod

# typing para el tipado estático, mejorando la legibilidad y el autocompletado
from typing import TYPE_CHECKING, List, Optional, Tuple

# Previene bucles de importación circular en tiempo de ejecución
if TYPE_CHECKING:
    from Estudiante import Estudiante
    from Profesor import Profesor
    from Curso import Curso
    from Matricula import Matricula
    from Evaluacion import Evaluacion


# Interfaz (Clase Abstracta) que define el contrato para el acceso a datos.
# Cualquier clase que herede de RepositorioBase ESTÁ OBLIGADA a implementar estos métodos.
# Esto nos permite cambiar de base de datos en el futuro sin romper el código principal.
class RepositorioBase(ABC):

    # Método para inicializar tablas o colecciones en la base de datos
    @abstractmethod
    def crear_estructura(self) -> None:
        pass

    # ==========================================
    # CRUD Y GESTIÓN DE USUARIOS (ESTUDIANTES)
    # ==========================================
    
    # Registra un nuevo objeto Estudiante en la persistencia
    @abstractmethod
    def guardar_estudiante(self, estudiante: "Estudiante") -> None:
        pass

    # Registra un nuevo objeto Profesor
    @abstractmethod
    def guardar_profesor(self, profesor: "Profesor") -> None:
        pass

    # Búsqueda por clave primaria (identificación). Retorna el objeto o None si no existe.
    @abstractmethod
    def buscar_estudiante(self, identificacion: str) -> Optional["Estudiante"]:
        pass

    @abstractmethod
    def buscar_profesor(self, identificacion: str) -> Optional["Profesor"]:
        pass

    # Métodos de autenticación: Validan credenciales y devuelven la instancia del usuario
    @abstractmethod
    def validar_login_estudiante(self, identificacion: str,
                                 contrasena: str) -> Optional["Estudiante"]:
        pass

    @abstractmethod
    def validar_login_profesor(self, identificacion: str,
                                contrasena: str) -> Optional["Profesor"]:
        pass

    # Consultas generales que retornan colecciones completas de usuarios
    @abstractmethod
    def listar_estudiantes(self) -> List["Estudiante"]:
        pass

    @abstractmethod
    def listar_profesores(self) -> List["Profesor"]:
        pass

    # Eliminación de registros a través de su identificador único
    @abstractmethod
    def eliminar_estudiante(self, identificacion: str) -> None:
        pass

    @abstractmethod
    def eliminar_profesor(self, identificacion: str) -> None:
        pass

    # Métodos de agregación para métricas o reportes (COUNT)
    @abstractmethod
    def total_estudiantes(self) -> int:
        pass

    @abstractmethod
    def total_profesores(self) -> int:
        pass

    # ==========================================
    # GESTIÓN ACADÉMICA: CURSOS
    # ==========================================

    # Inserta un nuevo curso en la malla
    @abstractmethod
    def guardar_curso(self, curso: "Curso") -> None:
        pass

    # Filtro avanzado: Retorna cursos específicos según la carrera y el nivel
    @abstractmethod
    def listar_cursos_por_carrera_semestre(self, carrera: str,
                                           semestre: int) -> List["Curso"]:
        pass

    # Recupera un curso específico por su código
    @abstractmethod
    def buscar_curso(self, codigo_curso: str) -> Optional["Curso"]:
        pass

    # ==========================================
    # GESTIÓN DE MATRÍCULAS
    # ==========================================

    # Guarda el registro transaccional de una matrícula
    @abstractmethod
    def guardar_matricula(self, matricula: "Matricula") -> None:
        pass

    # Consulta el historial o estado de matrícula de un alumno específico
    @abstractmethod
    def listar_matricula_por_estudiante(
        self, identificacion_estudiante: str
    ) -> Optional["Matricula"]:
        pass

    # ==========================================
    # NOTAS / EVALUACIONES
    # ==========================================

    # Relaciona una calificación con un estudiante y una materia específica
    @abstractmethod
    def guardar_evaluacion(self, identificacion_estudiante: str, codigo_curso: str,
                           evaluacion: "Evaluacion") -> None:
        pass

    # Retorna el listado de calificaciones asociadas a un alumno
    @abstractmethod
    def listar_evaluaciones_por_estudiante(
        self, identificacion_estudiante: str
    ) -> List[Tuple[str, "Evaluacion"]]:
        pass

    # ==========================================
    # ESTRUCTURA ORGANIZACIONAL (INFRAESTRUCTURA)
    # ==========================================

    # CRUD para Sedes Físicas
    @abstractmethod
    def guardar_sede(self, sede) -> None:
        pass

    @abstractmethod
    def listar_sedes(self) -> List[Tuple]:
        pass

    @abstractmethod
    def eliminar_sede(self, nombre_sede: str) -> None:
        pass

    # CRUD para Facultades (Dependen de una sede)
    @abstractmethod
    def guardar_facultad(self, nombre_sede: str, facultad) -> None:
        pass

    @abstractmethod
    def listar_facultades(self) -> List[Tuple]:
        pass

    @abstractmethod
    def eliminar_facultad(self, id_facultad: int) -> None:
        pass

    # CRUD para Carreras (Dependen de una facultad)
    @abstractmethod
    def guardar_carrera(self, id_facultad: int, carrera) -> None:
        pass

    @abstractmethod
    def listar_carreras(self) -> List[Tuple]:
        pass

    @abstractmethod
    def eliminar_carrera(self, codigo_carrera: str) -> None:
        pass

    # ==========================================
    # SEGURIDAD Y ACTUALIZACIÓN DE DATOS
    # ==========================================

    # Métodos específicos para modificar credenciales de acceso
    @abstractmethod
    def actualizar_contrasena_estudiante(self, identificacion: str,
                                         nueva_contrasena: str) -> None:
        pass

    @abstractmethod
    def actualizar_contrasena_profesor(self, identificacion: str,
                                        nueva_contrasena: str) -> None:
        pass

    # Actualizan el estado general o los atributos mutables de los perfiles
    @abstractmethod
    def actualizar_estudiante(self, estudiante: "Estudiante") -> None:
        pass

    @abstractmethod
    def actualizar_profesor(self, profesor: "Profesor") -> None:
        pass
