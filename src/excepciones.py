"""Excepciones personalizadas del sistema Software FJ."""

# Todas las excepciones propias cuelgan de esta clase.
class ErrorSoftwareFJ(Exception):
    """Error base de la aplicación Software FJ."""

    pass

class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato de entrada no cumple las validaciones."""

    pass

class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio."""

    pass

class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando una operación no es válida para el estado actual."""

    pass

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de una reserva son inválidos."""

    pass

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar un servicio no disponible."""

    pass

class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de cálculo son inconsistentes."""

    pass
