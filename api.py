from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Estudiante import Estudiante
from Profesor import Profesor
from Horario import Horario
from Aula import Aula
from Matricula import Matricula
from FabricaUniversitaria import FabricaRegimenRegular, FabricaRegimenNivelacion
from Repositorio import RepositorioMatriculas, RepositorioEstudiantes, RepositorioProfesores

app = FastAPI(title="Sistema Universitario", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias de repositorios (JSON -> futuro PostgreSQL)
repo_matriculas = RepositorioMatriculas()
repo_estudiantes = RepositorioEstudiantes()
repo_profesores = RepositorioProfesores()


class DatosMatricula(BaseModel):
    opcion_regimen: str
    estudiante: dict
    profesor: dict
    curso: dict
    horario: dict
    aula: dict
    evaluacion: dict
    fecha_matricula: str


@app.get("/")
def root():
    return {"message": "API del Sistema Universitario activa "}


@app.post("/api/matricular")
def matricular(datos: DatosMatricula):
    # Selección de fábrica
    if datos.opcion_regimen == "2":
        fabrica = FabricaRegimenNivelacion()
    else:
        fabrica = FabricaRegimenRegular()

    # --- ESTUDIANTE ---
    e = datos.estudiante
    estudiante1 = Estudiante(
        e.get('nombre', ''), e.get('telefono', ''), e.get('email', ''),
        e.get('id', ''), e.get('contra', ''),
        e.get('prom_ingreso', 0), e.get('prom_graduacion', 0),
        e.get('estado', ''), e.get('modalidad', '')
    )

    # --- PROFESOR ---
    p = datos.profesor
    profesor1 = Profesor(
        p.get('nombre', ''), p.get('telefono', ''), p.get('email', ''),
        p.get('id', ''), p.get('contra', ''),
        p.get('materia', ''), p.get('titulo', '')
    )

    # --- CURSO ---
    c = datos.curso
    if datos.opcion_regimen == "2":
        curso1 = fabrica.crear_curso(c.get('nombre', ''), c.get('paralelo', 'A'), profesor1)
    else:
        curso1 = fabrica.crear_curso(c.get('nombre', ''), c.get('codigo', '000'), c.get('creditos', '0'))

    # --- HORARIO Y AULA ---
    h = datos.horario
    horario1 = Horario(h.get('dia', ''), h.get('horaInicio', ''), h.get('horaFin', ''))
    a = datos.aula
    aula1 = Aula(a.get('numero', ''), a.get('capacidad', 0))
    curso1.agregar_horario(horario1)
    curso1.agregar_aula(aula1)

    # --- EVALUACIÓN ---
    ev = datos.evaluacion
    evaluacion1 = fabrica.crear_evaluacion(ev.get('nombre', ''), ev.get('nota', 0))

    # --- MATRÍCULA ---
    matricula1 = Matricula(datos.fecha_matricula, estudiante1)
    matricula1.agregar_curso(curso1)

    # Impresión en consola (mantiene comportamiento original)
    print("\n--- Ejecución de métodos desde API ---")
    estudiante1.iniciar_sesion()
    profesor1.crear_evaluacion()
    evaluacion1.mostrar_calificacion()
    matricula1.mostrar_matricula()
    print("--------------------------------------\n")

    # --- PERSISTENCIA EN JSON ---
    registro_estudiante = repo_estudiantes.guardar({
        "nombre": estudiante1.nombre,
        "identificacion": estudiante1.identificacion,
        "email": e.get('email', ''),
        "estado": e.get('estado', ''),
        "modalidad": e.get('modalidad', ''),
        "prom_ingreso": e.get('prom_ingreso', 0),
    })

    registro_profesor = repo_profesores.guardar({
        "nombre": profesor1.nombre,
        "identificacion": p.get('id', ''),
        "materia": profesor1.materia,
    })

    registro_matricula = repo_matriculas.guardar({
        "fecha": matricula1.fecha,
        "regimen": "Nivelación" if datos.opcion_regimen == "2" else "Regular",
        "estudiante_id": registro_estudiante["id"],
        "estudiante_nombre": estudiante1.nombre,
        "profesor_nombre": profesor1.nombre,
        "profesor_materia": profesor1.materia,
        "curso_nombre": curso1.nombreCurso,
        "curso_detalle": c.get('paralelo', c.get('codigo', '')),
        "horario": f"{h.get('dia','')} {h.get('horaInicio','')} - {h.get('horaFin','')}",
        "aula": a.get('numero', ''),
        "evaluacion_nombre": ev.get('nombre', ''),
        "evaluacion_nota": ev.get('nota', 0),
    })

    return {
        "status": "success",
        "data": {
            "estudiante": {
                "nombre": estudiante1.nombre,
                "identificacion": estudiante1.identificacion,
            },
            "profesor": {
                "nombre": profesor1.nombre,
                "materia": profesor1.materia,
            },
            "curso": {
                "nombre": curso1.nombreCurso,
                "detalle": c.get('paralelo', c.get('codigo', '')),
            },
            "evaluacion": {
                "nombre": ev.get('nombre', ''),
                "nota": ev.get('nota', 0),
            },
            "matricula": {
                "id": registro_matricula["id"],
                "fecha": matricula1.fecha,
                "estado": "Registrado correctamente ✅"
            }
        }
    }


@app.get("/api/matriculas")
def listar_matriculas():
    """Retorna todas las matrículas guardadas en JSON."""
    return repo_matriculas.obtener_todos()


@app.get("/api/estudiantes")
def listar_estudiantes():
    """Retorna todos los estudiantes guardados en JSON."""
    return repo_estudiantes.obtener_todos()
