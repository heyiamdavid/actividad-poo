from typing import TYPE_CHECKING, List

# Importación de la superclase base
from Persona import Persona

# Prevención de dependencias circulares durante el tipado estático
if TYPE_CHECKING:
    from Curso import Curso
    from Estudiante import Estudiante
    from BoletaNotas import BoletaNotas

# Herencia: La clase Profesor hereda de Persona, adquiriendo sus atributos y comportamientos base.
# Esto promueve la reutilización de código y cumple con el principio "Abierto/Cerrado" de SOLID.
class Profesor(Persona):

    # Constructor de la clase hija
    def __init__(self, nombre: str, telefono: str, email: str, identificacion: str,
                 contrasena: str, titulo: str, materia: str = ""):

        # Invocación al constructor de la clase padre (superclase) para inicializar 
        # los atributos comunes (nombre, teléfono, etc.) antes de los específicos.
        super().__init__(
            nombre,
            telefono,
            email,
            identificacion,
            contrasena
        )

        # Atributos específicos del dominio del Profesor
        # La materia se mantiene en el modelo, pero ya no se solicita
        # en el formulario de registro (puede asignarse más adelante).
        self.materia: str = materia
        self.titulo: str = titulo

        # Composición/Agregación: Lista privada para encapsular los cursos dictados
        self.__cursos: List["Curso"] = []

    # ENCAPSULAMIENTO
    # Getter para acceder a la lista de cursos sin exponer el atributo privado a modificaciones directas
    @property
    def cursos(self) -> List["Curso"]:
        return self.__cursos

    # MÉTODOS DE NEGOCIO
    # Asigna un curso al profesor estableciendo una relación bidireccional en memoria
    def asignar_curso(self, curso: "Curso") -> None:

        self.__cursos.append(curso)
        # Se actualiza también la referencia dentro del objeto Curso para mantener coherencia
        curso.asignar_profesor(self)

    # Lógica transaccional para el registro de calificaciones
    def registrar_nota_en_boleta(self, curso: "Curso", estudiante: "Estudiante",
                                  nombre_evaluacion: str, calificacion: float) -> "BoletaNotas":

        # Recupera la boleta específica del estudiante dentro del curso
        boleta = curso.obtener_boleta(estudiante.identificacion)
        
        # Delega la responsabilidad de registrar la nota al objeto Boleta (Alta Cohesión)
        registrado = boleta.registrar_nota(nombre_evaluacion, calificacion)

        # Feedback visual si la operación fue exitosa
        if registrado:
            print(f"\nNota de {nombre_evaluacion} registrada correctamente.")

        return boleta

    # Método de consulta y visualización de la nómina de estudiantes
    def listar_estudiantes_del_curso(self, curso: "Curso") -> None:

        print(f"\n===== ESTUDIANTES DE {curso.nombreCurso} =====")

        # Validación temprana (Early Return) si el curso está vacío
        if curso.total_estudiantes() == 0:
            print("No existen estudiantes matriculados en este curso.")
            return

        # Recorrido iterativo mostrando datos clave del estudiante
        for estudiante in curso.estudiantes:
            print(
                f"- {estudiante.nombre} "
                f"(Identificación: {estudiante.identificacion}, "
                f"Semestre: {estudiante.semestre})"
            )

    # Imprime la carga académica asignada al profesor
    def mostrar_cursos(self) -> None:

        if len(self.__cursos) == 0:
            print("\nNo existen cursos asignados.")
            return

        print("\n===== CURSOS =====")

        # Delega la impresión del detalle a cada objeto curso individual
        for curso in self.__cursos:
            curso.mostrar_curso()

    # Genera un reporte general de todas las evaluaciones registradas por el profesor
    def mostrar_evaluaciones(self) -> None:

        if len(self.__cursos) == 0:
            print("\nNo existen cursos asignados.")
            return

        print("\n===== EVALUACIONES =====")

        # Bandera lógica para controlar si se imprimieron datos o si todo está vacío
        hay_boletas = False

        for curso in self.__cursos:

            # Si el curso no tiene boletas, salta a la siguiente iteración
            if len(curso.boletas) == 0:
                continue

            hay_boletas = True
            print(f"\nCurso: {curso.nombreCurso}")

            # Recorre el diccionario de boletas extrayendo solo los valores (los objetos)
            for boleta in curso.boletas.values():
                boleta.mostrar_boleta()

        # Validación final por si todos los cursos carecían de boletas
        if not hay_boletas:
            print("No existen evaluaciones registradas.")

    # Sobreescritura (Polimorfismo implícito) para mostrar los datos del profesor
    def mostrar_datos(self) -> None:

        print("\n========== DATOS PROFESOR ==========")

        print("Nombre:", self.nombre)
        print("Teléfono:", self.telefono)
        print("Email:", self.email)
        print("Identificación:", self.identificacion)
        print("Título:", self.titulo)

        # Validación para imprimir la materia solo si ha sido asignada previamente
        if self.materia:
            print("Materia:", self.materia)

    # Método de acceso privilegiado para mostrar información sensible
    def mostrar_datos_administrativos(self) -> None:
        # Vista exclusiva del Administrador: incluye las claves.
        # Nunca se debe invocar desde el propio menú del profesor por seguridad.

        # Reutiliza el método base para imprimir los datos públicos (DRY)
        self.mostrar_datos()
        
        # Expone credenciales de acceso solo en la vista administrativa
        print(f"Clave temporal: {self.clave_temporal}")
        print(f"Clave actual: {self.contrasena}")
