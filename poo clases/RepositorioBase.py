from abc import ABC, abstractmethod

class RepositorioBase(ABC):
    
    @abstractmethod
    def crear_estructura(self):
        pass

    @abstractmethod
    def guardar_estudiante(self, estudiante):
        pass

    @abstractmethod
    def guardar_profesor(self, profesor):
        pass

    @abstractmethod
    def buscar_estudiante(self, identificacion):
        pass

    @abstractmethod
    def buscar_profesor(self, identificacion):
        pass

    @abstractmethod
    def validar_login_estudiante(self, identificacion, contrasena):
        pass

    @abstractmethod
    def validar_login_profesor(self, identificacion, contrasena):
        pass

    @abstractmethod
    def listar_estudiantes(self):
        pass

    @abstractmethod
    def listar_profesores(self):
        pass

    @abstractmethod
    def eliminar_estudiante(self, identificacion):
        pass

    @abstractmethod
    def eliminar_profesor(self, identificacion):
        pass

    @abstractmethod
    def total_estudiantes(self):
        pass

    @abstractmethod
    def total_profesores(self):
        pass
