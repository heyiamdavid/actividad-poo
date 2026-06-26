from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from Carrera import Carrera


class Facultad:

    def __init__(self,
                 id_facultad: int,
                 nombreFacultad: str,
                 ubicacion: str):

        self.id_facultad: int = id_facultad
        self.nombreFacultad: str = nombreFacultad
        self.ubicacion: str = ubicacion

        # Composición
        self.__carreras: List["Carrera"] = []

        # Agregación
        self.__cupos: List[Any] = []

    @property
    def carreras(self) -> List["Carrera"]:
        return self.__carreras

    @property
    def cupos(self) -> List[Any]:
        return self.__cupos

    def agregar_carrera(self, carrera: "Carrera") -> None:

        self.__carreras.append(carrera)

    def agregar_cupo(self, cupo: Any) -> None:

        self.__cupos.append(cupo)

    def asignar_carrera(self, carrera: "Carrera") -> None:

        self.__carreras.append(carrera)

        print(
            f"Carrera {carrera.nombreCarrera} "
            f"asignada correctamente"
        )

    def carreras_ofertadas(self) -> None:

        print("\n========== CARRERAS ==========")

        if len(self.__carreras) == 0:
            print("No existen carreras")
            return

        for carrera in self.__carreras:

            print(
                f"- {carrera.nombreCarrera}"
            )

    def buscar_carrera(self, codigo_carrera: str) -> Optional["Carrera"]:

        for carrera in self.__carreras:

            if carrera.codigoCarrera.lower() == codigo_carrera.lower():
                return carrera

        return None

    def eliminar_carrera(self, codigo_carrera: str) -> bool:

        carrera = self.buscar_carrera(codigo_carrera)

        if carrera is None:
            return False

        self.__carreras.remove(carrera)
        return True

    def mostrar_facultad(self) -> None:

        print("\n========== FACULTAD ==========")
        print(f"ID: {self.id_facultad}")
        print(f"Nombre: {self.nombreFacultad}")
        print(f"Ubicación: {self.ubicacion}")