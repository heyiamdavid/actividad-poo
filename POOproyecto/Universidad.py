from typing import TYPE_CHECKING, List, Optional
# Importación condicional para evitar errores de importación circular.
# Solo se ejecuta durante la fase de análisis de tipos estáticos, no en tiempo de ejecución.
if TYPE_CHECKING:
    from Sede import Sede


class Universidad:

    def __init__(self,
                 id_universidad: int,
                 nombreUniversidad: str,
                 direccion: str):

        self.id_universidad: int = id_universidad
        self.nombreUniversidad: str = nombreUniversidad
        self.direccion: str = direccion

        # Composición
        # Se declara como lista privada (__) para proteger su integridad desde el inicio.
        self.__sedes: List["Sede"] = []

    # ENCAPSULAMIENTO
    @property
    def sedes(self) -> List["Sede"]:
        return self.__sedes

    # MÉTODOS
    def agregar_sede(self, sede: "Sede") -> None:

        self.__sedes.append(sede)

    def buscar_sede(self, nombre_sede: str) -> Optional["Sede"]:

        for sede in self.__sedes:

            if sede.nombreSede.lower() == nombre_sede.lower():
                return sede

        return None

    def eliminar_sede(self, nombre_sede: str) -> bool:

        sede = self.buscar_sede(nombre_sede)

        if sede is None:
            return False

        self.__sedes.remove(sede)
        return True

    def validar_datos(self) -> bool:

        return (
            self.nombreUniversidad.strip() != ""
            and
            self.direccion.strip() != ""
        )

    def crear_oferta(self) -> None:

        print(
            f"\nOferta académica disponible en "
            f"{self.nombreUniversidad}"
        )

    def mostrar_universidad(self) -> None:

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
