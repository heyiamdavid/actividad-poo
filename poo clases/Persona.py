from abc import ABC
from Autenticable import Autenticable

class Persona(Autenticable, ABC):

    def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena):

        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.identificacion = identificacion
        self.__contrasena = contrasena
  
    # Encapsulación mediante Property
    @property
    def contrasena(self):
        return self.__contrasena

    # Encapsulación
    @contrasena.setter
    def contrasena(self, nueva_contrasena):

        if len(nueva_contrasena) >= 4:
            self.__contrasena = nueva_contrasena
        else:
            print("Contraseña inválida")

    # Método heredado de la interfaz/clase Autenticable
    # Polimorfismo 
    def iniciar_sesion(self):

        print(f"\nBienvenido {self.nombre}")

    # Método heredado de la interfaz/clase Autenticable
    # Polimorfismo
    def cerrar_sesion(self):

        print(f"\nSesión cerrada para {self.nombre}")

    def mostrar_datos(self):

        print("\n========== DATOS ==========")
        print(f"Nombre: {self.nombre}")
        print(f"Teléfono: {self.telefono}")
        print(f"Email: {self.email}")
        print(f"Identificación: {self.identificacion}")