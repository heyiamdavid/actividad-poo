from abc import ABC
from Autenticable import Autenticable

class Persona(Autenticable, ABC):

    def __init__(self,
                 nombre: str,
                 telefono: str,
                 email: str,
                 identificacion: str,
                 contrasena: str):

        self.nombre: str = nombre
        self.telefono: str = telefono
        self.email: str = email
        self.identificacion: str = identificacion
        self.__contrasena: str = contrasena

        # La clave temporal queda fija desde el registro: es la que
        # el administrador entregó originalmente. Se conserva aunque
        # la persona cambie su contraseña, para que el administrador
        # pueda consultar ambas.
        self.__clave_temporal: str = contrasena

    # Encapsulación mediante Property
    @property
    def contrasena(self) -> str:
        return self.__contrasena

    # Encapsulación
    @contrasena.setter
    def contrasena(self, nueva_contrasena: str) -> None:

        if len(nueva_contrasena) >= 4:
            self.__contrasena = nueva_contrasena
        else:
            print("Contraseña inválida")

    @property
    def clave_temporal(self) -> str:
        return self.__clave_temporal

    def cambiar_contrasena(self, contrasena_actual: str, nueva_contrasena: str,
                            confirmacion_nueva: str) -> bool:

        if contrasena_actual != self.__contrasena:
            print("\nLa contraseña actual no coincide.")
            return False

        if nueva_contrasena != confirmacion_nueva:
            print("\nLas contraseñas nuevas no coinciden.")
            return False

        if len(nueva_contrasena) < 4:
            print("\nLa nueva contraseña debe tener al menos 4 caracteres.")
            return False

        self.contrasena = nueva_contrasena
        print("\nContraseña actualizada correctamente.")
        return True

    # Método heredado de la interfaz/clase Autenticable
    # Polimorfismo 
    def iniciar_sesion(self) -> None:

        print(f"\nBienvenido {self.nombre}")

    # Método heredado de la interfaz/clase Autenticable
    # Polimorfismo
    def cerrar_sesion(self) -> None:

        print(f"\nSesión cerrada para {self.nombre}")

    def mostrar_datos(self) -> None:

        print("\n========== DATOS ==========")
        print(f"Nombre: {self.nombre}")
        print(f"Teléfono: {self.telefono}")
        print(f"Email: {self.email}")
        print(f"Identificación: {self.identificacion}")