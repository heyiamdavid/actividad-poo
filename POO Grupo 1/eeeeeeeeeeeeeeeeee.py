# ==========================================
# INTERFAZ
# ==========================================

from abc import ABC, abstractmethod


class Autenticable(ABC):

    @abstractmethod
    def iniciar_sesion(self):
        pass

    @abstractmethod
    def cerrar_sesion(self):
        pass


# ==========================================
# CLASE ABSTRACTA PERSONA
# ==========================================

class Persona(Autenticable, ABC):

    def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena):

        self.nombre = nombre
        self.telefono = telefono

        self._email = email

        self.identificacion = identificacion

        self.__contrasena = contrasena

    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, nueva_contrasena):

        if len(nueva_contrasena) >= 4:
            self.__contrasena = nueva_contrasena
        else:
            print("Contraseña inválida")

    def iniciar_sesion(self):

        print(f"{self.nombre} inició sesión")

    def cerrar_sesion(self):

        print(f"{self.nombre} cerró sesión")


# ==========================================
# ESTUDIANTE
# ==========================================

class Estudiante(Persona):

    def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena,
                 promedio_ingreso,
                 promedio_graduacion,
                 estado,
                 modalidad):

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

        self.__modalidad = modalidad

        self.__cursos = []

    @property
    def modalidad(self):
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, nueva_modalidad):

        if nueva_modalidad != "":
            self.__modalidad = nueva_modalidad
        else:
            print("Modalidad inválida")

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):

        self.__cursos.append(curso)

    def elegir_modalidad(self):

        print(f"Modalidad seleccionada: {self.__modalidad}")

    def consultar_cursos(self):

        print("\nCursos registrados:")

        for curso in self.__cursos:
            print(f"- {curso.nombreCurso}")

    def ver_notas(self):

        print("Visualizando notas...")


# ==========================================
# PROFESOR
# ==========================================

class Profesor(Persona):

    def __init__(self,
                 nombre,
                 telefono,
                 email,
                 identificacion,
                 contrasena,
                 materia,
                 titulo):

        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

        self.materia = materia
        self.titulo = titulo

        self.__notas = []

    @property
    def notas(self):
        return self.__notas

    @notas.setter
    def notas(self, nota):

        if 0 <= nota <= 10:
            self.__notas.append(nota)
        else:
            print("Nota inválida")

    def registrar_nota(self, nota):

        self.notas = nota

    def crear_evaluacion(self):

        print("Evaluación creada")

    def listar_estudiantes(self):

        print("Lista de estudiantes mostrada")


# ==========================================
# UNIVERSIDAD
# ==========================================

class Universidad:

    def __init__(self,
                 id_universidad,
                 nombreUniversidad,
                 direccion):

        self.id_universidad = id_universidad
        self.nombreUniversidad = nombreUniversidad
        self.direccion = direccion

        self.__sedes = []

    @property
    def sedes(self):
        return self.__sedes

    def agregar_sede(self, sede):

        self.__sedes.append(sede)

    def registrar_universidad(self):

        print("Universidad registrada")


# ==========================================
# SEDE
# ==========================================

class Sede:

    def __init__(self,
                 nombreSede,
                 direccion,
                 ciudad):

        self.nombreSede = nombreSede
        self.direccion = direccion
        self.ciudad = ciudad

        self.__facultades = []

    @property
    def facultades(self):
        return self.__facultades

    def agregar_facultad(self, facultad):

        self.__facultades.append(facultad)


# ==========================================
# FACULTAD
# ==========================================

class Facultad:

    def __init__(self,
                 id_facultad,
                 nombreFacultad,
                 ubicacion):

        self.id_facultad = id_facultad
        self.nombreFacultad = nombreFacultad
        self.ubicacion = ubicacion

        self.__carreras = []

    @property
    def carreras(self):
        return self.__carreras

    def agregar_carrera(self, carrera):

        self.__carreras.append(carrera)


# ==========================================
# CARRERA
# ==========================================

class Carrera:

    def __init__(self,
                 codigoCarrera,
                 nombreCarrera,
                 modalidad):

        self.codigoCarrera = codigoCarrera
        self.nombreCarrera = nombreCarrera

        self.__modalidad = modalidad

        self.__nivelaciones = []

    @property
    def modalidad(self):
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, nueva_modalidad):

        if nueva_modalidad != "":
            self.__modalidad = nueva_modalidad
        else:
            print("Modalidad inválida")

    @property
    def nivelaciones(self):
        return self.__nivelaciones

    def agregar_nivelacion(self, nivelacion):

        self.__nivelaciones.append(nivelacion)


# ==========================================
# NIVELACION
# ==========================================

class Nivelacion:

    def __init__(self,
                 periodo,
                 duracion):

        self.periodo = periodo

        self.__duracion = duracion

        self.__cursos = []

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, nueva_duracion):

        if nueva_duracion > 0:
            self.__duracion = nueva_duracion
        else:
            print("Duración inválida")

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):

        self.__cursos.append(curso)


# ==========================================
# CURSO NIVELACION
# ==========================================

class CursoNivelacion:

    def __init__(self,
                 nombreCurso,
                 paralelo,
                 profesor=None):

        self.nombreCurso = nombreCurso
        self.paralelo = paralelo

        self.profesor = profesor

        self.__evaluaciones = []

    @property
    def evaluaciones(self):
        return self.__evaluaciones

    def agregar_evaluacion(self, evaluacion):

        self.__evaluaciones.append(evaluacion)


# ==========================================
# EVALUACION
# ==========================================

class Evaluacion:

    def __init__(self,
                 nombreEvaluacion,
                 calificacion):

        self.nombreEvaluacion = nombreEvaluacion

        self.__calificacion = calificacion

    @property
    def calificacion(self):
        return self.__calificacion

    @calificacion.setter
    def calificacion(self, nueva_calificacion):

        if 0 <= nueva_calificacion <= 10:
            self.__calificacion = nueva_calificacion
        else:
            print("Calificación inválida")

    def mostrar_calificacion(self):

        print(f"Calificación: {self.__calificacion}")


# ==========================================
# CURSO
# ==========================================

class Curso:

    def __init__(self,
                 codigoCurso,
                 nombreCurso,
                 creditos):

        self.codigoCurso = codigoCurso
        self.nombreCurso = nombreCurso

        self.__creditos = creditos

        self.__horarios = []

        self.__aulas = []

    @property
    def creditos(self):
        return self.__creditos

    @creditos.setter
    def creditos(self, nuevos_creditos):

        if nuevos_creditos > 0:
            self.__creditos = nuevos_creditos
        else:
            print("Créditos inválidos")

    @property
    def horarios(self):
        return self.__horarios

    def agregar_horario(self, horario):

        self.__horarios.append(horario)

    @property
    def aulas(self):
        return self.__aulas

    def agregar_aula(self, aula):

        self.__aulas.append(aula)


# ==========================================
# HORARIO
# ==========================================

class Horario:

    def __init__(self,
                 dia,
                 hora_inicio,
                 hora_fin):

        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin


# ==========================================
# AULA
# ==========================================

class Aula:

    def __init__(self,
                 numeroAula,
                 capacidad):

        self.numeroAula = numeroAula

        self.__capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, nueva_capacidad):

        if nueva_capacidad > 0:
            self.__capacidad = nueva_capacidad
        else:
            print("Capacidad inválida")


# ==========================================
# MATRICULA
# ==========================================

class Matricula:

    def __init__(self,
                 fecha,
                 estudiante):

        self.fecha = fecha

        self.estudiante = estudiante

        self.__cursos = []

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):

        self.__cursos.append(curso)

    def mostrar_matricula(self):

        print("\n===== MATRÍCULA =====")

        print(f"Fecha: {self.fecha}")

        print(f"Estudiante: {self.estudiante.nombre}")

        print("\nCursos:")

        for curso in self.__cursos:
            print(f"- {curso.nombreCurso}")


# ==========================================
# MAIN
# ==========================================

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