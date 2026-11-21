"""Clase Reserva: integra cliente, servicio, duración, estado y excepciones."""  # Docstring del módulo.

from datetime import datetime  # Importa datetime para sellar la fecha de creación.
from .excepciones import (  # Importa las excepciones propias utilizadas.
    ReservaInvalidaError,  # Error de duración inválida.
    OperacionNoPermitidaError,  # Error de operación según estado.
    ServicioNoDisponibleError,  # Error de disponibilidad del servicio.
)


class Reserva:  # Representa una reserva de un servicio por parte de un cliente.
    """Reserva con estados controlados y manejo avanzado de excepciones."""  # Documentación.

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada", "procesada")  # Estados permitidos.

    def __init__(self, cliente, servicio, duracion, registrador):  # Constructor con dependencias.
        self._cliente = cliente  # Guarda la referencia al cliente.
        self._servicio = servicio  # Guarda la referencia al servicio.
        self._duracion = self.validar_duracion(duracion)  # Valida y guarda la duración.
        self._registrador = registrador  # Guarda el registrador de eventos.
        self._estado = "pendiente"  # Establece el estado inicial.
        self._fecha_creacion = datetime.now()  # Sella la fecha y hora de creación.
        self._costo = None  # El costo se calculará al confirmar la reserva.

    @property  # Propiedad de solo lectura.
    def cliente(self):  # Devuelve el cliente asociado.
        return self._cliente  # Retorna la referencia guardada.

    @property  # Propiedad de solo lectura.
    def servicio(self):  # Devuelve el servicio asociado.
        return self._servicio  # Retorna la referencia guardada.

    @property  # Propiedad de solo lectura.
    def duracion(self):  # Devuelve la duración.
        return self._duracion  # Retorna la duración validada.

    @property  # Propiedad de solo lectura.
    def estado(self):  # Devuelve el estado actual.
        return self._estado  # Retorna el estado guardado.

    @property  # Propiedad de solo lectura.
    def costo(self):  # Devuelve el costo calculado.
        return self._costo  # Retorna el costo (puede ser None si aún no se confirma).

    @staticmethod  # Validación estática.
    def validar_duracion(duracion):  # Valida que la duración sea positiva.
        if not isinstance(duracion, (int, float)) or duracion <= 0:  # Comprueba tipo y valor.
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor que cero.")  # Lanza error propio.
        return float(duracion)  # Devuelve la duración convertida a float.

    def confirmar(self, impuestos=0.0, descuento=0.0):  # Confirma la reserva y calcula el costo.
        """Confirma la reserva delegando el cálculo sobrecargado al servicio."""  # Documentación.
        if self._estado != "pendiente":  # Solo se pueden confirmar reservas pendientes.
            raise OperacionNoPermitidaError("Solo se puede confirmar una reserva pendiente.")  # Lanza error.
        try:  # Inicia el bloque de manejo de excepciones.
            self._costo = self._servicio.calcular_costo(self._duracion, impuestos, descuento)  # Calcula el costo.
        except ServicioNoDisponibleError as error:  # Captura error específico de disponibilidad.
            self._registrador.error(f"Confirmación fallida {self._servicio.identificador}: {error}")  # Registra.
            raise ServicioNoDisponibleError("No se pudo confirmar: servicio no disponible.") from error  # Encadena.
        except Exception as error:  # Captura cualquier otro error no previsto.
            self._registrador.excepcion(f"Error inesperado al confirmar reserva: {error}")  # Registra con traza.
            raise  # Propaga la excepción original sin alterarla.
        else:  # Se ejecuta únicamente si no ocurrió ninguna excepción.
            self._estado = "confirmada"  # Cambia el estado a confirmada.
            self._registrador.evento(f"Reserva confirmada: {self._cliente.documento} -> {self._servicio.identificador}")  # Registra.
        finally:  # Se ejecuta siempre, con error o sin error.
            self._registrador.evento(f"Confirmación finalizada con estado '{self._estado}'.")  # Registra el cierre.
        return self._costo  # Devuelve el costo calculado.

    def cancelar(self):  # Cancela una reserva pendiente o confirmada.
        """Cancela la reserva siempre que no esté cancelada o procesada."""  # Documentación.
        if self._estado in ("cancelada", "procesada"):  # Valida el estado antes de cancelar.
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva '{self._estado}'.")  # Lanza error.
        self._estado = "cancelada"  # Actualiza el estado a cancelada.
        self._registrador.evento(f"Reserva cancelada: {self._servicio.identificador}")  # Registra el evento.
        return True  # Devuelve True para indicar éxito.

    def procesar(self):  # Procesa una reserva confirmada.
        """Procesa la reserva confirmada y cambia su estado a procesada."""  # Documentación.
        if self._estado != "confirmada":  # Valida que la reserva esté confirmada.
            raise OperacionNoPermitidaError("Solo se puede procesar una reserva confirmada.")  # Lanza error.
        try:  # Inicia el bloque de verificación de disponibilidad.
            if not self._servicio.disponible:  # Comprueba la disponibilidad actual.
                raise ServicioNoDisponibleError("El servicio dejó de estar disponible.")  # Lanza error controlado.
        except ServicioNoDisponibleError as error:  # Captura el error de disponibilidad.
            self._registrador.error(f"Procesamiento fallido: {error}")  # Registra el fallo.
            raise  # Propaga el error al llamador.
        else:  # Se ejecuta si el servicio sí está disponible.
            self._estado = "procesada"  # Actualiza el estado a procesada.
            self._registrador.evento(f"Reserva procesada: {self._servicio.identificador}")  # Registra el evento.
        return self._estado  # Devuelve el estado final.
