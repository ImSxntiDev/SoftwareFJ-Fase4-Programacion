"""Servicio abstracto y tres servicios especializados de Software FJ."""  # Docstring del módulo.

from abc import ABC, abstractmethod  # Importa soporte para clases abstractas.
from typing import overload  # Importa overload para declarar firmas sobrecargadas.
from .entidades import Entidad  # Importa la clase base Entidad.
from .excepciones import (  # Importa las excepciones propias usadas en el módulo.
    DatoInvalidoError,  # Error de dato inválido.
    ServicioNoDisponibleError,  # Error de servicio no disponible.
    CalculoInconsistenteError,  # Error de cálculo inconsistente.
)


class Servicio(Entidad, ABC):  # Clase abstracta para todos los servicios.
    """Servicio genérico con tarifa base, disponibilidad y cálculo sobrecargado."""  # Documentación.

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):  # Constructor del servicio.
        super().__init__(identificador)  # Inicializa la porción Entidad.
        self._nombre = self.validar_nombre_servicio(nombre)  # Valida y guarda el nombre.
        self._tarifa_base = self.validar_tarifa(tarifa_base)  # Valida y guarda la tarifa base.
        self._disponible = bool(disponible)  # Guarda la disponibilidad como booleano.

    @property  # Propiedad de solo lectura.
    def nombre(self):  # Devuelve el nombre del servicio.
        return self._nombre  # Retorna el atributo privado.

    @property  # Propiedad de solo lectura.
    def tarifa_base(self):  # Devuelve la tarifa base.
        return self._tarifa_base  # Retorna el atributo privado.

    @property  # Propiedad de solo lectura.
    def disponible(self):  # Devuelve la disponibilidad.
        return self._disponible  # Retorna el atributo privado.

    @staticmethod  # Validación estática.
    def validar_nombre_servicio(nombre):  # Valida el nombre del servicio.
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:  # Comprueba tipo y longitud.
            raise DatoInvalidoError("El nombre del servicio debe tener al menos tres caracteres.")  # Lanza error.
        return nombre.strip()  # Devuelve el nombre sin espacios extremos.

    @staticmethod  # Validación estática.
    def validar_tarifa(tarifa):  # Valida que la tarifa sea un número positivo.
        if not isinstance(tarifa, (int, float)):  # Comprueba que sea numérica.
            raise DatoInvalidoError("La tarifa debe ser un número.")  # Lanza error.
        if tarifa <= 0:  # Comprueba que sea mayor que cero.
            raise DatoInvalidoError("La tarifa debe ser mayor que cero.")  # Lanza error.
        return float(tarifa)  # Devuelve la tarifa convertida a float.

    @overload  # Declaración de sobrecarga uno: sin parámetros.
    def calcular_costo(self) -> float: ...  # Usa la duración por defecto.

    @overload  # Declaración de sobrecarga dos: solo duración.
    def calcular_costo(self, duracion: int) -> float: ...  # Recibe únicamente la duración.

    @overload  # Declaración de sobrecarga tres: duración, impuestos y descuento.
    def calcular_costo(self, duracion: int, impuestos: float, descuento: float = 0.0) -> float: ...  # Recibe todos los parámetros.

    def calcular_costo(self, duracion=1, impuestos=0.0, descuento=0.0):  # Implementación única de las sobrecargas.
        """Simula sobrecarga: calcula el costo con parámetros opcionales."""  # Documentación del método.
        if not isinstance(duracion, (int, float)) or duracion <= 0:  # Valida la duración.
            raise CalculoInconsistenteError("La duración debe ser un número positivo.")  # Lanza error propio.
        if not isinstance(impuestos, (int, float)) or impuestos < 0:  # Valida los impuestos.
            raise CalculoInconsistenteError("Los impuestos no pueden ser negativos.")  # Lanza error propio.
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:  # Valida el descuento.
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 1.")  # Lanza error propio.
        if not self._disponible:  # Comprueba la disponibilidad antes de calcular.
            raise ServicioNoDisponibleError(f"El servicio {self._nombre} no está disponible.")  # Lanza error propio.
        subtotal = self._tarifa_base * duracion  # Calcula el subtotal según tarifa y duración.
        con_impuestos = subtotal * (1 + impuestos)  # Aplica los impuestos al subtotal.
        total = con_impuestos * (1 - descuento)  # Aplica el descuento final.
        return round(total, 2)  # Devuelve el total redondeado a dos decimales.

    @abstractmethod  # Marca la descripción detallada como obligatoria.
    def describir_servicio(self):  # Contrato polimórfico de descripción.
        """Devuelve una descripción específica del servicio."""  # Documentación del contrato.
        pass  # Implementado por cada subclase.

    @abstractmethod  # Marca la validación específica como obligatoria.
    def validar_parametros(self, **kwargs):  # Contrato polimórfico de validación.
        """Valida los parámetros propios de cada servicio."""  # Documentación del contrato.
        pass  # Implementado por cada subclase.

    def describir(self):  # Implementa el método abstracto de Entidad.
        return f"{self._nombre} (id={self.identificador}, tarifa={self._tarifa_base})"  # Descripción genérica.


class ReservaSala(Servicio):  # Servicio especializado en reserva de salas.
    """Reserva de salas con control de capacidad."""  # Documentación.

    def __init__(self, identificador, nombre, tarifa_base, capacidad):  # Constructor con capacidad.
        super().__init__(identificador, nombre, tarifa_base)  # Inicializa la porción Servicio.
        self._capacidad = self.validar_parametros(capacidad=capacidad)  # Valida y guarda la capacidad.

    @property  # Propiedad de solo lectura.
    def capacidad(self):  # Devuelve la capacidad de la sala.
        return self._capacidad  # Retorna el atributo privado.

    def validar_parametros(self, **kwargs):  # Implementa la validación polimórfica.
        capacidad = kwargs.get("capacidad")  # Obtiene la capacidad del diccionario recibido.
        if not isinstance(capacidad, int) or capacidad <= 0:  # Comprueba que sea entero positivo.
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero positivo.")  # Lanza error.
        return capacidad  # Devuelve la capacidad validada.

    def describir_servicio(self):  # Implementa la descripción polimórfica.
        return f"Sala '{self.nombre}' para {self._capacidad} personas."  # Devuelve texto específico.


class AlquilerEquipos(Servicio):  # Servicio especializado en alquiler de equipos.
    """Alquiler de equipos con control de stock."""  # Documentación.

    def __init__(self, identificador, nombre, tarifa_base, stock, disponible=True):  # Constructor con stock.
        super().__init__(identificador, nombre, tarifa_base, disponible)  # Inicializa la porción Servicio.
        self._stock = self.validar_parametros(stock=stock)  # Valida y guarda el stock.

    @property  # Propiedad de solo lectura.
    def stock(self):  # Devuelve el stock de equipos.
        return self._stock  # Retorna el atributo privado.

    def validar_parametros(self, **kwargs):  # Implementa la validación polimórfica.
        stock = kwargs.get("stock")  # Obtiene el stock del diccionario recibido.
        if not isinstance(stock, int) or stock < 0:  # Comprueba que sea entero no negativo.
            raise DatoInvalidoError("El stock de equipos no puede ser negativo.")  # Lanza error.
        return stock  # Devuelve el stock validado.

    def describir_servicio(self):  # Implementa la descripción polimórfica.
        return f"Equipo '{self.nombre}' con {self._stock} unidades en stock."  # Devuelve texto específico.


class AsesoriaEspecializada(Servicio):  # Servicio especializado en asesorías.
    """Asesoría especializada con área de conocimiento."""  # Documentación.

    def __init__(self, identificador, nombre, tarifa_base, area, disponible=True):  # Constructor con área.
        super().__init__(identificador, nombre, tarifa_base, disponible)  # Inicializa la porción Servicio.
        self._area = self.validar_parametros(area=area)  # Valida y guarda el área.

    @property  # Propiedad de solo lectura.
    def area(self):  # Devuelve el área de la asesoría.
        return self._area  # Retorna el atributo privado.

    def validar_parametros(self, **kwargs):  # Implementa la validación polimórfica.
        area = kwargs.get("area")  # Obtiene el área del diccionario recibido.
        if not isinstance(area, str) or len(area.strip()) < 4:  # Comprueba tipo y longitud.
            raise DatoInvalidoError("El área de la asesoría debe tener al menos cuatro caracteres.")  # Lanza error.
        return area.strip()  # Devuelve el área sin espacios extremos.

    def describir_servicio(self):  # Implementa la descripción polimórfica.
        return f"Asesoría '{self.nombre}' en {self._area}."  # Devuelve texto específico.
