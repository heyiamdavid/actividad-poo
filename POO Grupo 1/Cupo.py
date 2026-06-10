class Cupo:

    def __init__(self,
                 cantidad,
                 disponibles):

        self.cantidad = cantidad

        self.__disponibles = disponibles

    @property
    def disponibles(self):
        return self.__disponibles

    @disponibles.setter
    def disponibles(self, valor):

        if valor >= 0:
            self.__disponibles = valor
        else:
            print("Cantidad inválida")

    def reducir_cupo(self):

        if self.__disponibles > 0:
            self.__disponibles -= 1
        else:
            print("No hay cupos disponibles")

    def mostrar_cupos(self):

        print(f"Cupos disponibles: {self.__disponibles}")