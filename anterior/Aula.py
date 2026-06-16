class Aula:

    def __init__(self,
                 numeroAula,
                 capacidad):

        self.numeroAula = numeroAula

        self.__capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, nueva_capacidad):

        if nueva_capacidad > 0:
            self.__capacidad = nueva_capacidad
        else:
            print("Capacidad inválida")

    def mostrar_aula(self):

        print(f"Aula: {self.numeroAula}")
        print(f"Capacidad: {self.__capacidad}")