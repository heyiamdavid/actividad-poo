from typing import TYPE_CHECKING, List

from Persona import Persona

if TYPE_CHECKING:
    from Curso import Curso
    from Estudiante import Estudiante
    from BoletaNotas import BoletaNotas

#Clase Profesor
class Profesor(Persona):

    def __init__(self, nombre: str, telefono: str, email: str, identificacion: str,
                 contrasena: str, titulo: str, materia: str = ""):

        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

        # La materia se mantiene en el modelo, pero ya no se solicita
        # en el formulario de registro (puede asignarse más adelante).
        self.materia: str = materia
        self.titulo: str = titulo

        self.__cursos: List["Curso"] = []

    @property
    def cursos(self) -> List["Curso"]:
        return self.__cursos

    def asignar_curso(self, curso: "Curso") -> None:

        self.__cursos.append(curso)
        curso.asignar_profesor(self)

    def registrar_nota_en_boleta(self, curso: "Curso", estudiante: "Estudiante",
                                  nombre_evaluacion: str, calificacion: float) -> "BoletaNotas":

        boleta = curso.obtener_boleta(estudiante.identificacion)
        registrado = boleta.registrar_nota(nombre_evaluacion, calificacion)

        if registrado:
            print(f"\nNota de {nombre_evaluacion} registrada correctamente.")

        return boleta

    def listar_estudiantes_del_curso(self, curso: "Curso") -> None:

        print(f"\n===== ESTUDIANTES DE {curso.nombreCurso} =====")

        if curso.total_estudiantes() == 0:

            print("No existen estudiantes matriculados en este curso.")
            return

        for estudiante in curso.estudiantes:
            print(
                f"- {estudiante.nombre} "
                f"(Identificación: {estudiante.identificacion}, "
                f"Semestre: {estudiante.semestre})"
            )

    def mostrar_cursos(self) -> None:

        if len(self.__cursos) == 0:

            print("\nNo existen cursos asignados.")
            return

        print("\n===== CURSOS =====")

        for curso in self.__cursos:
            curso.mostrar_curso()

    def mostrar_evaluaciones(self) -> None:

        if len(self.__cursos) == 0:

            print("\nNo existen cursos asignados.")
            return

        print("\n===== EVALUACIONES =====")

        hay_boletas = False

        for curso in self.__cursos:

            if len(curso.boletas) == 0:
                continue

            hay_boletas = True
            print(f"\nCurso: {curso.nombreCurso}")

            for boleta in curso.boletas.values():
                boleta.mostrar_boleta()

        if not hay_boletas:
            print("No existen evaluaciones registradas.")

    def mostrar_datos(self) -> None:

        print("\n========== DATOS PROFESOR ==========")

        print("Nombre:", self.nombre)
        print("Teléfono:", self.telefono)
        print("Email:", self.email)
        print("Identificación:", self.identificacion)
        print("Título:", self.titulo)

        if self.materia:
            print("Materia:", self.materia)

    def mostrar_datos_administrativos(self) -> None:
        # Vista exclusiva del Administrador: incluye las claves.
        # Nunca se debe invocar desde el propio menú del profesor.

        self.mostrar_datos()
        print(f"Clave temporal: {self.clave_temporal}")
        print(f"Clave actual: {self.contrasena}")
