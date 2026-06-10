from DATABASE import *

crear_bd()
while True:

    print("\n===== SISTEMA =====")
    print("1. Registrar profesor")
    print("2. Registrar Estudiante")
    print("3. Buscar profesor")
    print("4. Buscar Estudiante")
    print("5. Mostrar profesores")
    print("6. Mostrar Estudiantes")
    print("7. Salir")

    opcion = input("Seleccione: ")

    if opcion == "1":

        nombre = input("Nombre: ")
        telefono = input("Telefono: ")
        email = input("Email: ")
        materia = input("Materia: ")
        titulo = input("Titulo: ")

        guardar_profesor(
            nombre,
            telefono,
            email,
            materia,
            titulo
        )

        print("Profesor guardado")

    elif opcion == "2":

        print("\n===== REGISTRO ESTUDIANTE =====\n")

        nombre = input("Nombre: ")
        telefono = input("Teléfono: ")
        email = input("Email: ")
        identificacion = input("Identificación: ")

        modalidad = input("Modalidad: ")
        estado = input("Estado: ")

        guardar_estudiante(
            nombre,
            telefono,
            email,
            identificacion,
            modalidad,
            estado
        )

        print("\nEstudiante guardado correctamente.")

    elif opcion == "3":

        nombre = input("Nombre a buscar: ")

        profesor = buscar_profesor(nombre)

        if profesor:
            print("\n===== DATOS DEL PROFESOR =====")
            print(f"ID: {profesor[0]}")
            print(f"Nombre: {profesor[1]}")
            print(f"Teléfono: {profesor[2]}")
            print(f"Email: {profesor[3]}")
            print(f"Materia: {profesor[4]}")
            print(f"Título: {profesor[5]}")
            print("==============================")

    elif opcion == "4":
        nombre = input("\nNombre del estudiante: ")
        estudiante = buscar_estudiante(nombre)

        if estudiante:

            print("\n===== DATOS DEL ESTUDIANTE =====")

            print(f"ID: {estudiante[0]}")
            print(f"Nombre: {estudiante[1]}")
            print(f"Teléfono: {estudiante[2]}")
            print(f"Email: {estudiante[3]}")
            print(f"Identificación: {estudiante[4]}")
            print(f"Modalidad: {estudiante[5]}")
            print(f"Estado: {estudiante[6]}")
            print("=" * 35)
        else:
            print("Estudiante no encontrado.")

    elif opcion == "5":
        for profesor in mostrar_profesores():
                print("\n-------------------------")
                print(f"ID: {profesor[0]}")
                print(f"Nombre: {profesor[1]}")
                print(f"Teléfono: {profesor[2]}")
                print(f"Email: {profesor[3]}")
                print(f"Materia: {profesor[4]}")
                print(f"Título: {profesor[5]}")
        
    elif opcion == "6":
     print("\n===== LISTA DE ESTUDIANTES =====")
     for estudiante in mostrar_estudiantes():

            print(f"""
            ID: {estudiante[0]}
            Nombre: {estudiante[1]}
            Teléfono: {estudiante[2]}
            Email: {estudiante[3]}
            Identificación: {estudiante[4]}
            Modalidad: {estudiante[5]}
            Estado: {estudiante[6]}
            ----------------------------------------
            """)

    elif opcion == "7":
        break
