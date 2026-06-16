from datetime import datetime

class Reporte:

    def __init__(self, tipo, fecha_generacion=None):
        self.tipo = tipo
# Genera automáticamente la fecha actual si no se proporciona una
        if fecha_generacion is None:
            self.fecha_generacion = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        else:
            self.fecha_generacion = fecha_generacion
    def generar_reporte_estudiantil(
            self,
            estudiantes):

        print("REPORTE DE ESTUDIANTES")
        print(f"Fecha: {self.fecha_generacion}")

        if len(estudiantes) == 0:
            print("No existen estudiantes registrados")
            return
        print()
        for estudiante in estudiantes:
            print(f"ID: {estudiante[0]}")
            print(f"Nombre: {estudiante[1]}")
            print(f"Modalidad: {estudiante[9]}")
            print(f"Estado: {estudiante[8]}")
            print("-----------------------------------")

    def generar_reporte_profesores(self, profesores):

        print("REPORTE DE PROFESORES")
        print(f"Fecha: {self.fecha_generacion}")

        if len(profesores) == 0:
            print("No existen profesores registrados")
            return
        print()

        for profesor in profesores:
            print(f"ID: {profesor[0]}")
            print(f"Nombre: {profesor[1]}")
            print(f"Materia: {profesor[6]}")
            print(f"Título: {profesor[7]}")
            print("-----------------------------------")

    def generar_reporte_general(self, estudiantes, profesores):
        print("REPORTE GENERAL")

        print(f"Fecha: {self.fecha_generacion}")

        print(
            f"Total estudiantes: "
            f"{len(estudiantes)}"
        )

        print(
            f"Total profesores: "
            f"{len(profesores)}"
        )

        print(
            f"Total registros: "
            f"{len(estudiantes) + len(profesores)}"
        )
