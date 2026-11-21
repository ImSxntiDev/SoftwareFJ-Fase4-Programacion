"""Servicio abstracto y tres servicios especializados de Software FJ."""

from abc import ABC, abstractmethod
from typing import overload
from .entidades import Entidad
from .excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)

class Servicio(Entidad, ABC):
    """Servicio genérico con tarifa base, disponibilidad y cálculo sobrecargado."""

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        self._nombre = self.validar_nombre_servicio(nombre)
        self._tarifa_base = self.validar_tarifa(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @staticmethod
    def validar_nombre_servicio(nombre):
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre del servicio debe tener al menos tres caracteres.")
        return nombre.strip()

    @staticmethod
    def validar_tarifa(tarifa):
        if not isinstance(tarifa, (int, float)):
            raise DatoInvalidoError("La tarifa debe ser un número.")
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa debe ser mayor que cero.")
        return float(tarifa)

    # Python no sobrecarga en ejecución: se declaran firmas y se usa una sola implementación.
    @overload
    def calcular_costo(self) -> float: ...

    @overload
    def calcular_costo(self, duracion: int) -> float: ...

    @overload
    def calcular_costo(self, duracion: int, impuestos: float, descuento: float = 0.0) -> float: ...

    def calcular_costo(self, duracion=1, impuestos=0.0, descuento=0.0):
        """Simula sobrecarga: calcula el costo con parámetros opcionales."""
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise CalculoInconsistenteError("La duración debe ser un número positivo.")
        if not isinstance(impuestos, (int, float)) or impuestos < 0:
            raise CalculoInconsistenteError("Los impuestos no pueden ser negativos.")
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 1.")
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self._nombre} no está disponible.")
        subtotal = self._tarifa_base * duracion
        con_impuestos = subtotal * (1 + impuestos)
        total = con_impuestos * (1 - descuento)
        return round(total, 2)

    @abstractmethod
    def describir_servicio(self):
        """Devuelve una descripción específica del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Valida los parámetros propios de cada servicio."""
        pass

    def describir(self):
        return f"{self._nombre} (id={self.identificador}, tarifa={self._tarifa_base})"

# Cada servicio valida sus propios datos y sobrescribe su descripción.
class ReservaSala(Servicio):
    """Reserva de salas con control de capacidad."""

    def __init__(self, identificador, nombre, tarifa_base, capacidad):
        super().__init__(identificador, nombre, tarifa_base)
        self._capacidad = self.validar_parametros(capacidad=capacidad)

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self, **kwargs):
        capacidad = kwargs.get("capacidad")
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        return capacidad

    def describir_servicio(self):
        return f"Sala '{self.nombre}' para {self._capacidad} personas."

class AlquilerEquipos(Servicio):
    """Alquiler de equipos con control de stock."""

    def __init__(self, identificador, nombre, tarifa_base, stock, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self._stock = self.validar_parametros(stock=stock)

    @property
    def stock(self):
        return self._stock

    def validar_parametros(self, **kwargs):
        stock = kwargs.get("stock")
        if not isinstance(stock, int) or stock < 0:
            raise DatoInvalidoError("El stock de equipos no puede ser negativo.")
        return stock

    def describir_servicio(self):
        return f"Equipo '{self.nombre}' con {self._stock} unidades en stock."

class AsesoriaEspecializada(Servicio):
    """Asesoría especializada con área de conocimiento."""

    def __init__(self, identificador, nombre, tarifa_base, area, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self._area = self.validar_parametros(area=area)

    @property
    def area(self):
        return self._area

    def validar_parametros(self, **kwargs):
        area = kwargs.get("area")
        if not isinstance(area, str) or len(area.strip()) < 4:
            raise DatoInvalidoError("El área de la asesoría debe tener al menos cuatro caracteres.")
        return area.strip()

    def describir_servicio(self):
        return f"Asesoría '{self.nombre}' en {self._area}."
