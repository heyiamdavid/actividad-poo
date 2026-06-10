#class persona
from abc import ABC
from Autenticable import Autenticable

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

#class estudiante

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

#class profesor
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

#class universidad
class Universidad:

    def __init__(self, id_universidad, nombreUniversidad,
                 direccion):

        self.id_universidad = id_universidad
        self.nombreUniversidad = nombreUniversidad
        self.direccion = direccion

        self.__sedes = []       # composición
        self.__reportes = []    # agregación

    @property
    def sedes(self):
        return self.__sedes

    def agregar_sede(self, sede):
        self.__sedes.append(sede)

    @property
    def reportes(self):
        return self.__reportes

    def agregar_reporte(self, reporte):
        self.__reportes.append(reporte)

    def registrar_universidad(self):
        print(f"Universidad {self.nombreUniversidad} registrada")

    def crear_oferta(self):
        print("Oferta académica creada")

    def validar_datos(self):
        print("Datos validados")

    def validar_disponibilidad(self):
        print("Disponibilidad verificada")

#class sede
class Sede:

    def __init__(self, nombreSede, direccion,
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

    def listar_facultades(self):

        for facultad in self.__facultades:
            print(facultad.nombreFacultad)

#class facultad
class Facultad:

    def __init__(self, id_facultad,
                 nombreFacultad,
                 ubicacion):

        self.id_facultad = id_facultad
        self.nombreFacultad = nombreFacultad
        self.ubicacion = ubicacion

        self.__carreras = []
        self.__cupos = []

    @property
    def carreras(self):
        return self.__carreras

    def agregar_carrera(self, carrera):
        self.__carreras.append(carrera)

    @property
    def cupos(self):
        return self.__cupos

    def agregar_cupo(self, cupo):
        self.__cupos.append(cupo)

    def asignar_carrera(self):
        print("Carrera asignada")

    def carreras_ofertadas(self):

        for carrera in self.__carreras:
            print(carrera.nombreCarrera)

    def buscar_carreras(self, nombre):

        for carrera in self.__carreras:

            if carrera.nombreCarrera == nombre:
                return carrera

        return None
    
#class carrera
class Carrera:

    def __init__(self, codigoCarrera,
                 nombreCarrera,
                 modalidad):

        self.codigoCarrera = codigoCarrera
        self.nombreCarrera = nombreCarrera

        self.__modalidad = modalidad

        self.__nivelaciones = []
        self.__estudiantes = []

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

    @property
    def estudiantes(self):
        return self.__estudiantes

    def agregar_estudiante(self, estudiante):
        self.__estudiantes.append(estudiante)

    def mostrar_carrera(self):

        print(f"Carrera: {self.nombreCarrera}")
        print(f"Modalidad: {self.__modalidad}")

#class nivelación
class Nivelacion:

    def __init__(self,
                 periodo,
                 duracion):

        self.periodo = periodo

        self.__duracion = duracion

        self.__cursos_nivelacion = []

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
    def cursos_nivelacion(self):
        return self.__cursos_nivelacion

    def agregar_curso(self, curso):
        self.__cursos_nivelacion.append(curso)

#class curso nivelacion
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

    def asignar_profesor(self, profesor):

        self.profesor = profesor

    def mostrar_curso(self):

        print(f"Curso: {self.nombreCurso}")
        print(f"Paralelo: {self.paralelo}")

        if self.profesor:
            print(f"Profesor: {self.profesor.nombre}")
    
#class evaluacion
class Evaluacion:

    def __init__(self,
                 nombreEvaluacion,
                 calificacion=0):

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

        print(f"{self.nombreEvaluacion}: {self.__calificacion}")

    # sobrecarga con parámetro opcional
    def corregir_evaluacion(self, puntos_extra=0):

        nueva_nota = self.__calificacion + puntos_extra

        if nueva_nota > 10:
            nueva_nota = 10

        self.__calificacion = nueva_nota

        print(f"Nueva nota: {self.__calificacion}")

#class curso
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

    def mostrar_curso(self):

        print(f"Curso: {self.nombreCurso}")
        print(f"Créditos: {self.__creditos}")

#class horario
class Horario:

    def __init__(self,
                 dia,
                 hora_inicio,
                 hora_fin):

        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def mostrar_horario(self):

        print(f"{self.dia}: {self.hora_inicio} - {self.hora_fin}")

#class aula
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

    def mostrar_aula(self):

        print(f"Aula: {self.numeroAula}")
        print(f"Capacidad: {self.__capacidad}")

#class matricula
class Matricula:

    def __init__(self,
                 fecha,
                 estudiante=None):

        self.fecha = fecha

        self.estudiante = estudiante

        self.__cursos = []

    @property
    def cursos(self):
        return self.__cursos

    def agregar_curso(self, curso):
        self.__cursos.append(curso)

    def mostrar_matricula(self):

        print(f"Fecha matrícula: {self.fecha}")

        if self.estudiante:
            print(f"Estudiante: {self.estudiante.nombre}")

        print("Cursos registrados:")

        for curso in self.__cursos:
            print(curso.nombreCurso)

    # sobrecarga simple
    def generar_comprobante(self, formato="PDF"):

        print(f"Comprobante generado en formato {formato}")
#class reporte
class Reporte:

    def __init__(self, tipo, fecha_generacion):

        self.tipo = tipo
        self.fecha_generacion = fecha_generacion

    def generar_reporte_estudiantil(self):
        print("Reporte estudiantil generado")

    def generar_reporte_general(self):
        print("Reporte general generado")

#DATABASE

import sqlite3

def crear_bd():
    cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    telefono TEXT,
    email TEXT,
    identificacion TEXT,
    modalidad TEXT,
    estado TEXT
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS profesores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        telefono TEXT,
        email TEXT,
        materia TEXT,
        titulo TEXT
    )
    """)
    conexion.commit()
    conexion.close()
def guardar_profesor(nombre,
                      telefono,
                      email,
                      materia,
                      titulo):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO profesores
    (nombre,telefono,email,materia,titulo)
    VALUES(?,?,?,?,?)
    """,
    (nombre,telefono,email,materia,titulo))

    conexion.commit()
    conexion.close()
def buscar_profesor(nombre):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM profesores
    WHERE nombre = ?
    """,(nombre,))

    resultado = cursor.fetchone()

    conexion.close()

    return resultado
def mostrar_profesores():

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM profesores
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

def guardar_estudiante(
    nombre,
    telefono,
    email,
    identificacion,
    modalidad,
    estado
):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO estudiantes
    (nombre,telefono,email,identificacion,modalidad,estado)
    VALUES(?,?,?,?,?,?)
    """,
    (
        nombre,
        telefono,
        email,
        identificacion,
        modalidad,
        estado
    ))

    conexion.commit()
    conexion.close()
def buscar_estudiante(nombre):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM estudiantes
    WHERE nombre = ?
    """, (nombre,))

    estudiante = cursor.fetchone()

    conexion.close()

    return estudiante
def mostrar_estudiantes():

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM estudiantes
    """)

    estudiantes = cursor.fetchall()

    conexion.close()

    return estudiantes

conexion = sqlite3.connect("universidad.db")
cursor = conexion.cursor()


#main
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