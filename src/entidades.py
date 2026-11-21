"""Entidades generales del sistema: abstracción base y cliente."""  # Docstring del módulo.

from abc import ABC, abstractmethod  # Importa herramientas para definir clases abstractas.
import re  # Importa expresiones regulares para validar textos.
from .excepciones import DatoInvalidoError  # Importa la excepción de datos inválidos (import relativo del paquete).


class Entidad(ABC):  # Clase abstracta que representa a cualquier entidad del sistema.
    """Abstracción base con identificador validado y descripción obligatoria."""  # Documentación.

    def __init__(self, identificador):  # Constructor que recibe el identificador único.
        self._identificador = self.validar_identificador(identificador)  # Guarda el id validado y encapsulado.

    @property  # Define una propiedad de solo lectura.
    def identificador(self):  # Devuelve el identificador de la entidad.
        return self._identificador  # Retorna el atributo privado.

    @staticmethod  # Método que no depende del estado de la instancia.
    def validar_identificador(identificador):  # Valida que el identificador sea texto no vacío.
        if not isinstance(identificador, str):  # Comprueba que el dato sea una cadena.
            raise DatoInvalidoError("El identificador debe ser una cadena de texto.")  # Lanza error propio.
        if not identificador.strip():  # Comprueba que no esté vacío o solo con espacios.
            raise DatoInvalidoError("El identificador no puede estar vacío.")  # Lanza error propio.
        return identificador.strip()  # Devuelve el identificador sin espacios extremos.

    @abstractmethod  # Marca el método como obligatorio para las subclases.
    def describir(self):  # Contrato para describir la entidad.
        """Devuelve una descripción legible de la entidad."""  # Documentación del contrato.
        pass  # Las subclases deberán implementar este método.


class Cliente(Entidad):  # Representa a un cliente de Software FJ.
    """Cliente con datos personales validados y encapsulados."""  # Documentación.

    def __init__(self, documento, nombre, correo, telefono):  # Constructor con datos personales.
        super().__init__(self.validar_documento(documento))  # Valida el documento y lo usa como identificador.
        self._nombre = self.validar_nombre(nombre)  # Valida y guarda el nombre.
        self._correo = self.validar_correo(correo)  # Valida y guarda el correo.
        self._telefono = self.validar_telefono(telefono)  # Valida y guarda el teléfono.

    @property  # Propiedad de solo lectura.
    def documento(self):  # Devuelve el documento del cliente.
        return self.identificador  # Reutiliza el identificador de la clase base.

    @property  # Propiedad de solo lectura.
    def nombre(self):  # Devuelve el nombre del cliente.
        return self._nombre  # Retorna el atributo privado.

    @property  # Propiedad de solo lectura.
    def correo(self):  # Devuelve el correo del cliente.
        return self._correo  # Retorna el atributo privado.

    @property  # Propiedad de solo lectura.
    def telefono(self):  # Devuelve el teléfono del cliente.
        return self._telefono  # Retorna el atributo privado.

    @staticmethod  # Método estático de validación.
    def validar_documento(documento):  # Valida el formato del documento de identidad.
        if not isinstance(documento, str):  # Comprueba el tipo del dato.
            raise DatoInvalidoError("El documento debe ser una cadena de texto.")  # Lanza error propio.
        if not re.fullmatch(r"[A-Z]{2}\d{6,10}", documento.strip().upper()):  # Verifica siglas y dígitos.
            raise DatoInvalidoError("El documento debe tener dos letras y entre 6 y 10 dígitos.")  # Lanza error.
        return documento.strip().upper()  # Devuelve el documento normalizado a mayúsculas.

    @staticmethod  # Método estático de validación.
    def validar_nombre(nombre):  # Valida que el nombre tenga al menos dos caracteres.
        if not isinstance(nombre, str):  # Comprueba el tipo del dato.
            raise DatoInvalidoError("El nombre debe ser una cadena de texto.")  # Lanza error propio.
        if len(nombre.strip()) < 2:  # Comprueba la longitud mínima.
            raise DatoInvalidoError("El nombre debe tener al menos dos caracteres.")  # Lanza error propio.
        return nombre.strip()  # Devuelve el nombre sin espacios extremos.

    @staticmethod  # Método estático de validación.
    def validar_correo(correo):  # Valida el formato básico de correo electrónico.
        patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"  # Define el patrón simple de correo.
        if not isinstance(correo, str) or re.match(patron, correo) is None:  # Verifica tipo y formato.
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")  # Lanza error propio.
        return correo.strip().lower()  # Devuelve el correo normalizado a minúsculas.

    @staticmethod  # Método estático de validación.
    def validar_telefono(telefono):  # Valida que el teléfono tenga entre 7 y 15 dígitos.
        if not isinstance(telefono, str):  # Comprueba el tipo del dato.
            raise DatoInvalidoError("El teléfono debe ser una cadena de texto.")  # Lanza error propio.
        if not re.fullmatch(r"\d{7,15}", telefono.strip()):  # Verifica la cantidad de dígitos.
            raise DatoInvalidoError("El teléfono debe tener entre 7 y 15 dígitos.")  # Lanza error propio.
        return telefono.strip()  # Devuelve el teléfono sin espacios extremos.

    def describir(self):  # Implementa el método abstracto de Entidad.
        return f"Cliente {self._nombre} ({self.documento}) - {self._correo}"  # Devuelve una descripción legible.
