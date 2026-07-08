# Clase que representa una carrera universitaria
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from Curso import Curso
    from Estudiante import Estudiante
    from Nivelacion import Nivelacion


class Carrera:

    def __init__(self,
                 codigoCarrera: str,
                 nombreCarrera: str,
                 modalidad: str):

        self.codigoCarrera: str = codigoCarrera
        self.nombreCarrera: str = nombreCarrera

        self.__modalidad: str = modalidad

        # Agregación
        self.__estudiantes: List["Estudiante"] = []

        # Composición
        self.__nivelaciones: List["Nivelacion"] = []

        # Composición: malla de cursos de la carrera
        self.__cursos: List["Curso"] = []

    # ENCAPSULAMIENTO
    @property
    def modalidad(self) -> str:
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, nueva_modalidad: str) -> None:

        if nueva_modalidad.strip() != "":
            self.__modalidad = nueva_modalidad

    @property
    def estudiantes(self) -> List["Estudiante"]:
        return self.__estudiantes

    @property
    def nivelaciones(self) -> List["Nivelacion"]:
        return self.__nivelaciones

    @property
    def cursos(self) -> List["Curso"]:
        return self.__cursos

    def agregar_curso(self, curso: "Curso") -> bool:

        if self.buscar_curso(curso.codigoCurso):
            print(f"Ya hay un curso existente con el código {curso.codigoCurso}")
            return False

        for curso_existente in self.__cursos:
            if curso_existente.choca_con(curso):
                print(
                    f"Error: El horario y aula de {curso.nombreCurso} "
                    f"chocan con el curso {curso_existente.nombreCurso}"
                )
                return False

        self.__cursos.append(curso)
        return True

    def buscar_curso(self, codigo_curso: str) -> Optional["Curso"]:

        for curso in self.__cursos:
            if curso.codigoCurso.lower() == codigo_curso.lower():
                return curso

        return None

    def eliminar_curso(self, codigo_curso: str) -> bool:

        curso = self.buscar_curso(codigo_curso)

        if curso is None:
            return False

        self.__cursos.remove(curso)
        return True

    def cursos_por_semestre(self, semestre: int) -> List["Curso"]:

        return [
            curso for curso in self.__cursos
            if curso.semestre == semestre
        ]

    def semestres_disponibles(self) -> List[int]:

        semestres = sorted(set(curso.semestre for curso in self.__cursos))
        return semestres

    def tiene_semestre(self, semestre: int) -> bool:

        return semestre in self.semestres_disponibles()

    def curso_de_nivelacion(self) -> Optional["Curso"]:
        # El curso de nivelación de la carrera se identifica por
        # estar en el semestre 0, sin importar qué código le haya
        # puesto el administrador al crearlo (no se asume el patrón
        # "NIV-<CODIGO_CARRERA>", ya que las materias de nivelación
        # creadas manualmente pueden tener cualquier código).
        cursos_nivelacion = self.cursos_por_semestre(0)

        if len(cursos_nivelacion) == 0:
            return None

        return cursos_nivelacion[0]

    def agregar_estudiante(self, estudiante: "Estudiante") -> None:

        self.__estudiantes.append(estudiante)

    def buscar_estudiante(self, identificacion: str) -> Optional["Estudiante"]:

        for estudiante in self.__estudiantes:
            if estudiante.identificacion == identificacion:
                return estudiante

        return None

    def eliminar_estudiante(self, identificacion: str) -> bool:

        estudiante = self.buscar_estudiante(identificacion)

        if estudiante is None:
            return False

        self.__estudiantes.remove(estudiante)
        return True

    def agregar_nivelacion(self, nivelacion: "Nivelacion") -> None:

        self.__nivelaciones.append(nivelacion)

    def mostrar_carrera(self) -> None:

        print(" CARRERA ")
        print(f"Código: {self.codigoCarrera}")
        print(f"Nombre: {self.nombreCarrera}")
        print(f"Modalidad: {self.__modalidad}")
        print()

    def mostrar_carrera_con_materias(self) -> None:

        self.mostrar_carrera()

        if len(self.__cursos) == 0:
            print("Materias: no existen materias registradas")
            return

        print("Materias:")

        for curso in sorted(self.__cursos, key=lambda c: c.semestre):

            nombre_profesor = curso.profesor.nombre if curso.profesor else "Sin asignar"

            print(
                f"  - [{curso.codigoCurso}] {curso.nombreCurso} "
                f"(Semestre {curso.descripcion_semestre()}, Profesor: {nombre_profesor})"
            )

            for horario in curso.horarios:
                print(f"      Horario: {horario.dia} {horario.hora_inicio}-{horario.hora_fin}")

            for aula in curso.aulas:
                print(f"      Aula: {aula.numeroAula} (Capacidad: {aula.capacidad})")

    def listar_estudiantes(self) -> None:

        print(f"ESTUDIANTES DE: {self.nombreCarrera}")

        if len(self.__estudiantes) == 0:
            print("No existen estudiantes")
            return

        for estudiante in self.__estudiantes:

            print(f"- {estudiante.nombre}")

    def tiene_nivelacion(self) -> bool:

        return len(self.__nivelaciones) > 0
