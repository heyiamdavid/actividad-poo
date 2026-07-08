#Esta clase representa un aula dentro del sistema universitario
class Aula:
    def __init__(self,
                 numeroAula: str,
                 capacidad: int):
        self.numeroAula: str = numeroAula
        self.__capacidad: int = capacidad #atributo encapsulado

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, nueva_capacidad: int) -> None:
        if nueva_capacidad > 0:
            self.__capacidad = nueva_capacidad
       #si se ingresa una cantidad invalida dará un error y se pedirá ingresar nuevamente
        else:
            print("Capacidad inválida, ingrese un rango válido")

    def es_la_misma(self, otra_aula: "Aula") -> bool:

        return self.numeroAula == otra_aula.numeroAula

    # MÉTODOS
    def mostrar_aula(self) -> None:
        print(
            f"Aula {self.numeroAula} "
            f"(Capacidad: {self.__capacidad})"
        )
