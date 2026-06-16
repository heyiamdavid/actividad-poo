from RepositorioBase import RepositorioBase

class GestorUniversidad:
   # INYECCIÓN DE DEPENDENCIAS:
    def __init__(self, repositorio: RepositorioBase):
        if not isinstance(repositorio, RepositorioBase):
            raise TypeError("repositorio debe implementar RepositorioBase")
        # Dependencia inyectada por constructor
        self.__repositorio = repositorio
    # Estudiantes 
    def registrar_estudiante(self, estudiante):
        self.__repositorio.guardar_estudiante(estudiante)

    def autenticar_estudiante(self, identificacion, contrasena):
        return self.__repositorio.validar_login_estudiante(identificacion, contrasena)

    def buscar_estudiante(self, identificacion):
        return self.__repositorio.buscar_estudiante(identificacion)

    def eliminar_estudiante(self, identificacion):
        self.__repositorio.eliminar_estudiante(identificacion)

    def listar_estudiantes(self):
        return self.__repositorio.listar_estudiantes()

    def total_estudiantes(self):
        return self.__repositorio.total_estudiantes()

    # Profesores 

    def registrar_profesor(self, profesor):
        self.__repositorio.guardar_profesor(profesor)

    def autenticar_profesor(self, identificacion, contrasena):
        return self.__repositorio.validar_login_profesor(identificacion, contrasena)

    def buscar_profesor(self, identificacion):
        return self.__repositorio.buscar_profesor(identificacion)

    def eliminar_profesor(self, identificacion):
        self.__repositorio.eliminar_profesor(identificacion)

    def listar_profesores(self):
        return self.__repositorio.listar_profesores()

    def total_profesores(self):
        return self.__repositorio.total_profesores()
