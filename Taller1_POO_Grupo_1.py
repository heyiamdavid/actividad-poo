#GRUPO 1
#Molina Cedeño Vanessa
#Stiven Simba Ramirez
#Elizabeth Alcivar Loor
#David Alvarado Merchan
#Jeidy Vera Pilligua

class DocenteNivelacion:
    def __init__(self, cedula, nombre, nombreCurso, titulo, modalidad="Virtual"):
        self.__cedula = cedula #privado
        self.nombre = nombre
        self.nombreCurso = nombreCurso
        self.titulo = titulo
        self.modalidad = modalidad

        self.__notasEstudiantes = []   # privado
        self.__cuposMaximos = 30       # privado

    @property #uso de property
    def notasEstudiantes(self):
        return self.__notasEstudiantes

    @notasEstudiantes.setter #uso de setter para las notas de los estudiantes
    def notasEstudiantes(self, nota):
        if 0 <= nota <= 10: #ciclo para verificar la nota 
            self.__notasEstudiantes.append(nota)
        else:
            print("Error: la nota debe estar entre 0 y 10.")

    @property
    def cuposMaximos(self):
        return self.__cuposMaximos

    @cuposMaximos.setter
    def cuposMaximos(self, valor):
        if valor > 0:
            self.__cuposMaximos = valor
        else:
            print("Error: los cupos deben ser mayores a 0.")

    def registrar_estudiante(self, nombre_estudiante, **kwargs): #sobrecarga utilizada para el registro de los estudiantes
        if len(self.__notasEstudiantes) < self.__cuposMaximos: #ciclo para verificar la disponibilidad de cupos
            if "nota" in kwargs:
                self.notasEstudiantes = kwargs["nota"]
                print(f"Estudiante {nombre_estudiante} registrado con nota {kwargs['nota']}")
            else:
                print(f"Estudiante {nombre_estudiante} registrado sin nota")
        else:
            print("No hay cupos disponibles.")

    def mostrar_info(self):
        print("----- DOCENTE DE NIVELACIÓN -----")
        print(f"Cédula: {self.__cedula}")
        print(f"Nombre: {self.nombre}")
        print(f"Curso: {self.nombreCurso}")
        print(f"Título: {self.titulo}")
        print(f"Modalidad: {self.modalidad}")
        print(f"Cupos máximos: {self.__cuposMaximos}")
        print(f"Notas registradas: {self.__notasEstudiantes}")
        print("--------------------------------")


    # SOBRECARGA 2 
    def cambiar_modalidad(self, modalidad=None):
        if modalidad is None:
            print(f"La modalidad actual es: {self.modalidad}")
        else:
            self.modalidad = modalidad
            print(f"Modalidad cambiada a: {self.modalidad}")

    #Sobrecarga 3
    def registrar_nota(self, *notasEstudiantes):
        for nota in notasEstudiantes:
         if 0 <= nota <= 10:
            self.__notasEstudiantes.append(nota)
         else:
            print(f"Nota inválida: {nota}")

class Correo:
    #Sobrecarga 4
    def __init__(self, usuario, dominio="gmail.com"):
        self.usuario = usuario
        self.dominio = dominio

    def generar_correo(self, extension=None):
        if extension:
            return f"{self.usuario}@{extension}"
        return f"{self.usuario}@{self.dominio}"
    

#Instancias de objetos para la clase
docente1 = DocenteNivelacion(
    "0912345678",
    "Stiven Simba",
    "Nivelación Matemática",
    "Ingeniero",
    "Presencial"
)

docente2 = DocenteNivelacion(
    "0923456789",
    "Elizabeth Alcivar",
    "Nivelación Programación",
    "Licenciada",
    "Virtual"
)

docente1.mostrar_info()
docente1.registrar_estudiante("Vanessa", nota=8.5)
docente1.registrar_estudiante("Jeidy")
docente1.registrar_estudiante("David", nota=11)  # error

print()

docente2.mostrar_info()
docente2.registrar_estudiante("Luis", nota=9)


c = Correo("stiven")
print(c.generar_correo())              # default
print(c.generar_correo("outlook.com")) # sobrecarga
