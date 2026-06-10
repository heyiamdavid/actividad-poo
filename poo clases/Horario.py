class Horario:

    def __init__(self,
                 dia,
                 hora_inicio,
                 hora_fin):

        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def mostrar_horario(self):

        print(
            f"{self.dia}: "
            f"{self.hora_inicio} - {self.hora_fin}"
        )