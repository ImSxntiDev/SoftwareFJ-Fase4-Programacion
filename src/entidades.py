"""Entidades generales del sistema: abstracción base y cliente."""

from abc import ABC, abstractmethod
import re
from .excepciones import DatoInvalidoError

class Entidad(ABC):
    """Abstracción base con identificador validado y descripción obligatoria."""

    def __init__(self, identificador):
        self._identificador = self.validar_identificador(identificador)

    @property
    def identificador(self):
        return self._identificador

    @staticmethod
    def validar_identificador(identificador):
        if not isinstance(identificador, str):
            raise DatoInvalidoError("El identificador debe ser una cadena de texto.")
        if not identificador.strip():
            raise DatoInvalidoError("El identificador no puede estar vacío.")
        return identificador.strip()

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible de la entidad."""
        pass

class Cliente(Entidad):
    """Cliente con datos personales validados y encapsulados."""

    def __init__(self, documento, nombre, correo, telefono):
        super().__init__(self.validar_documento(documento))
        self._nombre = self.validar_nombre(nombre)
        self._correo = self.validar_correo(correo)
        self._telefono = self.validar_telefono(telefono)

    @property
    def documento(self):
        return self.identificador

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    @staticmethod
    def validar_documento(documento):
        if not isinstance(documento, str):
            raise DatoInvalidoError("El documento debe ser una cadena de texto.")
        if not re.fullmatch(r"[A-Z]{2}\d{6,10}", documento.strip().upper()):
            raise DatoInvalidoError("El documento debe tener dos letras y entre 6 y 10 dígitos.")
        return documento.strip().upper()

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise DatoInvalidoError("El nombre debe ser una cadena de texto.")
        if len(nombre.strip()) < 2:
            raise DatoInvalidoError("El nombre debe tener al menos dos caracteres.")
        return nombre.strip()

    @staticmethod
    def validar_correo(correo):
        patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not isinstance(correo, str) or re.match(patron, correo) is None:
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        return correo.strip().lower()

    @staticmethod
    def validar_telefono(telefono):
        if not isinstance(telefono, str):
            raise DatoInvalidoError("El teléfono debe ser una cadena de texto.")
        if not re.fullmatch(r"\d{7,15}", telefono.strip()):
            raise DatoInvalidoError("El teléfono debe tener entre 7 y 15 dígitos.")
        return telefono.strip()

    def describir(self):
        return f"Cliente {self._nombre} ({self.documento}) - {self._correo}"
