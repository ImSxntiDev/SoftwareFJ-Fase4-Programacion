"""Gestión centralizada del archivo de eventos y errores."""

import logging
from pathlib import Path

class RegistroEventos:
    """Configura el logger y registra eventos y errores en un archivo."""

    def __init__(self, ruta_archivo="logs/sistema.log"):
        self.ruta = Path(ruta_archivo)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("SoftwareFJ")
        self.logger.setLevel(logging.DEBUG)
        for manejador_actual in list(self.logger.handlers):
            self.logger.removeHandler(manejador_actual)
            manejador_actual.close()
        manejador = logging.FileHandler(self.ruta, encoding="utf-8")
        manejador.setLevel(logging.DEBUG)
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        manejador.setFormatter(formato)
        self.logger.addHandler(manejador)

    def evento(self, mensaje):
        """Escribe un mensaje con nivel INFO."""
        self.logger.info(mensaje)
        return None

    def error(self, mensaje):
        """Escribe un mensaje con nivel ERROR."""
        self.logger.error(mensaje)
        return None

    def excepcion(self, mensaje):
        """Escribe un mensaje con nivel ERROR e incluye la pila de llamadas."""
        self.logger.exception(mensaje)
        return None
