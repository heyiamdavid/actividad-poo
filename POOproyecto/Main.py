from RepositorioSQLite import RepositorioSQLite
from Administrador import Administrador
from Sistema import Sistema

if __name__ == "__main__":
    repositorio = RepositorioSQLite("universidad.db")
    administrador = Administrador(repositorio)
    app = Sistema(administrador)
    app.iniciar()
