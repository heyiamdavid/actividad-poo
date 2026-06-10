from Estudiante import Estudiante
from Profesor import Profesor

from Carrera import Carrera
from Nivelacion import Nivelacion
from CursoNivelacion import CursoNivelacion
from Evaluacion import Evaluacion

from Curso import Curso
from Horario import Horario
from Aula import Aula
from Matricula import Matricula

print("\n========== ESTUDIANTE ==========\n")
while True:
    nombre_est = input("Nombre: ")
    telefono_est = input("Teléfono: ")
    email_est = input("Email: ")
    id_est = input("Identificación: ")
    contra_est = input("Contraseña: ")

    prom_ingreso = float(input("Promedio ingreso: "))
    prom_graduacion = float(input("Promedio graduación: "))

    estado_est = input("Estado: ")
    modalidad_est = input("Modalidad: ")

    estudiante1 = Estudiante(
        nombre_est,
        telefono_est,
        email_est,
        id_est,
        contra_est,
        prom_ingreso,
        prom_graduacion,
        estado_est,
        modalidad_est
    )

    print("\n========== PROFESOR ==========\n")

    nombre_prof = input("Nombre profesor: ")
    telefono_prof = input("Teléfono profesor: ")
    email_prof = input("Email profesor: ")
    id_prof = input("Identificación profesor: ")
    contra_prof = input("Contraseña profesor: ")

    materia_prof = input("Materia: ")
    titulo_prof = input("Título: ")

    profesor1 = Profesor(
        nombre_prof,
        telefono_prof,
        email_prof,
        id_prof,
        contra_prof,
        materia_prof,
        titulo_prof
)

    print("\n========== CURSO ==========\n")

    codigoCurso = input("Código curso: ")
    nombreCurso = input("Nombre curso: ")
    creditosCurso = int(input("Créditos: "))

    curso1 = Curso(
        codigoCurso,
        nombreCurso,
        creditosCurso
    )

    print("\n========== HORARIO ==========\n")

    diaHorario = input("Día: ")
    horaInicio = input("Hora inicio: ")
    horaFin = input("Hora fin: ")

    horario1 = Horario(
        diaHorario,
        horaInicio,
        horaFin
    )

    curso1.agregar_horario(horario1)

    print("\n========== AULA ==========\n")

    numeroAula = input("Número aula: ")
    capacidadAula = int(input("Capacidad aula: "))

    aula1 = Aula(
        numeroAula,
        capacidadAula
    )

    curso1.agregar_aula(aula1)

    print("\n========== EVALUACIÓN ==========\n")

    nombreEval = input("Nombre evaluación: ")
    notaEval = float(input("Nota: "))

    evaluacion1 = Evaluacion(
        nombreEval,
        notaEval
    )

    print("\n========== MATRÍCULA ==========\n")

    fechaMatricula = input("Fecha matrícula: ")

    matricula1 = Matricula(
        fechaMatricula,
        estudiante1
    )

    matricula1.agregar_curso(curso1)

    # ==========================================
    # RESULTADOS
    # ==========================================

    print("\n========== RESULTADOS ==========\n")

    estudiante1.iniciar_sesion()

    profesor1.crear_evaluacion()

    evaluacion1.mostrar_calificacion()

    matricula1.mostrar_matricula()