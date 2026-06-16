from Persona import Persona

class Estudiante(Persona):

    def __init__(self, nombre, telefono, email,
                 identificacion, contrasena,
                 promedio_ingreso, promedio_graduacion,
                 estado, modalidad):

        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

        self.promedio_ingreso = promedio_ingreso
        self.promedio_graduacion = promedio_graduacion
        self.estado = estado
        self.modalidad = modalidad
        self.cursos = []

    def elegir_modalidad(self):
        print(f"{self.nombre} eligió modalidad {self.modalidad}")

    def consultar_cursos(self):
        print(self.cursos)

    def ver_notas(self):
        print("Mostrando notas...")