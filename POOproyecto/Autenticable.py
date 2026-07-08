from abc import ABC, abstractmethod
# Clase abstracta para definir métodos de autenticación
# Se heredan a Persona
class Autenticable(ABC):

    @abstractmethod
    def iniciar_sesion(self) -> None:
        pass

    @abstractmethod
    def cerrar_sesion(self) -> None:
        pass
