from abc import ABC
from Autenticable import Autenticable

class Persona(Autenticable, ABC):

    def __init__(self, nombre, numero_telefono, email,
                 identificacion, contrasena_temporal):

        self.nombre = nombre
        self.numero_telefono = numero_telefono
        self._email = email
        self.identificacion = identificacion
        self.__contrasena_temporal = contrasena_temporal

    def ingresar(self):
        print(f"{self.nombre} ingresó al sistema")

    def iniciar_sesion(self):
        print(f"{self.nombre} inició sesión")

    def cerrar_sesion(self):
        print(f"{self.nombre} cerró sesión")