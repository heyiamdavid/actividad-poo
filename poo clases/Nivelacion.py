class Nivelacion:

    def __init__(self,
                 periodo,
                 duracion):

        self.periodo = periodo

        self.__duracion = duracion

        # Composición
        self.__cursos_nivelacion = []

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, nueva_duracion):

        if nueva_duracion > 0:
            self.__duracion = nueva_duracion
        else:
            print("Duración inválida")

    @property
    def cursos_nivelacion(self):
        return self.__cursos_nivelacion

    def agregar_curso(self, curso):

        self.__cursos_nivelacion.append(curso)

    def mostrar_nivelacion(self):

        print("\n========== NIVELACIÓN ==========")
        print(f"Periodo: {self.periodo}")
        print(f"Duración: {self.__duracion} meses")

        print("\nCursos de nivelación:")

        if len(self.__cursos_nivelacion) == 0:
            print("No existen cursos")
            return

        for curso in self.__cursos_nivelacion:
            print(f"- {curso.nombreCurso}")