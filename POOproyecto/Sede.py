# CLASE SEDE
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from Facultad import Facultad


class Sede:

    def __init__(self,
                 nombreSede: str,
                 direccion: str,
                 ciudad: str):

        self.nombreSede: str = nombreSede
        self.direccion: str = direccion
        self.ciudad: str = ciudad

        # Composición
        self.__facultades: List["Facultad"] = []

    # ENCAPSULAMIENTO
    @property
    def facultades(self) -> List["Facultad"]:
        return self.__facultades

    def agregar_facultad(self, facultad: "Facultad") -> None:

        self.__facultades.append(facultad)

    def buscar_facultad(self, id_facultad: int) -> Optional["Facultad"]:

        for facultad in self.__facultades:

            if facultad.id_facultad == id_facultad:
                return facultad

        return None

    def eliminar_facultad(self, id_facultad: int) -> bool:

        facultad = self.buscar_facultad(id_facultad)

        if facultad is None:
            return False

        self.__facultades.remove(facultad)
        return True

    def validar_disponibilidad(self) -> bool:

        return len(self.__facultades) > 0

    def listar_facultades(self) -> None:

        print("\n========== FACULTADES ==========")

        if len(self.__facultades) == 0:
            print("No existen facultades")
            return

        for facultad in self.__facultades:
            print(f"- {facultad.nombreFacultad}")

    def mostrar_sede(self) -> None:

        print("\n========== SEDE ==========")
        print(f"Nombre: {self.nombreSede}")
        print(f"Dirección: {self.direccion}")
        print(f"Ciudad: {self.ciudad}")