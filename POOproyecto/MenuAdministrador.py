from typing import Callable, Optional

from Validador import Validador
from Administrador import Administrador
from Facultad import Facultad
from Carrera import Carrera
from Estudiante import Estudiante


# Menú del Administrador.
# Únicamente contiene flujo de pantallas y llamadas a métodos
# de Administrador y de las clases de dominio. No existe
# lógica de negocio aquí.
class MenuAdministrador:

    ESTADOS_ESTUDIANTE = ["Activo", "Inactivo"]
    MODALIDADES = ["Presencial", "Semipresencial", "Virtual"]

    def __init__(self, administrador: Administrador):
        self.administrador = administrador

    # ---------- ESTUDIANTES ----------

    def registrar_estudiante(self) -> None:

        print("\n========== REGISTRO ESTUDIANTE ==========\n")

        nombre = Validador.leer_nombre_completo("Nombre y apellido: ")
        telefono = Validador.leer_telefono()
        email = Validador.leer_email()
        identificacion = Validador.leer_identificacion("estudiante", self.administrador)

        contrasena = Validador.generar_clave_temporal()
        print(f"[*] Clave temporal generada: {contrasena}")

        promedio_ingreso = Validador.leer_nota("Promedio ingreso: ")
        promedio_graduacion = Validador.leer_nota("Promedio graduación: ")

        estado = Validador.seleccionar_opcion(
            "Seleccione el estado del estudiante:", self.ESTADOS_ESTUDIANTE
        )
        modalidad = Validador.seleccionar_opcion(
            "Seleccione la modalidad:", self.MODALIDADES
        )

        # Solo se muestran las carreras que ofrecen la modalidad elegida.
        carreras = self.administrador.carreras_por_modalidad(modalidad)

        if len(carreras) == 0:
            print(f"\nNo existen carreras registradas con modalidad {modalidad}.")
            return

        codigos_carrera = [carrera.codigoCarrera for carrera in carreras]

        print("\nCarreras disponibles para esa modalidad:")
        for carrera in carreras:
            carrera.mostrar_carrera()

        codigo_carrera = Validador.seleccionar_opcion(
            "Seleccione la carrera:", codigos_carrera
        )

        if self.administrador.requiere_nivelacion_por_ingreso(
            promedio_ingreso, promedio_graduacion
        ):
            print(
                "\nEl promedio entre ingreso y graduación es menor a 8: "
                "el estudiante pasará directamente a nivelación."
            )
            semestre = None
        else:
            print(
                "\nEl promedio entre ingreso y graduación es mayor a 8: "
                "el estudiante queda inscrito directamente en primer semestre."
            )
            semestre = 1

        estudiante = self.administrador.registrar_estudiante(
            nombre, telefono, email, identificacion, contrasena,
            promedio_ingreso, promedio_graduacion, estado, modalidad,
            codigo_carrera, semestre
        )

    def eliminar_estudiante(self) -> None:

        print("\n========== ELIMINAR ESTUDIANTE ==========\n")

        identificacion = input("Identificación del estudiante: ")
        estudiante = self.administrador.buscar_estudiante(identificacion)

        if estudiante is None:
            print("\nNo existe un estudiante con esa identificación")
            return

        self.administrador.eliminar_estudiante(identificacion)
        print(f"\nEstudiante {estudiante.nombre} eliminado correctamente")

    def consultar_estudiantes(self) -> None:

        while True:
            print("\n========================")
            print("CONSULTAR ESTUDIANTES")
            print("========================")
            print("1. Estudiantes en nivelación")
            print("2. Estudiantes en primer semestre")
            print("3. Salir")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self._mostrar_estudiantes_por_filtro(
                    "ESTUDIANTES EN NIVELACIÓN",
                    lambda estudiante: estudiante.semestre == 0
                )
            elif opcion == "2":
                self._mostrar_estudiantes_por_filtro(
                    "ESTUDIANTES EN PRIMER SEMESTRE",
                    lambda estudiante: estudiante.semestre == 1
                )
            elif opcion == "3":
                break
            else:
                print("\nOpción inválida")

    def _mostrar_estudiantes_por_filtro(self, titulo: str,
                                         filtro: Callable[[Estudiante], bool]) -> None:

        print(f"\n========== {titulo} ==========\n")

        estudiantes = [
            estudiante for estudiante in self.administrador.listar_estudiantes()
            if filtro(estudiante)
        ]

        if len(estudiantes) == 0:
            print("No existen estudiantes registrados en esta categoría")
            return

        for estudiante in estudiantes:
            # Vista administrativa: incluye las claves (temporal y actual).
            estudiante.mostrar_datos_administrativos()
            print("-----------------------------------")

    def editar_estudiante(self) -> None:

        print("\n========== EDITAR ESTUDIANTE ==========\n")

        identificacion = input("Identificación del estudiante: ")
        estudiante = self.administrador.buscar_estudiante(identificacion)

        if estudiante is None:
            print("\nNo existe un estudiante con esa identificación")
            return

        estudiante.mostrar_datos_administrativos()

        print("\nDeje en blanco un campo para no modificarlo.")

        nuevo_nombre = input(f"Nombre [{estudiante.nombre}]: ").strip()
        if nuevo_nombre:
            estudiante.nombre = nuevo_nombre

        nuevo_telefono = input(f"Teléfono [{estudiante.telefono}]: ").strip()
        if nuevo_telefono:
            estudiante.telefono = nuevo_telefono

        nuevo_email = input(f"Email [{estudiante.email}]: ").strip()
        if nuevo_email:
            estudiante.email = nuevo_email

        cambiar_estado = input("¿Cambiar estado? (s/n): ").strip().lower()
        if cambiar_estado == "s":
            estudiante.estado = Validador.seleccionar_opcion(
                "Seleccione el nuevo estado:", self.ESTADOS_ESTUDIANTE
            )

        self.administrador.actualizar_datos_estudiante(estudiante)

    # ---------- PROFESORES ----------

    def registrar_profesor(self) -> None:

        print("\n========== REGISTRO PROFESOR ==========\n")

        nombre = Validador.leer_nombre_completo("Nombre y apellido: ")
        telefono = Validador.leer_telefono()
        email = Validador.leer_email()
        identificacion = Validador.leer_identificacion("profesor", self.administrador)

        contrasena = Validador.generar_clave_temporal()
        print(f"[*] Clave temporal generada: {contrasena}")

        titulo = Validador.leer_texto(
            "Título: ", "El título", minimo_palabras=1, solo_letras=True
        )

        self.administrador.registrar_profesor(
            nombre, telefono, email, identificacion, contrasena,
            titulo
        )

    def eliminar_profesor(self) -> None:

        print("\n========== ELIMINAR PROFESOR ==========\n")

        identificacion = input("Identificación del profesor: ")
        profesor = self.administrador.buscar_profesor(identificacion)

        if profesor is None:
            print("\nNo existe un profesor con esa identificación")
            return

        self.administrador.eliminar_profesor(identificacion)
        print(f"\nProfesor {profesor.nombre} eliminado correctamente")

    def consultar_profesores(self) -> None:

        print("\n========== PROFESORES ==========\n")

        profesores = self.administrador.listar_profesores()

        if len(profesores) == 0:
            print("No existen profesores registrados")
            return

        for profesor in profesores:
            # Vista administrativa: incluye las claves (temporal y actual).
            profesor.mostrar_datos_administrativos()
            print("-----------------------------------")

    def editar_profesor(self) -> None:

        print("\n========== EDITAR PROFESOR ==========\n")

        identificacion = input("Identificación del profesor: ")
        profesor = self.administrador.buscar_profesor(identificacion)

        if profesor is None:
            print("\nNo existe un profesor con esa identificación")
            return

        profesor.mostrar_datos_administrativos()

        print("\nDeje en blanco un campo para no modificarlo.")

        nuevo_nombre = input(f"Nombre [{profesor.nombre}]: ").strip()
        if nuevo_nombre:
            profesor.nombre = nuevo_nombre

        nuevo_telefono = input(f"Teléfono [{profesor.telefono}]: ").strip()
        if nuevo_telefono:
            profesor.telefono = nuevo_telefono

        nuevo_email = input(f"Email [{profesor.email}]: ").strip()
        if nuevo_email:
            profesor.email = nuevo_email

        nueva_materia = input(f"Materia [{profesor.materia}]: ").strip()
        if nueva_materia:
            profesor.materia = nueva_materia

        nuevo_titulo = input(f"Título [{profesor.titulo}]: ").strip()
        if nuevo_titulo:
            profesor.titulo = nuevo_titulo

        self.administrador.actualizar_datos_profesor(profesor)

    def asignar_curso_profesor(self) -> None:

        print("\n========== ASIGNAR CURSO A PROFESOR ==========\n")

        identificacion_profesor = input("Identificación del profesor: ")
        profesor = self.administrador.buscar_profesor(identificacion_profesor)

        if profesor is None:
            print("\nNo existe un profesor con esa identificación")
            return

        facultades = self.administrador.listar_facultades()

        if len(facultades) == 0:
            print("\nNo existen facultades registradas")
            return

        print("\nFacultades disponibles:")
        for facultad in facultades:
            facultad.mostrar_facultad()

        ids_facultad = [facultad.id_facultad for facultad in facultades]
        id_facultad = Validador.seleccionar_opcion(
            "Seleccione la facultad:", ids_facultad, permitir_cancelar=True
        )

        if id_facultad is None:
            print("\nOperación cancelada.")
            return

        facultad = self.administrador.buscar_facultad(id_facultad)

        modalidad = self._seleccionar_modalidad()

        if modalidad is None:
            print("\nOperación cancelada.")
            return

        carreras = [
            carrera for carrera in facultad.carreras
            if carrera.modalidad == modalidad
        ]

        if len(carreras) == 0:
            print(f"\nEsa facultad no tiene carreras con modalidad {modalidad}")
            return

        print(f"\nCarreras de la facultad ({modalidad}):")
        for carrera in carreras:
            carrera.mostrar_carrera()

        codigos_carrera = [carrera.codigoCarrera for carrera in carreras]
        codigo_carrera = Validador.seleccionar_opcion(
            "Seleccione la carrera:", codigos_carrera, permitir_cancelar=True
        )

        if codigo_carrera is None:
            print("\nOperación cancelada.")
            return

        carrera = self.administrador.buscar_carrera(codigo_carrera)
        cursos = carrera.cursos

        if len(cursos) == 0:
            print("\nEsa carrera no tiene cursos/materias registradas")
            return

        print("\nCursos de la carrera:")
        for curso in cursos:
            curso.mostrar_resumen()

        codigos_curso = [curso.codigoCurso for curso in cursos]
        codigo_curso = Validador.seleccionar_opcion(
            "Seleccione el curso a asignar:", codigos_curso, permitir_cancelar=True
        )

        if codigo_curso is None:
            print("\nOperación cancelada.")
            return

        curso_asignado = self.administrador.asignar_curso_a_profesor(
            identificacion_profesor, codigo_curso
        )

        if curso_asignado:
            print(
                f"\nCurso {curso_asignado.nombreCurso} asignado "
                f"a {profesor.nombre} correctamente"
            )

    # ---------- ADMINISTRAR UNIVERSIDADES ----------

    def administrar_universidades(self) -> None:

        while True:
            print("\n========================")
            print("ADMINISTRAR UNIVERSIDADES")
            print("========================")
            print("1. Consultar universidad")
            print("2. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.administrador.mostrar_universidad()
            elif opcion == "2":
                break
            else:
                print("\nOpción inválida")

    # ---------- ADMINISTRAR SEDES ----------

    def agregar_sede(self) -> None:

        print("\n========== AGREGAR SEDE ==========\n")

        nombre_sede = Validador.leer_texto("Nombre de la sede: ", "El nombre de la sede")

        if self.administrador.buscar_sede(nombre_sede):
            print("\nYa existe una sede con ese nombre")
            return

        direccion = Validador.leer_texto("Dirección: ", "La dirección")
        ciudad = Validador.leer_texto("Ciudad: ", "La ciudad")

        self.administrador.agregar_sede(nombre_sede, direccion, ciudad)
        print(f"\nSede {nombre_sede} agregada correctamente")

    def eliminar_sede(self) -> None:

        print("\n========== ELIMINAR SEDE ==========\n")

        sedes = self.administrador.listar_sedes()

        if len(sedes) == 0:
            print("No existen sedes registradas")
            return

        nombres_sede = [sede.nombreSede for sede in sedes]
        nombre_sede = Validador.seleccionar_opcion(
            "Seleccione la sede a eliminar:", nombres_sede, permitir_cancelar=True
        )

        if nombre_sede is None:
            print("\nOperación cancelada.")
            return

        if self.administrador.eliminar_sede(nombre_sede):
            print(f"\nSede {nombre_sede} eliminada correctamente")
        else:
            print("\nNo existe una sede con ese nombre")

    def consultar_sedes(self) -> None:

        print("\n========== SEDES ==========\n")

        sedes = self.administrador.listar_sedes()

        if len(sedes) == 0:
            print("No existen sedes registradas")
            return

        for sede in sedes:
            sede.mostrar_sede()
            sede.listar_facultades()
            print("-----------------------------------")

    def administrar_sedes(self) -> None:

        while True:
            print("\n========================")
            print("ADMINISTRAR SEDES")
            print("========================")
            print("1. Agregar sede")
            print("2. Eliminar sede")
            print("3. Consultar sedes")
            print("4. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.agregar_sede()
            elif opcion == "2":
                self.eliminar_sede()
            elif opcion == "3":
                self.consultar_sedes()
            elif opcion == "4":
                break
            else:
                print("\nOpción inválida")

    # ---------- ADMINISTRAR FACULTADES ----------

    def agregar_facultad(self) -> None:

        print("\n========== AGREGAR FACULTAD ==========\n")

        sedes = self.administrador.listar_sedes()

        if len(sedes) == 0:
            print("No existen sedes registradas. Registre una sede primero.")
            return

        nombres_sede = [sede.nombreSede for sede in sedes]
        nombre_sede = Validador.seleccionar_opcion(
            "Seleccione la sede:", nombres_sede, permitir_cancelar=True
        )

        if nombre_sede is None:
            print("\nOperación cancelada.")
            return

        id_facultad = Validador.leer_entero("ID de la facultad: ")
        nombre_facultad = Validador.leer_texto("Nombre de la facultad: ", "El nombre de la facultad")
        ubicacion = Validador.leer_texto("Ubicación: ", "La ubicación")

        facultad = self.administrador.agregar_facultad(
            nombre_sede, id_facultad, nombre_facultad, ubicacion
        )

        if facultad:
            print(f"\nFacultad {nombre_facultad} agregada correctamente")

    def eliminar_facultad(self) -> None:

        print("\n========== ELIMINAR FACULTAD ==========\n")

        sedes = self.administrador.listar_sedes()

        if len(sedes) == 0:
            print("No existen sedes registradas")
            return

        nombres_sede = [sede.nombreSede for sede in sedes]
        nombre_sede = Validador.seleccionar_opcion(
            "Seleccione la sede:", nombres_sede, permitir_cancelar=True
        )

        if nombre_sede is None:
            print("\nOperación cancelada.")
            return

        sede = self.administrador.buscar_sede(nombre_sede)
        facultades_sede = sede.facultades

        if len(facultades_sede) == 0:
            print("\nEsa sede no tiene facultades registradas.")
            return

        ids_facultad = [facultad.id_facultad for facultad in facultades_sede]
        id_facultad = Validador.seleccionar_opcion(
            "Seleccione el ID de la facultad a eliminar:",
            ids_facultad, permitir_cancelar=True
        )

        if id_facultad is None:
            print("\nOperación cancelada.")
            return

        if self.administrador.eliminar_facultad(nombre_sede, id_facultad):
            print("\nFacultad eliminada correctamente")
        else:
            print("\nNo existe una facultad con ese ID en esa sede")

    def consultar_facultades(self) -> None:

        print("\n========== FACULTADES ==========\n")

        facultades = self.administrador.listar_facultades()

        if len(facultades) == 0:
            print("No existen facultades registradas")
            return

        for facultad in facultades:
            facultad.mostrar_facultad()
            print("-----------------------------------")

    def administrar_facultades(self) -> None:

        while True:
            print("\n========================")
            print("ADMINISTRAR FACULTADES")
            print("========================")
            print("1. Agregar facultad")
            print("2. Eliminar facultad")
            print("3. Consultar facultades")
            print("4. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.agregar_facultad()
            elif opcion == "2":
                self.eliminar_facultad()
            elif opcion == "3":
                self.consultar_facultades()
            elif opcion == "4":
                break
            else:
                print("\nOpción inválida")

    # ---------- ADMINISTRAR CARRERAS ----------

    def agregar_carrera(self) -> None:

        print("\n========== AGREGAR CARRERA ==========\n")

        facultades = self.administrador.listar_facultades()

        if len(facultades) == 0:
            print("No existen facultades registradas. Registre una facultad primero.")
            return

        ids_facultad = [facultad.id_facultad for facultad in facultades]

        print("\nFacultades disponibles:")
        for facultad in facultades:
            facultad.mostrar_facultad()

        id_facultad = Validador.seleccionar_opcion(
            "Seleccione el ID de la facultad:", ids_facultad, permitir_cancelar=True
        )

        if id_facultad is None:
            print("\nOperación cancelada.")
            return

        codigo_carrera = Validador.leer_codigo(
            "Código de la carrera: ", self.administrador, "carrera"
        )
        nombre_carrera = Validador.leer_texto("Nombre de la carrera: ", "El nombre de la carrera")
        modalidad = Validador.seleccionar_opcion(
            "Seleccione la modalidad:", self.MODALIDADES
        )

        carrera = self.administrador.agregar_carrera(
            id_facultad, codigo_carrera, nombre_carrera, modalidad
        )

        if carrera:
            print(f"\nCarrera {nombre_carrera} agregada correctamente")

    def eliminar_carrera(self) -> None:

        print("\n========== ELIMINAR CARRERA ==========\n")

        modalidad = self._seleccionar_modalidad()

        if modalidad is None:
            return

        carrera = self._seleccionar_carrera_por_modalidad(modalidad)

        if carrera is None:
            return

        facultad = self._buscar_facultad_de_carrera(carrera.codigoCarrera)

        if facultad is None:
            print("\nNo se pudo determinar la facultad de esa carrera.")
            return

        if self.administrador.eliminar_carrera(facultad.id_facultad, carrera.codigoCarrera):
            print("\nCarrera eliminada correctamente")
        else:
            print("\nNo existe una carrera con ese código en esa facultad")

    def _buscar_facultad_de_carrera(self, codigo_carrera: str) -> Optional[Facultad]:

        for facultad in self.administrador.listar_facultades():
            if facultad.buscar_carrera(codigo_carrera):
                return facultad

        return None

    def consultar_carreras(self) -> None:

        print("\n========== CONSULTAR CARRERAS ==========\n")

        modalidad = self._seleccionar_modalidad()

        if modalidad is None:
            return

        carrera = self._seleccionar_carrera_por_modalidad(modalidad)

        if carrera is None:
            return

        print()
        carrera.mostrar_carrera_con_materias()

    def _seleccionar_modalidad(self) -> Optional[str]:

        print("\n========================")
        print("MODALIDADES DE CARRERAS")
        print("========================")

        return Validador.seleccionar_opcion(
            "Seleccione la modalidad:", self.MODALIDADES, permitir_cancelar=True
        )

    def _seleccionar_carrera_por_modalidad(self, modalidad: str) -> Optional[Carrera]:

        carreras = self.administrador.carreras_por_modalidad(modalidad)

        if len(carreras) == 0:
            print(f"\nNo existen carreras con modalidad {modalidad}.")
            return None

        print(f"\nCarreras disponibles ({modalidad}):\n")
        for carrera in carreras:
            carrera.mostrar_carrera()

        codigos_carrera = [carrera.codigoCarrera for carrera in carreras]
        codigo_carrera = Validador.seleccionar_opcion(
            "Seleccione la carrera:", codigos_carrera, permitir_cancelar=True
        )

        if codigo_carrera is None:
            return None

        return self.administrador.buscar_carrera(codigo_carrera)

    def agregar_materia_a_carrera(self, carrera: Carrera) -> None:

        print(f"\n========== AGREGAR MATERIA A {carrera.codigoCarrera} ==========\n")

        codigo_curso = Validador.leer_codigo(
            "Código de la materia: ", self.administrador, "curso"
        )
        nombre_curso = Validador.leer_texto(
            "Nombre de la materia: ", "El nombre de la materia"
        )
        creditos = Validador.leer_entero_en_rango("Créditos (1 a 5): ", 1, 5)

        es_nivelacion = input(
            "¿Es una materia de nivelación? (s/n): "
        ).strip().lower() == "s"

        semestre = 0 if es_nivelacion else 1

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        dia = Validador.seleccionar_opcion("Seleccione el día:", dias)

        hora_inicio = Validador.leer_hora("Hora de inicio (HH:MM): ")
        hora_fin = Validador.leer_hora("Hora de fin (HH:MM): ")
        numero_aula = Validador.leer_aula("Número de aula (ej. A101): ")
        capacidad_aula = Validador.leer_entero_en_rango("Capacidad del aula (1 a 40): ", 1, 40)

        curso = self.administrador.registrar_curso_en_carrera(
            carrera.codigoCarrera, codigo_curso, nombre_curso, creditos, semestre,
            dia, hora_inicio, hora_fin, numero_aula, capacidad_aula
        )

        if curso:
            print(
                f"\nMateria {nombre_curso} agregada correctamente "
                f"a {carrera.codigoCarrera}"
            )

    def administrar_carreras(self) -> None:

        while True:
            print("\n========================")
            print("ADMINISTRAR CARRERAS")
            print("========================")
            print("1. Agregar carrera")
            print("2. Eliminar carrera")
            print("3. Consultar carreras")
            print("4. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.agregar_carrera()
            elif opcion == "2":
                self.eliminar_carrera()
            elif opcion == "3":
                self.consultar_carreras()
            elif opcion == "4":
                break
            else:
                print("\nOpción inválida")

    def administrar_materias(self) -> None:

        while True:
            print("\n========================")
            print("ADMINISTRAR MATERIAS")
            print("========================")
            print("1. Agregar Materia")
            print("2. Consultar Materia")
            print("3. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self._flujo_materia_por_modalidad(agregar=True)
            elif opcion == "2":
                self._flujo_materia_por_modalidad(agregar=False)
            elif opcion == "3":
                break
            else:
                print("\nOpción inválida")

    def _flujo_materia_por_modalidad(self, agregar: bool) -> None:

        modalidad = self._seleccionar_modalidad()

        if modalidad is None:
            return

        carrera = self._seleccionar_carrera_por_modalidad(modalidad)

        if carrera is None:
            return

        print()
        carrera.mostrar_carrera_con_materias()

        if agregar:
            self.agregar_materia_a_carrera(carrera)

    # ---------- MENÚ PRINCIPAL ----------

    def menu_gestion_personas(self) -> None:

        while True:
            print("\n========================")
            print("GESTIÓN ESTUDIANTES/PROFESORES")
            print("========================")
            print("1. Registrar estudiante")
            print("2. Registrar profesor")
            print("3. Consultar estudiantes")
            print("4. Consultar profesores")
            print("5. Editar estudiante")
            print("6. Editar profesor")
            print("7. Eliminar estudiante")
            print("8. Eliminar profesor")
            print("9. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.registrar_estudiante()
            elif opcion == "2":
                self.registrar_profesor()
            elif opcion == "3":
                self.consultar_estudiantes()
            elif opcion == "4":
                self.consultar_profesores()
            elif opcion == "5":
                self.editar_estudiante()
            elif opcion == "6":
                self.editar_profesor()
            elif opcion == "7":
                self.eliminar_estudiante()
            elif opcion == "8":
                self.eliminar_profesor()
            elif opcion == "9":
                break
            else:
                print("\nOpción inválida")

    def menu_gestion_universidad(self) -> None:

        while True:
            print("\n========================")
            print("GESTIÓN UNIVERSIDAD")
            print("========================")
            print("1. Administrar universidades")
            print("2. Administrar sedes")
            print("3. Administrar facultades")
            print("4. Administrar carreras")
            print("5. Administrar materia")
            print("6. Asignar curso a profesor")
            print("7. Volver")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.administrar_universidades()
            elif opcion == "2":
                self.administrar_sedes()
            elif opcion == "3":
                self.administrar_facultades()
            elif opcion == "4":
                self.administrar_carreras()
            elif opcion == "5":
                self.administrar_materias()
            elif opcion == "6":
                self.asignar_curso_profesor()
            elif opcion == "7":
                break
            else:
                print("\nOpción inválida")

    def mostrar(self) -> None:

        while True:
            print("\n========================")
            print("MENÚ ADMINISTRADOR")
            print("========================")
            print("1. Gestión Estudiantes/Profesores")
            print("2. Gestión Universidad")
            print("3. Cerrar sesión")
            opcion = input("\nSeleccione: ")

            if opcion == "1":
                self.menu_gestion_personas()
            elif opcion == "2":
                self.menu_gestion_universidad()
            elif opcion == "3":
                print("\nSesión de administrador cerrada")
                break
            else:
                print("\nOpción inválida")
