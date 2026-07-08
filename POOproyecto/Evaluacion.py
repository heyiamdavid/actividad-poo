from typing import List


class Evaluacion:

    # Nombres fijos de las evaluaciones de un curso. Las primeras
    # tres son obligatorias para calcular el promedio; la cuarta
    # (Recuperación) es opcional y, si existe, sustituye a las tres
    # primeras en el cálculo del promedio final.
    PRIMER_PARCIAL: str = "1er Parcial" #parciales predefinidos segun la universidad
    SEGUNDO_PARCIAL: str = "2do Parcial" #parciales predefinidos segun la universidad
    EXAMEN_FINAL: str = "Examen Final"
    RECUPERACION: str = "Recuperación"

    NOMBRES_REGULARES: List[str] = [PRIMER_PARCIAL, SEGUNDO_PARCIAL, EXAMEN_FINAL]
    NOMBRES_EVALUACIONES: List[str] = NOMBRES_REGULARES + [RECUPERACION]

    def __init__(self, nombreEvaluacion: str, calificacion: float = 0):

        self.nombreEvaluacion: str = nombreEvaluacion
        self.__calificacion: float = calificacion

    @property
    def calificacion(self) -> float:
        return self.__calificacion

    @calificacion.setter
    def calificacion(self, nueva_calificacion: float) -> None:

        if 0 <= nueva_calificacion <= 10:
            self.__calificacion = nueva_calificacion
        else:
            print("Calificación inválida")

    def tiene_nota(self) -> bool:
        return self.__calificacion > 0

    def mostrar_calificacion(self) -> None:

        if not self.tiene_nota():
            print(f"{self.nombreEvaluacion}: (sin registrar)")
            return

        print(
            f"{self.nombreEvaluacion}: "
            f"{self.__calificacion}"
        )

    def corregir_evaluacion(self, *args) -> float:
    #Sobrecarga de método mediante *args
        if len(args) == 0:
            print(f"Nota sin cambios: {self.__calificacion}")
            return self.__calificacion
    # Corrige usando otra evaluación
        if len(args) == 1 and isinstance(args[0], Evaluacion):
            otra_evaluacion = args[0]
            nueva_nota = (self.__calificacion + otra_evaluacion.calificacion) / 2
    # Corrige agregando puntos extra
        elif len(args) == 1:
            puntos_extra = args[0]
            nueva_nota = (self.__calificacion + puntos_extra)

        else:
            print("Argumentos inválidos para corregir evaluacion")
            return self.__calificacion

        if nueva_nota > 10:
            nueva_nota = 10
        elif nueva_nota < 0:
            nueva_nota = 0
        self.__calificacion = nueva_nota
        print(f"Nueva nota: {self.__calificacion}")
        return self.__calificacion
