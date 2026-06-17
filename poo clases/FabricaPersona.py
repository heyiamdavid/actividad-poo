from abc import ABC, abstractmethod

from Curso import Curso
from CursoNivelacion import CursoNivelacion
from Evaluacion import Evaluacion

class FabricaUniversitaria(ABC):
    @abstractmethod
    def crear_curso(self, nombre, identificador, extra):
        pass

    @abstractmethod
    def crear_evaluacion(self, nombre, calificacion):
        pass

class FabricaRegimenRegular(FabricaUniversitaria):
    #Fábrica concreta para cursos del régimen regular

    def crear_curso(self, nombre, identificador, extra):
        return Curso(codigoCurso=identificador, nombreCurso=nombre, creditos=int(extra))

    def crear_evaluacion(self, nombre, calificacion):
        return Evaluacion(nombreEvaluacion=nombre, calificacion=float(calificacion))
        
class FabricaRegimenNivelacion(FabricaUniversitaria):
    #Fábrica concreta para cursos de nivelación
    def crear_curso(self, nombre, identificador, extra):
        return CursoNivelacion(nombreCurso=nombre, paralelo=identificador, profesor=extra)

    def crear_evaluacion(self, nombre, calificacion):
        return Evaluacion(nombreEvaluacion=nombre, calificacion=float(calificacion))
