from abc import ABC, abstractmethod

from Estudiante import Estudiante
from Profesor import Profesor

#Factory Method 
class FabricaPersona(ABC):

    @abstractmethod
    def crear_persona(self, *args):
        pass


class FabricaEstudiante(FabricaPersona):

    def crear_persona(
        self,
        nombre,
        telefono,
        email,
        identificacion,
        contrasena,
        promedio_ingreso,
        promedio_graduacion,
        estado,
        modalidad
    ):

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


class FabricaProfesor(FabricaPersona):

    def crear_persona(
        self,
        nombre,
        telefono,
        email,
        identificacion,
        contrasena,
        materia,
        titulo
    ):

        return Profesor(

            nombre,
            telefono,
            email,
            identificacion,
            contrasena,

            materia,
            titulo
        )