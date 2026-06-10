class Universidad:

    def __init__(self,
                 id_universidad,
                 nombreUniversidad,
                 direccion):

        self.id_universidad = id_universidad
        self.nombreUniversidad = nombreUniversidad
        self.direccion = direccion

        # Composición
        self.__sedes = []

    # ENCAPSULAMIENTO
    @property
    def sedes(self):
        return self.__sedes

    # MÉTODOS
    def agregar_sede(self, sede):

        self.__sedes.append(sede)

    def validar_datos(self):

        return (
            self.nombreUniversidad.strip() != ""
            and
            self.direccion.strip() != ""
        )

    def crear_oferta(self):

        print(
            f"\nOferta académica disponible en "
            f"{self.nombreUniversidad}"
        )

    def mostrar_universidad(self):

        print("\n========== UNIVERSIDAD ==========")
        print(f"ID: {self.id_universidad}")
        print(f"Nombre: {self.nombreUniversidad}")
        print(f"Dirección: {self.direccion}")

        print("\nSedes registradas:")

        if len(self.__sedes) == 0:
            print("No existen sedes")
            return

        for sede in self.__sedes:
            print(f"- {sede.nombreSede}")