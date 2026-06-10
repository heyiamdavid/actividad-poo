class Nivelacion:

    def __init__(self,
                 periodo,
                 duracion):

        self.periodo = periodo

        self.__duracion = duracion

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

