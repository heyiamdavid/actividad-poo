from datetime import datetime
from Validador import Validador
from Administrador import Administrador
from Estudiante import Estudiante


# Menú del Estudiante.
# Únicamente contiene flujo de pantallas y llamadas a métodos
# de Administrador y de las clases de dominio (Estudiante, Matricula).
class MenuEstudiante:

    def __init__(self, administrador: Administrador, estudiante: Estudiante):
        self.administrador: Administrador = administrador
        self.estudiante: Estudiante = estudiante

    def ver_datos(self) -> None:
        self.estudiante.mostrar_datos()

    def realizar_matricula(self) -> None:

        print("\n========== MATRÍCULA ==========\n")

        if not self.estudiante.esta_activo():
            print(
                f"El estudiante {self.estudiante.nombre} está Inactivo "
                f"y no puede realizar la matrícula."
            )
            return

        if self.estudiante.semestre == 0:
            print(
                "Te encuentras en nivelación. Debes completarla antes "
                "de matricularte en cursos regulares."
            )
            curso_nivelacion = self.administrador.curso_de_nivelacion_de(
                self.estudiante.carrera
            )
            if curso_nivelacion:
                curso_nivelacion.mostrar_curso()
            return

        print(f"Carrera: {self.estudiante.carrera}")
        print(f"Semestre: {self.estudiante.semestre}")

        cursos = self.administrador.cursos_disponibles(
            self.estudiante.carrera, self.estudiante.semestre
        )

        if len(cursos) == 0:
            print("\nNo existen cursos disponibles para tu carrera y semestre")
            return

        print("\nCursos disponibles:")
        for curso in cursos:
            curso.mostrar_curso()
            print("-----------------------------------")

        codigos_curso = [curso.codigoCurso for curso in cursos]
        codigos_seleccionados = []

        while True:
            codigo = Validador.seleccionar_opcion(
                "Seleccione un curso a matricular:",
                codigos_curso + ["Terminar selección"]
            )

            if codigo == "Terminar selección":
                break

            if codigo not in codigos_seleccionados:
                codigos_seleccionados.append(codigo)

        if len(codigos_seleccionados) == 0:
            print("\nNo se seleccionaron cursos")
            return

        fecha = datetime.now().strftime("%d/%m/%Y")

        self.administrador.matricular(self.estudiante, codigos_seleccionados, fecha)

    def ver_matricula(self) -> None:
        # Incluye la modalidad del estudiante junto a la matrícula.
        self.estudiante.ver_matricula()

    def consultar_cursos_y_horarios(self) -> None:

        print("\n========== CURSOS Y HORARIOS ==========")

        if not self.estudiante.esta_activo():
            print(
                f"El estudiante {self.estudiante.nombre} está Inactivo "
                f"y no puede consultar cursos."
            )
            return

        cursos = self.administrador.cursos_disponibles(
            self.estudiante.carrera, self.estudiante.semestre
        )

        if len(cursos) == 0:
            print("No existen cursos disponibles para tu carrera y semestre")
            return

        for curso in cursos:
            curso.mostrar_curso()
            print("-----------------------------------")

    def ver_notas(self) -> None:
        self.estudiante.ver_notas()

    def cambiar_contrasena(self) -> None:

        print("\n========== CAMBIAR CONTRASEÑA ==========\n")

        contrasena_actual = input("Contraseña actual: ")
        nueva_contrasena, confirmacion = Validador.leer_clave_nueva()

        self.administrador.cambiar_contrasena_estudiante(
            self.estudiante, contrasena_actual, nueva_contrasena, confirmacion
        )

    def mostrar(self) -> None:

        self.estudiante.iniciar_sesion()

        while True:
            print("\n========================")
            print("MENÚ ESTUDIANTE")
            print("========================")
            print("1. Ver datos")
            print("2. Realizar matrícula")
            print("3. Ver matrícula")
            print("4. Consultar cursos y horarios")
            print("5. Ver notas")
            print("6. Cambiar contraseña")
            print("7. Cerrar sesión")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.ver_datos()
            elif opcion == "2":
                self.realizar_matricula()
            elif opcion == "3":
                self.ver_matricula()
            elif opcion == "4":
                self.consultar_cursos_y_horarios()
            elif opcion == "5":
                self.ver_notas()
            elif opcion == "6":
                self.cambiar_contrasena()
            elif opcion == "7":
                self.estudiante.cerrar_sesion()
                break
            else:
                print("\nOpción inválida")
