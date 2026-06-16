from Persona import Persona

class Profesor(Persona):

    # Herencia y reutilización de código mediante super()
    def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena,
                 materia,
                 titulo):

        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

        self.materia = materia
        self.titulo = titulo
    #Encapsulacion en las listas
        self.__notas = []
        self.__evaluaciones = []

    # Encapsulación
    @property
    def notas(self):
        return self.__notas

    @property
    def evaluaciones(self):
        return self.__evaluaciones

    # Abstracción
    # Permite registrar notas ocultando la lógica interna.
    def registrar_nota(self, nota):

        if 0 <= nota <= 10:

            self.__notas.append(nota)

            print("Nota registrada correctamente")

        else:
            print("Nota inválida")

    # Asociación
    # Un profesor puede crear y administrar objetos Evaluacion.
    def crear_evaluacion(self, evaluacion):

        self.__evaluaciones.append(evaluacion)

        print(
            f"Evaluación {evaluacion.nombreEvaluacion} registrada"
        )

    # Asociación
    # Interactúa con una colección de objetos Estudiante.
    def listar_estudiantes(self, estudiantes):

        print("\n========== ESTUDIANTES ==========")

        if len(estudiantes) == 0:
            print("No existen estudiantes")
            return

        for estudiante in estudiantes:

            print(
                f"{estudiante.nombre} - "
                f"{estudiante.identificacion}"
            )

    # Polimorfismo (Sobrescritura de método), se redefine mostrar_datos() heredado de Persona,
    # agregando información específica del profesor.
    def mostrar_datos(self):

        super().mostrar_datos()

        print(f"Materia: {self.materia}")
        print(f"Título: {self.titulo}")