from Persona import Persona

class Profesor(Persona):

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

        self.__notas = []
        self.__evaluaciones = []

    @property
    def notas(self):
        return self.__notas

    @property
    def evaluaciones(self):
        return self.__evaluaciones

    def registrar_nota(self, nota):

        if 0 <= nota <= 10:

            self.__notas.append(nota)

            print("Nota registrada correctamente")

        else:
            print("Nota inválida")

    def crear_evaluacion(self, evaluacion):

        self.__evaluaciones.append(evaluacion)

        print(
            f"Evaluación {evaluacion.nombreEvaluacion} registrada"
        )

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

    def mostrar_datos(self):

        super().mostrar_datos()

        print(f"Materia: {self.materia}")
        print(f"Título: {self.titulo}")