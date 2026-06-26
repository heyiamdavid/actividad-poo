from typing import Optional

from Validador import Validador
from Evaluacion import Evaluacion
from Administrador import Administrador
from Profesor import Profesor
from Curso import Curso
from Estudiante import Estudiante


# Menú del Profesor.
# Únicamente contiene flujo de pantallas y llamadas a métodos
# de Administrador y de las clases de dominio (Profesor, Curso, Evaluacion).
class MenuProfesor:

    def __init__(self, administrador: Administrador, profesor: Profesor):
        self.administrador: Administrador = administrador
        self.profesor: Profesor = profesor

    def ver_datos(self) -> None:
        self.profesor.mostrar_datos()

    def ver_cursos_asignados(self) -> None:
        self.profesor.mostrar_cursos()

    def _seleccionar_curso_asignado(self) -> Optional[Curso]:

        cursos = self.profesor.cursos

        if len(cursos) == 0:
            print("\nNo tienes cursos asignados todavía.")
            return None

        print("\nCursos asignados:")
        for curso in cursos:
            curso.mostrar_resumen()

        codigos_curso = [curso.codigoCurso for curso in cursos]
        codigo_seleccionado = Validador.seleccionar_opcion(
            "Seleccione un curso:", codigos_curso, permitir_cancelar=True
        )

        if codigo_seleccionado is None:
            return None

        for curso in cursos:
            if curso.codigoCurso == codigo_seleccionado:
                return curso

        return None

    def _seleccionar_estudiante_del_curso(self, curso: Curso) -> Optional[Estudiante]:

        if curso.total_estudiantes() == 0:
            print("\nNo existen estudiantes matriculados en este curso.")
            return None

        print("\nEstudiantes matriculados en el curso:")
        for estudiante in curso.estudiantes:
            print(f"- {estudiante.identificacion}: {estudiante.nombre}")

        identificaciones = [estudiante.identificacion for estudiante in curso.estudiantes]
        identificacion_estudiante = Validador.seleccionar_opcion(
            "Seleccione el estudiante:", identificaciones, permitir_cancelar=True
        )

        if identificacion_estudiante is None:
            return None

        return self.administrador.buscar_estudiante(identificacion_estudiante)

    def ver_estudiantes_del_curso(self) -> None:

        print("\n========== ESTUDIANTES DEL CURSO ==========\n")

        curso = self._seleccionar_curso_asignado()

        if curso is None:
            return

        self.profesor.listar_estudiantes_del_curso(curso)

    def evaluaciones_y_notas(self) -> None:
        # Menú de "Evaluaciones / Registro de Notas": selecciona curso,
        # estudiante y una de las 4 evaluaciones fijas (1er Parcial,
        # 2do Parcial, Examen Final, Recuperación) para ingresar su
        # calificación. Aquí solo se guarda la nota; el resultado de
        # si el estudiante pasó o no se anuncia en "Cerrar curso".

        print("\n========== EVALUACIONES / REGISTRO DE NOTAS ==========\n")

        curso = self._seleccionar_curso_asignado()

        if curso is None:
            return

        estudiante = self._seleccionar_estudiante_del_curso(curso)

        if estudiante is None:
            return

        boleta = curso.obtener_boleta(estudiante.identificacion)
        boleta.mostrar_boleta()

        nombre_evaluacion = Validador.seleccionar_opcion(
            "Seleccione la evaluación:", Evaluacion.NOMBRES_EVALUACIONES,
            permitir_cancelar=True
        )

        if nombre_evaluacion is None:
            return

        calificacion = Validador.leer_nota(f"Calificación de {nombre_evaluacion}: ")

        self.administrador.registrar_nota(
            estudiante, curso, nombre_evaluacion, calificacion
        )

        boleta.mostrar_boleta()

    def cerrar_curso_estudiante(self) -> None:
        # El profesor cierra el curso para un estudiante: calcula el
        # promedio final (según las 4 evaluaciones) y anuncia si pasó
        # o no. El criterio de aprobación es siempre el mismo
        # (promedio >= 7). Si el curso es el de nivelación de su
        # carrera y aprueba, pasa directo a primer semestre; si es
        # un curso regular y aprueba, puede elegir el siguiente
        # semestre.

        print("\n========== CERRAR CURSO (RESULTADO FINAL) ==========\n")

        curso = self._seleccionar_curso_asignado()

        if curso is None:
            return

        estudiante = self._seleccionar_estudiante_del_curso(curso)

        if estudiante is None:
            return

        resultado = self.administrador.procesar_resultado_final_curso(
            estudiante, curso.codigoCurso
        )

        if not resultado["tiene_notas"]:
            print("\nEste estudiante no tiene notas registradas en este curso.")
            return

        promedio = resultado["promedio"]
        print(f"\nPromedio de {estudiante.nombre} en {curso.nombreCurso}: {promedio:.2f}")

        if resultado["es_nivelacion"]:
            if resultado["aprobo"]:
                print(
                    f"\nEl estudiante {estudiante.nombre} aprobó la nivelación "
                    f"y pasa a primer semestre."
                )
            else:
                print(
                    f"\nEl estudiante {estudiante.nombre} no aprobó la "
                    f"nivelación. Debe repetirla."
                )
            return

        if resultado["aprobo"]:
            print(
                f"\nEl estudiante {estudiante.nombre} aprobó el curso "
                f"con promedio {promedio:.2f}."
            )
        else:
            print(
                f"\nEl estudiante {estudiante.nombre} no aprobó el curso "
                f"con promedio {promedio:.2f}."
            )

    def ver_evaluaciones(self) -> None:
        self.profesor.mostrar_evaluaciones()

    def editar_datos(self) -> None:

        print("\n========== EDITAR MIS DATOS ==========\n")

        self.profesor.mostrar_datos()

        print("\nDeje en blanco un campo para no modificarlo.")

        nuevo_telefono = input(f"Teléfono [{self.profesor.telefono}]: ").strip()
        if nuevo_telefono:
            self.profesor.telefono = nuevo_telefono

        nuevo_email = input(f"Email [{self.profesor.email}]: ").strip()
        if nuevo_email:
            self.profesor.email = nuevo_email

        self.administrador.actualizar_datos_profesor(self.profesor)

    def cambiar_contrasena(self) -> None:

        print("\n========== CAMBIAR CONTRASEÑA ==========\n")

        contrasena_actual = input("Contraseña actual: ")
        nueva_contrasena, confirmacion = Validador.leer_clave_nueva()

        self.administrador.cambiar_contrasena_profesor(
            self.profesor, contrasena_actual, nueva_contrasena, confirmacion
        )

    def mostrar(self) -> None:

        self.profesor.iniciar_sesion()

        while True:
            print("\n========================")
            print("MENÚ PROFESOR")
            print("========================")
            print("1. Ver datos")
            print("2. Ver cursos asignados")
            print("3. Ver estudiantes del curso")
            print("4. Evaluaciones/ Registro de Notas")
            print("5. Cerrar curso (resultado final)")
            print("6. Editar mis datos")
            print("7. Cambiar contraseña")
            print("8. Cerrar sesión")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.ver_datos()
            elif opcion == "2":
                self.ver_cursos_asignados()
            elif opcion == "3":
                self.ver_estudiantes_del_curso()
            elif opcion == "4":
                self.evaluaciones_y_notas()
            elif opcion == "5":
                self.cerrar_curso_estudiante()
            elif opcion == "6":
                self.editar_datos()
            elif opcion == "7":
                self.cambiar_contrasena()
            elif opcion == "8":
                self.profesor.cerrar_sesion()
                break
            else:
                print("\nOpción inválida")
