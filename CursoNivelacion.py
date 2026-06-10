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

    def agregar_horario(self, horario):
        print(f"Nota: Horario asignado a nivelación ({horario.dia})")

    def agregar_aula(self, aula):
        print(f"Nota: Aula asignada a nivelación ({aula.numeroAula})")