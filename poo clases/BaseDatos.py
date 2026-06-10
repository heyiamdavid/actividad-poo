import sqlite3

def crear_bd():

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        email TEXT NOT NULL,
        identificacion TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,

        promedio_ingreso REAL,
        promedio_graduacion REAL,

        estado TEXT,
        modalidad TEXT
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

        materia TEXT,
        titulo TEXT
    )
    """)

    conexion.commit()
    conexion.close()

def guardar_estudiante(estudiante):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    try:

        cursor.execute("""
        INSERT INTO estudiantes(

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
        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (
            estudiante.nombre,
            estudiante.telefono,
            estudiante.email,
            estudiante.identificacion,
            estudiante.contrasena,
            estudiante.promedio_ingreso,
            estudiante.promedio_graduacion,
            estudiante.estado,
            estudiante.modalidad
        ))

        conexion.commit()

        print("\nEstudiante guardado correctamente")

    except sqlite3.IntegrityError:

        print(
            "\nYa existe un estudiante con "
            "esa identificación"
        )

    finally:

        conexion.close()

def guardar_profesor(profesor):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    try:

        cursor.execute("""
        INSERT INTO profesores(

            nombre,
            telefono,
            email,
            identificacion,
            contrasena,
            materia,
            titulo

        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            profesor.nombre,
            profesor.telefono,
            profesor.email,
            profesor.identificacion,
            profesor.contrasena,
            profesor.materia,
            profesor.titulo
        ))

        conexion.commit()

        print("\nProfesor guardado correctamente")

    except sqlite3.IntegrityError:

        print(
            "\nYa existe un profesor con "
            "esa identificación"
        )

    finally:

        conexion.close()

def buscar_estudiante(identificacion):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM estudiantes
    WHERE identificacion = ?
    """,
    (identificacion,))

    estudiante = cursor.fetchone()

    conexion.close()

    return estudiante

def buscar_profesor(identificacion):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM profesores
    WHERE identificacion = ?
    """,
    (identificacion,))

    profesor = cursor.fetchone()

    conexion.close()

    return profesor

def mostrar_estudiantes():

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM estudiantes
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

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

def validar_login_estudiante(
        identificacion,
        contrasena):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM estudiantes
    WHERE identificacion = ?
    AND contrasena = ?
    """,
    (
        identificacion,
        contrasena
    ))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario

def validar_login_profesor(
        identificacion,
        contrasena):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM profesores
    WHERE identificacion = ?
    AND contrasena = ?
    """,
    (
        identificacion,
        contrasena
    ))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario

def eliminar_estudiante(
        identificacion):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    DELETE FROM estudiantes
    WHERE identificacion = ?
    """,
    (identificacion,))

    conexion.commit()
    conexion.close()

def eliminar_profesor(
        identificacion):

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    DELETE FROM profesores
    WHERE identificacion = ?
    """,
    (identificacion,))

    conexion.commit()
    conexion.close()

def total_estudiantes():

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM estudiantes
    """)

    total = cursor.fetchone()[0]

    conexion.close()

    return total

def total_profesores():

    conexion = sqlite3.connect("universidad.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM profesores
    """)

    total = cursor.fetchone()[0]

    conexion.close()

    return total