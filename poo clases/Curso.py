class Curso:

    def __init__(self,
                 codigoCurso,
                 nombreCurso,
                 creditos):

        self.codigoCurso = codigoCurso
        self.nombreCurso = nombreCurso

        self.__creditos = creditos

        # Composición
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

    @property
    def aulas(self):
        return self.__aulas

    def agregar_horario(self, horario):

        self.__horarios.append(horario)

    def agregar_aula(self, aula):

        self.__aulas.append(aula)

    def mostrar_curso(self):

        print("\n========== CURSO ==========")
        print(f"Código: {self.codigoCurso}")
        print(f"Nombre: {self.nombreCurso}")
        print(f"Créditos: {self.__creditos}")

    def mostrar_horarios(self):

        print("\nHorarios:")

        if len(self.__horarios) == 0:
            print("No existen horarios")
            return

        for horario in self.__horarios:
            horario.mostrar_horario()

    def mostrar_aulas(self):

        print("\nAulas:")

        if len(self.__aulas) == 0:
            print("No existen aulas")
            return

        for aula in self.__aulas:
            aula.mostrar_aula()