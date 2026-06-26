class Horario:

    def __init__(self,
                 dia: str,
                 hora_inicio: str,
                 hora_fin: str):

        self.dia: str = dia
        self.hora_inicio: str = hora_inicio
        self.hora_fin: str = hora_fin

    def coincide_con(self, otro_horario: "Horario") -> bool:

        return (
            self.dia == otro_horario.dia
            and self.hora_inicio == otro_horario.hora_inicio
            and self.hora_fin == otro_horario.hora_fin
        )

    def mostrar_horario(self) -> None:

        print(
            f"{self.dia}: "
            f"{self.hora_inicio} - {self.hora_fin}"
        )