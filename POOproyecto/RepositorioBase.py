from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from Estudiante import Estudiante
    from Profesor import Profesor
    from Curso import Curso
    from Matricula import Matricula
    from Evaluacion import Evaluacion


class RepositorioBase(ABC):

    @abstractmethod
    def crear_estructura(self) -> None:
        pass

    @abstractmethod
    def guardar_estudiante(self, estudiante: "Estudiante") -> None:
        pass

    @abstractmethod
    def guardar_profesor(self, profesor: "Profesor") -> None:
        pass

    @abstractmethod
    def buscar_estudiante(self, identificacion: str) -> Optional["Estudiante"]:
        pass

    @abstractmethod
    def buscar_profesor(self, identificacion: str) -> Optional["Profesor"]:
        pass

    @abstractmethod
    def validar_login_estudiante(self, identificacion: str,
                                  contrasena: str) -> Optional["Estudiante"]:
        pass

    @abstractmethod
    def validar_login_profesor(self, identificacion: str,
                                contrasena: str) -> Optional["Profesor"]:
        pass

    @abstractmethod
    def listar_estudiantes(self) -> List["Estudiante"]:
        pass

    @abstractmethod
    def listar_profesores(self) -> List["Profesor"]:
        pass

    @abstractmethod
    def eliminar_estudiante(self, identificacion: str) -> None:
        pass

    @abstractmethod
    def eliminar_profesor(self, identificacion: str) -> None:
        pass

    @abstractmethod
    def total_estudiantes(self) -> int:
        pass

    @abstractmethod
    def total_profesores(self) -> int:
        pass

    # CURSOS

    @abstractmethod
    def guardar_curso(self, curso: "Curso") -> None:
        pass

    @abstractmethod
    def listar_cursos_por_carrera_semestre(self, carrera: str,
                                            semestre: int) -> List["Curso"]:
        pass

    @abstractmethod
    def buscar_curso(self, codigo_curso: str) -> Optional["Curso"]:
        pass

    # MATRÍCULA

    @abstractmethod
    def guardar_matricula(self, matricula: "Matricula") -> None:
        pass

    @abstractmethod
    def listar_matricula_por_estudiante(
        self, identificacion_estudiante: str
    ) -> Optional["Matricula"]:
        pass

    # NOTAS / EVALUACIONES

    @abstractmethod
    def guardar_evaluacion(self, identificacion_estudiante: str, codigo_curso: str,
                            evaluacion: "Evaluacion") -> None:
        pass

    @abstractmethod
    def listar_evaluaciones_por_estudiante(
        self, identificacion_estudiante: str
    ) -> List[Tuple[str, "Evaluacion"]]:
        pass

    # ESTRUCTURA ORGANIZACIONAL

    @abstractmethod
    def guardar_sede(self, sede) -> None:
        pass

    @abstractmethod
    def listar_sedes(self) -> List[Tuple]:
        pass

    @abstractmethod
    def eliminar_sede(self, nombre_sede: str) -> None:
        pass

    @abstractmethod
    def guardar_facultad(self, nombre_sede: str, facultad) -> None:
        pass

    @abstractmethod
    def listar_facultades(self) -> List[Tuple]:
        pass

    @abstractmethod
    def eliminar_facultad(self, id_facultad: int) -> None:
        pass

    @abstractmethod
    def guardar_carrera(self, id_facultad: int, carrera) -> None:
        pass

    @abstractmethod
    def listar_carreras(self) -> List[Tuple]:
        pass

    @abstractmethod
    def eliminar_carrera(self, codigo_carrera: str) -> None:
        pass

    # CONTRASEÑAS

    @abstractmethod
    def actualizar_contrasena_estudiante(self, identificacion: str,
                                          nueva_contrasena: str) -> None:
        pass

    @abstractmethod
    def actualizar_contrasena_profesor(self, identificacion: str,
                                        nueva_contrasena: str) -> None:
        pass

    # ACTUALIZACIÓN DE DATOS

    @abstractmethod
    def actualizar_estudiante(self, estudiante: "Estudiante") -> None:
        pass

    @abstractmethod
    def actualizar_profesor(self, profesor: "Profesor") -> None:
        pass
