class Universidad:

    def __init__(self, id_universidad, nombreUniversidad,
                 direccion):

        self.id_universidad = id_universidad
        self.nombreUniversidad = nombreUniversidad
        self.direccion = direccion

        self.__sedes = []       # composición
        self.__reportes = []    # agregación

    @property
    def sedes(self):
        return self.__sedes

    def agregar_sede(self, sede):
        self.__sedes.append(sede)

    @property
    def reportes(self):
        return self.__reportes

    def agregar_reporte(self, reporte):
        self.__reportes.append(reporte)

    def registrar_universidad(self):
        print(f"Universidad {self.nombreUniversidad} registrada")

    def crear_oferta(self):
        print("Oferta académica creada")

    def validar_datos(self):
        print("Datos validados")

    def validar_disponibilidad(self):
        print("Disponibilidad verificada")