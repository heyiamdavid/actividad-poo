from abc import ABC, abstractmethod

# Se importan los modelos concretos que las fábricas van a instanciar
from Estudiante import Estudiante
from Profesor import Profesor

# PATRÓN DE DISEÑO CREACIONAL: Factory Method (Método Fábrica)
# Interfaz base (Clase Abstracta) que define el contrato central para crear objetos.
# Su propósito es desacoplar la creación de objetos de la lógica principal del sistema.
class FabricaPersona(ABC):

    # Método abstracto que obliga a cualquier clase hija a implementar su propia lógica de creación.
    # Se usa *args para permitir flexibilidad (diferentes tipos de personas requerirán diferentes parámetros).
    @abstractmethod
    def crear_persona(self, *args):
        pass


# Fábrica Concreta: Clase especializada exclusivamente en instanciar objetos Estudiante.
# Hereda de la clase base FabricaPersona y cumple con su contrato.
class FabricaEstudiante(FabricaPersona):

    # Sobreescritura del método abstracto (Polimorfismo).
    # Se tipan fuertemente los parámetros específicos que requiere un Estudiante.
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

        # Encapsula la instanciación: Retorna un objeto Estudiante ya construido y listo para usarse.
        # Si el día de mañana la creación de un estudiante cambia, solo se modifica esta fábrica.
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


# Fábrica Concreta: Clase especializada exclusivamente en instanciar objetos Profesor.
# Al igual que la fábrica de estudiantes, extiende la clase base aplicando el Principio de Sustitución de Liskov.
class FabricaProfesor(FabricaPersona):

    # Implementación específica del método de creación para el perfil Profesor.
    # Los argumentos cambian (ej. se requiere 'titulo' en lugar de 'promedio_ingreso'),
    # pero el método se llama exactamente igual gracias a la abstracción.
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

        # Construye y retorna la instancia limpia del Profesor
        return Profesor(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena,
            titulo,
            materia
        )
