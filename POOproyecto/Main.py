from RepositorioSQLite import RepositorioSQLite
from Administrador import Administrador
from Sistema import Sistema
# Se instancia el repositorio que manejará la persistencia de datos, 
# conectándolo a la base de datos local 'universidad.db'
if __name__ == "__main__":
    repositorio = RepositorioSQLite("universidad.db")
    administrador = Administrador(repositorio) #inyección de dependencias
    app = Sistema(administrador) #Inyección de dependencias
    app.iniciar()
