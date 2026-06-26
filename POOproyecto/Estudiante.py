from typing import TYPE_CHECKING, List, Optional

from Persona import Persona

if TYPE_CHECKING:
    from Curso import Curso
    from Matricula import Matricula
    from BoletaNotas import BoletaNotas


#Clase Estudiante
class Estudiante(Persona):

    def __init__(self, nombre: str, telefono: str, email: str, identificacion: str,
                 contrasena: str, promedio_ingreso: float, promedio_graduacion: float,
                 estado: str, modalidad: str,
                 carrera: Optional[str] = None, semestre: Optional[int] = None):

        super().__init__(nombre, telefono, email, identificacion, contrasena)

        self.promedio_ingreso: float = promedio_ingreso
        self.promedio_graduacion: float = promedio_graduacion
        self.estado: str = estado

        self.__modalidad: str = modalidad

        # Agregación: a qué carrera y semestre pertenece el estudiante
        self.carrera: Optional[str] = carrera
        self.semestre: Optional[int] = semestre

        # Composición: cursos en los que está matriculado actualmente
        self.__cursos: List["Curso"] = []

        # Composición: matrícula propia del estudiante
        self.__matricula: Optional["Matricula"] = None

        # Indica si el estudiante todavía está en su periodo de
        # nivelación de ingreso. Una vez que pasa a semestre 1, esta
        # bandera queda en False para siempre: ya no vuelve a pasar
        # por la lógica especial de nivelación, sin importar sus
        # notas futuras en cursos regulares.
        self.en_nivelacion: bool = False

    @property
    def modalidad(self) -> str:
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, nueva_modalidad: str) -> None:

        if nueva_modalidad.strip() != "":
            self.__modalidad = nueva_modalidad
        else:
            print("Modalidad inválida")

    @property
    def cursos(self) -> List["Curso"]:
        return self.__cursos

    @property
    def matricula(self) -> Optional["Matricula"]:
        return self.__matricula

    @matricula.setter
    def matricula(self, nueva_matricula: "Matricula") -> None:
        self.__matricula = nueva_matricula

    def esta_activo(self) -> bool:
        return self.estado == "Activo"

    def agregar_curso(self, curso: "Curso") -> None:

        if curso not in self.__cursos:
            self.__cursos.append(curso)
            print(f"Curso {curso.nombreCurso} agregado")

    def boleta_de_curso(self, codigo_curso: str) -> Optional["BoletaNotas"]:

        for curso in self.__cursos:
            if curso.codigoCurso == codigo_curso:
                return curso.obtener_boleta(self.identificacion)

        return None

    def promedio_de_curso(self, codigo_curso: str) -> Optional[float]:

        boleta = self.boleta_de_curso(codigo_curso)

        if boleta is None:
            return None

        return boleta.calcular_promedio()

    def consultar_cursos_y_horarios(self) -> None:

        print("\n========== CURSOS Y HORARIOS ==========")

        if len(self.__cursos) == 0:
            print("No existen cursos registrados")
            return

        for curso in self.__cursos:
            curso.mostrar_curso()
            print("-----------------------------------")

    def elegir_modalidad(self) -> None:

        print(f"Modalidad: {self.__modalidad}")

    def ver_notas(self) -> None:

        print("\n========== NOTAS ==========")

        if len(self.__cursos) == 0:
            print("No existen notas registradas")
            return

        for curso in self.__cursos:

            boleta = curso.obtener_boleta(self.identificacion)
            boleta.mostrar_boleta()

    def ver_matricula(self) -> None:

        if self.__matricula is None:
            print("\nNo existe una matrícula registrada")
            return

        self.__matricula.mostrar_matricula()
        print(f"Modalidad: {self.__modalidad}")

    def mostrar_datos(self) -> None:

        super().mostrar_datos()

        print(f"Promedio ingreso: {self.promedio_ingreso}")
        print(f"Promedio graduación: {self.promedio_graduacion}")
        print(f"Estado: {self.estado}")
        print(f"Modalidad: {self.__modalidad}")
        print(f"Carrera: {self.carrera}")
        print(f"Semestre: {self.semestre}")

    def mostrar_datos_administrativos(self) -> None:
        # Vista exclusiva del Administrador: incluye las claves.
        # Nunca se debe invocar desde el propio menú del estudiante.

        self.mostrar_datos()
        print(f"Clave temporal: {self.clave_temporal}")
        print(f"Clave actual: {self.contrasena}")