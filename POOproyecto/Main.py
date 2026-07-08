from RepositorioSQLite import RepositorioSQLite
from Administrador import Administrador
from Sistema import Sistema

if __name__ == "__main__":
    repositorio = RepositorioSQLite("universidad.db")
    administrador = Administrador(repositorio) #inyección de dependencias
    app = Sistema(administrador) #Inyección de dependencias
    app.iniciar()
