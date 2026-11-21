"""Fachada del sistema sin base de datos: listas internas y logs."""  # Docstring del módulo.

from .entidades import Cliente  # Importa la clase Cliente.
from .reserva import Reserva  # Importa la clase Reserva.
from .excepciones import DatoInvalidoError, ParametroFaltanteError  # Importa excepciones propias.


class SistemaGestion:  # Administra clientes, servicios y reservas en memoria.
    """Sistema integral de Software FJ sin motor de base de datos."""  # Documentación.

    def __init__(self, registrador):  # Constructor que recibe el registrador.
        self.registrador = registrador  # Guarda el registrador como atributo público.
        self._clientes = []  # Lista interna de clientes.
        self._servicios = []  # Lista interna de servicios.
        self._reservas = []  # Lista interna de reservas.

    @property  # Propiedad de solo lectura.
    def clientes(self):  # Devuelve la lista de clientes.
        return list(self._clientes)  # Devuelve una copia para proteger la lista interna.

    @property  # Propiedad de solo lectura.
    def servicios(self):  # Devuelve la lista de servicios.
        return list(self._servicios)  # Devuelve una copia para proteger la lista interna.

    @property  # Propiedad de solo lectura.
    def reservas(self):  # Devuelve la lista de reservas.
        return list(self._reservas)  # Devuelve una copia para proteger la lista interna.

    def registrar_cliente(self, documento=None, nombre=None, correo=None, telefono=None):  # Registra un cliente.
        """Registra un cliente validando parámetros, datos y duplicados."""  # Documentación.
        datos = {"documento": documento, "nombre": nombre, "correo": correo, "telefono": telefono}  # Agrupa parámetros.
        try:  # Inicia el manejo controlado de errores.
            for clave, valor in datos.items():  # Recorre cada parámetro obligatorio.
                if valor is None:  # Detecta un parámetro faltante.
                    raise ParametroFaltanteError(f"Falta el parámetro '{clave}'.")  # Lanza error propio.
            cliente = Cliente(documento, nombre, correo, telefono)  # Crea el cliente y valida sus datos.
            if any(c.documento == cliente.documento for c in self._clientes):  # Comprueba duplicados.
                raise DatoInvalidoError(f"El cliente {cliente.documento} ya está registrado.")  # Lanza error.
        except (ParametroFaltanteError, DatoInvalidoError) as error:  # Captura los errores esperados.
            self.registrador.error(f"Registro de cliente fallido: {error}")  # Registra el error en el log.
            raise  # Propaga la excepción original al llamador.
        else:  # Se ejecuta únicamente si no hubo errores.
            self._clientes.append(cliente)  # Agrega el cliente a la lista interna.
            self.registrador.evento(f"Cliente registrado: {cliente.documento}")  # Registra el evento.
        finally:  # Se ejecuta siempre, con error o sin error.
            self.registrador.evento(f"Intento de registro con documento '{documento}' finalizado.")  # Registra cierre.
        return cliente  # Devuelve el cliente creado.

    def agregar_servicio(self, servicio):  # Agrega un servicio a la lista interna.
        """Agrega un servicio validando que el parámetro no sea None."""  # Documentación.
        if servicio is None:  # Comprueba que se haya recibido un servicio.
            raise ParametroFaltanteError("No se recibió el servicio a agregar.")  # Lanza error propio.
        self._servicios.append(servicio)  # Agrega el servicio a la lista interna.
        self.registrador.evento(f"Servicio agregado: {servicio.identificador}")  # Registra el evento.
        return servicio  # Devuelve el servicio agregado.

    def crear_reserva(self, documento_cliente, id_servicio, duracion):  # Crea una reserva.
        """Crea una reserva buscando cliente y servicio en las listas internas."""  # Documentación.
        cliente = next((c for c in self._clientes if c.documento == documento_cliente), None)  # Busca el cliente.
        servicio = next((s for s in self._servicios if s.identificador == id_servicio), None)  # Busca el servicio.
        if cliente is None:  # Verifica que el cliente exista.
            raise ParametroFaltanteError(f"No existe el cliente {documento_cliente}.")  # Lanza error propio.
        if servicio is None:  # Verifica que el servicio exista.
            raise ParametroFaltanteError(f"No existe el servicio {id_servicio}.")  # Lanza error propio.
        reserva = Reserva(cliente, servicio, duracion, self.registrador)  # Crea la reserva y valida duración.
        self._reservas.append(reserva)  # Agrega la reserva a la lista interna.
        self.registrador.evento(f"Reserva creada: {cliente.documento} -> {servicio.identificador}")  # Registra evento.
        return reserva  # Devuelve la reserva creada.
