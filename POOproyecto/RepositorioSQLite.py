import sqlite3
from typing import TYPE_CHECKING, List, Optional, Tuple

from RepositorioBase import RepositorioBase
from Estudiante import Estudiante
from Profesor import Profesor
from Curso import Curso
from Horario import Horario
from Aula import Aula
from Evaluacion import Evaluacion
from Matricula import Matricula

if TYPE_CHECKING:
    from Sede import Sede
    from Facultad import Facultad
    from Carrera import Carrera


class RepositorioSQLite(RepositorioBase):
    # Implementación concreta de RepositorioBase usando SQLite.

    def __init__(self, nombre_bd: str = "universidad.db"):
        self.nombre_bd: str = nombre_bd
        self.crear_estructura()

    def _conectar(self) -> sqlite3.Connection:
        conexion = sqlite3.connect(self.nombre_bd)
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def crear_estructura(self) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            identificacion TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            clave_temporal TEXT,
            promedio_ingreso REAL,
            promedio_graduacion REAL,
            estado TEXT,
            modalidad TEXT,
            carrera TEXT,
            semestre INTEGER,
            en_nivelacion INTEGER DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profesores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            identificacion TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            clave_temporal TEXT,
            materia TEXT,
            titulo TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cursos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_curso TEXT UNIQUE NOT NULL,
            nombre_curso TEXT NOT NULL,
            creditos INTEGER,
            carrera TEXT,
            semestre INTEGER,
            profesor_identificacion TEXT,
            dia TEXT,
            hora_inicio TEXT,
            hora_fin TEXT,
            numero_aula TEXT,
            capacidad_aula INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS matriculas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_identificacion TEXT NOT NULL,
            codigo_curso TEXT NOT NULL,
            fecha TEXT,
            UNIQUE(estudiante_identificacion, codigo_curso)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluaciones(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_identificacion TEXT NOT NULL,
            codigo_curso TEXT NOT NULL,
            nombre_evaluacion TEXT NOT NULL,
            calificacion REAL,
            UNIQUE(estudiante_identificacion, codigo_curso, nombre_evaluacion)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sedes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_sede TEXT UNIQUE NOT NULL,
            direccion TEXT,
            ciudad TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS facultades(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_facultad INTEGER UNIQUE NOT NULL,
            nombre_sede TEXT NOT NULL,
            nombre_facultad TEXT,
            ubicacion TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS carreras(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_carrera TEXT UNIQUE NOT NULL,
            id_facultad INTEGER NOT NULL,
            nombre_carrera TEXT,
            modalidad TEXT
        )
        """)

        conexion.commit()
        conexion.close()

    # ---------- ESTUDIANTES ----------

    def guardar_estudiante(self, estudiante: Estudiante) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
            INSERT INTO estudiantes(
                nombre, telefono, email, identificacion, contrasena,
                clave_temporal, promedio_ingreso, promedio_graduacion,
                estado, modalidad, carrera, semestre, en_nivelacion
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                estudiante.nombre,
                estudiante.telefono,
                estudiante.email,
                estudiante.identificacion,
                estudiante.contrasena,
                estudiante.clave_temporal,
                estudiante.promedio_ingreso,
                estudiante.promedio_graduacion,
                estudiante.estado,
                estudiante.modalidad,
                estudiante.carrera,
                estudiante.semestre,
                1 if estudiante.en_nivelacion else 0
            ))

            conexion.commit()
            print("Los datos del Estudiante se han guardado correctamente")
        except sqlite3.IntegrityError:
            print("Ya existe un estudiante con esa identificación")
        finally:
            conexion.close()

    def _fila_a_estudiante(self, fila: Optional[Tuple]) -> Optional[Estudiante]:
        if fila is None:
            return None

        estudiante = Estudiante(
            nombre=fila[1],
            telefono=fila[2],
            email=fila[3],
            identificacion=fila[4],
            contrasena=fila[5],
            promedio_ingreso=fila[7],
            promedio_graduacion=fila[8],
            estado=fila[9],
            modalidad=fila[10],
            carrera=fila[11],
            semestre=fila[12]
        )

        # La clave temporal original puede diferir de la contraseña
        # actual si la persona ya cambió su clave. Se restaura tal
        # cual está en la base de datos en vez de la que el
        # constructor fija por defecto (igual a la contraseña actual).
        clave_temporal_guardada = fila[6]
        if clave_temporal_guardada:
            estudiante._Persona__clave_temporal = clave_temporal_guardada

        estudiante.en_nivelacion = bool(fila[13]) if len(fila) > 13 else False

        return estudiante

    def buscar_estudiante(self, identificacion: str) -> Optional[Estudiante]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM estudiantes WHERE identificacion = ?
        """, (identificacion,))
        fila = cursor.fetchone()
        conexion.close()
        return self._fila_a_estudiante(fila)

    def validar_login_estudiante(self, identificacion: str,
                                  contrasena: str) -> Optional[Estudiante]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM estudiantes
        WHERE identificacion = ? AND contrasena = ?
        """, (identificacion, contrasena))
        fila = cursor.fetchone()
        conexion.close()
        return self._fila_a_estudiante(fila)

    def listar_estudiantes(self) -> List[Estudiante]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM estudiantes")
        filas = cursor.fetchall()
        conexion.close()
        return [self._fila_a_estudiante(fila) for fila in filas]

    def eliminar_estudiante(self, identificacion: str) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        DELETE FROM estudiantes WHERE identificacion = ?
        """, (identificacion,))
        conexion.commit()
        conexion.close()

    def total_estudiantes(self) -> int:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM estudiantes")
        total = cursor.fetchone()[0]
        conexion.close()
        return total

    def actualizar_estudiante(self, estudiante: Estudiante) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        UPDATE estudiantes SET
            nombre = ?, telefono = ?, email = ?,
            promedio_ingreso = ?, promedio_graduacion = ?,
            estado = ?, modalidad = ?, carrera = ?, semestre = ?,
            en_nivelacion = ?
        WHERE identificacion = ?
        """,
        (
            estudiante.nombre,
            estudiante.telefono,
            estudiante.email,
            estudiante.promedio_ingreso,
            estudiante.promedio_graduacion,
            estudiante.estado,
            estudiante.modalidad,
            estudiante.carrera,
            estudiante.semestre,
            1 if estudiante.en_nivelacion else 0,
            estudiante.identificacion
        ))
        conexion.commit()
        conexion.close()
        print("\nDatos del estudiante actualizados correctamente")

    def actualizar_contrasena_estudiante(self, identificacion: str,
                                          nueva_contrasena: str) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        UPDATE estudiantes SET contrasena = ? WHERE identificacion = ?
        """, (nueva_contrasena, identificacion))
        conexion.commit()
        conexion.close()

    # ---------- PROFESORES ----------

    def guardar_profesor(self, profesor: Profesor) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
            INSERT INTO profesores(
                nombre, telefono, email, identificacion, contrasena,
                clave_temporal, materia, titulo
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                profesor.nombre,
                profesor.telefono,
                profesor.email,
                profesor.identificacion,
                profesor.contrasena,
                profesor.clave_temporal,
                profesor.materia,
                profesor.titulo
            ))

            conexion.commit()
            print("\nProfesor guardado correctamente")
        except sqlite3.IntegrityError:
            print("Ya existe un profesor con esa identificación")
        finally:
            conexion.close()

    def _fila_a_profesor(self, fila: Optional[Tuple]) -> Optional[Profesor]:
        if fila is None:
            return None

        profesor = Profesor(
            nombre=fila[1],
            telefono=fila[2],
            email=fila[3],
            identificacion=fila[4],
            contrasena=fila[5],
            materia=fila[7],
            titulo=fila[8]
        )

        clave_temporal_guardada = fila[6]
        if clave_temporal_guardada:
            profesor._Persona__clave_temporal = clave_temporal_guardada

        return profesor

    def buscar_profesor(self, identificacion: str) -> Optional[Profesor]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM profesores WHERE identificacion = ?
        """, (identificacion,))
        fila = cursor.fetchone()
        conexion.close()
        return self._fila_a_profesor(fila)

    def validar_login_profesor(self, identificacion: str,
                                contrasena: str) -> Optional[Profesor]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM profesores
        WHERE identificacion = ? AND contrasena = ?
        """, (identificacion, contrasena))
        fila = cursor.fetchone()
        conexion.close()
        return self._fila_a_profesor(fila)

    def listar_profesores(self) -> List[Profesor]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM profesores")
        filas = cursor.fetchall()
        conexion.close()
        return [self._fila_a_profesor(fila) for fila in filas]

    def eliminar_profesor(self, identificacion: str) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        DELETE FROM profesores WHERE identificacion = ?
        """, (identificacion,))
        conexion.commit()
        conexion.close()

    def total_profesores(self) -> int:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM profesores")
        total = cursor.fetchone()[0]
        conexion.close()
        return total

    def actualizar_profesor(self, profesor: Profesor) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        UPDATE profesores SET
            nombre = ?, telefono = ?, email = ?, materia = ?, titulo = ?
        WHERE identificacion = ?
        """,
        (
            profesor.nombre,
            profesor.telefono,
            profesor.email,
            profesor.materia,
            profesor.titulo,
            profesor.identificacion
        ))
        conexion.commit()
        conexion.close()
        print("\nDatos del profesor actualizados correctamente")

    def actualizar_contrasena_profesor(self, identificacion: str,
                                        nueva_contrasena: str) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        UPDATE profesores SET contrasena = ? WHERE identificacion = ?
        """, (nueva_contrasena, identificacion))
        conexion.commit()
        conexion.close()

    # ---------- CURSOS ----------

    def guardar_curso(self, curso: Curso) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()

        horario = curso.horarios[0] if curso.horarios else None
        aula = curso.aulas[0] if curso.aulas else None

        cursor.execute("""
        INSERT INTO cursos(
            codigo_curso, nombre_curso, creditos, carrera, semestre,
            profesor_identificacion, dia, hora_inicio, hora_fin,
            numero_aula, capacidad_aula
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(codigo_curso) DO UPDATE SET
            nombre_curso = excluded.nombre_curso,
            creditos = excluded.creditos,
            carrera = excluded.carrera,
            semestre = excluded.semestre,
            profesor_identificacion = excluded.profesor_identificacion,
            dia = excluded.dia,
            hora_inicio = excluded.hora_inicio,
            hora_fin = excluded.hora_fin,
            numero_aula = excluded.numero_aula,
            capacidad_aula = excluded.capacidad_aula
        """,
        (
            curso.codigoCurso,
            curso.nombreCurso,
            curso.creditos,
            curso.carrera,
            curso.semestre,
            curso.profesor.identificacion if curso.profesor else None,
            horario.dia if horario else None,
            horario.hora_inicio if horario else None,
            horario.hora_fin if horario else None,
            aula.numeroAula if aula else None,
            aula.capacidad if aula else None
        ))

        conexion.commit()
        conexion.close()
        print(f"Curso {curso.nombreCurso} guardado correctamente")

    def _fila_a_curso(self, fila: Optional[Tuple]) -> Optional[Curso]:
        if fila is None:
            return None

        curso = Curso(
            codigoCurso=fila[1],
            nombreCurso=fila[2],
            creditos=fila[3],
            carrera=fila[4],
            semestre=fila[5]
        )

        profesor_identificacion = fila[6]
        if profesor_identificacion:
            profesor = self.buscar_profesor(profesor_identificacion)
            if profesor:
                curso.asignar_profesor(profesor)

        dia, hora_inicio, hora_fin = fila[7], fila[8], fila[9]
        numero_aula, capacidad_aula = fila[10], fila[11]

        if dia and numero_aula:
            horario = Horario(dia, hora_inicio, hora_fin)
            aula = Aula(numero_aula, capacidad_aula)
            curso.asignar_horario_y_aula(horario, aula)

        return curso

    def listar_cursos_por_carrera_semestre(self, carrera: str,
                                            semestre: int) -> List[Curso]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM cursos WHERE carrera = ? AND semestre = ?
        """, (carrera, semestre))
        filas = cursor.fetchall()
        conexion.close()
        return [self._fila_a_curso(fila) for fila in filas]

    def buscar_curso(self, codigo_curso: str) -> Optional[Curso]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM cursos WHERE codigo_curso = ?
        """, (codigo_curso,))
        fila = cursor.fetchone()
        conexion.close()
        return self._fila_a_curso(fila)

    # ---------- MATRÍCULA ----------

    def guardar_matricula(self, matricula: Matricula) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()

        for curso in matricula.cursos:
            try:
                cursor.execute("""
                INSERT INTO matriculas(
                    estudiante_identificacion, codigo_curso, fecha
                )
                VALUES(?,?,?)
                """,
                (
                    matricula.estudiante.identificacion,
                    curso.codigoCurso,
                    matricula.fecha
                ))
            except sqlite3.IntegrityError:
                print(f"El curso {curso.nombreCurso} ya estaba matriculado")

        conexion.commit()
        conexion.close()
        print("\nMatrícula guardada correctamente")

    def listar_matricula_por_estudiante(self, identificacion_estudiante: str) -> Optional[Matricula]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT codigo_curso, fecha FROM matriculas
        WHERE estudiante_identificacion = ?
        """, (identificacion_estudiante,))
        filas = cursor.fetchall()
        conexion.close()

        cursos_matriculados = []
        fecha_matricula = None

        for codigo_curso, fecha in filas:
            curso = self.buscar_curso(codigo_curso)
            if curso:
                cursos_matriculados.append(curso)
            fecha_matricula = fecha

        if not cursos_matriculados:
            return None

        estudiante = self.buscar_estudiante(identificacion_estudiante)
        matricula = Matricula(fecha_matricula, estudiante)

        for curso in cursos_matriculados:
            matricula.cursos.append(curso)

        return matricula

    # ---------- EVALUACIONES ----------

    def guardar_evaluacion(self, identificacion_estudiante: str, codigo_curso: str,
                            evaluacion: Evaluacion) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO evaluaciones(
            estudiante_identificacion, codigo_curso,
            nombre_evaluacion, calificacion
        )
        VALUES(?,?,?,?)
        ON CONFLICT(estudiante_identificacion, codigo_curso, nombre_evaluacion)
        DO UPDATE SET calificacion = excluded.calificacion
        """,
        (
            identificacion_estudiante,
            codigo_curso,
            evaluacion.nombreEvaluacion,
            evaluacion.calificacion
        ))

        conexion.commit()
        conexion.close()
        print("\nNota guardada correctamente")

    def listar_evaluaciones_por_estudiante(
        self, identificacion_estudiante: str
    ) -> List[Tuple[str, Evaluacion]]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT codigo_curso, nombre_evaluacion, calificacion
        FROM evaluaciones
        WHERE estudiante_identificacion = ?
        """, (identificacion_estudiante,))
        filas = cursor.fetchall()
        conexion.close()

        return [
            (codigo_curso, Evaluacion(nombre_evaluacion, calificacion))
            for codigo_curso, nombre_evaluacion, calificacion in filas
        ]

    # ---------- ESTRUCTURA ORGANIZACIONAL ----------

    def guardar_sede(self, sede: "Sede") -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
            INSERT INTO sedes(nombre_sede, direccion, ciudad)
            VALUES(?,?,?)
            """, (sede.nombreSede, sede.direccion, sede.ciudad))
            conexion.commit()
        except sqlite3.IntegrityError:
            print(f"Ya existe una sede con el nombre {sede.nombreSede}")
        finally:
            conexion.close()

    def listar_sedes(self) -> List[Tuple]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre_sede, direccion, ciudad FROM sedes")
        filas = cursor.fetchall()
        conexion.close()
        return filas

    def eliminar_sede(self, nombre_sede: str) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM sedes WHERE nombre_sede = ?", (nombre_sede,))
        conexion.commit()
        conexion.close()

    def guardar_facultad(self, nombre_sede: str, facultad: "Facultad") -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
            INSERT INTO facultades(id_facultad, nombre_sede, nombre_facultad, ubicacion)
            VALUES(?,?,?,?)
            """, (facultad.id_facultad, nombre_sede, facultad.nombreFacultad, facultad.ubicacion))
            conexion.commit()
        except sqlite3.IntegrityError:
            print(f"Ya existe una facultad con el ID {facultad.id_facultad}")
        finally:
            conexion.close()

    def listar_facultades(self) -> List[Tuple]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_facultad, nombre_sede, nombre_facultad, ubicacion FROM facultades"
        )
        filas = cursor.fetchall()
        conexion.close()
        return filas

    def eliminar_facultad(self, id_facultad: int) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM facultades WHERE id_facultad = ?", (id_facultad,))
        conexion.commit()
        conexion.close()

    def guardar_carrera(self, id_facultad: int, carrera: "Carrera") -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
            INSERT INTO carreras(codigo_carrera, id_facultad, nombre_carrera, modalidad)
            VALUES(?,?,?,?)
            """, (carrera.codigoCarrera, id_facultad, carrera.nombreCarrera, carrera.modalidad))
            conexion.commit()
        except sqlite3.IntegrityError:
            print(f"Ya existe una carrera con el código {carrera.codigoCarrera}")
        finally:
            conexion.close()

    def listar_carreras(self) -> List[Tuple]:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT codigo_carrera, id_facultad, nombre_carrera, modalidad FROM carreras"
        )
        filas = cursor.fetchall()
        conexion.close()
        return filas

    def eliminar_carrera(self, codigo_carrera: str) -> None:
        conexion = self._conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM carreras WHERE codigo_carrera = ?", (codigo_carrera,))
        conexion.commit()
        conexion.close()
