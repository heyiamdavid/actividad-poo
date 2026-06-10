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

        if self.estudiante:
            self.estudiante.agregar_curso(curso)

    def mostrar_matricula(self):

        print("\n========== MATRÍCULA ==========")
        print(f"Fecha: {self.fecha}")

        if self.estudiante:
            print(
                f"Estudiante: "
                f"{self.estudiante.nombre}"
            )

        print("\nCursos:")

        if len(self.__cursos) == 0:
            print("No existen cursos")
            return

        for curso in self.__cursos:

            print(
                f"- {curso.nombreCurso}"
            )

    def generar_comprobante(
            self,
            formato="PDF"):

        print(
            f"\nComprobante generado "
            f"en formato {formato}"
        )