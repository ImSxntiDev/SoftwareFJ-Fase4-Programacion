"""Gestión centralizada del archivo de eventos y errores."""  # Docstring del módulo.

import logging  # Importa el módulo estándar de registro de eventos.
from pathlib import Path  # Importa Path para construir rutas portables.


class RegistroEventos:  # Clase encargada de escribir el log del sistema.
    """Configura el logger y registra eventos y errores en un archivo."""  # Documentación de la clase.

    def __init__(self, ruta_archivo="logs/sistema.log"):  # Constructor con ruta por defecto.
        self.ruta = Path(ruta_archivo)  # Convierte la ruta recibida en un objeto Path.
        self.ruta.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta 'logs' si todavía no existe.
        self.logger = logging.getLogger("SoftwareFJ")  # Obtiene el logger con un nombre identificador.
        self.logger.setLevel(logging.DEBUG)  # Permite registrar todos los niveles de importancia.
        for manejador_actual in list(self.logger.handlers):  # Recorre los manejadores de instancias anteriores.
            self.logger.removeHandler(manejador_actual)  # Quita el manejador anterior para evitar duplicados.
            manejador_actual.close()  # Cierra el archivo anterior antes de abrir uno nuevo.
        manejador = logging.FileHandler(self.ruta, encoding="utf-8")  # Crea el manejador del archivo de log.
        manejador.setLevel(logging.DEBUG)  # El manejador acepta también todos los niveles.
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # Define el formato de cada línea.
        manejador.setFormatter(formato)  # Aplica el formato definido al manejador.
        self.logger.addHandler(manejador)  # Agrega el manejador al logger.

    def evento(self, mensaje):  # Registra un evento informativo.
        """Escribe un mensaje con nivel INFO."""  # Documentación del método.
        self.logger.info(mensaje)  # Envía el mensaje al archivo de log.
        return None  # Devuelve None de forma explícita.

    def error(self, mensaje):  # Registra un error controlado.
        """Escribe un mensaje con nivel ERROR."""  # Documentación del método.
        self.logger.error(mensaje)  # Envía el mensaje de error al archivo de log.
        return None  # Devuelve None de forma explícita.

    def excepcion(self, mensaje):  # Registra una excepción con su traza.
        """Escribe un mensaje con nivel ERROR e incluye la pila de llamadas."""  # Documentación del método.
        self.logger.exception(mensaje)  # Envía el mensaje y la traza de la excepción actual.
        return None  # Devuelve None de forma explícita.
