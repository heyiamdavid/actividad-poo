from abc import ABC, abstractmethod

from Curso import Curso
from CursoNivelacion import CursoNivelacion
from Evaluacion import Evaluacion


class FabricaUniversitaria(ABC):
    """
    PATRÓN CREACIONAL: Factory Method.

    Define una interfaz común para crear cursos y evaluaciones,
    pero deja que las subclases decidan qué clase concreta
    instanciar (Curso "normal" vs CursoNivelacion).

    Esto evita que el código cliente (Main.py) tenga que usar
    if/else para decidir qué clase construir: simplemente elige
    QUÉ fábrica usar, y la fábrica se encarga del resto (OCP: para
    agregar un nuevo tipo de curso, se crea una nueva fábrica sin
    modificar el código existente).
    """

    @abstractmethod
    def crear_curso(self, nombre, identificador, extra):
        pass

    @abstractmethod
    def crear_evaluacion(self, nombre, calificacion):
        pass


class FabricaRegimenRegular(FabricaUniversitaria):
    """Fábrica concreta para cursos del régimen regular."""

    def crear_curso(self, nombre, identificador, extra):

        return Curso(
            codigoCurso=identificador,
            nombreCurso=nombre,
            creditos=int(extra)
        )

    def crear_evaluacion(self, nombre, calificacion):

        return Evaluacion(
            nombreEvaluacion=nombre,
            calificacion=float(calificacion)
        )


class FabricaRegimenNivelacion(FabricaUniversitaria):
    """Fábrica concreta para cursos de nivelación."""

    def crear_curso(self, nombre, identificador, extra):

        return CursoNivelacion(
            nombreCurso=nombre,
            paralelo=identificador,
            profesor=extra
        )

    def crear_evaluacion(self, nombre, calificacion):

        return Evaluacion(
            nombreEvaluacion=nombre,
            calificacion=float(calificacion)
        )
