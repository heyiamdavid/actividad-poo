from typing import TYPE_CHECKING, Dict, List, Optional

from BoletaNotas import BoletaNotas
from Horario import Horario
from Aula import Aula

if TYPE_CHECKING:
    from Profesor import Profesor
    from Estudiante import Estudiante


class Curso:

    def __init__(self, codigoCurso: str, nombreCurso: str, creditos: int,
                 carrera: Optional[str] = None, semestre: Optional[int] = None,
                 profesor: Optional["Profesor"] = None):

        self.codigoCurso: str = codigoCurso
        self.nombreCurso: str = nombreCurso
        self.__creditos: int = creditos

        # Agregación: el curso pertenece a una carrera y semestre
        self.carrera: Optional[str] = carrera
        self.semestre: Optional[int] = semestre

        # Agregación: el curso es impartido por un profesor
        self.profesor: Optional["Profesor"] = profesor

        # Composición
        self.__horarios: List[Horario] = []
        self.__aulas: List[Aula] = []

        # Composición: boleta de notas por estudiante (identificación -> BoletaNotas)
        self.__boletas: Dict[str, BoletaNotas] = {}

        # Agregación: estudiantes matriculados en este curso
        self.__estudiantes: List["Estudiante"] = []

    @property
    def creditos(self) -> int:
        return self.__creditos

    @creditos.setter
    def creditos(self, nuevos_creditos: int) -> None:

        if nuevos_creditos > 0:
            self.__creditos = nuevos_creditos
        else:
            print("Créditos inválidos")

    @property
    def horarios(self) -> List[Horario]:
        return self.__horarios

    @property
    def aulas(self) -> List[Aula]:
        return self.__aulas

    @property
    def boletas(self) -> Dict[str, BoletaNotas]:
        return self.__boletas

    def obtener_boleta(self, identificacion_estudiante: str) -> BoletaNotas:

        if identificacion_estudiante not in self.__boletas:
            self.__boletas[identificacion_estudiante] = BoletaNotas(
                identificacion_estudiante, self.codigoCurso
            )

        return self.__boletas[identificacion_estudiante]

    @property
    def estudiantes(self) -> List["Estudiante"]:
        return self.__estudiantes

    def matricular_estudiante(self, estudiante: "Estudiante") -> None:

        if estudiante in self.__estudiantes:
            return

        self.__estudiantes.append(estudiante)

    def total_estudiantes(self) -> int:

        return len(self.__estudiantes)

    def capacidad_maxima(self) -> Optional[int]:
        # Capacidad del aula asignada al curso. Si el curso todavía
        # no tiene aula asignada, no hay límite conocido (None).

        if len(self.__aulas) == 0:
            return None

        return self.__aulas[0].capacidad

    def tiene_cupo_disponible(self) -> bool:

        capacidad = self.capacidad_maxima()

        if capacidad is None:
            return True

        return self.total_estudiantes() < capacidad

    def agregar_horario(self, horario: Horario) -> None:

        self.__horarios.append(horario)

    def agregar_aula(self, aula: Aula) -> None:

        self.__aulas.append(aula)

    def asignar_horario_y_aula(self, horario: Horario, aula: Aula) -> None:

        self.agregar_horario(horario)
        self.agregar_aula(aula)

    def asignar_profesor(self, profesor: "Profesor") -> None:

        self.profesor = profesor

    def pertenece_a(self, carrera: str, semestre: int) -> bool:

        return self.carrera == carrera and self.semestre == semestre

    def choca_con(self, otro_curso: "Curso") -> bool:

        if self.codigoCurso == otro_curso.codigoCurso:
            return False
# Dos cursos no relacionados no pueden compartir la misma aula en el mismo horario de clases. 
        # Cursos iguales (mismo código) no se consideran choque entre sí.
        
        for horario in self.__horarios:
            for aula in self.__aulas:
                for otro_horario in otro_curso.horarios:
                    for otra_aula in otro_curso.aulas:
                        if (
                            horario.coincide_con(otro_horario)
                            and aula.es_la_misma(otra_aula)
                        ):
                            return True

        return False

    def descripcion_semestre(self) -> str:

        if self.semestre == 0:
            return "Nivelación"

        return str(self.semestre)

    def mostrar_curso(self) -> None:

        print("CURSO")
        print(f"Código: {self.codigoCurso}")
        print(f"Nombre: {self.nombreCurso}")
        print(f"Créditos: {self.__creditos}")
        print(f"Carrera: {self.carrera}")
        print(f"Semestre: {self.descripcion_semestre()}")
        print(f"Estudiantes matriculados: {self.total_estudiantes()}")

        if self.profesor:
            print(f"Profesor: {self.profesor.nombre}")

        self.mostrar_horarios()
        self.mostrar_aulas()

    def mostrar_resumen(self) -> None:

        nombre_profesor = self.profesor.nombre if self.profesor else "Sin asignar"

        print(
            f"- [{self.codigoCurso}] {self.nombreCurso} "
            f"| Profesor: {nombre_profesor} "
            f"| Estudiantes: {self.total_estudiantes()}"
        )

    def mostrar_horarios(self) -> None:

        print("Horarios:")

        if len(self.__horarios) == 0:
            print("No existen horarios")
            return

        for horario in self.__horarios:
            horario.mostrar_horario()

    def mostrar_aulas(self) -> None:

        print("\nAulas:")

        if len(self.__aulas) == 0:
            print("No existen aulas")
            return

        for aula in self.__aulas:
            aula.mostrar_aula()
