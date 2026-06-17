from RepositorioSupabase import RepositorioSupabase

class FakeObj:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

repo = RepositorioSupabase()

estudiante = FakeObj(
    nombre="Juan Perez (Estudiante)",
    telefono="0999999999",
    email="juan@estudiante.edu",
    identificacion="1111111111",
    contrasena="estudiante123",
    promedio_ingreso=9.0,
    promedio_graduacion=0.0,
    estado="Activo",
    modalidad="Presencial"
)

profesor = FakeObj(
    nombre="Maria Gomez (Profesora)",
    telefono="0888888888",
    email="maria@profesor.edu",
    identificacion="2222222222",
    contrasena="profesor123",
    materia="Programacion",
    titulo="Ingeniera en Software"
)

repo.guardar_estudiante(estudiante)
repo.guardar_profesor(profesor)

print("Datos insertados con exito.")
