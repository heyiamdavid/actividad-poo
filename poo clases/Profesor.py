from Persona import Persona
from Evaluacion import Evaluacion

#Clase Profesor
class Profesor(Persona):

    def __init__(self, nombre, telefono, email, identificacion,
                 contrasena, materia, titulo):

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
            print("\nNota registrada correctamente.")

        else:

            print("\nLa nota debe estar entre 0 y 10.")

    def crear_evaluacion(self):

        nombre = input("Nombre de la evaluación: ")
        nota = float(input("Calificación inicial: "))

        evaluacion = Evaluacion(nombre, nota)

        self.__evaluaciones.append(evaluacion)

        print("\nEvaluación creada correctamente.")

        return evaluacion

    def listar_estudiantes(self, estudiantes):

        if len(estudiantes) == 0:

            print("\nNo existen estudiantes registrados.")
            return

        print("\n===== ESTUDIANTES =====")

        for estudiante in estudiantes:
            print(estudiante.nombre)

    def mostrar_notas(self):

        if len(self.__notas) == 0:

            print("\nNo existen notas registradas.")
            return

        print("\n===== NOTAS =====")

        for nota in self.__notas:
            print(nota)

    def mostrar_evaluaciones(self):

        if len(self.__evaluaciones) == 0:

            print("\nNo existen evaluaciones.")
            return

        print("\n===== EVALUACIONES =====")

        for evaluacion in self.__evaluaciones:
            evaluacion.mostrar_calificacion()

    def mostrar_datos(self):

        print("\n========== DATOS PROFESOR ==========")

        print("Nombre:", self.nombre)
        print("Teléfono:", self.telefono)
        print("Email:", self.email)
        print("Identificación:", self.identificacion)
        print("Materia:", self.materia)
        print("Título:", self.titulo)