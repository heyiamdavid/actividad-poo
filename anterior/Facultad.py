class Facultad:

    def __init__(self, id_facultad,
                 nombreFacultad,
                 ubicacion):

        self.id_facultad = id_facultad
        self.nombreFacultad = nombreFacultad
        self.ubicacion = ubicacion

        self.__carreras = []
        self.__cupos = []

    @property
    def carreras(self):
        return self.__carreras

    def agregar_carrera(self, carrera):
        self.__carreras.append(carrera)

    @property
    def cupos(self):
        return self.__cupos

    def agregar_cupo(self, cupo):
        self.__cupos.append(cupo)

    def asignar_carrera(self):
        print("Carrera asignada")

    def carreras_ofertadas(self):

        for carrera in self.__carreras:
            print(carrera.nombreCarrera)

    def buscar_carreras(self, nombre):

        for carrera in self.__carreras:

            if carrera.nombreCarrera == nombre:
                return carrera

        return None