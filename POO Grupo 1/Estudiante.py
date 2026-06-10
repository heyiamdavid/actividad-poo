from Persona import Persona

class Estudiante(Persona):

    def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena,
                 promedio_ingreso,
                 promedio_graduacion,
                 estado,
                 modalidad):

        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

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

        if nueva_modalidad != "":
            self.__modalidad = nueva_modalidad
        else:
            print("Modalidad inválida")

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):

        self.__cursos.append(curso)

    def elegir_modalidad(self):

        print(f"Modalidad seleccionada: {self.__modalidad}")

    def consultar_cursos(self):

        print("\nCursos registrados:")

        for curso in self.__cursos:
            print(f"- {curso.nombreCurso}")

    def ver_notas(self):

        print("Visualizando notas...")
