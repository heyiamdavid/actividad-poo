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

# =========================
# ESTUDIANTE
# =========================

estudiante1 = Estudiante(
    "Vanessa",
    "099999999",
    "vanessa@gmail.com",
    "12345",
    "abc123",
    8.5,
    9.0,
    "Activo",
    "Virtual"
)

# =========================
# PROFESOR
# =========================

profesor1 = Profesor(
    "Stiven",
    "088888888",
    "stiven@gmail.com",
    "54321",
    "pass123",
    "Matemáticas",
    "Ingeniero"
)

# =========================
# CARRERA
# =========================

carrera1 = Carrera(
    "SOF01",
    "Software",
    "Virtual"
)

# =========================
# NIVELACION
# =========================

nivelacion1 = Nivelacion(
    "2026-A",
    4
)

# =========================
# CURSO NIVELACION
# =========================

curso_nivelacion = CursoNivelacion(
    "Matemáticas Básicas",
    "A1",
    profesor1
)

# =========================
# EVALUACION
# =========================

evaluacion1 = Evaluacion(
    "Primer Parcial",
    8
)

curso_nivelacion.agregar_evaluacion(
    evaluacion1
)

nivelacion1.agregar_curso(
    curso_nivelacion
)

carrera1.agregar_nivelacion(
    nivelacion1
)

# =========================
# CURSO NORMAL
# =========================

curso1 = Curso(
    "POO101",
    "Programación Orientada a Objetos",
    5
)

# =========================
# HORARIO
# =========================

horario1 = Horario(
    "Lunes",
    "07:00",
    "09:00"
)

curso1.agregar_horario(horario1)

# =========================
# AULA
# =========================

aula1 = Aula(
    "A-201",
    40
)

curso1.agregar_aula(aula1)

# =========================
# MATRICULA
# =========================

matricula1 = Matricula(
    "20/05/2026",
    estudiante1
)

matricula1.agregar_curso(curso1)

# =========================
# PRUEBAS
# =========================

estudiante1.iniciar_sesion()

profesor1.crear_evaluacion()

curso1.mostrar_curso()

horario1.mostrar_horario()

aula1.mostrar_aula()

evaluacion1.mostrar_calificacion()

matricula1.mostrar_matricula()

matricula1.generar_comprobante()

matricula1.generar_comprobante("WORD")