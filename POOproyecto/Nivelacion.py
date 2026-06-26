from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Curso import Curso


class Nivelacion:
    # Representa el periodo de nivelación de un estudiante. El curso
    # de nivelación en sí es un Curso normal (código "NIV-<CARRERA>",
    # nombre "Nivelación <Carrera>"), ya predefinido en la carrera;
    # esta clase solo guarda el periodo y duración administrativos.

    def __init__(self, periodo: str, duracion: int,
                 curso_nivelacion: Optional["Curso"] = None):

        self.periodo: str = periodo
        self.__duracion: int = duracion

        # Agregación: el curso de nivelación real, donde se registran
        # las evaluaciones del estudiante.
        self.curso_nivelacion: Optional["Curso"] = curso_nivelacion

    @property
    def duracion(self) -> int:
        return self.__duracion

    @duracion.setter
    def duracion(self, nueva_duracion: int) -> None:

        if nueva_duracion > 0:
            self.__duracion = nueva_duracion
        else:
            print("Duración inválida")

    def mostrar_nivelacion(self) -> None:

        print("\n========== NIVELACIÓN ==========")
        print(f"Periodo: {self.periodo}")
        print(f"Duración: {self.__duracion} meses")

        if self.curso_nivelacion:
            print(f"Curso: {self.curso_nivelacion.nombreCurso}")
        else:
            print("Curso: no asignado")
