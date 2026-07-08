from abc import ABC, abstractmethod

from Estudiante import Estudiante
from Profesor import Profesor

#Factory Method 
class FabricaPersona(ABC):

    @abstractmethod
    def crear_persona(self, *args):
        pass


class FabricaEstudiante(FabricaPersona): #clase fabrica estudiante hereda metodo de la clase base fabrica persona

    def crear_persona(
        self,
        nombre: str,
        telefono: str,
        email: str,
        identificacion: str,
        contrasena: str,
        promedio_ingreso: float,
        promedio_graduacion: float,
        estado: str,
        modalidad: str
    ) -> Estudiante:

        return Estudiante(

            nombre,
            telefono,
            email,
            identificacion,
            contrasena,

            promedio_ingreso,
            promedio_graduacion,

            estado,
            modalidad
        )


class FabricaProfesor(FabricaPersona): #clase fabrica profesor hereda metodo de la clase base fabrica persona

    def crear_persona(
        self,
        nombre: str,
        telefono: str,
        email: str,
        identificacion: str,
        contrasena: str,
        titulo: str,
        materia: str = ""
    ) -> Profesor:

        return Profesor(

            nombre,
            telefono,
            email,
            identificacion,
            contrasena,

            titulo,
            materia
        )