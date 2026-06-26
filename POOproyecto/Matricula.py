from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from Curso import Curso
    from Estudiante import Estudiante


class Matricula:

    # Constructor
    def __init__(self,
                 fecha: str,
                 estudiante: Optional["Estudiante"] = None):
        self.fecha: str = fecha
        self.estudiante: Optional["Estudiante"] = estudiante

#       Encapsulación
        self.__cursos: List["Curso"] = []

    @property
    def cursos(self) -> List["Curso"]:
        return self.__cursos

    def ya_tiene_curso(self, codigo_curso: str) -> bool:

        return any(
            curso.codigoCurso == codigo_curso
            for curso in self.__cursos
        )

    def agregar_curso(self, curso: "Curso") -> None:

        if self.ya_tiene_curso(curso.codigoCurso):
            print(f"El curso {curso.nombreCurso} ya está matriculado")
            return

        self.__cursos.append(curso)

        if self.estudiante:
            self.estudiante.agregar_curso(curso)
            curso.matricular_estudiante(self.estudiante)

    def mostrar_matricula(self) -> None:

        print("\n========== MATRÍCULA ==========")
        print(f"Fecha: {self.fecha}")

        if self.estudiante:
            print(
                f"Estudiante: "
                f"{self.estudiante.nombre}"
            )

        print("\nCursos:")

        if len(self.__cursos) == 0:
            print("No existen cursos")
            return

        for curso in self.__cursos:

            print(
                f"- {curso.nombreCurso}"
            )

    def generar_comprobante(
            self,
            formato: str = "PDF") -> None:

        print(
            f"\nComprobante generado "
            f"en formato {formato}"
        )