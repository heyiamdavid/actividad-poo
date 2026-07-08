from Administrador import Administrador
from MenuAdministrador import MenuAdministrador
from MenuEstudiante import MenuEstudiante
from MenuProfesor import MenuProfesor


# El Sistema únicamente muestra el menú de acceso inicial y delega en los menús específicos (Administrador, Estudiante, Profesor).
class Sistema:

    def __init__(self, administrador: Administrador):
        self.administrador: Administrador = administrador
    #Se validan los datos/credenciales para poder acceder al sistema 
    def acceder_administrador(self) -> None:

        print("\n========== LOGIN ADMINISTRADOR ==========\n")

        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        if not self.administrador.autenticar_administrador(identificacion, contrasena):
            print("\nCredenciales incorrectas")
            return

        menu_administrador = MenuAdministrador(self.administrador)
        menu_administrador.mostrar()

    def acceder_estudiante(self) -> None:

        print("\n========== LOGIN ESTUDIANTE ==========\n")

        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        estudiante = self.administrador.autenticar_estudiante(identificacion, contrasena)

        if estudiante is None:
            print("\nCredenciales incorrectas")
            return

        menu_estudiante = MenuEstudiante(self.administrador, estudiante)
        menu_estudiante.mostrar()

    def acceder_profesor(self) -> None:

        print("\n========== LOGIN PROFESOR ==========\n")

        identificacion = input("Identificación: ")
        contrasena = input("Contraseña: ")

        profesor = self.administrador.autenticar_profesor(identificacion, contrasena)

        if profesor is None:
            print("\nCredenciales incorrectas")
            return

        menu_profesor = MenuProfesor(self.administrador, profesor)
        menu_profesor.mostrar()

    #Iniciar el sistema en el main
    def iniciar(self) -> None:

        while True:
            print("\n=================================")
            print("SISTEMA UNIVERSITARIO")
            print("=================================")
            print("1. Administrador")
            print("2. Estudiante")
            print("3. Profesor")
            print("4. Salir")
            opcion = input("\nSeleccione: ")

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
                print("\nOpción inválida")
