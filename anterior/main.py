from Estudiante import Estudiante
from Profesor import Profesor
from Horario import Horario
from Aula import Aula
from Matricula import Matricula
from FabricaUniversitaria import FabricaRegimenRegular, FabricaRegimenNivelacion

# 1. SELECCIÓN DE RÉGIMEN
print("\n========== SELECCIÓN DE RÉGIMEN ==========\n")
print("1. Régimen Regular (Carreras)")
print("2. Régimen de Nivelación")
opcion_regimen = input("Seleccione: ")

if opcion_regimen == "2":
    fabrica = FabricaRegimenNivelacion()
    print("-> Configurado con Nivelación.\n")
else:
    fabrica = FabricaRegimenRegular()
    print("-> Configurado con Régimen Regular.\n")


# 2. DATOS DEL ESTUDIANTE
print("\n========== ESTUDIANTE ==========\n")
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
    nombre_est, telefono_est, email_est, id_est, contra_est, 
    prom_ingreso, prom_graduacion, estado_est, modalidad_est
)


# 3. DATOS DEL PROFESOR
print("\n========== PROFESOR ==========\n")
nombre_prof = input("Nombre profesor: ")
telefono_prof = input("Teléfono profesor: ")
email_prof = input("Email profesor: ")
id_prof = input("Identificación profesor: ")
contra_prof = input("Contraseña profesor: ")
materia_prof = input("Materia: ")
titulo_prof = input("Título: ")

profesor1 = Profesor(
    nombre_prof, telefono_prof, email_prof, id_prof, contra_prof, materia_prof, titulo_prof
)


# 4. CREACIÓN DEL CURSO (Abstract Factory)
print("\n========== CURSO ==========\n")
nombreCurso = input("Nombre curso: ")

if opcion_regimen == "2":
    paralelo = input("Paralelo (ej. 'A'): ")
    curso1 = fabrica.crear_curso(nombreCurso, paralelo, profesor1)
else:
    codigoCurso = input("Código curso: ")
    creditosCurso = input("Créditos: ")
    curso1 = fabrica.crear_curso(nombreCurso, codigoCurso, creditosCurso)


# 5. HORARIO Y AULA
print("\n========== HORARIO ==========\n")
diaHorario = input("Día: ")
horaInicio = input("Hora inicio: ")
horaFin = input("Hora fin: ")
horario1 = Horario(diaHorario, horaInicio, horaFin)

print("\n========== AULA ==========\n")
numeroAula = input("Número aula: ")
capacidadAula = int(input("Capacidad aula: "))
aula1 = Aula(numeroAula, capacidadAula)

# Ejecución de métodos comunes
curso1.agregar_horario(horario1)
curso1.agregar_aula(aula1)


# 6. EVALUACIÓN (Abstract Factory)
print("\n========== EVALUACIÓN ==========\n")
nombreEval = input("Nombre evaluación: ")
notaEval = float(input("Nota: "))
evaluacion1 = fabrica.crear_evaluacion(nombreEval, notaEval)


# 7. MATRÍCULA
print("\n========== MATRÍCULA ==========\n")
fechaMatricula = input("Fecha matrícula: ")
matricula1 = Matricula(fechaMatricula, estudiante1)
matricula1.agregar_curso(curso1)


# 8. IMPRESIÓN DE RESULTADOS
print("\n========== RESULTADOS ==========\n")
estudiante1.iniciar_sesion()
profesor1.crear_evaluacion()
evaluacion1.mostrar_calificacion()
matricula1.mostrar_matricula()