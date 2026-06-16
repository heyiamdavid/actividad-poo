class Evaluacion:

    def __init__(self,
                 nombreEvaluacion,
                 calificacion=0):

        self.nombreEvaluacion = nombreEvaluacion

        self.__calificacion = calificacion

    @property
    def calificacion(self):
        return self.__calificacion

    @calificacion.setter
    def calificacion(self, nueva_calificacion):

        if 0 <= nueva_calificacion <= 10:
            self.__calificacion = nueva_calificacion
        else:
            print("Calificación inválida")

    def mostrar_calificacion(self):

        print(f"{self.nombreEvaluacion}: {self.__calificacion}")

    # sobrecarga con parámetro opcional
    def corregir_evaluacion(self, puntos_extra=0):

        nueva_nota = self.__calificacion + puntos_extra

        if nueva_nota > 10:
            nueva_nota = 10

        self.__calificacion = nueva_nota

        print(f"Nueva nota: {self.__calificacion}")