class Carrera:

    def __init__(self,
                 codigoCarrera,
                 nombreCarrera,
                 modalidad):

        self.codigoCarrera = codigoCarrera
        self.nombreCarrera = nombreCarrera

        self.__modalidad = modalidad

        # Agregación
        self.__estudiantes = []

        # Composición
        self.__nivelaciones = []

    # ENCAPSULAMIENTO
    @property
    def modalidad(self):
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, nueva_modalidad):

        if nueva_modalidad.strip() != "":
            self.__modalidad = nueva_modalidad

    @property
    def estudiantes(self):
        return self.__estudiantes

    @property
    def nivelaciones(self):
        return self.__nivelaciones

    def agregar_estudiante(self, estudiante):

        self.__estudiantes.append(estudiante)

    def agregar_nivelacion(self, nivelacion):

        self.__nivelaciones.append(nivelacion)

    def mostrar_carrera(self):

        print("\n========== CARRERA ==========")
        print(f"Código: {self.codigoCarrera}")
        print(f"Nombre: {self.nombreCarrera}")
        print(f"Modalidad: {self.__modalidad}")

    def listar_estudiantes(self):

        print(
            f"\n===== ESTUDIANTES DE "
            f"{self.nombreCarrera} ====="
        )

        if len(self.__estudiantes) == 0:
            print("No existen estudiantes")
            return

        for estudiante in self.__estudiantes:

            print(
                f"- {estudiante.nombre}"
            )

    def tiene_nivelacion(self):

        return len(self.__nivelaciones) > 0