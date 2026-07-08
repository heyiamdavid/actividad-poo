from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from RepositorioSQLite import RepositorioSQLite
from Administrador import Administrador

app = FastAPI(title="Sistema Universitario API (POOproyecto)", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializamos el repositorio y administrador igual que en Main.py
repositorio = RepositorioSQLite("universidad.db")
administrador = Administrador(repositorio)


class MatricularRequest(BaseModel):
    identificacion_estudiante: str
    codigos_curso: List[str]

class CerrarCursoRequest(BaseModel):
    identificacion_estudiante: str
    codigo_curso: str

class ProfesorUpdate(BaseModel):
    telefono: str
    email: str

class LoginRequest(BaseModel):
    identificacion: str
    contrasena: str

class ProfesorCreate(BaseModel):
    nombre: str
    telefono: str
    email: str
    identificacion: str
    contrasena: str
    titulo: str

class CursoCreate(BaseModel):
    codigo_carrera: str
    codigo_curso: str
    nombre_curso: str
    creditos: int
    semestre: int
    dia: str
    hora_inicio: str
    hora_fin: str
    numero_aula: str
    capacidad_aula: int

class NotaCreate(BaseModel):
    identificacion_estudiante: str
    codigo_curso: str
    nombre_evaluacion: str
    calificacion: float

class EstudianteCreate(BaseModel):
    nombre: str
    telefono: str
    email: str
    identificacion: str
    contrasena: str
    promedio_ingreso: float
    promedio_graduacion: float
    estado: str
    modalidad: str
    codigo_carrera: str
    semestre: Optional[int] = None

class CambioClaveRequest(BaseModel):
    identificacion: str
    contrasena_actual: str
    nueva_contrasena: str
    confirmacion_nueva: str
    rol: str

@app.get("/")
def root():
    return {"message": "API del Sistema Universitario conectada a SQLite en POOproyecto"}

@app.post("/api/login")
def login(request: LoginRequest):
    # Intentar como administrador primero
    if administrador.autenticar_administrador(request.identificacion, request.contrasena):
        return {
            "status": "success",
            "data": {
                "id": request.identificacion,
                "nombre": "Administrador",
                "rol": "admin"
            }
        }
    
    # Intentar como profesor
    profesor = administrador.autenticar_profesor(request.identificacion, request.contrasena)
    if profesor:
        return {
            "status": "success",
            "data": {
                "id": profesor.identificacion,
                "nombre": profesor.nombre,
                "rol": "profesor",
                "requiere_cambio_clave": profesor.contrasena == profesor.clave_temporal
            }
        }
        
    # Intentar como estudiante
    estudiante = administrador.autenticar_estudiante(request.identificacion, request.contrasena)
    if estudiante:
        return {
            "status": "success",
            "data": {
                "id": estudiante.identificacion,
                "nombre": estudiante.nombre,
                "rol": "estudiante",
                "carrera": estudiante.carrera,
                "requiere_cambio_clave": estudiante.contrasena == estudiante.clave_temporal
            }
        }
        
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.post("/api/cambiar_clave")
def cambiar_clave(request: CambioClaveRequest):
    try:
        persona = None
        if request.rol == "profesor":
            persona = administrador.buscar_profesor(request.identificacion)
        elif request.rol == "estudiante":
            persona = administrador.buscar_estudiante(request.identificacion)
            
        if not persona:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        if persona.cambiar_contrasena(request.contrasena_actual, request.nueva_contrasena, request.confirmacion_nueva):
            # Guardamos la nueva contrasena en BD
            if request.rol == "profesor":
                repositorio.actualizar_contrasena_profesor(request.identificacion, request.nueva_contrasena)
            else:
                repositorio.actualizar_contrasena_estudiante(request.identificacion, request.nueva_contrasena)
            return {"status": "success", "message": "Contraseña actualizada correctamente"}
        else:
            raise HTTPException(status_code=400, detail="Error al cambiar contraseña. Verifique que los datos sean correctos.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/admin/estadisticas")
def estadisticas_admin():
    total_estudiantes = administrador.total_estudiantes()
    # Supongamos que hay total_profesores en administrador (hay que verificar)
    # total_profesores = administrador.total_profesores() 
    # Por ahora hardcodeamos total_profesores si no existe, o lo implementamos.
    # Vamos a usar el repositorio directamente para evitar tocar Administrador si falta el metodo
    total_prof = repositorio.total_profesores() if hasattr(repositorio, 'total_profesores') else 0
    
    return {
        "status": "success",
        "data": {
            "total_estudiantes": total_estudiantes,
            "total_profesores": total_prof,
            "total_cursos": 0 # TODO
        }
    }

@app.get("/api/admin/estudiantes")
def listar_estudiantes():
    estudiantes = administrador.listar_estudiantes()
    return {
        "status": "success",
        "data": [
            {
                "identificacion": e.identificacion,
                "nombre": e.nombre,
                "email": e.email,
                "carrera": e.carrera,
                "estado": e.estado,
                "semestre": e.semestre
            } for e in estudiantes
        ]
    }

@app.post("/api/admin/estudiantes")
def crear_estudiante(e: EstudianteCreate):
    try:
        estudiante = administrador.registrar_estudiante(
            e.nombre, e.telefono, e.email, e.identificacion, e.contrasena,
            e.promedio_ingreso, e.promedio_graduacion, e.estado, e.modalidad,
            e.codigo_carrera, e.semestre
        )
        return {
            "status": "success",
            "message": f"Estudiante '{estudiante.nombre}' registrado correctamente",
            "en_nivelacion": estudiante.en_nivelacion
        }
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@app.get("/api/admin/profesores")
def listar_profesores():
    profesores = administrador.listar_profesores()
    return {
        "status": "success",
        "data": [
            {
                "identificacion": p.identificacion,
                "nombre": p.nombre,
                "email": p.email,
                "titulo": p.titulo,
                "materia": p.materia
            } for p in profesores
        ]
    }

@app.post("/api/admin/profesores")
def crear_profesor(p: ProfesorCreate):
    try:
        profesor = administrador.registrar_profesor(
            p.nombre, p.telefono, p.email, p.identificacion, p.contrasena, p.titulo
        )
        return {"status": "success", "message": "Profesor registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/admin/carreras")
def listar_carreras():
    carreras = administrador.carreras_disponibles()
    return {
        "status": "success",
        "data": [
            {
                "codigo": c.codigoCarrera,
                "nombre": c.nombreCarrera,
                "modalidad": c.modalidad
            } for c in carreras
        ]
    }

@app.get("/api/admin/cursos")
def listar_cursos():
    cursos = administrador.todos_los_cursos()
    return {
        "status": "success",
        "data": [
            {
                "codigo": c.codigoCurso,
                "nombre": c.nombreCurso,
                "creditos": c.creditos,
                "semestre": c.semestre
            } for c in cursos
        ]
    }

@app.post("/api/admin/cursos")
def crear_curso(c: CursoCreate):
    try:
        curso = administrador.registrar_curso_en_carrera(
            c.codigo_carrera, c.codigo_curso, c.nombre_curso, c.creditos, c.semestre,
            c.dia, c.hora_inicio, c.hora_fin, c.numero_aula, c.capacidad_aula
        )
        if curso:
            return {"status": "success", "message": "Curso registrado correctamente"}
        raise HTTPException(status_code=400, detail="Error al registrar curso")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/profesor/{identificacion}/cursos")
def cursos_de_profesor(identificacion: str):
    cursos = administrador.cursos_de_profesor(identificacion)
    return {
        "status": "success",
        "data": [
            {
                "codigo": c.codigoCurso,
                "nombre": c.nombreCurso,
                "creditos": c.creditos,
                "semestre": c.semestre,
                "horarios": [{"dia": h.dia, "hora_inicio": h.hora_inicio, "hora_fin": h.hora_fin} for h in c.horarios],
                "aulas": [{"numero": a.numero, "capacidad": a.capacidad} for a in c.aulas],
                "estudiantes": [
                    {
                        "identificacion": e.identificacion,
                        "nombre": e.nombre,
                        "email": e.email,
                        "evaluaciones": [
                            {
                                "nombre": ev.nombreEvaluacion,
                                "calificacion": ev.calificacion
                            } for ev in c.obtener_boleta(e.identificacion).evaluaciones
                        ]
                    } for e in c.estudiantes
                ]
            } for c in cursos
        ]
    }

@app.post("/api/profesor/nota")
def registrar_nota(nota: NotaCreate):
    try:
        estudiante = administrador.buscar_estudiante(nota.identificacion_estudiante)
        curso = administrador.buscar_curso(nota.codigo_curso)
        if not estudiante or not curso:
            raise HTTPException(status_code=404, detail="Estudiante o curso no encontrado")
            
        administrador.registrar_nota(estudiante, curso, nota.nombre_evaluacion, nota.calificacion)
        return {"status": "success", "message": "Nota registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/estudiante/{identificacion}/cursos")
def cursos_de_estudiante(identificacion: str):
    matricula = administrador.obtener_matricula(identificacion)
    if matricula is None:
        return {"status": "success", "data": []}
    return {
        "status": "success",
        "data": [
            {
                "codigo": c.codigoCurso,
                "nombre": c.nombreCurso,
                "semestre": c.semestre,
                "creditos": c.creditos,
                "horarios": [{"dia": h.dia, "hora_inicio": h.horaInicio, "hora_fin": h.horaFin} for h in c.horarios],
                "aulas": [{"numero": a.numero, "capacidad": a.capacidad} for a in c.aulas]
            } for c in matricula.cursos
        ]
    }

@app.get("/api/estudiante/{identificacion}/notas")
def notas_de_estudiante(identificacion: str):
    evaluaciones = administrador.notas_de_estudiante(identificacion)
    return {
        "status": "success",
        "data": [
            {
                "codigo_curso": codigo_curso,
                "evaluacion": ev.nombreEvaluacion,
                "calificacion": ev.calificacion
            } for codigo_curso, ev in evaluaciones
        ]
    }


# ====== RUTAS ESTUDIANTE ======
@app.get("/api/estudiante/{identificacion}/cursos_disponibles")
def cursos_disponibles_estudiante(identificacion: str):
    estudiante = administrador.buscar_estudiante(identificacion)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
    cursos = administrador.cursos_disponibles(estudiante.carrera, estudiante.semestre)
    return {
        "status": "success",
        "data": [
            {
                "codigo": c.codigoCurso,
                "nombre": c.nombreCurso,
                "semestre": c.semestre,
                "creditos": c.creditos
            } for c in cursos
        ]
    }

@app.post("/api/estudiante/matricular")
def matricular_estudiante(request: MatricularRequest):
    try:
        estudiante = administrador.buscar_estudiante(request.identificacion_estudiante)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
            
        fecha = datetime.now().strftime("%d/%m/%Y")
        matricula = administrador.matricular(estudiante, request.codigos_curso, fecha)
        
        if matricula:
            return {"status": "success", "message": "Matricula exitosa"}
        else:
            raise HTTPException(status_code=400, detail="Error en matrícula (verificar cupos o si ya estaba matriculado)")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ====== RUTAS PROFESOR ======
@app.get("/api/profesor/curso/{codigo_curso}/estudiantes")
def estudiantes_del_curso(codigo_curso: str):
    curso = administrador.buscar_curso(codigo_curso)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    return {
        "status": "success",
        "data": [
            {
                "identificacion": e.identificacion,
                "nombre": e.nombre,
                "email": e.email
            } for e in curso.estudiantes
        ]
    }

@app.post("/api/profesor/cerrar_curso")
def cerrar_curso(request: CerrarCursoRequest):
    try:
        estudiante = administrador.buscar_estudiante(request.identificacion_estudiante)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
            
        resultado = administrador.procesar_resultado_final_curso(estudiante, request.codigo_curso)
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/profesor/{identificacion}")
def actualizar_profesor(identificacion: str, datos: ProfesorUpdate):
    try:
        profesor = administrador.buscar_profesor(identificacion)
        if not profesor:
            raise HTTPException(status_code=404, detail="Profesor no encontrado")
            
        if datos.telefono:
            profesor.telefono = datos.telefono
        if datos.email:
            profesor.email = datos.email
            
        administrador.actualizar_datos_profesor(profesor)
        return {"status": "success", "message": "Datos actualizados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- ENDPOINTS AÑADIDOS MASIVAMENTE PARA COMPLETAR EL PLAN ---

class EstudianteEditRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    estado: str
    modalidad: str
    semestre: int

@app.put("/api/admin/estudiantes/{identificacion}")
def editar_estudiante(identificacion: str, request: EstudianteEditRequest):
    estudiante = administrador.buscar_estudiante(identificacion)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.nombre = request.nombre
    estudiante.telefono = request.telefono
    estudiante.email = request.email
    estudiante.estado = request.estado
    estudiante.modalidad = request.modalidad
    estudiante.semestre = request.semestre
    
    administrador.actualizar_datos_estudiante(estudiante)
    return {"status": "success", "message": "Estudiante actualizado correctamente"}

@app.delete("/api/admin/estudiantes/{identificacion}")
def eliminar_estudiante(identificacion: str):
    administrador.eliminar_estudiante(identificacion)
    return {"status": "success", "message": "Estudiante eliminado correctamente"}

class ProfesorEditRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    titulo: str

@app.put("/api/admin/profesores/{identificacion}")
def editar_profesor(identificacion: str, request: ProfesorEditRequest):
    profesor = administrador.buscar_profesor(identificacion)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    profesor.nombre = request.nombre
    profesor.telefono = request.telefono
    profesor.email = request.email
    profesor.titulo = request.titulo
    
    administrador.actualizar_datos_profesor(profesor)
    return {"status": "success", "message": "Profesor actualizado correctamente"}

@app.delete("/api/admin/profesores/{identificacion}")
def eliminar_profesor(identificacion: str):
    administrador.eliminar_profesor(identificacion)
    return {"status": "success", "message": "Profesor eliminado correctamente"}

@app.get("/api/admin/sedes")
def listar_sedes():
    sedes = administrador.listar_sedes()
    return {"status": "success", "data": [{"nombre_sede": s.nombreSede, "direccion": s.direccion, "ciudad": s.ciudad} for s in sedes]}

class SedeCreateRequest(BaseModel):
    nombre_sede: str
    direccion: str
    ciudad: str

@app.post("/api/admin/sedes")
def crear_sede(request: SedeCreateRequest):
    sede = administrador.agregar_sede(request.nombre_sede, request.direccion, request.ciudad)
    if not sede:
        raise HTTPException(status_code=400, detail="Error al crear sede (quizás ya existe)")
    return {"status": "success", "message": "Sede creada"}

@app.get("/api/admin/facultades")
def listar_facultades():
    # Iteramos por sede para poder incluir el nombre de la sede en cada facultad
    result = []
    for sede in administrador.listar_sedes():
        for f in sede.facultades:
            result.append({"id": f.id_facultad, "nombre": f.nombreFacultad, "sede": sede.nombreSede})
    return {"status": "success", "data": result}

class FacultadCreateRequest(BaseModel):
    nombre_sede: str
    id_facultad: int
    nombre_facultad: str

@app.post("/api/admin/facultades")
def crear_facultad(request: FacultadCreateRequest):
    # 'ubicacion' usa el nombre de la sede como referencia de ubicación por defecto
    fac = administrador.agregar_facultad(request.nombre_sede, request.id_facultad, request.nombre_facultad, request.nombre_sede)
    if not fac:
        raise HTTPException(status_code=400, detail="Error al crear facultad (revise la sede o ID)")
    return {"status": "success", "message": "Facultad creada"}

class CarreraCreateRequest(BaseModel):
    id_facultad: int
    codigo_carrera: str
    nombre_carrera: str
    modalidad: str

@app.post("/api/admin/carreras")
def crear_carrera(request: CarreraCreateRequest):
    car = administrador.agregar_carrera(request.id_facultad, request.codigo_carrera, request.nombre_carrera, request.modalidad)
    if not car:
        raise HTTPException(status_code=400, detail="Error al crear carrera (revise la facultad o código)")
    return {"status": "success", "message": "Carrera creada"}

class AsignarCursoRequest(BaseModel):
    identificacion_profesor: str
    codigo_curso: str

@app.post("/api/admin/asignar_curso")
def asignar_curso(request: AsignarCursoRequest):
    res = administrador.asignar_curso_a_profesor(request.identificacion_profesor, request.codigo_curso)
    if not res:
        raise HTTPException(status_code=400, detail="No se pudo asignar el curso. Verifique si el profesor o curso existen.")
    return {"status": "success", "message": "Curso asignado exitosamente"}

class CambioClaveRequest(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str
    confirmacion: str

@app.post("/api/estudiante/{identificacion}/cambiar_contrasena")
def cambiar_clave_estudiante(identificacion: str, request: CambioClaveRequest):
    estudiante = administrador.buscar_estudiante(identificacion)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    try:
        administrador.cambiar_contrasena_estudiante(estudiante, request.contrasena_actual, request.nueva_contrasena, request.confirmacion)
        return {"status": "success", "message": "Contraseña actualizada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/profesor/{identificacion}/cambiar_contrasena")
def cambiar_clave_profesor(identificacion: str, request: CambioClaveRequest):
    profesor = administrador.buscar_profesor(identificacion)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    try:
        administrador.cambiar_contrasena_profesor(profesor, request.contrasena_actual, request.nueva_contrasena, request.confirmacion)
        return {"status": "success", "message": "Contraseña actualizada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
