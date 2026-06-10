# CLASE SEDE
class Sede:

    def __init__(self,
                 nombreSede,
                 direccion,
                 ciudad):

        self.nombreSede = nombreSede
        self.direccion = direccion
        self.ciudad = ciudad

        # Composición
        self.__facultades = []

    # ENCAPSULAMIENTO
    @property
    def facultades(self):
        return self.__facultades

    def agregar_facultad(self, facultad):

        self.__facultades.append(facultad)

    def validar_disponibilidad(self):

        return len(self.__facultades) > 0

    def listar_facultades(self):

        print("\n========== FACULTADES ==========")

        if len(self.__facultades) == 0:
            print("No existen facultades")
            return

        for facultad in self.__facultades:
            print(f"- {facultad.nombreFacultad}")

    def mostrar_sede(self):

        print("\n========== SEDE ==========")
        print(f"Nombre: {self.nombreSede}")
        print(f"Dirección: {self.direccion}")
        print(f"Ciudad: {self.ciudad}")