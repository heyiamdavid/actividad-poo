class CursoNivelacion:

    def __init__(self,
                 nombreCurso,
                 paralelo,
                 profesor=None):

        self.nombreCurso = nombreCurso
        self.paralelo = paralelo

        # Agregación
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

        print("\n========== CURSO NIVELACIÓN ==========")
        print(f"Curso: {self.nombreCurso}")
        print(f"Paralelo: {self.paralelo}")

        if self.profesor:
            print(f"Profesor: {self.profesor.nombre}")

    def mostrar_evaluaciones(self):

        print("\nEvaluaciones:")

        if len(self.__evaluaciones) == 0:
            print("No existen evaluaciones")
            return

        for evaluacion in self.__evaluaciones:
            evaluacion.mostrar_calificacion()