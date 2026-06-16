from abc import ABC, abstractmethod

class Autenticable(ABC):

    @abstractmethod
    def iniciar_sesion(self):
        pass

    @abstractmethod
    def cerrar_sesion(self):
        pass