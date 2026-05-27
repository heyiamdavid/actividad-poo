from Persona import Persona

class Profesor(Persona):

    def __init__(self, nombre, telefono, email,
                 identificacion, contrasena,
                 materias_que_imparte, titulo):

        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

        self.materias_que_imparte = materias_que_imparte
        self.titulo = titulo
        self.notasEstudiantes = []

    def registrar_notas(self, nota):
        self.notasEstudiantes.append(nota)

    def crear_evaluacion(self):
        print("Evaluación creada")

    def listar_estudiantes(self):
        print("Lista de estudiantes")