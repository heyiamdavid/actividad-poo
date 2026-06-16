from abc import ABC, abstractmethod
# Clase abstracta para definir métodos de autenticación
class Autenticable(ABC):

    @abstractmethod
    def iniciar_sesion(self):
        pass

    @abstractmethod
    def cerrar_sesion(self):
        pass
