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
