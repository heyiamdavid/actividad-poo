# CLASE SEDE
from typing import TYPE_CHECKING, List, Optional

# Evita importaciones circulares, solo se utiliza para ayuda de tipos
if TYPE_CHECKING:
    from Facultad import Facultad


class Sede:

    # Constructor de la clase Sede
    def __init__(self,
                 nombreSede: str,
                 direccion: str,
                 ciudad: str):

        # Nombre de la sede
        self.nombreSede: str = nombreSede

        # Dirección de la sede
        self.direccion: str = direccion

        # Ciudad donde se encuentra la sede
        self.ciudad: str = ciudad

        # Composición: una sede contiene una lista de facultades
        self.__facultades: List["Facultad"] = []

    # ENCAPSULAMIENTO
    # Permite acceder a la lista de facultades de forma controlada
    @property
    def facultades(self) -> List["Facultad"]:
        return self.__facultades

    # Agrega una facultad a la sede
    def agregar_facultad(self, facultad: "Facultad") -> None:

        self.__facultades.append(facultad)

    # Busca una facultad por su identificador
    def buscar_facultad(self, id_facultad: int) -> Optional["Facultad"]:

        # Recorre la lista de facultades
        for facultad in self.__facultades:

            # Si encuentra la facultad con el ID indicado, la retorna
            if facultad.id_facultad == id_facultad:
                return facultad

        # Retorna None si no existe la facultad
        return None

    # Elimina una facultad por su identificador
    def eliminar_facultad(self, id_facultad: int) -> bool:

        # Busca la facultad
        facultad = self.buscar_facultad(id_facultad)

        # Si no existe, retorna False
        if facultad is None:
            return False

        # Elimina la facultad de la lista
        self.__facultades.remove(facultad)

        # Retorna True indicando que la eliminación fue exitosa
        return True

    # Verifica si la sede tiene al menos una facultad registrada
    def validar_disponibilidad(self) -> bool:

        return len(self.__facultades) > 0

    # Muestra todas las facultades registradas en la sede
    def listar_facultades(self) -> None:

        print("\n========== FACULTADES ==========")

        # Verifica si existen facultades
        if len(self.__facultades) == 0:
            print("No existen facultades")
            return

        # Recorre e imprime el nombre de cada facultad
        for facultad in self.__facultades:
            print(f"- {facultad.nombreFacultad}")

    # Muestra la información de la sede
    def mostrar_sede(self) -> None:

        # Se imprimen los datos de la sede
        print("\n========== SEDE ==========")
        print(f"Nombre: {self.nombreSede}")
        print(f"Dirección: {self.direccion}")
        print(f"Ciudad: {self.ciudad}")