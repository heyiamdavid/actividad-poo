import sys

path = r"c:\Users\Deivid\Desktop\actividad-poo\POOproyecto\api_v2.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix imports
content = content.replace("from typing import Optional", "from typing import Optional, List\nfrom datetime import datetime")

# Models to add
models = """
class MatricularRequest(BaseModel):
    identificacion_estudiante: str
    codigos_curso: List[str]

class CerrarCursoRequest(BaseModel):
    identificacion_estudiante: str
    codigo_curso: str

class ProfesorUpdate(BaseModel):
    telefono: str
    email: str
"""
if "class MatricularRequest" not in content:
    content = content.replace("class LoginRequest(BaseModel):", models + "\nclass LoginRequest(BaseModel):")

# Endpoints to append
endpoints = """

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
"""

if "@app.post(\"/api/estudiante/matricular\")" not in content:
    content += endpoints

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("api_v2.py modificado correctamente.")

