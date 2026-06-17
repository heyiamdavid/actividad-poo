from Persona import Persona
#Clase Estudiante
class Estudiante(Persona):

    def __init__(self,nombre,telefono,email,identificacion,contrasena,promedio_ingreso,promedio_graduacion,estado,modalidad):

        super().__init__(nombre,telefono,email,identificacion,contrasena)

        self.promedio_ingreso = promedio_ingreso
        self.promedio_graduacion = promedio_graduacion
        self.estado = estado

        self.__modalidad = modalidad

        self.__cursos = []

    @property
    def modalidad(self):
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, nueva_modalidad):

        if nueva_modalidad.strip() != "":
            self.__modalidad = nueva_modalidad
        else:
            print("Modalidad inválida")

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):

        self.__cursos.append(curso)

        print(f"Curso {curso.nombreCurso} agregado")

    def consultar_cursos(self):

        print("\n========== CURSOS ==========")

        if len(self.__cursos) == 0:
            print("No existen cursos registrados")
            return

        for curso in self.__cursos:
            print(f"- {curso.nombreCurso}")

    def elegir_modalidad(self):

        print(f"Modalidad: {self.__modalidad}")

    def ver_notas(self):

        print("Visualizando notas registradas")


    def mostrar_datos(self):

        super().mostrar_datos()

        print(f"Promedio ingreso: {self.promedio_ingreso}")
        print(f"Promedio graduación: {self.promedio_graduacion}")
        print(f"Estado: {self.estado}")
        print(f"Modalidad: {self.__modalidad}")