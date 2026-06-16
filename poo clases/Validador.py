import random
import string
from BaseDatos import buscar_estudiante, buscar_profesor

class Validador:
    
    @staticmethod
    def validar_secuencia(identificacion):
        if len(set(identificacion)) == 1:
            return False
        secuencias_invalidas = [
            "1234567890", "0123456789", 
            "9876543210", "0987654321"
        ]
        if identificacion in secuencias_invalidas:
            return False
        return True

    @staticmethod
    def leer_identificacion(tipo_usuario):
        while True:
            identificacion = input("Identificación (10 dígitos): ")
            if len(identificacion) == 10 and identificacion.isdigit():
                if not Validador.validar_secuencia(identificacion):
                    print("\nError: La identificación no puede ser repetida o secuencial.")
                    continue
                
                if tipo_usuario == "estudiante":
                    if buscar_estudiante(identificacion):
                        print("\nError: Ya existe un estudiante con esa identificación.")
                        continue
                elif tipo_usuario == "profesor":
                    if buscar_profesor(identificacion):
                        print("\nError: Ya existe un profesor con esa identificación.")
                        continue
                return identificacion
            else:
                print("\nError: La identificación debe tener exactamente 10 números.")

    @staticmethod
    def leer_float(mensaje):
        while True:
            try:
                valor = float(input(mensaje))
                return valor
            except ValueError:
                print("\nError: Debe ingresar un valor numérico válido.")

    @staticmethod
    def leer_nota(mensaje):
        while True:
            try:
                valor = float(input(mensaje))
                if 0 <= valor <= 10:
                    return valor
                else:
                    print("\nError: La nota/promedio debe estar entre 0 y 10.")
            except ValueError:
                print("\nError: Debe ingresar un valor numérico válido.")

    @staticmethod
    def leer_email():
        while True:
            email = input("Email: ")
            if "@" in email and "." in email:
                return email
            else:
                print("\nError: Ingrese un email válido (ejemplo@dominio.com).")

    @staticmethod
    def generar_clave_temporal():
        caracteres = string.ascii_letters + string.digits
        clave = ''.join(random.choice(caracteres) for i in range(6))
        return clave
