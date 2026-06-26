from datetime import datetime
from typing import Dict, List, Optional, Any

from RepositorioBase import RepositorioBase
from FabricaPersona import FabricaEstudiante, FabricaProfesor
from Nivelacion import Nivelacion
from Matricula import Matricula
from Universidad import Universidad
from Sede import Sede
from Facultad import Facultad
from Carrera import Carrera
from Curso import Curso
from Horario import Horario
from Aula import Aula
from Estudiante import Estudiante
from Profesor import Profesor
from Evaluacion import Evaluacion
from BoletaNotas import BoletaNotas
from DatosPredefinidos import DatosPredefinidos


# Administrador (antes GestorUniversidad) representa al Administrador
# del sistema. Recibe un RepositorioBase por Inyección de Dependencias
# y utiliza el Factory Method (FabricaEstudiante / FabricaProfesor)
# para crear a las personas que administra. También mantiene la
# estructura organizacional (Universidad -> Sede -> Facultad ->
# Carrera -> Curso), reconstruyéndola desde la base de datos en cada
# inicio para que los cambios del administrador sobrevivan reinicios.
class Administrador:

    # Credenciales fijas del administrador del sistema.
    IDENTIFICACION: str = "12346776"
    CONTRASENA: str = "Sigma67"

    ESTADOS_ESTUDIANTE: List[str] = ["Activo", "Inactivo"]
    MODALIDADES: List[str] = ["Presencial", "Semipresencial", "Virtual"]
    SEMESTRE_MAXIMO: int = 10

    def __init__(self, repositorio: RepositorioBase):
        self.__repositorio: RepositorioBase = repositorio
        self.__fabrica_estudiante: FabricaEstudiante = FabricaEstudiante()
        self.__fabrica_profesor: FabricaProfesor = FabricaProfesor()

        # Caché en memoria de los profesores que ya tienen cursos
        # asignados, para no perder esa referencia entre logins
        # (RepositorioSQLite reconstruye un objeto nuevo en cada
        # consulta a la base de datos).
        self.__profesores_con_cursos: Dict[str, Profesor] = {}

        # Caché en memoria de estudiantes ya cargados durante esta
        # ejecución (con su matrícula, cursos y notas reconstruidos),
        # para que distintas pantallas que buscan al mismo estudiante
        # compartan la misma instancia en vez de perder su estado.
        self.__estudiantes_en_memoria: Dict[str, Estudiante] = {}

        self.__universidad: Optional[Universidad] = None
        self._construir_estructura_organizacional()

    # ---------- LOGIN DEL ADMINISTRADOR ----------

    def autenticar_administrador(self, identificacion: str, contrasena: str) -> bool:

        return (
            identificacion == self.IDENTIFICACION
            and contrasena == self.CONTRASENA
        )

    # ---------- ESTRUCTURA ORGANIZACIONAL (carga inicial) ----------

    def _construir_estructura_organizacional(self) -> None:

        universidad = Universidad(1, "Uleam", "Manta")
        sede_central = Sede("Sede Central", "Av. Principal", "Manta")

        sedes_existian = bool(self.__repositorio.listar_sedes())
        facultades_existian = bool(self.__repositorio.listar_facultades())
        carreras_existian = bool(self.__repositorio.listar_carreras())

        for facultad, carreras in DatosPredefinidos.facultades_predefinidas():

            for carrera in carreras:
                facultad.agregar_carrera(carrera)

            sede_central.agregar_facultad(facultad)

        universidad.agregar_sede(sede_central)
        self.__universidad = universidad

        # Persistir la base inicial si es la primera ejecución.
        if not sedes_existian:
            self.__repositorio.guardar_sede(sede_central)

        for facultad in sede_central.facultades:

            if not facultades_existian:
                self.__repositorio.guardar_facultad("Sede Central", facultad)

            for carrera in facultad.carreras:

                if not carreras_existian:
                    self.__repositorio.guardar_carrera(facultad.id_facultad, carrera)

                self._registrar_malla_curricular(carrera)

        self._restaurar_estructura_desde_bd()

    def _registrar_malla_curricular(self, carrera: Carrera) -> None:

        # Los horarios y aulas ya existen de antemano; el estudiante
        # nunca los escribe manualmente, solo elige el curso.
        cursos_predefinidos = DatosPredefinidos.malla_curricular_por_carrera(
            carrera.codigoCarrera
        )

        # El curso de nivelación de la carrera (prefijo "Nivelación")
        # se crea junto con el resto de la malla, no dinámicamente al
        # momento de registrar a un estudiante.
        curso_nivelacion, horario_nivelacion, aula_nivelacion = (
            DatosPredefinidos.curso_nivelacion_por_carrera(
                carrera.codigoCarrera, carrera.nombreCarrera
            )
        )
        cursos_predefinidos = cursos_predefinidos + [
            (curso_nivelacion, horario_nivelacion, aula_nivelacion)
        ]

        for curso_nuevo, horario, aula in cursos_predefinidos:

            curso_existente = self.__repositorio.buscar_curso(curso_nuevo.codigoCurso)

            if curso_existente is not None:
                # El curso ya fue persistido en una ejecución anterior
                # (puede tener profesor asignado): se reconstruye desde
                # la base de datos en lugar de crear uno en blanco.
                carrera.agregar_curso(curso_existente)
                self._restaurar_relacion_profesor(curso_existente)
            else:
                curso_nuevo.asignar_horario_y_aula(horario, aula)
                carrera.agregar_curso(curso_nuevo)
                self.__repositorio.guardar_curso(curso_nuevo)

    def _restaurar_estructura_desde_bd(self) -> None:

        # Reconstruye sedes, facultades y carreras adicionales que el
        # administrador haya creado en ejecuciones anteriores (la
        # sede central y las facultades/carreras predefinidas en
        # DatosPredefinidos ya se crean arriba, por lo que se evita
        # duplicarlas).
        for nombre_sede, direccion, ciudad in self.__repositorio.listar_sedes():

            if self.__universidad.buscar_sede(nombre_sede) is None:
                self.__universidad.agregar_sede(Sede(nombre_sede, direccion, ciudad))

        for id_facultad, nombre_sede, nombre_facultad, ubicacion in self.__repositorio.listar_facultades():

            sede = self.__universidad.buscar_sede(nombre_sede)

            if sede is None:
                continue

            if sede.buscar_facultad(id_facultad) is None:
                sede.agregar_facultad(Facultad(id_facultad, nombre_facultad, ubicacion))

        for codigo_carrera, id_facultad, nombre_carrera, modalidad in self.__repositorio.listar_carreras():

            facultad = self.buscar_facultad(id_facultad)

            if facultad is None:
                continue

            if facultad.buscar_carrera(codigo_carrera) is None:
                nueva_carrera = Carrera(codigo_carrera, nombre_carrera, modalidad)
                facultad.agregar_carrera(nueva_carrera)
                self._restaurar_cursos_de_carrera(nueva_carrera)

        self._restaurar_matriculas_y_notas()

    def _restaurar_cursos_de_carrera(self, carrera: Carrera) -> None:

        # Reconstruye los cursos/materias que el administrador haya
        # creado para esta carrera en una ejecución anterior. Como
        # RepositorioSQLite no indexa cursos por carrera de forma
        # directa salvo por carrera+semestre, se recorre un rango
        # razonable de semestres, incluyendo el semestre 0
        # (nivelación), que de otro modo nunca se restauraría.
        for semestre in range(0, self.SEMESTRE_MAXIMO + 1):

            cursos = self.__repositorio.listar_cursos_por_carrera_semestre(
                carrera.codigoCarrera, semestre
            )

            for curso in cursos:
                if carrera.buscar_curso(curso.codigoCurso) is None:
                    carrera.agregar_curso(curso)
                    self._restaurar_relacion_profesor(curso)

    def _restaurar_relacion_profesor(self, curso: Curso) -> None:

        # RepositorioSQLite ya reconstruye curso.profesor a partir de
        # la base de datos. Aquí se completa la relación bidireccional
        # (profesor.cursos) y se guarda esa instancia en caché para
        # que el próximo login del profesor la conserve.
        profesor = curso.profesor

        if profesor is None:
            return

        if curso not in profesor.cursos:
            profesor.asignar_curso(curso)

        self.__profesores_con_cursos[profesor.identificacion] = profesor

    def _restaurar_matriculas_y_notas(self) -> None:

        # Reconstruye en memoria qué estudiantes están matriculados
        # en cada curso, a partir de lo persistido en SQLite, para
        # que curso.estudiantes refleje la realidad tras un reinicio.
        for estudiante in self.__repositorio.listar_estudiantes():

            matricula = self.__repositorio.listar_matricula_por_estudiante(
                estudiante.identificacion
            )

            if matricula is not None:
                for curso_matriculado in matricula.cursos:

                    curso_en_memoria = self.buscar_curso(curso_matriculado.codigoCurso)

                    if curso_en_memoria:
                        curso_en_memoria.matricular_estudiante(estudiante)
                        estudiante.agregar_curso(curso_en_memoria)

                estudiante.matricula = matricula

            for codigo_curso, evaluacion in self.__repositorio.listar_evaluaciones_por_estudiante(
                estudiante.identificacion
            ):
                curso_en_memoria = self.buscar_curso(codigo_curso)

                if curso_en_memoria:
                    boleta = curso_en_memoria.obtener_boleta(estudiante.identificacion)
                    boleta.registrar_nota(evaluacion.nombreEvaluacion, evaluacion.calificacion)

            self.__estudiantes_en_memoria[estudiante.identificacion] = estudiante

    # ---------- UNIVERSIDADES ----------

    @property
    def universidad(self) -> Optional[Universidad]:
        return self.__universidad

    def mostrar_universidad(self) -> None:
        self.__universidad.mostrar_universidad()

    # ---------- SEDES ----------

    def agregar_sede(self, nombre_sede: str, direccion: str, ciudad: str) -> Optional[Sede]:

        if self.buscar_sede(nombre_sede) is not None:
            print(f"Ya existe una sede con el nombre {nombre_sede}")
            return None

        sede = Sede(nombre_sede, direccion, ciudad)
        self.__universidad.agregar_sede(sede)
        self.__repositorio.guardar_sede(sede)
        return sede

    def eliminar_sede(self, nombre_sede: str) -> bool:

        eliminada = self.__universidad.eliminar_sede(nombre_sede)

        if eliminada:
            self.__repositorio.eliminar_sede(nombre_sede)

        return eliminada

    def listar_sedes(self) -> List[Sede]:
        return self.__universidad.sedes

    def buscar_sede(self, nombre_sede: str) -> Optional[Sede]:
        return self.__universidad.buscar_sede(nombre_sede)

    # ---------- FACULTADES ----------

    def agregar_facultad(self, nombre_sede: str, id_facultad: int,
                          nombre_facultad: str, ubicacion: str) -> Optional[Facultad]:

        sede = self.buscar_sede(nombre_sede)

        if sede is None:
            print(f"No existe la sede {nombre_sede}")
            return None

        if self.buscar_facultad(id_facultad) is not None:
            print(f"Ya existe una facultad con el ID {id_facultad}")
            return None

        facultad = Facultad(id_facultad, nombre_facultad, ubicacion)
        sede.agregar_facultad(facultad)
        self.__repositorio.guardar_facultad(nombre_sede, facultad)
        return facultad

    def eliminar_facultad(self, nombre_sede: str, id_facultad: int) -> bool:

        sede = self.buscar_sede(nombre_sede)

        if sede is None:
            print(f"No existe la sede {nombre_sede}")
            return False

        eliminada = sede.eliminar_facultad(id_facultad)

        if eliminada:
            self.__repositorio.eliminar_facultad(id_facultad)

        return eliminada

    def listar_facultades(self) -> List[Facultad]:

        facultades = []

        for sede in self.__universidad.sedes:
            facultades.extend(sede.facultades)

        return facultades

    def buscar_facultad(self, id_facultad: int) -> Optional[Facultad]:

        for sede in self.__universidad.sedes:
            facultad = sede.buscar_facultad(id_facultad)
            if facultad:
                return facultad

        return None

    # ---------- CARRERAS ----------

    def agregar_carrera(self, id_facultad: int, codigo_carrera: str,
                         nombre_carrera: str, modalidad: str) -> Optional[Carrera]:

        facultad = self.buscar_facultad(id_facultad)

        if facultad is None:
            print(f"No existe la facultad con ID {id_facultad}")
            return None

        if self.buscar_carrera(codigo_carrera) is not None:
            print(f"Ya existe una carrera con el código {codigo_carrera}")
            return None

        carrera = Carrera(codigo_carrera, nombre_carrera, modalidad)
        facultad.agregar_carrera(carrera)
        self.__repositorio.guardar_carrera(id_facultad, carrera)
        return carrera

    def eliminar_carrera(self, id_facultad: int, codigo_carrera: str) -> bool:

        facultad = self.buscar_facultad(id_facultad)

        if facultad is None:
            print(f"No existe la facultad con ID {id_facultad}")
            return False

        eliminada = facultad.eliminar_carrera(codigo_carrera)

        if eliminada:
            self.__repositorio.eliminar_carrera(codigo_carrera)

        return eliminada

    def buscar_carrera(self, codigo_carrera: str) -> Optional[Carrera]:

        for sede in self.__universidad.sedes:
            for facultad in sede.facultades:
                carrera = facultad.buscar_carrera(codigo_carrera)
                if carrera:
                    return carrera

        return None

    def carreras_disponibles(self) -> List[Carrera]:

        carreras = []

        for sede in self.__universidad.sedes:
            for facultad in sede.facultades:
                carreras.extend(facultad.carreras)

        return carreras

    def carreras_por_modalidad(self, modalidad: str) -> List[Carrera]:

        return [
            carrera for carrera in self.carreras_disponibles()
            if carrera.modalidad == modalidad
        ]

    # ---------- CURSOS / MATERIAS (administración) ----------

    def registrar_curso_en_carrera(self, codigo_carrera: str, codigo_curso: str,
                                    nombre_curso: str, creditos: int, semestre: int,
                                    dia: str, hora_inicio: str, hora_fin: str,
                                    numero_aula: str, capacidad_aula: int) -> Optional[Curso]:

        carrera = self.buscar_carrera(codigo_carrera)

        if carrera is None:
            print(f"No existe la carrera {codigo_carrera}")
            return None

        curso = Curso(codigo_curso, nombre_curso, creditos, codigo_carrera, semestre)
        horario = Horario(dia, hora_inicio, hora_fin)
        aula = Aula(numero_aula, capacidad_aula)
        curso.asignar_horario_y_aula(horario, aula)

        agregado = carrera.agregar_curso(curso)

        if not agregado:
            return None

        self.__repositorio.guardar_curso(curso)
        return curso

    def validar_semestre_para_carrera(self, codigo_carrera: str, semestre: int) -> bool:

        if not (1 <= semestre <= self.SEMESTRE_MAXIMO):
            return False

        carrera = self.buscar_carrera(codigo_carrera)

        if carrera is None:
            return False

        # Si la carrera todavía no tiene materias registradas en ese
        # semestre, no se exige coincidencia exacta (permite matricular
        # administrativamente antes de cargar la malla), pero si ya
        # existen semestres definidos, el elegido debe ser uno de ellos.
        semestres_existentes = carrera.semestres_disponibles()

        if not semestres_existentes:
            return True

        return semestre in semestres_existentes

    # ---------- ESTUDIANTES ----------

    def registrar_estudiante(self, nombre: str, telefono: str, email: str,
                              identificacion: str, contrasena: str,
                              promedio_ingreso: float, promedio_graduacion: float,
                              estado: str, modalidad: str, codigo_carrera: str,
                              semestre: Optional[int] = None) -> Estudiante:
        # Se calcula el promedio entre el promedio de ingreso y el de
        # graduación. Si ese promedio combinado es menor a 8, el
        # estudiante entra directo a nivelación (semestre 0, sin
        # matrícula regular). Si es mayor a 8, se matricula en el
        # semestre indicado (primer semestre en adelante).

        estudiante = self.__fabrica_estudiante.crear_persona(
            nombre, telefono, email, identificacion, contrasena,
            promedio_ingreso, promedio_graduacion, estado, modalidad
        )

        estudiante.carrera = codigo_carrera

        carrera_obj = self.buscar_carrera(codigo_carrera)
        if carrera_obj:
            carrera_obj.agregar_estudiante(estudiante)

        if self.requiere_nivelacion_por_ingreso(promedio_ingreso, promedio_graduacion):
            estudiante.semestre = 0
            estudiante.en_nivelacion = True
        else:
            estudiante.semestre = semestre
            estudiante.en_nivelacion = False

        self.__repositorio.guardar_estudiante(estudiante)
        self.__estudiantes_en_memoria[identificacion] = estudiante

        if estudiante.en_nivelacion and estudiante.esta_activo():
            self.matricular_en_nivelacion(estudiante)
        elif estudiante.en_nivelacion and not estudiante.esta_activo():
            print(
                f"\nEl estudiante {estudiante.nombre} está Inactivo y no "
                f"puede realizar la matrícula."
            )

        return estudiante

    def requiere_nivelacion_por_ingreso(self, promedio_ingreso: float,
                                         promedio_graduacion: float) -> bool:
        # Promedio combinado de ingreso y graduación. Menor a 8 ->
        # nivelación; mayor a 8 -> directo a primer semestre.
        promedio_combinado = (promedio_ingreso + promedio_graduacion) / 2
        return promedio_combinado < 8

    def matricular_en_nivelacion(self, estudiante: Estudiante) -> Optional[Matricula]:
        # Matricula automáticamente al estudiante en el curso de
        # nivelación de su carrera (semestre 0), sin importar el
        # código que tenga ese curso.

        carrera_obj = self.buscar_carrera(estudiante.carrera)
        curso_nivelacion = carrera_obj.curso_de_nivelacion() if carrera_obj else None

        if curso_nivelacion is None:
            print("\nNo existe un curso de nivelación configurado para esta carrera.")
            return None

        fecha = datetime.now().strftime("%d/%m/%Y")

        matricula = self.matricular(estudiante, [curso_nivelacion.codigoCurso], fecha)

        print(
            f"\nEl estudiante {estudiante.nombre} requiere nivelación "
            f"académica y fue matriculado en {curso_nivelacion.nombreCurso}."
        )

        return matricula

    def autenticar_estudiante(self, identificacion: str,
                               contrasena: str) -> Optional[Estudiante]:

        estudiante = self.__repositorio.validar_login_estudiante(identificacion, contrasena)

        if estudiante is None:
            return None

        # Si el estudiante ya está en memoria (con matrícula, cursos
        # o notas cargadas), se devuelve esa misma instancia para no
        # perder esa referencia en distintas pantallas.
        if identificacion in self.__estudiantes_en_memoria:
            return self.__estudiantes_en_memoria[identificacion]

        self.__estudiantes_en_memoria[identificacion] = estudiante
        return estudiante

    def buscar_estudiante(self, identificacion: str) -> Optional[Estudiante]:

        if identificacion in self.__estudiantes_en_memoria:
            return self.__estudiantes_en_memoria[identificacion]

        estudiante = self.__repositorio.buscar_estudiante(identificacion)

        if estudiante:
            self.__estudiantes_en_memoria[identificacion] = estudiante

        return estudiante

    def eliminar_estudiante(self, identificacion: str) -> None:

        estudiante = self.buscar_estudiante(identificacion)

        if estudiante:
            carrera_obj = self.buscar_carrera(estudiante.carrera)
            if carrera_obj:
                carrera_obj.eliminar_estudiante(identificacion)

        self.__repositorio.eliminar_estudiante(identificacion)
        self.__estudiantes_en_memoria.pop(identificacion, None)

    def listar_estudiantes(self) -> List[Estudiante]:
        return self.__repositorio.listar_estudiantes()

    def total_estudiantes(self) -> int:
        return self.__repositorio.total_estudiantes()

    def actualizar_datos_estudiante(self, estudiante: Estudiante) -> None:
        self.__repositorio.actualizar_estudiante(estudiante)

    def cambiar_contrasena_estudiante(self, estudiante: Estudiante, contrasena_actual: str,
                                       nueva_contrasena: str, confirmacion_nueva: str) -> bool:

        cambiado = estudiante.cambiar_contrasena(
            contrasena_actual, nueva_contrasena, confirmacion_nueva
        )

        if cambiado:
            self.__repositorio.actualizar_contrasena_estudiante(
                estudiante.identificacion, nueva_contrasena
            )

        return cambiado

    # ---------- PROFESORES ----------

    def registrar_profesor(self, nombre: str, telefono: str, email: str,
                            identificacion: str, contrasena: str, titulo: str) -> Profesor:

        profesor = self.__fabrica_profesor.crear_persona(
            nombre, telefono, email, identificacion, contrasena,
            titulo
        )

        self.__repositorio.guardar_profesor(profesor)

        return profesor

    def autenticar_profesor(self, identificacion: str,
                             contrasena: str) -> Optional[Profesor]:

        profesor = self.__repositorio.validar_login_profesor(identificacion, contrasena)

        if profesor is None:
            return None

        # Si el profesor ya tiene cursos asignados en memoria,
        # se devuelve esa misma instancia para no perder la
        # referencia a sus cursos.
        if identificacion in self.__profesores_con_cursos:
            return self.__profesores_con_cursos[identificacion]

        return profesor

    def buscar_profesor(self, identificacion: str) -> Optional[Profesor]:

        if identificacion in self.__profesores_con_cursos:
            return self.__profesores_con_cursos[identificacion]

        return self.__repositorio.buscar_profesor(identificacion)

    def eliminar_profesor(self, identificacion: str) -> None:
        self.__repositorio.eliminar_profesor(identificacion)
        self.__profesores_con_cursos.pop(identificacion, None)

    def listar_profesores(self) -> List[Profesor]:
        return self.__repositorio.listar_profesores()

    def total_profesores(self) -> int:
        return self.__repositorio.total_profesores()

    def actualizar_datos_profesor(self, profesor: Profesor) -> None:
        self.__repositorio.actualizar_profesor(profesor)

    def cambiar_contrasena_profesor(self, profesor: Profesor, contrasena_actual: str,
                                     nueva_contrasena: str, confirmacion_nueva: str) -> bool:

        cambiado = profesor.cambiar_contrasena(
            contrasena_actual, nueva_contrasena, confirmacion_nueva
        )

        if cambiado:
            self.__repositorio.actualizar_contrasena_profesor(
                profesor.identificacion, nueva_contrasena
            )

        return cambiado

    # ---------- CURSOS (consulta y asignación) ----------

    def asignar_curso_a_profesor(self, identificacion_profesor: str,
                                  codigo_curso: str) -> Optional[Curso]:

        profesor = self.buscar_profesor(identificacion_profesor)
        if profesor is None:
            print("No existe un profesor con esa identificación")
            return None

        curso = self.buscar_curso(codigo_curso)
        if curso is None:
            print("No existe un curso con ese código")
            return None

        profesor.asignar_curso(curso)
        self.__repositorio.guardar_curso(curso)

        # Se guarda en caché para conservar la referencia en
        # próximos logins de este mismo profesor.
        self.__profesores_con_cursos[identificacion_profesor] = profesor

        return curso

    def cursos_disponibles(self, codigo_carrera: str, semestre: int) -> List[Curso]:

        carrera_obj = self.buscar_carrera(codigo_carrera)

        if carrera_obj is None:
            return []

        return carrera_obj.cursos_por_semestre(semestre)

    def buscar_curso(self, codigo_curso: str) -> Optional[Curso]:

        for carrera in self.carreras_disponibles():
            curso = carrera.buscar_curso(codigo_curso)
            if curso:
                return curso

        return None

    def todos_los_cursos(self) -> List[Curso]:

        cursos = []

        for carrera in self.carreras_disponibles():
            cursos.extend(carrera.cursos)

        return cursos

    def cursos_de_profesor(self, identificacion_profesor: str) -> List[Curso]:

        profesor = self.buscar_profesor(identificacion_profesor)

        if profesor is None:
            return []

        return profesor.cursos

    # ---------- MATRÍCULA ----------

    def matricular(self, estudiante: Estudiante, codigos_curso: List[str],
                    fecha: str) -> Optional[Matricula]:

        if not estudiante.esta_activo():
            print(
                f"\nEl estudiante {estudiante.nombre} está Inactivo "
                f"y no puede realizar la matrícula."
            )
            return None

        matricula = Matricula(fecha, estudiante)

        for codigo_curso in codigos_curso:
            curso = self.buscar_curso(codigo_curso)

            if curso is None:
                print(f"El curso {codigo_curso} no existe")
                continue

            if not curso.pertenece_a(estudiante.carrera, estudiante.semestre):
                print(
                    f"El curso {curso.nombreCurso} no corresponde "
                    f"a tu carrera o semestre"
                )
                continue

            if not curso.tiene_cupo_disponible():
                print(
                    f"El curso {curso.nombreCurso} ya alcanzó el máximo "
                    f"de {curso.capacidad_maxima()} estudiantes. No se "
                    f"puede matricular."
                )
                continue

            matricula.agregar_curso(curso)

        self.__repositorio.guardar_matricula(matricula)
        estudiante.matricula = matricula

        return matricula

    def obtener_matricula(self, identificacion_estudiante: str) -> Optional[Matricula]:
        return self.__repositorio.listar_matricula_por_estudiante(identificacion_estudiante)

    # ---------- EVALUACIONES Y NIVELACIÓN ----------

    def registrar_nota(self, estudiante: Estudiante, curso: Curso,
                        nombre_evaluacion: str, calificacion: float) -> BoletaNotas:

        boleta = curso.obtener_boleta(estudiante.identificacion)
        registrado = boleta.registrar_nota(nombre_evaluacion, calificacion)

        if registrado:
            self.__repositorio.guardar_evaluacion(
                estudiante.identificacion, curso.codigoCurso,
                boleta.obtener_evaluacion(nombre_evaluacion)
            )

        return boleta

    def notas_de_estudiante(self, identificacion_estudiante: str) -> List[Any]:
        return self.__repositorio.listar_evaluaciones_por_estudiante(identificacion_estudiante)

    def es_curso_de_nivelacion(self, curso: Curso) -> bool:
        # Un curso es de nivelación si vive en el semestre 0, sin
        # importar qué código le haya puesto el administrador.
        return curso.semestre == 0

    def procesar_resultado_final_curso(self, estudiante: Estudiante,
                                        codigo_curso: str) -> Dict[str, Any]:
        # Calcula el promedio final del estudiante en el curso (según
        # la boleta de 4 evaluaciones) y determina si aprueba. El
        # criterio de aprobación es siempre el mismo: promedio >= 7
        # (no hay distinción entre nivelación y curso regular en este
        # punto). Si el curso es el de nivelación de su carrera y
        # aprueba, pasa a semestre 1 y "en_nivelacion" queda en False
        # para siempre.
        #
        # Devuelve un diccionario con el resultado para que el menú
        # decida qué mostrar, sin imprimir aquí mensajes de "pasó" o
        # "no pasó" (esos viven únicamente en Cerrar curso).
        curso = self.buscar_curso(codigo_curso)
        promedio = estudiante.promedio_de_curso(codigo_curso)

        if promedio is None:
            return {"tiene_notas": False}

        es_nivelacion = curso is not None and self.es_curso_de_nivelacion(curso)
        nota_minima = 7
        aprobo = promedio >= nota_minima

        resultado = {
            "tiene_notas": True,
            "promedio": promedio,
            "es_nivelacion": es_nivelacion,
            "nota_minima": nota_minima,
            "aprobo": aprobo,
        }

        if es_nivelacion and aprobo:
            estudiante.semestre = 1
            estudiante.en_nivelacion = False
            self.__repositorio.actualizar_estudiante(estudiante)

        return resultado

    def avanzar_semestre(self, estudiante: Estudiante, nuevo_semestre: int) -> bool:

        # Para avanzar de semestre solo se exige que el número esté
        # dentro del rango general (1 a SEMESTRE_MAXIMO). No se exige
        # que la carrera ya tenga materias cargadas en ese semestre,
        # porque avanzar es precisamente cómo se llega a un semestre
        # nuevo que todavía no tiene malla curricular registrada.
        if not (1 <= nuevo_semestre <= self.SEMESTRE_MAXIMO):
            print(f"\nEl semestre debe estar entre 1 y {self.SEMESTRE_MAXIMO}.")
            return False

        if nuevo_semestre <= estudiante.semestre:
            print(
                f"\nEl estudiante ya está en el semestre {estudiante.semestre}; "
                f"debe avanzar a uno mayor."
            )
            return False

        estudiante.semestre = nuevo_semestre
        self.__repositorio.actualizar_estudiante(estudiante)

        print(f"\nEl estudiante {estudiante.nombre} avanzó al semestre {nuevo_semestre}.")
        return True

    def curso_de_nivelacion_de(self, codigo_carrera: str) -> Optional[Curso]:
        # Se identifica por estar en el semestre 0 de la carrera,
        # sin asumir ningún patrón de código.
        carrera_obj = self.buscar_carrera(codigo_carrera)

        if carrera_obj is None:
            return None

        return carrera_obj.curso_de_nivelacion()
