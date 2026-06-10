from abc import ABC
from Autenticable import Autenticable

def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena):

        self.nombre = nombre
        self.telefono = telefono

        self._email = email

        self.identificacion = identificacion

        self.__contrasena = contrasena

@property
def contrasena(self):
        return self.__contrasena

@contrasena.setter
def contrasena(self, nueva_contrasena):

        if len(nueva_contrasena) >= 4:
            self.__contrasena = nueva_contrasena
        else:
            print("Contraseña inválida")

def iniciar_sesion(self):

        print(f"{self.nombre} inició sesión")

def cerrar_sesion(self):

        print(f"{self.nombre} cerró sesión")