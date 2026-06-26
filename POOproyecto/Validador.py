import random
import string
from typing import List, Optional, Tuple, TypeVar, TYPE_CHECKING

from ValidadorEslabon import (
    EslabonNoVacio,
    EslabonSoloLetras,
    EslabonMinimoPalabras,
    EslabonSoloDigitos,
    EslabonLongitudExacta,
    EslabonLongitudRango,
    EslabonSinSecuenciaRepetida,
    EslabonContieneArroba,
    EslabonRangoNumerico,
    EslabonEsNumerico,
    EslabonEsEntero,
    EslabonFormatoHora,
    EslabonSinEspacios,
    EslabonAlfanumerico,
    EslabonFormatoAula,
    EslabonIdentificacionUnica,
)

if TYPE_CHECKING:
    from Administrador import Administrador

T = TypeVar("T")


# Validador actúa como fachada del patrón Chain of Responsibility:
# construye la cadena de eslabones adecuada para cada campo y
# repite la solicitud por consola hasta que la cadena la acepte.
# La regla de validación vive en los eslabones (ValidadorEslabon.py);
# aquí solo se ensamblan las cadenas y se maneja el input.
class Validador:

    @staticmethod
    def leer_nombre_completo(mensaje: str = "Nombre completo: ") -> str:

        cadena = EslabonNoVacio("El nombre")
        cadena.encadenar(EslabonSoloLetras()).encadenar(EslabonMinimoPalabras(2))

        while True:
            nombre = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(nombre)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            partes = [parte for parte in nombre.split(" ") if parte != ""]
            return " ".join(partes)

    @staticmethod
    def leer_telefono(mensaje: str = "Teléfono: ") -> str:

        cadena = EslabonNoVacio("El teléfono")
        cadena.encadenar(EslabonSoloDigitos()).encadenar(EslabonLongitudRango(7, 10))

        while True:
            telefono = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(telefono)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return telefono

    @staticmethod
    def leer_email(mensaje: str = "Email: ") -> str:

        cadena = EslabonNoVacio("El email")
        cadena.encadenar(EslabonContieneArroba())

        while True:
            email = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(email)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return email

    @staticmethod
    def leer_identificacion(tipo_usuario: str, administrador: "Administrador",
                             mensaje: str = "Identificación (10 dígitos): ") -> str:

        cadena = EslabonNoVacio("La identificación")
        (
            cadena
            .encadenar(EslabonSoloDigitos())
            .encadenar(EslabonLongitudExacta(10))
            .encadenar(EslabonSinSecuenciaRepetida())
            .encadenar(EslabonIdentificacionUnica(administrador, tipo_usuario))
        )

        while True:
            identificacion = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(identificacion)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return identificacion

    @staticmethod
    def leer_nota(mensaje: str) -> float:

        cadena = EslabonEsNumerico()
        cadena.encadenar(EslabonRangoNumerico(0, 10))

        while True:
            valor = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(valor)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return float(valor)

    @staticmethod
    def leer_float(mensaje: str) -> float:

        cadena = EslabonEsNumerico()

        while True:
            valor = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(valor)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return float(valor)

    @staticmethod
    def leer_entero(mensaje: str) -> int:

        cadena = EslabonEsEntero()

        while True:
            valor = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(valor)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return int(valor)

    @staticmethod
    def leer_entero_en_rango(mensaje: str, minimo: int, maximo: int) -> int:
        # Para campos numéricos enteros con un rango de validez propio
        # (créditos, número de aula, capacidad del aula, etc).

        cadena = EslabonEsEntero()
        cadena.encadenar(EslabonRangoNumerico(minimo, maximo))

        while True:
            valor = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(valor)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return int(valor)

    @staticmethod
    def leer_semestre(mensaje: str = "Semestre: ", maximo: int = 10) -> int:

        cadena = EslabonEsEntero()
        cadena.encadenar(EslabonRangoNumerico(1, maximo))

        while True:
            valor = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(valor)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return int(valor)

    @staticmethod
    def leer_clave_nueva() -> Tuple[str, str]:

        while True:
            nueva = input("Nueva contraseña: ").strip()
            confirmacion = input("Confirme la nueva contraseña: ").strip()

            if len(nueva) < 4:
                print("\nError: La contraseña debe tener al menos 4 caracteres.")
                continue

            if nueva != confirmacion:
                print("\nError: Las contraseñas no coinciden.")
                continue

            return nueva, confirmacion

    @staticmethod
    def leer_texto(mensaje: str, nombre_campo: str = "El campo",
                    minimo_palabras: int = 1, solo_letras: bool = False) -> str:
        # Para nombres de carrera, facultad, sede, etc: no admite
        # dejarlo vacío (Enter) ni que esté compuesto solo de espacios.
        # Con solo_letras=True (ej. título de un profesor) tampoco
        # admite números ni símbolos.

        cadena = EslabonNoVacio(nombre_campo)

        if solo_letras:
            cadena.encadenar(EslabonSoloLetras())

        if minimo_palabras > 1:
            cadena.encadenar(EslabonMinimoPalabras(minimo_palabras))

        while True:
            texto = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(texto)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return texto

    @staticmethod
    def leer_codigo(mensaje: str, administrador: Optional["Administrador"] = None,
                     tipo_codigo: Optional[str] = None) -> str:
        # Para códigos de carrera/curso: alfanumérico, sin espacios,
        # no vacío. Si se indica administrador y tipo_codigo, también
        # valida que el código no esté ya en uso.

        cadena = EslabonNoVacio("El código")
        cadena.encadenar(EslabonSinEspacios()).encadenar(EslabonAlfanumerico())

        while True:
            codigo = input(mensaje).strip().upper()

            es_valido, mensaje_error = cadena.validar(codigo)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            if administrador is not None and tipo_codigo == "carrera":
                if administrador.buscar_carrera(codigo):
                    print(f"\nError: Ya existe una carrera con el código {codigo}.")
                    continue

            if administrador is not None and tipo_codigo == "curso":
                if administrador.buscar_curso(codigo):
                    print(f"\nError: Ya existe un curso con el código {codigo}.")
                    continue

            return codigo

    @staticmethod
    def leer_hora(mensaje: str) -> str:

        cadena = EslabonNoVacio("La hora")
        cadena.encadenar(EslabonFormatoHora())

        while True:
            hora = input(mensaje).strip()

            es_valido, mensaje_error = cadena.validar(hora)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return hora

    @staticmethod
    def leer_aula(mensaje: str = "Número de aula (ej. A101): ") -> str:
        # Formato real usado por las aulas del sistema: una letra de
        # bloque seguida de 3 dígitos (ej. A101, B204).

        cadena = EslabonNoVacio("El aula")
        cadena.encadenar(EslabonFormatoAula())

        while True:
            aula = input(mensaje).strip().upper()

            es_valido, mensaje_error = cadena.validar(aula)

            if not es_valido:
                print(f"\nError: {mensaje_error}")
                continue

            return aula

    @staticmethod
    def seleccionar_opcion(mensaje: str, opciones: List[T],
                            permitir_cancelar: bool = False) -> Optional[T]:
        # Muestra una lista numerada de opciones y devuelve la elegida.
        # Evita texto libre para campos cerrados (estado, modalidad, etc).
        # Si permitir_cancelar es True, se agrega la opción "0. Cancelar"
        # y, si el usuario la elige, el método devuelve None en vez de
        # forzarlo a escoger una de las opciones reales.
        while True:
            print(f"\n{mensaje}")

            if permitir_cancelar:
                print("0. Cancelar")

            for indice, opcion in enumerate(opciones, start=1):
                print(f"{indice}. {opcion}")

            seleccion = input("Seleccione una opción: ")

            if permitir_cancelar and seleccion == "0":
                return None

            if seleccion.isdigit() and 1 <= int(seleccion) <= len(opciones):
                return opciones[int(seleccion) - 1]

            print("\nError: Opción inválida.")

    @staticmethod
    def generar_clave_temporal() -> str:
        caracteres = string.ascii_letters + string.digits
        clave = ''.join(random.choice(caracteres) for i in range(6))
        return clave
