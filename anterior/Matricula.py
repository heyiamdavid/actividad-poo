class Matricula:

    def __init__(self,
                 fecha,
                 estudiante=None):

        self.fecha = fecha

        self.estudiante = estudiante

        self.__cursos = []

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):
        self.__cursos.append(curso)

    def mostrar_matricula(self):

        print(f"Fecha matrícula: {self.fecha}")

        if self.estudiante:
            print(f"Estudiante: {self.estudiante.nombre}")

        print("Cursos registrados:")

        for curso in self.__cursos:
            print(curso.nombreCurso)

    # sobrecarga simple
    def generar_comprobante(self, formato="PDF"):

        print(f"Comprobante generado en formato {formato}")