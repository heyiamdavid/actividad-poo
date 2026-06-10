class Facultad:

    def __init__(self,
                 id_facultad,
                 nombreFacultad,
                 ubicacion):

        self.id_facultad = id_facultad
        self.nombreFacultad = nombreFacultad
        self.ubicacion = ubicacion

        # Composición
        self.__carreras = []

        # Agregación
        self.__cupos = []

    @property
    def carreras(self):
        return self.__carreras

    @property
    def cupos(self):
        return self.__cupos

    def agregar_carrera(self, carrera):

        self.__carreras.append(carrera)

    def agregar_cupo(self, cupo):

        self.__cupos.append(cupo)

    def asignar_carrera(self, carrera):

        self.__carreras.append(carrera)

        print(
            f"Carrera {carrera.nombreCarrera} "
            f"asignada correctamente"
        )

    def carreras_ofertadas(self):

        print("\n========== CARRERAS ==========")

        if len(self.__carreras) == 0:
            print("No existen carreras")
            return

        for carrera in self.__carreras:

            print(
                f"- {carrera.nombreCarrera}"
            )

    def buscar_carrera(self, nombre):

        for carrera in self.__carreras:

            if carrera.nombreCarrera.lower() == nombre.lower():
                return carrera

        return None

    def mostrar_facultad(self):

        print("\n========== FACULTAD ==========")
        print(f"ID: {self.id_facultad}")
        print(f"Nombre: {self.nombreFacultad}")
        print(f"Ubicación: {self.ubicacion}")