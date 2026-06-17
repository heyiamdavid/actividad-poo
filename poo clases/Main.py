import uvicorn
import sys
from Sistema import Sistema

if __name__ == "__main__":
    print("========================================")
    print("  SIGMA - SISTEMA UNIVERSITARIO")
    print("========================================")
    print("1. Iniciar Aplicacion de Consola (Pantalla negra)")
    print("2. Iniciar Servidor Web (Interfaz de navegador)")
    print("3. Salir")
    
    opcion = input("\nSelecciona el modo de inicio (1, 2 o 3): ")
    
    if opcion == "1":
        print("\nIniciando la aplicacion de consola")
        app = Sistema()
        app.iniciar()
    elif opcion == "2":
        print("\nIniciando el servidor Backend para la interfaz web")
        # El reload=False es necesario porque uvicorn da error con reload=True si hubo un input() antes
        uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
    elif opcion == "3":
        print("\nSaliendo")
        sys.exit()
    else:
        print("Opcion no valida. Saliendo")
        sys.exit()
