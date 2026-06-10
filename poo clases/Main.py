from Estudiante import Estudiante
from Profesor import Profesor

from Universidad import Universidad
from Sede import Sede
from Facultad import Facultad
from Carrera import Carrera

from Curso import Curso
from Horario import Horario
from Aula import Aula

from Nivelacion import Nivelacion
from CursoNivelacion import CursoNivelacion

from Evaluacion import Evaluacion
from Matricula import Matricula

from Reporte import Reporte

from BaseDatos import *

crear_bd()

def registrar_estudiante():

    print("\n========== REGISTRO ESTUDIANTE ==========\n")

    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    identificacion = input("Identificación: ")
    contrasena = input("Contraseña: ")

    promedio_ingreso = float(
        input("Promedio ingreso: ")
    )

    promedio_graduacion = float(
        input("Promedio graduación: ")
    )

    estado = input("Estado: ")
    modalidad = input("Modalidad: ")

    universidad = Universidad(
        1,
        "Universidad Estatal",
        "Guayaquil"
    )

    sede = Sede(
        "Sede Central",
        "Av. Principal",
        "Guayaquil"
    )

    facultad = Facultad(
        1,
        "Ingeniería",
        "Bloque A"
    )

    carrera = Carrera(
        "SOF01",
        "Software",
        modalidad
    )

    facultad.agregar_carrera(carrera)

    sede.agregar_facultad(
        facultad
    )

    universidad.agregar_sede(
        sede
    )

    estudiante = Estudiante(
        nombre,
        telefono,
        email,
        identificacion,
        contrasena,
        promedio_ingreso,
        promedio_graduacion,
        estado,
        modalidad
    )

    carrera.agregar_estudiante(
        estudiante
    )

    if promedio_ingreso < 7:

        nivelacion = Nivelacion(
            "2026-A",
            3
        )

        curso_nivelacion = CursoNivelacion(
            "Matemática Básica",
            "A1"
        )

        nivelacion.agregar_curso(
            curso_nivelacion
        )

        carrera.agregar_nivelacion(
            nivelacion
        )

        print(
            "\nEl estudiante requiere "
            "nivelación académica"
        )

    guardar_estudiante(
        estudiante
    )

def registrar_profesor():

    print("\n========== REGISTRO PROFESOR ==========\n")

    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    identificacion = input(
        "Identificación: "
    )

    contrasena = input(
        "Contraseña: "
    )

    materia = input(
        "Materia: "
    )

    titulo = input(
        "Título: "
    )

    profesor = Profesor(
        nombre,
        telefono,
        email,
        identificacion,
        contrasena,
        materia,
        titulo
    )

    guardar_profesor(
        profesor
    )

def menu_estudiante(
        estudiante):

    estudiante.iniciar_sesion()

    while True:

        print("\n========================")
        print("MENÚ ESTUDIANTE")
        print("========================")

        print("1. Ver datos")
        print("2. Consultar cursos")
        print("3. Ver modalidad")
        print("4. Ver notas")
        print("5. Cerrar sesión")

        opcion = input(
            "\nSeleccione: "
        )

        if opcion == "1":

            estudiante.mostrar_datos()

        elif opcion == "2":

            estudiante.consultar_cursos()

        elif opcion == "3":

            estudiante.elegir_modalidad()

        elif opcion == "4":

            estudiante.ver_notas()

        elif opcion == "5":

            estudiante.cerrar_sesion()
            break

        else:

            print("Opción inválida")

def menu_profesor(
        profesor):

    profesor.iniciar_sesion()

    while True:

        print("\n========================")
        print("MENÚ PROFESOR")
        print("========================")

        print("1. Ver datos")
        print("2. Crear evaluación")
        print("3. Registrar nota")
        print("4. Cerrar sesión")

        opcion = input(
            "\nSeleccione: "
        )

        if opcion == "1":

            profesor.mostrar_datos()

        elif opcion == "2":

            nombre = input(
                "Nombre evaluación: "
            )

            nota = float(
                input("Calificación: ")
            )

            evaluacion = Evaluacion(
                nombre,
                nota
            )

            profesor.crear_evaluacion(
                evaluacion
            )

        elif opcion == "3":

            nota = float(
                input("Nota: ")
            )

            profesor.registrar_nota(
                nota
            )

        elif opcion == "4":

            profesor.cerrar_sesion()
            break

        else:

            print("Opción inválida")

def login_estudiante():

    print("\n========== LOGIN ESTUDIANTE ==========\n")

    identificacion = input(
        "Identificación: "
    )

    contrasena = input(
        "Contraseña: "
    )

    datos = validar_login_estudiante(
        identificacion,
        contrasena
    )

    if datos:

        estudiante = Estudiante(

            datos[1],  # nombre
            datos[2],  # telefono
            datos[3],  # email
            datos[4],  # identificacion
            datos[5],  # contrasena
            datos[6],  # promedio ingreso
            datos[7],  # promedio graduacion
            datos[8],  # estado
            datos[9]   # modalidad

        )

        curso = Curso(
            "SOF101",
            "Programación",
            4
        )

        horario = Horario(
            "Lunes",
            "08:00",
            "10:00"
        )

        aula = Aula(
            "A-101",
            40
        )

        curso.agregar_horario(
            horario
        )

        curso.agregar_aula(
            aula
        )

        matricula = Matricula(
            "08/06/2026",
            estudiante
        )

        matricula.agregar_curso(
            curso
        )

        menu_estudiante(
            estudiante
        )

    else:

        print(
            "\nCredenciales incorrectas"
        )

def login_profesor():

    print("\n========== LOGIN PROFESOR ==========\n")

    identificacion = input(
        "Identificación: "
    )

    contrasena = input(
        "Contraseña: "
    )

    datos = validar_login_profesor(
        identificacion,
        contrasena
    )

    if datos:

        profesor = Profesor(

            datos[1],  # nombre
            datos[2],  # telefono
            datos[3],  # email
            datos[4],  # identificacion
            datos[5],  # contrasena
            datos[6],  # materia
            datos[7]   # titulo

        )

        menu_profesor(
            profesor
        )

    else:

        print(
            "\nCredenciales incorrectas"
        )

def menu_reportes():

    while True:

        print("\n========================")
        print("REPORTES")
        print("========================")

        print("1. Ver estudiantes")
        print("2. Ver profesores")
        print("3. Resumen general")
        print("4. Volver")

        opcion = input(
            "\nSeleccione: "
        )

        if opcion == "1":

            estudiantes = (
                mostrar_estudiantes()
            )

            reporte = Reporte(
                "Estudiantil"
            )

            reporte.generar_reporte_estudiantil(
                estudiantes
            )

        elif opcion == "2":

            profesores = (
                mostrar_profesores()
            )

            reporte = Reporte(
                "Profesores"
            )

            reporte.generar_reporte_profesores(
                profesores
            )

        elif opcion == "3":

            estudiantes = (
                mostrar_estudiantes()
            )

            profesores = (
                mostrar_profesores()
            )

            reporte = Reporte(
                "General"
            )

            reporte.generar_reporte_general(
                estudiantes,
                profesores
            )

        elif opcion == "4":

            break

        else:

            print(
                "\nOpción inválida"
            )

def menu_principal():

    while True:

        print("\n=================================")
        print("SISTEMA UNIVERSITARIO")
        print("=================================")

        print("1. Registrar estudiante")
        print("2. Registrar profesor")
        print("3. Iniciar sesión estudiante")
        print("4. Iniciar sesión profesor")
        print("5. Reportes")
        print("6. Salir")

        opcion = input(
            "\nSeleccione: "
        )

        if opcion == "1":

            registrar_estudiante()

        elif opcion == "2":

            registrar_profesor()

        elif opcion == "3":

            login_estudiante()

        elif opcion == "4":

            login_profesor()

        elif opcion == "5":

            menu_reportes()

        elif opcion == "6":

            print(
                "\nPrograma finalizado"
            )

            break

        else:

            print(
                "\nOpción inválida"
            )

if __name__ == "__main__":

    menu_principal()