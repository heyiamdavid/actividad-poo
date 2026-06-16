class Reporte:

    def __init__(self, tipo, fecha_generacion):

        self.tipo = tipo
        self.fecha_generacion = fecha_generacion

    def generar_reporte_estudiantil(self):
        print("Reporte estudiantil generado")

    def generar_reporte_general(self):
        print("Reporte general generado")