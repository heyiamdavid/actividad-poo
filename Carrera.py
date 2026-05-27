class Carrera:

    def __init__(self, codigoCarrera,
                 nombreCarrera,
                 modalidad):

        self.codigoCarrera = codigoCarrera
        self.nombreCarrera = nombreCarrera

        self.__modalidad = modalidad

        self.__nivelaciones = []
        self.__estudiantes = []

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
    def nivelaciones(self):
        return self.__nivelaciones

    def agregar_nivelacion(self, nivelacion):
        self.__nivelaciones.append(nivelacion)

    @property
    def estudiantes(self):
        return self.__estudiantes

    def agregar_estudiante(self, estudiante):
        self.__estudiantes.append(estudiante)

    def mostrar_carrera(self):

        print(f"Carrera: {self.nombreCarrera}")
        print(f"Modalidad: {self.__modalidad}")