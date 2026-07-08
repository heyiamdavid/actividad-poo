class Horario:

    # Constructor de la clase Horario
    def __init__(self,
                 dia: str,
                 hora_inicio: str,
                 hora_fin: str):

        # Día en el que se imparte el horario
        self.dia: str = dia

        # Hora de inicio del horario
        self.hora_inicio: str = hora_inicio

        # Hora de finalización del horario
        self.hora_fin: str = hora_fin

    # Método que compara si dos horarios son iguales
    def coincide_con(self, otro_horario: "Horario") -> bool:

        # Retorna True si el día, la hora de inicio y la hora de fin coinciden
        return (
            self.dia == otro_horario.dia
            and self.hora_inicio == otro_horario.hora_inicio
            and self.hora_fin == otro_horario.hora_fin
        )

    # Método para mostrar el horario en pantalla
    def mostrar_horario(self) -> None:

        # Imprime el día junto con el rango de horas
        print(
            f"{self.dia}: "
            f"{self.hora_inicio} - {self.hora_fin}"
        )