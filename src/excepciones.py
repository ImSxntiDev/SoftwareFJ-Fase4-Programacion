"""Excepciones personalizadas del sistema Software FJ."""  # Docstring del módulo: describe su propósito general.


class ErrorSoftwareFJ(Exception):  # Clase base de todos los errores propios del sistema.
    """Error base de la aplicación Software FJ."""  # Documentación de la clase base.

    pass  # No añade lógica: solo sirve como raíz común para las demás excepciones.


class DatoInvalidoError(ErrorSoftwareFJ):  # Error cuando un dato no supera las validaciones.
    """Se lanza cuando un dato de entrada no cumple las validaciones."""  # Documentación.

    pass  # Hereda el comportamiento de ErrorSoftwareFJ sin cambios.


class ParametroFaltanteError(ErrorSoftwareFJ):  # Error cuando falta un argumento obligatorio.
    """Se lanza cuando falta un parámetro obligatorio."""  # Documentación.

    pass  # Hereda el comportamiento de ErrorSoftwareFJ sin cambios.


class OperacionNoPermitidaError(ErrorSoftwareFJ):  # Error cuando el estado impide la operación.
    """Se lanza cuando una operación no es válida para el estado actual."""  # Documentación.

    pass  # Hereda el comportamiento de ErrorSoftwareFJ sin cambios.


class ReservaInvalidaError(ErrorSoftwareFJ):  # Error relacionado con datos de reserva incorrectos.
    """Se lanza cuando los datos de una reserva son inválidos."""  # Documentación.

    pass  # Hereda el comportamiento de ErrorSoftwareFJ sin cambios.


class ServicioNoDisponibleError(ErrorSoftwareFJ):  # Error cuando el servicio no está disponible.
    """Se lanza cuando se intenta usar un servicio no disponible."""  # Documentación.

    pass  # Hereda el comportamiento de ErrorSoftwareFJ sin cambios.


class CalculoInconsistenteError(ErrorSoftwareFJ):  # Error en parámetros de cálculo de costos.
    """Se lanza cuando los parámetros de cálculo son inconsistentes."""  # Documentación.

    pass  # Hereda el comportamiento de ErrorSoftwareFJ sin cambios.
