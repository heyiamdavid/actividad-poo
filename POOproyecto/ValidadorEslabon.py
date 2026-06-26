from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from Administrador import Administrador


# Patrón de Comportamiento: Chain of Responsibility.
#
# Cada eslabón valida una sola regla sobre el valor recibido. Si la
# regla se cumple, delega en el siguiente eslabón de la cadena (si
# existe). Si no se cumple, la cadena se detiene y devuelve el
# mensaje de error correspondiente a esa regla, sin que el resto de
# eslabones se evalúen.
#
# Esto permite componer distintas cadenas de validación (nombre,
# teléfono, email, identificación, nota...) reutilizando los mismos
# eslabones básicos, en lugar de repetir condicionales sueltos.
class ValidadorEslabon(ABC):

    def __init__(self):
        self._siguiente: Optional["ValidadorEslabon"] = None

    def encadenar(self, siguiente_eslabon: "ValidadorEslabon") -> "ValidadorEslabon":

        self._siguiente = siguiente_eslabon
        return siguiente_eslabon

    def validar(self, valor: Any) -> Tuple[bool, str]:

        es_valido, mensaje_error = self._validar_regla(valor)

        if not es_valido:
            return False, mensaje_error

        if self._siguiente is not None:
            return self._siguiente.validar(valor)

        return True, ""

    @abstractmethod
    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:
        # Cada subclase implementa su propia regla puntual.
        # Devuelve una tupla (es_valido: bool, mensaje_error: str)
        pass


# ---------- ESLABONES GENÉRICOS (reutilizables entre campos) ----------

class EslabonNoVacio(ValidadorEslabon):

    def __init__(self, nombre_campo: str = "El campo"):
        super().__init__()
        self.nombre_campo: str = nombre_campo

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if valor is None or str(valor).strip() == "":
            return False, f"{self.nombre_campo} no puede estar vacío."

        return True, ""


class EslabonSoloLetras(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        texto = str(valor).replace(" ", "")

        if not texto.isalpha():
            return False, "El campo solo puede contener letras."

        return True, ""


class EslabonMinimoPalabras(ValidadorEslabon):

    def __init__(self, minimo_palabras: int = 2):
        super().__init__()
        self.minimo_palabras: int = minimo_palabras

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        partes = [parte for parte in str(valor).split(" ") if parte != ""]

        if len(partes) < self.minimo_palabras:
            return False, (
                f"Debe ingresar al menos {self.minimo_palabras} "
                f"palabras (nombre y apellido)."
            )

        return True, ""


class EslabonSoloDigitos(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if not str(valor).isdigit():
            return False, "El campo solo puede contener números."

        return True, ""


class EslabonLongitudExacta(ValidadorEslabon):

    def __init__(self, longitud: int):
        super().__init__()
        self.longitud: int = longitud

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if len(str(valor)) != self.longitud:
            return False, f"El campo debe tener exactamente {self.longitud} caracteres."

        return True, ""


class EslabonLongitudRango(ValidadorEslabon):

    def __init__(self, minimo: int, maximo: int):
        super().__init__()
        self.minimo: int = minimo
        self.maximo: int = maximo

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if not (self.minimo <= len(str(valor)) <= self.maximo):
            return False, (
                f"El campo debe tener entre {self.minimo} "
                f"y {self.maximo} caracteres."
            )

        return True, ""


class EslabonSinSecuenciaRepetida(ValidadorEslabon):

    SECUENCIAS_INVALIDAS: List[str] = [
        "1234567890", "0123456789",
        "9876543210", "0987654321"
    ]

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        texto = str(valor)

        if len(set(texto)) == 1:
            return False, "El campo no puede ser una secuencia de dígitos repetidos."

        if texto in self.SECUENCIAS_INVALIDAS:
            return False, "El campo no puede ser una secuencia numérica obvia."

        return True, ""


class EslabonContieneArroba(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        texto = str(valor)

        if "@" not in texto or "." not in texto:
            return False, "Ingrese un email válido (ejemplo@dominio.com)."

        usuario, _, dominio = texto.partition("@")

        if usuario == "" or "." not in dominio or dominio.startswith("."):
            return False, "Ingrese un email válido (ejemplo@dominio.com)."

        return True, ""


class EslabonRangoNumerico(ValidadorEslabon):

    def __init__(self, minimo: float, maximo: float):
        super().__init__()
        self.minimo: float = minimo
        self.maximo: float = maximo

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        try:
            numero = float(valor)
        except (TypeError, ValueError):
            return False, "Debe ingresar un valor numérico válido."

        if not (self.minimo <= numero <= self.maximo):
            return False, f"El valor debe estar entre {self.minimo} y {self.maximo}."

        return True, ""


class EslabonEsNumerico(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        try:
            float(valor)
        except (TypeError, ValueError):
            return False, "Debe ingresar un valor numérico válido."

        return True, ""


class EslabonEsEntero(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        try:
            int(valor)
        except (TypeError, ValueError):
            return False, "Debe ingresar un número entero válido."

        return True, ""


class EslabonFormatoHora(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        texto = str(valor).strip()
        partes = texto.split(":")

        if len(partes) != 2:
            return False, "La hora debe tener el formato HH:MM (ej. 08:00)."

        hora_texto, minuto_texto = partes

        if not (hora_texto.isdigit() and minuto_texto.isdigit()):
            return False, "La hora debe tener el formato HH:MM (ej. 08:00)."

        hora, minuto = int(hora_texto), int(minuto_texto)

        if not (0 <= hora <= 23 and 0 <= minuto <= 59):
            return False, "La hora debe estar entre 00:00 y 23:59."

        return True, ""


class EslabonSinEspacios(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if " " in str(valor):
            return False, "El campo no puede contener espacios."

        return True, ""


class EslabonAlfanumerico(ValidadorEslabon):

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if not str(valor).isalnum():
            return False, "El campo solo puede contener letras y números, sin espacios."

        return True, ""


class EslabonFormatoAula(ValidadorEslabon):
    # Formato real usado por las aulas del sistema: una letra de
    # bloque seguida de exactamente 3 dígitos (ej. A101, B204, D304).

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        texto = str(valor).strip().upper()

        if len(texto) != 4:
            return False, "El aula debe tener el formato Bloque + 3 dígitos (ej. A101)."

        bloque, numero = texto[0], texto[1:]

        if not bloque.isalpha():
            return False, "El aula debe iniciar con una letra de bloque (ej. A101)."

        if not numero.isdigit():
            return False, "El aula debe tener 3 dígitos después del bloque (ej. A101)."

        return True, ""


# ---------- ESLABONES ESPECÍFICOS DE NEGOCIO ----------
# Dependen del administrador para consultar duplicados, por lo que se
# construyen en tiempo de uso y no son genéricos como los anteriores.

class EslabonIdentificacionUnica(ValidadorEslabon):

    def __init__(self, administrador: "Administrador", tipo_usuario: str):
        super().__init__()
        self.administrador: "Administrador" = administrador
        self.tipo_usuario: str = tipo_usuario

    def _validar_regla(self, valor: Any) -> Tuple[bool, str]:

        if self.tipo_usuario == "estudiante":
            existe = self.administrador.buscar_estudiante(valor) is not None
        elif self.tipo_usuario == "profesor":
            existe = self.administrador.buscar_profesor(valor) is not None
        else:
            existe = False

        if existe:
            return False, f"Ya existe un {self.tipo_usuario} con esa identificación."

        return True, ""
