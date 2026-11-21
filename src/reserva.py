"""Clase Reserva: integra cliente, servicio, duración, estado y excepciones."""

from datetime import datetime
from .excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)

class Reserva:
    """Reserva con estados controlados y manejo avanzado de excepciones."""

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada", "procesada")

    def __init__(self, cliente, servicio, duracion, registrador):
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = self.validar_duracion(duracion)
        self._registrador = registrador
        self._estado = "pendiente"
        self._fecha_creacion = datetime.now()
        self._costo = None

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    @staticmethod
    def validar_duracion(duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor que cero.")
        return float(duracion)

    def confirmar(self, impuestos=0.0, descuento=0.0):
        """Confirma la reserva delegando el cálculo sobrecargado al servicio."""
        if self._estado != "pendiente":
            raise OperacionNoPermitidaError("Solo se puede confirmar una reserva pendiente.")
        try:
            self._costo = self._servicio.calcular_costo(self._duracion, impuestos, descuento)
        except ServicioNoDisponibleError as error:
            self._registrador.error(f"Confirmación fallida {self._servicio.identificador}: {error}")
            raise ServicioNoDisponibleError("No se pudo confirmar: servicio no disponible.") from error
        except Exception as error:
            self._registrador.excepcion(f"Error inesperado al confirmar reserva: {error}")
            raise
        else:
            self._estado = "confirmada"
            self._registrador.evento(f"Reserva confirmada: {self._cliente.documento} -> {self._servicio.identificador}")
        finally:
            self._registrador.evento(f"Confirmación finalizada con estado '{self._estado}'.")
        return self._costo

    def cancelar(self):
        """Cancela la reserva siempre que no esté cancelada o procesada."""
        if self._estado in ("cancelada", "procesada"):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva '{self._estado}'.")
        self._estado = "cancelada"
        self._registrador.evento(f"Reserva cancelada: {self._servicio.identificador}")
        return True

    def procesar(self):
        """Procesa la reserva confirmada y cambia su estado a procesada."""
        if self._estado != "confirmada":
            raise OperacionNoPermitidaError("Solo se puede procesar una reserva confirmada.")
        try:
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError("El servicio dejó de estar disponible.")
        except ServicioNoDisponibleError as error:
            self._registrador.error(f"Procesamiento fallido: {error}")
            raise
        else:
            self._estado = "procesada"
            self._registrador.evento(f"Reserva procesada: {self._servicio.identificador}")
        return self._estado
