from typing import List, Tuple

from Facultad import Facultad
from Carrera import Carrera
from Curso import Curso
from Horario import Horario
from Aula import Aula


# Datos de fábrica de la universidad: facultades, carreras y su malla
# curricular predefinida (horario y aula ya asignados de antemano).
# Centralizar esta información aquí evita que Administrador.py crezca
# cada vez que se agrega una carrera más al catálogo inicial. No hay
# profesores predefinidos: todos los profesores se registran y
# asignan manualmente desde el menú del Administrador.
#
# Cada carrera predefinida tiene únicamente: 1 curso de nivelación
# (semestre 0) + 3 cursos de primer semestre (semestre 1). No existe
# segundo semestre en los datos de fábrica.
class DatosPredefinidos:

    @staticmethod
    def facultades_predefinidas() -> List[Tuple[Facultad, List[Carrera]]]:
        # Devuelve una lista de tuplas (Facultad, [Carrera, ...]) que
        # se agregan todas a la misma Sede Central.
        # Distribución de modalidades: 2 Presencial (SOF, MED),
        # 1 Semipresencial (ART), 1 Virtual (ARQ).

        facultad_ingenieria = Facultad(1, "Ingeniería", "Bloque A")
        carrera_software = Carrera("SOF", "Software", "Presencial")

        facultad_medicina = Facultad(2, "Ciencias de la Salud", "Bloque B")
        carrera_medicina = Carrera("MED", "Medicina", "Presencial")

        facultad_artes = Facultad(3, "Artes y Humanidades", "Bloque C")
        carrera_artes = Carrera("ART", "Artes", "Semipresencial")

        facultad_arquitectura = Facultad(4, "Arquitectura y Urbanismo", "Bloque D")
        carrera_arquitectura = Carrera("ARQ", "Arquitectura", "Virtual")

        return [
            (facultad_ingenieria, [carrera_software]),
            (facultad_medicina, [carrera_medicina]),
            (facultad_artes, [carrera_artes]),
            (facultad_arquitectura, [carrera_arquitectura]),
        ]

    @staticmethod
    def malla_curricular_por_carrera(
        codigo_carrera: str
    ) -> List[Tuple[Curso, Horario, Aula]]:
        # Los horarios y aulas ya existen de antemano; el estudiante
        # nunca los escribe manualmente, solo elige el curso. Devuelve
        # una lista de tuplas (Curso, Horario, Aula). Solo primer
        # semestre: 3 cursos por carrera.

        mallas = {
            "SOF": [
                (
                    Curso("SOF101", "Programación I", 4, codigo_carrera, 1),
                    Horario("Lunes", "07:00", "09:00"),
                    Aula("A101", 40)
                ),
                (
                    Curso("SOF102", "Matemática I", 4, codigo_carrera, 1),
                    Horario("Martes", "09:00", "11:00"),
                    Aula("A102", 40)
                ),
                (
                    Curso("SOF103", "Bases de Programación", 4, codigo_carrera, 1),
                    Horario("Miércoles", "07:00", "09:00"),
                    Aula("A103", 40)
                ),
            ],
            "MED": [
                (
                    Curso("MED101", "Anatomía I", 5, codigo_carrera, 1),
                    Horario("Lunes", "07:00", "09:00"),
                    Aula("B101", 35)
                ),
                (
                    Curso("MED102", "Biología Celular", 4, codigo_carrera, 1),
                    Horario("Martes", "09:00", "11:00"),
                    Aula("B102", 35)
                ),
                (
                    Curso("MED103", "Química General", 4, codigo_carrera, 1),
                    Horario("Miércoles", "07:00", "09:00"),
                    Aula("B103", 35)
                ),
            ],
            "ART": [
                (
                    Curso("ART101", "Historia del Arte", 3, codigo_carrera, 1),
                    Horario("Lunes", "07:00", "09:00"),
                    Aula("C101", 30)
                ),
                (
                    Curso("ART102", "Dibujo I", 4, codigo_carrera, 1),
                    Horario("Martes", "09:00", "11:00"),
                    Aula("C102", 30)
                ),
                (
                    Curso("ART103", "Apreciación Musical", 3, codigo_carrera, 1),
                    Horario("Miércoles", "07:00", "09:00"),
                    Aula("C103", 30)
                ),
            ],
            "ARQ": [
                (
                    Curso("ARQ101", "Dibujo Técnico", 4, codigo_carrera, 1),
                    Horario("Lunes", "07:00", "09:00"),
                    Aula("D101", 35)
                ),
                (
                    Curso("ARQ102", "Geometría Descriptiva", 4, codigo_carrera, 1),
                    Horario("Martes", "09:00", "11:00"),
                    Aula("D102", 35)
                ),
                (
                    Curso("ARQ103", "Introducción a la Arquitectura", 3, codigo_carrera, 1),
                    Horario("Miércoles", "07:00", "09:00"),
                    Aula("D103", 35)
                ),
            ],
        }

        return mallas.get(codigo_carrera, [])

    @staticmethod
    def curso_nivelacion_por_carrera(
        codigo_carrera: str, nombre_carrera: str
    ) -> Tuple[Curso, Horario, Aula]:
        # Cada carrera tiene un único curso de nivelación, con el
        # prefijo "Nivelación" desde su creación (no se genera el
        # nombre dinámicamente al momento del registro). Vive en el
        # semestre 0, fuera de la malla regular. Sin créditos, ya
        # que es un curso de refuerzo, no de la malla curricular.

        aulas_nivelacion = {
            "SOF": ("A100", 40),
            "MED": ("B100", 35),
            "ART": ("C100", 30),
            "ARQ": ("D100", 35),
        }

        numero_aula, capacidad = aulas_nivelacion.get(codigo_carrera, ("N100", 30))

        curso = Curso(
            f"NIV-{codigo_carrera}", f"Nivelación {nombre_carrera}", 0,
            codigo_carrera, 0
        )
        horario = Horario("Sábado", "08:00", "12:00")
        aula = Aula(numero_aula, capacidad)

        return curso, horario, aula
