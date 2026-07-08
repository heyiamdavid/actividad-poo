from abc import ABC

# Importación de la interfaz/clase base que define el contrato de autenticación
from Autenticable import Autenticable

# Herencia Múltiple: La clase Persona hereda de Autenticable (adquiere sus métodos) 
# y de ABC (se convierte en una clase abstracta que no puede instanciarse directamente, 
# solo sirve como plantilla para Estudiante y Profesor).
class Persona(Autenticable, ABC):

    # Constructor base: Define los atributos comunes que compartirán todas las clases hijas
    def __init__(self,
                 nombre: str,
                 telefono: str,
                 email: str,
                 identificacion: str,
                 contrasena: str):

        # Atributos públicos de información general
        self.nombre: str = nombre
        self.telefono: str = telefono
        self.email: str = email
        self.identificacion: str = identificacion
        
        # ENCAPSULAMIENTO ESTRICTO
        # Atributo fuertemente privado (__) para proteger la contraseña real
        self.__contrasena: str = contrasena

        # La clave temporal queda fija desde el registro: es la que
        # el administrador entregó originalmente. Se conserva aunque
        # la persona cambie su contraseña, para que el administrador
        # pueda consultar ambas.
        self.__clave_temporal: str = contrasena

    # Encapsulación mediante Property (Getter)
    # Permite leer la contraseña privada de forma controlada sin exponer el atributo real
    @property
    def contrasena(self) -> str:
        return self.__contrasena

    # Encapsulación mediante Setter
    # Intercepta cualquier intento de cambiar la contraseña para aplicar reglas de validación
    @contrasena.setter
    def contrasena(self, nueva_contrasena: str) -> None:
        
        # Validación de longitud mínima por seguridad
        if len(nueva_contrasena) >= 4:
            self.__contrasena = nueva_contrasena
        else:
            print("Contraseña inválida")

    # Getter de solo lectura para la clave temporal (no tiene setter, así que no se puede mutar)
    @property
    def clave_temporal(self) -> str:
        return self.__clave_temporal

    # MÉTODOS DE NEGOCIO
    # Función de seguridad para actualizar credenciales con múltiples filtros
    def cambiar_contrasena(self, contrasena_actual: str, nueva_contrasena: str,
                            confirmacion_nueva: str) -> bool:

        # Validaciones tempranas (Guard Clauses) para abortar la operación rápido si algo falla
        
        # 1. Verifica que el usuario conozca su contraseña actual
        if contrasena_actual != self.__contrasena:
            print("\nLa contraseña actual no coincide.")
            return False

        # 2. Verifica que no se haya equivocado al tipear la nueva
        if nueva_contrasena != confirmacion_nueva:
            print("\nLas contraseñas nuevas no coinciden.")
            return False

        # 3. Verifica las políticas de seguridad (mínimo 4 caracteres)
        if len(nueva_contrasena) < 4:
            print("\nLa nueva contraseña debe tener al menos 4 caracteres.")
            return False

        # Si pasa todas las validaciones, usa el setter (self.contrasena) para actualizarla
        self.contrasena = nueva_contrasena
        print("\nContraseña actualizada correctamente.")
        return True

    # Método heredado de la interfaz/clase Autenticable
    # POLIMORFISMO: Implementación concreta del comportamiento de inicio de sesión
    def iniciar_sesion(self) -> None:
        print(f"\nBienvenido {self.nombre}")

    # Método heredado de la interfaz/clase Autenticable
    # POLIMORFISMO: Implementación concreta del comportamiento de cierre de sesión
    def cerrar_sesion(self) -> None:
        print(f"\nSesión cerrada para {self.nombre}")

    # Método genérico para imprimir la ficha de la persona
    # Al estar en la clase padre, las clases hijas pueden invocarlo con super().mostrar_datos()
    def mostrar_datos(self) -> None:
        print("\n========== DATOS ==========")
        print(f"Nombre: {self.nombre}")
        print(f"Teléfono: {self.telefono}")
        print(f"Email: {self.email}")
        print(f"Identificación: {self.identificacion}")
