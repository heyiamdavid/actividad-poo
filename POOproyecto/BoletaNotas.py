from typing import Dict, Optional

from Evaluacion import Evaluacion


# Una BoletaNotas agrupa las 4 evaluaciones fijas (1er Parcial,
# 2do Parcial, Examen Final y Recuperación) de UN estudiante en
# UN curso específico. Centraliza el cálculo del promedio final:
# - Si no hay Recuperación: promedio de las 3 evaluaciones regulares.
# - Si hay Recuperación: se promedia el resultado de las 3 regulares
#   junto con la nota de Recuperación, es decir
#   (promedio_regulares + recuperacion) / 2. La recuperación no
#   sustituye a las 3 primeras, las complementa — puede haber
#   estudiantes que aprueben sin necesitar recuperación.
class BoletaNotas:

    def __init__(self, identificacion_estudiante: str, codigo_curso: str):

        self.identificacion_estudiante: str = identificacion_estudiante
        self.codigo_curso: str = codigo_curso

        self.__evaluaciones: Dict[str, Evaluacion] = {
            nombre: Evaluacion(nombre, 0)
            for nombre in Evaluacion.NOMBRES_EVALUACIONES
        }

    @property
    def evaluaciones(self) -> Dict[str, Evaluacion]:
        return self.__evaluaciones

    def obtener_evaluacion(self, nombre_evaluacion: str) -> Optional[Evaluacion]:
        return self.__evaluaciones.get(nombre_evaluacion)

    def registrar_nota(self, nombre_evaluacion: str, calificacion: float) -> bool:

        evaluacion = self.__evaluaciones.get(nombre_evaluacion)

        if evaluacion is None:
            print(f"\nNo existe la evaluación con nombre {nombre_evaluacion}.")
            return False

        evaluacion.calificacion = calificacion
        return True

    def tiene_recuperacion(self) -> bool:
        return self.__evaluaciones[Evaluacion.RECUPERACION].tiene_nota()

    def evaluaciones_regulares_completas(self) -> bool:

        return all(
            self.__evaluaciones[nombre].tiene_nota()
            for nombre in Evaluacion.NOMBRES_REGULARES
        )

    def promedio_regulares(self) -> Optional[float]:

        if not self.evaluaciones_regulares_completas():
            return None

        suma = sum(
            self.__evaluaciones[nombre].calificacion
            for nombre in Evaluacion.NOMBRES_REGULARES
        )
        return suma / len(Evaluacion.NOMBRES_REGULARES)

    def calcular_promedio(self) -> Optional[float]:

        promedio_regular = self.promedio_regulares()

        if promedio_regular is None:
            return None

        if not self.tiene_recuperacion():
            return promedio_regular

        # La recuperación complementa el promedio de las 3 regulares,
        # no lo sustituye: se promedian ambos resultados entre sí.
        nota_recuperacion = self.__evaluaciones[Evaluacion.RECUPERACION].calificacion
        return (promedio_regular + nota_recuperacion) / 2

    def mostrar_boleta(self) -> None:

        print(f"\n----- Boleta del curso {self.codigo_curso} -----")

        for nombre in Evaluacion.NOMBRES_EVALUACIONES:
            self.__evaluaciones[nombre].mostrar_calificacion()

        promedio = self.calcular_promedio()

        if promedio is None:
            print("Promedio: pendiente (faltan evaluaciones regulares para calcular un promedio)")
        else:
            print(f"Promedio: {promedio:.2f}")
