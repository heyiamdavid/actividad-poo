from Administrador import Administrador
from MenuAdministrador import MenuAdministrador
from MenuEstudiante import MenuEstudiante
from MenuProfesor import MenuProfesor


# El Sistema únicamente muestra el menú de acceso inicial
# y delega el control a los menús específicos (Administrador, Estudiante y Profesor).
class Sistema:

    # Constructor de la clase Sistema
    def __init__(self, administrador: Administrador):

        # Guarda la instancia del administrador principal del sistema
        self.administrador: Administrador = administrador

    # Permite el acceso al menú del administrador validando sus credenciales
    def acceder_administrador(self) -> None:

        print("\n========== LOGIN ADMINISTRADOR ==========\n")

        # Solicita las credenciales del administrador
        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        # Verifica si las credenciales son correctas
        if not self.administrador.autenticar_administrador(identificacion, contrasena):
            print("\nCredenciales incorrectas")
            return

        # Si la autenticación es exitosa, muestra el menú del administrador
        menu_administrador = MenuAdministrador(self.administrador)
        menu_administrador.mostrar()

    # Permite el acceso al menú del estudiante validando sus credenciales
    def acceder_estudiante(self) -> None:

        print("\n========== LOGIN ESTUDIANTE ==========\n")

        # Solicita las credenciales del estudiante
        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        # Busca y autentica al estudiante
        estudiante = self.administrador.autenticar_estudiante(identificacion, contrasena)

        # Si no existe o las credenciales son incorrectas
        if estudiante is None:
            print("\nCredenciales incorrectas")
            return

        # Muestra el menú correspondiente al estudiante autenticado
        menu_estudiante = MenuEstudiante(self.administrador, estudiante)
        menu_estudiante.mostrar()

    # Permite el acceso al menú del profesor validando sus credenciales
    def acceder_profesor(self) -> None:

        print("\n========== LOGIN PROFESOR ==========\n")

        # Solicita las credenciales del profesor
        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        # Busca y autentica al profesor
        profesor = self.administrador.autenticar_profesor(identificacion, contrasena)

        # Si no existe o las credenciales son incorrectas
        if profesor is None:
            print("\nCredenciales incorrectas")
            return

        # Muestra el menú correspondiente al profesor autenticado
        menu_profesor = MenuProfesor(self.administrador, profesor)
        menu_profesor.mostrar()

    # Inicia el sistema mostrando el menú principal
    def iniciar(self) -> None:

        # Mantiene el menú activo hasta que el usuario decida salir
        while True:
            print("\n=================================")
            print("SISTEMA UNIVERSITARIO")
            print("=================================")
            print("1. Administrador")
            print("2. Estudiante")
            print("3. Profesor")
            print("4. Salir")

            # Solicita una opción al usuario
            opcion = input("\nSeleccione: ")

            # Redirige al menú correspondiente según la opción elegida
            if opcion == "1":
                self.acceder_administrador()
            elif opcion == "2":
                self.acceder_estudiante()
            elif opcion == "3":
                self.acceder_profesor()
            elif opcion == "4":
                print("\nPrograma finalizado")
                break
            else:
                # Se muestra cuando el usuario ingresa una opción no válida
                print("\nOpción inválida")