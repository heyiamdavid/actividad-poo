from Estudiante import Estudiante
from Profesor import Profesor

from Universidad import Universidad
from Sede import Sede
from Facultad import Facultad
from Carrera import Carrera

from Horario import Horario
from Aula import Aula

from Nivelacion import Nivelacion

from Evaluacion import Evaluacion
from Matricula import Matricula

from Reporte import Reporte

from RepositorioSQLite import RepositorioSQLite
from GestorUniversidad import GestorUniversidad

# --- Patrón creacional (Factory Method) ---
from FabricaUniversitaria import (FabricaRegimenRegular, FabricaRegimenNivelacion)

repositorio = RepositorioSQLite("universidad.db")
gestor = GestorUniversidad(repositorio)

fabrica_regular = FabricaRegimenRegular()
fabrica_nivelacion = FabricaRegimenNivelacion()


def registrar_estudiante():
    print("REGISTRO ESTUDIANTE")
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
    sede.agregar_facultad(facultad)
    universidad.agregar_sede(sede)
    estudiante = Estudiante(nombre, telefono, email, identificacion, contrasena, promedio_ingreso, promedio_graduacion, estado, modalidad)
    carrera.agregar_estudiante(estudiante)
    if promedio_ingreso < 7:
        nivelacion = Nivelacion("2026-A", 3)
        curso_nivelacion = fabrica_nivelacion.crear_curso("Matemática Básica", "A1", None)
        nivelacion.agregar_curso(curso_nivelacion)
        carrera.agregar_nivelacion(nivelacion)
        print("El estudiante requiere nivelación académica")
    gestor.registrar_estudiante(estudiante)

def registrar_profesor():
    print("REGISTRO PROFESOR")
    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    identificacion = input("Identificación: ")
    contrasena = input("Contraseña: ")
    materia = input("Materia: ")
    titulo = input("Título: ")

    profesor = Profesor(
        nombre,
        telefono,
        email,
        identificacion,
        contrasena,
        materia,
        titulo
    )
    gestor.registrar_profesor(profesor)

def menu_estudiante(estudiante):
    estudiante.iniciar_sesion()
    opciones = {
        "1": estudiante.mostrar_datos,
        "2": estudiante.consultar_cursos,
        "3": estudiante.elegir_modalidad,
        "4": estudiante.ver_notas,
    }

    while True:
        print("MENÚ ESTUDIANTE")
        print("1. Ver datos")
        print("2. Consultar cursos")
        print("3. Ver modalidad")
        print("4. Ver notas")
        print("5. Cerrar sesión")
        opcion = input("Seleccione: ")
        if opcion == "5":
            estudiante.cerrar_sesion()
            break
        accion = opciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción inválida")


def menu_profesor(profesor):
    profesor.iniciar_sesion()

    while True:
        print("MENÚ PROFESOR")
        print("1. Ver datos")
        print("2. Crear evaluación")
        print("3. Registrar nota")
        print("4. Cerrar sesión")
        opcion = input("Seleccione: ")
        if opcion == "1":
            profesor.mostrar_datos()
        elif opcion == "2":
            nombre = input("Nombre evaluación: ")
            nota = float(input("Calificación: "))

            # Creación delegada a la fábrica 
            evaluacion = fabrica_regular.crear_evaluacion(nombre, nota)
            profesor.crear_evaluacion(evaluacion)
        elif opcion == "3":
            nota = float(input("Nota: "))
            profesor.registrar_nota(nota)
        elif opcion == "4":
            profesor.cerrar_sesion()
            break
        else:
            print("Opción inválida")

def login_estudiante():
    print("LOGIN ESTUDIANTE")
    identificacion = input("Identificación: ")
    contrasena = input("Contraseña: ")
    datos = gestor.autenticar_estudiante(identificacion, contrasena)
    if not datos:
        print("Credenciales incorrectas")
        return
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

    # Creación del curso regular vía Factory Method.
    curso = fabrica_regular.crear_curso(
        "Programación",
        "SOF101",
        4
    )
    horario = Horario("Lunes", "08:00", "10:00")
    aula = Aula("A-101", 40)
    matricula = Matricula("08/06/2026", estudiante)

    # Sobrecarga de agregar_curso
    matricula.agregar_curso(curso, horario, aula)
    menu_estudiante(estudiante)

def login_profesor():
    print("LOGIN PROFESOR")
    identificacion = input("Identificación: ")
    contrasena = input("Contraseña: ")
    datos = gestor.autenticar_profesor(
        identificacion,
        contrasena
    )
    if not datos:
        print("Credenciales incorrectas")
        return

    profesor = Profesor(
        datos[1],  # nombre
        datos[2],  # telefono
        datos[3],  # email
        datos[4],  # identificacion
        datos[5],  # contrasena
        datos[6],  # materia
        datos[7]   # titulo
    )
    
    menu_profesor(profesor)

def menu_reportes():
    while True:
        print("REPORTES")
        print("1. Ver estudiantes")
        print("2. Ver profesores")
        print("3. Resumen general")
        print("4. Volver")
        opcion = input("Seleccione: ")
        if opcion == "1":
            estudiantes = gestor.listar_estudiantes()
            reporte = Reporte("Estudiantil")
            reporte.generar_reporte_estudiantil(estudiantes)
        elif opcion == "2":
            profesores = gestor.listar_profesores()
            reporte = Reporte("Profesores")
            reporte.generar_reporte_profesores(profesores)
        elif opcion == "3":
            estudiantes = gestor.listar_estudiantes()
            profesores = gestor.listar_profesores()
            reporte = Reporte("General")
            reporte.generar_reporte_general(
                estudiantes,
                profesores
            )
        elif opcion == "4":
            break
        else:
            print("Opción inválida")


def menu_principal():
    opciones = {
        "1": registrar_estudiante,
        "2": registrar_profesor,
        "3": login_estudiante,
        "4": login_profesor,
        "5": menu_reportes,
    }

    while True:

        print("SISTEMA UNIVERSITARIO")
        print("1. Registrar estudiante")
        print("2. Registrar profesor")
        print("3. Iniciar sesión estudiante")
        print("4. Iniciar sesión profesor")
        print("5. Reportes")
        print("6. Salir")

        opcion = input("Seleccione: ")
        if opcion == "6":
            print("\nPrograma finalizado")
            break
        accion = opciones.get(opcion)
        if accion:
            accion()
        else:
            print("\nOpción inválida")


if __name__ == "__main__":

    menu_principal()
