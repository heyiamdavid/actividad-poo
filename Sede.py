class Sede:

    def __init__(self, nombreSede, direccion,
                 ciudad):

        self.nombreSede = nombreSede
        self.direccion = direccion
        self.ciudad = ciudad

        self.__facultades = []

    @property
    def facultades(self):
        return self.__facultades

    def agregar_facultad(self, facultad):
        self.__facultades.append(facultad)

    def listar_facultades(self):

        for facultad in self.__facultades:
            print(facultad.nombreFacultad)