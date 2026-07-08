from typing import TYPE_CHECKING, List, Optional

# Evita dependencias circulares durante la evaluación estática de tipos
if TYPE_CHECKING:
    from Curso import Curso
    from Estudiante import Estudiante


# Clase Matricula: Actúa como una entidad transaccional que documenta 
# y resuelve la relación entre un Estudiante y múltiples Cursos.
class Matricula:

    # Constructor de la transacción
    # Utiliza Optional de la librería typing para indicar que el estudiante 
    # puede ser inyectado al momento de crear la matrícula o posteriormente.
    def __init__(self,
                 fecha: str,
                 estudiante: Optional["Estudiante"] = None):
        self.fecha: str = fecha
        self.estudiante: Optional["Estudiante"] = estudiante

        # Encapsulación: Lista privada para aislar los cursos de esta transacción
        # de posibles modificaciones externas no autorizadas.
        self.__cursos: List["Curso"] = []

    # Propiedad de solo lectura (Getter) para acceder a los cursos
    @property
    def cursos(self) -> List["Curso"]:
        return self.__cursos

    # Validación optimizada utilizando una expresión generadora (generator expression)
    # y la función any(). Esto consume mucha menos memoria que un bucle for tradicional.
    def ya_tiene_curso(self, codigo_curso: str) -> bool:
        return any(
            curso.codigoCurso == codigo_curso
            for curso in self.__cursos
        )

    # Método complejo que gestiona la inserción de datos y la integridad referencial
    def agregar_curso(self, curso: "Curso") -> None:

        # Guard clause: Aborta la operación inmediatamente si detecta un duplicado
        if self.ya_tiene_curso(curso.codigoCurso):
            print(f"El curso {curso.nombreCurso} ya está matriculado")
            return

        # Agrega el objeto curso a la lista privada de la transacción
        self.__cursos.append(curso)

        # Sincronización bidireccional: Si existe un estudiante asociado, 
        # actualiza las referencias cruzadas en todos los objetos involucrados 
        # para mantener la coherencia del sistema en memoria.
        if self.estudiante:
            self.estudiante.agregar_curso(curso)
            curso.matricular_estudiante(self.estudiante)

    # Método de visualización para generar un reporte del estado de la transacción
    def mostrar_matricula(self) -> None:

        print("\n========== MATRÍCULA ==========")
        print(f"Fecha: {self.fecha}")

        # Comprueba si el objeto opcional 'estudiante' ya fue instanciado
        if self.estudiante:
            print(
                f"Estudiante: "
                f"{self.estudiante.nombre}"
            )

        print("\nCursos:")

        # Validación visual para transacciones en blanco
        if len(self.__cursos) == 0:
            print("No existen cursos")
            return

        # Despliegue iterativo de la malla de cursos asociados a la matrícula
        for curso in self.__cursos:
            print(
                f"- {curso.nombreCurso}"
            )

    # Simulación de un proceso de exportación de datos con un parámetro por defecto
    def generar_comprobante(
            self,
            formato: str = "PDF") -> None:

        print(
            f"\nComprobante generado "
            f"en formato {formato}"
        )
