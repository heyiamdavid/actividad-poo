# Importación de módulos externos necesarios para la navegación y gestión de datos.
# Se importan los menús específicos para mantener la Responsabilidad Única en cada clase.
from Administrador import Administrador
from MenuAdministrador import MenuAdministrador
from MenuEstudiante import MenuEstudiante
from MenuProfesor import MenuProfesor


# Clase Sistema: Actúa como el controlador principal (Front Controller) de la aplicación.
# Su única responsabilidad es gestionar el acceso inicial y delegar el control 
# a las vistas (menús) correspondientes según el tipo de usuario.
class Sistema:

    # Constructor de la clase Sistema
    # Recibe una instancia de Administrador por Inyección de Dependencias.
    # Esto evita el alto acoplamiento y permite que el sistema comparta 
    # la misma fuente de datos en toda la ejecución.
    def __init__(self, administrador: Administrador):
        
        # Atributo público que almacena la instancia del gestor principal
        self.administrador: Administrador = administrador

    # Método de autenticación y ruteo para el perfil Administrador
    def acceder_administrador(self) -> None:

        print("\n========== LOGIN ADMINISTRADOR ==========\n")

        # Captura de credenciales por entrada estándar (CLI)
        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        # Validación de seguridad delegada a la clase Administrador.
        # Si la autenticación falla, se interrumpe el flujo (return temprano)
        if not self.administrador.autenticar_administrador(identificacion, contrasena):
            print("\nCredenciales incorrectas")
            return

        # Si el login es exitoso, se instancia y despliega la vista específica del administrador
        menu_administrador = MenuAdministrador(self.administrador)
        menu_administrador.mostrar()

    # Método de autenticación y ruteo para el perfil Estudiante
    def acceder_estudiante(self) -> None:

        print("\n========== LOGIN ESTUDIANTE ==========\n")

        # Captura de credenciales
        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        # Consulta al gestor (Administrador) para verificar la existencia y validez del estudiante
        estudiante = self.administrador.autenticar_estudiante(identificacion, contrasena)

        # Validación: Si el objeto retornado es None, el login falla
        if estudiante is None:
            print("\nCredenciales incorrectas")
            return

        # Despliegue de la vista del estudiante, pasando su propia instancia para personalizar su sesión
        menu_estudiante = MenuEstudiante(self.administrador, estudiante)
        menu_estudiante.mostrar()

    # Método de autenticación y ruteo para el perfil Profesor
    def acceder_profesor(self) -> None:

        print("\n========== LOGIN PROFESOR ==========\n")

        # Captura de credenciales
        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        # Consulta al gestor para validar al profesor en la base de datos
        profesor = self.administrador.autenticar_profesor(identificacion, contrasena)

        # Control de errores de autenticación
        if profesor is None:
            print("\nCredenciales incorrectas")
            return

        # Transición al submenú del profesor inyectando su instancia específica
        menu_profesor = MenuProfesor(self.administrador, profesor)
        menu_profesor.mostrar()

    # Bucle principal de ejecución (Ciclo de vida del programa)
    def iniciar(self) -> None:

        # Bucle infinito que mantiene la consola activa hasta recibir la orden de quiebre (break)
        while True:
            print("\n=================================")
            print("SISTEMA UNIVERSITARIO")
            print("=================================")
            print("1. Administrador")
            print("2. Estudiante")
            print("3. Profesor")
            print("4. Salir")

            # Captura de la selección del usuario
            opcion = input("\nSeleccione: ")

            # Estructura de control condicional para enrutar el flujo del programa
            if opcion == "1":
                self.acceder_administrador()
            elif opcion == "2":
                self.acceder_estudiante()
            elif opcion == "3":
                self.acceder_profesor()
            elif opcion == "4":
                # Finalización controlada del proceso
                print("\nPrograma finalizado")
                break
            else:
                # Manejo de excepciones para entradas fuera de rango
                print("\nOpción inválida")
