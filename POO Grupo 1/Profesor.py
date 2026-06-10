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

    @property
    def notas(self):
        return self.__notas

    @notas.setter
    def notas(self, nota):

        if 0 <= nota <= 10:
            self.__notas.append(nota)
        else:
            print("Nota inválida")

    def registrar_nota(self, nota):

        self.notas = nota

    def crear_evaluacion(self):

        print("Evaluación creada")

    def listar_estudiantes(self):

        print("Lista de estudiantes mostrada")