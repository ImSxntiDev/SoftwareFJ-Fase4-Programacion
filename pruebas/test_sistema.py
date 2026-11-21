"""Pruebas unitarias: validan cada segmento del sistema de forma secuencial."""  # Docstring del módulo.

import tempfile  # Importa tempfile para crear un log temporal en cada prueba.
from pathlib import Path  # Importa Path para construir la ruta del log temporal.
import unittest  # Importa el marco de pruebas estándar.

from src.registro import RegistroEventos  # Importa el registrador de eventos.
from src.servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada  # Importa los servicios.
from src.sistema import SistemaGestion  # Importa la fachada del sistema.
from src.excepciones import (  # Importa las excepciones propias.
    DatoInvalidoError,  # Error de dato inválido.
    ParametroFaltanteError,  # Error de parámetro faltante.
    OperacionNoPermitidaError,  # Error de operación no permitida.
    ServicioNoDisponibleError,  # Error de servicio no disponible.
    CalculoInconsistenteError,  # Error de cálculo inconsistente.
    ReservaInvalidaError,  # Error de reserva inválida.
)


class TestSistemaSoftwareFJ(unittest.TestCase):  # Clase con las pruebas del sistema.
    """Agrupa las verificaciones secuenciales de las reglas de negocio."""  # Documentación.

    def setUp(self):  # Prepara un sistema nuevo antes de cada prueba.
        self.directorio = tempfile.TemporaryDirectory()  # Crea un directorio temporal.
        ruta = Path(self.directorio.name) / "sistema.log"  # Construye la ruta del log temporal.
        self.registro = RegistroEventos(str(ruta))  # Crea el registrador apuntando al log temporal.
        self.sistema = SistemaGestion(self.registro)  # Crea el sistema con ese registrador.
        self.cliente = self.sistema.registrar_cliente("CC000001", "Ana Torres", "ana@correo.com", "3001234567")  # Cliente base.

    def tearDown(self):  # Libera el directorio temporal después de cada prueba.
        for manejador in list(self.registro.logger.handlers):  # Recorre los manejadores abiertos por el logger.
            self.registro.logger.removeHandler(manejador)  # Quita el manejador del logger.
            manejador.close()  # Cierra el archivo de log para poder borrarlo en Windows.
        self.directorio.cleanup()  # Borra el directorio temporal y su contenido.

    def test_01_cliente_valido(self):  # Prueba 1: cliente válido.
        self.assertEqual(self.cliente.documento, "CC000001")  # Verifica el documento asignado.
        self.assertEqual(self.cliente.correo, "ana@correo.com")  # Verifica el correo normalizado.

    def test_02_cliente_invalido(self):  # Prueba 2: documento con letras.
        with self.assertRaises(DatoInvalidoError):  # Espera una excepción propia.
            self.sistema.registrar_cliente("ABC", "Luis", "luis@correo.com", "3001234567")  # Intento inválido.

    def test_03_parametro_faltante(self):  # Prueba 3: parámetro faltante.
        with self.assertRaises(ParametroFaltanteError):  # Espera una excepción propia.
            self.sistema.registrar_cliente("CC000002", "Luis", None, "3001234567")  # Falta el correo.

    def test_04_servicios_polimorficos(self):  # Prueba 4: los tres servicios describen su tipo.
        sala = ReservaSala("SAL-01", "Sala Angular", 50000, 20)  # Crea sala.
        equipo = AlquilerEquipos("EQ-01", "Video Beam", 35000, 5)  # Crea equipo.
        asesoria = AsesoriaEspecializada("ASE-01", "Asesoría POO", 80000, "Programación")  # Crea asesoría.
        self.assertIn("personas", sala.describir_servicio())  # Verifica descripción de sala.
        self.assertIn("stock", equipo.describir_servicio())  # Verifica descripción de equipo.
        self.assertIn("Programación", asesoria.describir_servicio())  # Verifica descripción de asesoría.

    def test_05_servicio_tarifa_negativa(self):  # Prueba 5: tarifa negativa.
        with self.assertRaises(DatoInvalidoError):  # Espera una excepción propia.
            ReservaSala("SAL-02", "Sala Inválida", -1, 10)  # Intento inválido.

    def test_06_calculo_sobrecargado(self):  # Prueba 6: cálculo con impuestos y descuento.
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)  # Tarifa sencilla para calcular.
        self.assertEqual(sala.calcular_costo(), 100.0)  # Sobrecarga sin parámetros.
        self.assertEqual(sala.calcular_costo(2), 200.0)  # Sobrecarga con duración.
        self.assertEqual(sala.calcular_costo(2, 0.5, 0.2), 240.0)  # Sobrecarga completa: 100*2*1.5*0.8 = 240.

    def test_07_reserva_valida_y_estados(self):  # Prueba 7: ciclo de vida de una reserva.
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)  # Crea sala.
        self.sistema.agregar_servicio(sala)  # Agrega la sala al sistema.
        reserva = self.sistema.crear_reserva("CC000001", "SAL-01", 2)  # Crea reserva.
        reserva.confirmar()  # Confirma la reserva.
        reserva.procesar()  # Procesa la reserva.
        self.assertEqual(reserva.estado, "procesada")  # Verifica el estado final.

    def test_08_reserva_duracion_invalida(self):  # Prueba 8: duración cero.
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)  # Crea sala.
        self.sistema.agregar_servicio(sala)  # Agrega la sala al sistema.
        with self.assertRaises(ReservaInvalidaError):  # Espera una excepción propia.
            self.sistema.crear_reserva("CC000001", "SAL-01", 0)  # Duración inválida.

    def test_09_cancelacion_no_permitida(self):  # Prueba 9: doble cancelación.
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)  # Crea sala.
        self.sistema.agregar_servicio(sala)  # Agrega la sala al sistema.
        reserva = self.sistema.crear_reserva("CC000001", "SAL-01", 1)  # Crea reserva.
        reserva.cancelar()  # Cancela una vez.
        with self.assertRaises(OperacionNoPermitidaError):  # Espera una excepción propia.
            reserva.cancelar()  # Intenta cancelar de nuevo.

    def test_10_servicio_no_disponible_encadenado(self):  # Prueba 10: excepción encadenada.
        equipo = AlquilerEquipos("EQ-02", "Cámara", 100, 2, False)  # Crea equipo no disponible.
        self.sistema.agregar_servicio(equipo)  # Agrega el equipo al sistema.
        reserva = self.sistema.crear_reserva("CC000001", "EQ-02", 1)  # Crea reserva.
        with self.assertRaises(ServicioNoDisponibleError) as contexto:  # Espera excepción con causa.
            reserva.confirmar()  # Intenta confirmar.
        self.assertIsNotNone(contexto.exception.__cause__)  # Verifica el encadenamiento de excepciones.

    def test_11_calculo_inconsistente(self):  # Prueba 11: descuento fuera de rango.
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)  # Crea sala.
        self.sistema.agregar_servicio(sala)  # Agrega la sala al sistema.
        reserva = self.sistema.crear_reserva("CC000001", "SAL-01", 1)  # Crea reserva.
        with self.assertRaises(CalculoInconsistenteError):  # Espera una excepción propia.
            reserva.confirmar(descuento=1.5)  # Descuento mayor al 100 %.


if __name__ == "__main__":  # Permite ejecutar el archivo directamente.
    unittest.main(verbosity=2)  # Ejecuta todas las pruebas con detalle.
