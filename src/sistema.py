"""Fachada del sistema sin base de datos: listas internas y logs."""

from .entidades import Cliente
from .reserva import Reserva
from .excepciones import DatoInvalidoError, ParametroFaltanteError

class SistemaGestion:
    """Sistema integral de Software FJ sin motor de base de datos."""

    def __init__(self, registrador):
        self.registrador = registrador
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    def registrar_cliente(self, documento=None, nombre=None, correo=None, telefono=None):
        """Registra un cliente validando parámetros, datos y duplicados."""
        datos = {"documento": documento, "nombre": nombre, "correo": correo, "telefono": telefono}
        try:
            # Reviso los parámetros antes de crear el cliente.
            for clave, valor in datos.items():
                if valor is None:
                    raise ParametroFaltanteError(f"Falta el parámetro '{clave}'.")
            cliente = Cliente(documento, nombre, correo, telefono)
            if any(c.documento == cliente.documento for c in self._clientes):
                raise DatoInvalidoError(f"El cliente {cliente.documento} ya está registrado.")
        except (ParametroFaltanteError, DatoInvalidoError) as error:
            self.registrador.error(f"Registro de cliente fallido: {error}")
            raise
        else:
            self._clientes.append(cliente)
            self.registrador.evento(f"Cliente registrado: {cliente.documento}")
        finally:
            self.registrador.evento(f"Intento de registro con documento '{documento}' finalizado.")
        return cliente

    def agregar_servicio(self, servicio):
        """Agrega un servicio validando que el parámetro no sea None."""
        if servicio is None:
            raise ParametroFaltanteError("No se recibió el servicio a agregar.")
        self._servicios.append(servicio)
        self.registrador.evento(f"Servicio agregado: {servicio.identificador}")
        return servicio

    def crear_reserva(self, documento_cliente, id_servicio, duracion):
        """Crea una reserva buscando cliente y servicio en las listas internas."""
        cliente = next((c for c in self._clientes if c.documento == documento_cliente), None)
        servicio = next((s for s in self._servicios if s.identificador == id_servicio), None)
        if cliente is None:
            raise ParametroFaltanteError(f"No existe el cliente {documento_cliente}.")
        if servicio is None:
            raise ParametroFaltanteError(f"No existe el servicio {id_servicio}.")
        reserva = Reserva(cliente, servicio, duracion, self.registrador)
        self._reservas.append(reserva)
        self.registrador.evento(f"Reserva creada: {cliente.documento} -> {servicio.identificador}")
        return reserva
