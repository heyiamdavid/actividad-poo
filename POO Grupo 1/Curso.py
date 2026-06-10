class Curso:

    def __init__(self,
                 codigoCurso,
                 nombreCurso,
                 creditos):

        self.codigoCurso = codigoCurso
        self.nombreCurso = nombreCurso

        self.__creditos = creditos

        self.__horarios = []
        self.__aulas = []

    @property
    def creditos(self):
        return self.__creditos

    @creditos.setter
    def creditos(self, nuevos_creditos):

        if nuevos_creditos > 0:
            self.__creditos = nuevos_creditos
        else:
            print("Créditos inválidos")

    @property
    def horarios(self):
        return self.__horarios

    def agregar_horario(self, horario):
        self.__horarios.append(horario)

    @property
    def aulas(self):
        return self.__aulas

    def agregar_aula(self, aula):
        self.__aulas.append(aula)

    def mostrar_curso(self):

        print(f"Curso: {self.nombreCurso}")
        print(f"Créditos: {self.__creditos}")