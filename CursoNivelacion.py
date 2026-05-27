class CursoNivelacion:

    def __init__(self,
                 nombreCurso,
                 paralelo,
                 profesor=None):

        self.nombreCurso = nombreCurso
        self.paralelo = paralelo

        self.profesor = profesor

        self.__evaluaciones = []

    @property
    def evaluaciones(self):
        return self.__evaluaciones

    def agregar_evaluacion(self, evaluacion):
        self.__evaluaciones.append(evaluacion)

    def asignar_profesor(self, profesor):

        self.profesor = profesor

    def mostrar_curso(self):

        print(f"Curso: {self.nombreCurso}")
        print(f"Paralelo: {self.paralelo}")

        if self.profesor:
            print(f"Profesor: {self.profesor.nombre}")