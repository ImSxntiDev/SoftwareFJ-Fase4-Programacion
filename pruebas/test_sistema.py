"""Pruebas del sistema para clientes, servicios y reservas."""

import tempfile
from pathlib import Path
import unittest

from src.registro import RegistroEventos
from src.servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada
from src.sistema import SistemaGestion
from src.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    ReservaInvalidaError,
)

class TestSistemaSoftwareFJ(unittest.TestCase):
    """Casos de prueba sobre las reglas del sistema."""

    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        ruta = Path(self.directorio.name) / "sistema.log"
        self.registro = RegistroEventos(str(ruta))
        self.sistema = SistemaGestion(self.registro)
        self.cliente = self.sistema.registrar_cliente("CC000001", "Ana Torres", "ana@correo.com", "3001234567")

    def tearDown(self):
        for manejador in list(self.registro.logger.handlers):
            self.registro.logger.removeHandler(manejador)
            manejador.close()
        self.directorio.cleanup()

    def test_registro_cliente_valido(self):
        self.assertEqual(self.cliente.documento, "CC000001")
        self.assertEqual(self.cliente.correo, "ana@correo.com")

    def test_documento_cliente_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            self.sistema.registrar_cliente("ABC", "Luis", "luis@correo.com", "3001234567")

    def test_cliente_sin_correo(self):
        with self.assertRaises(ParametroFaltanteError):
            self.sistema.registrar_cliente("CC000002", "Luis", None, "3001234567")

    def test_descripcion_de_servicios(self):
        sala = ReservaSala("SAL-01", "Sala Angular", 50000, 20)
        equipo = AlquilerEquipos("EQ-01", "Video Beam", 35000, 5)
        asesoria = AsesoriaEspecializada("ASE-01", "Asesoría POO", 80000, "Programación")
        self.assertIn("personas", sala.describir_servicio())
        self.assertIn("stock", equipo.describir_servicio())
        self.assertIn("Programación", asesoria.describir_servicio())

    def test_sala_con_tarifa_negativa(self):
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("SAL-02", "Sala Inválida", -1, 10)

    def test_calcular_costo_con_opciones(self):
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)
        self.assertEqual(sala.calcular_costo(), 100.0)
        self.assertEqual(sala.calcular_costo(2), 200.0)
        self.assertEqual(sala.calcular_costo(2, 0.5, 0.2), 240.0)

    def test_reserva_hasta_procesada(self):
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)
        self.sistema.agregar_servicio(sala)
        reserva = self.sistema.crear_reserva("CC000001", "SAL-01", 2)
        reserva.confirmar()
        reserva.procesar()
        self.assertEqual(reserva.estado, "procesada")

    def test_reserva_con_duracion_cero(self):
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)
        self.sistema.agregar_servicio(sala)
        with self.assertRaises(ReservaInvalidaError):
            self.sistema.crear_reserva("CC000001", "SAL-01", 0)

    def test_cancelar_reserva_dos_veces(self):
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)
        self.sistema.agregar_servicio(sala)
        reserva = self.sistema.crear_reserva("CC000001", "SAL-01", 1)
        reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    # La causa original debe seguir disponible después de encadenar.
    def test_confirmar_servicio_no_disponible(self):
        equipo = AlquilerEquipos("EQ-02", "Cámara", 100, 2, False)
        self.sistema.agregar_servicio(equipo)
        reserva = self.sistema.crear_reserva("CC000001", "EQ-02", 1)
        with self.assertRaises(ServicioNoDisponibleError) as contexto:
            reserva.confirmar()
        self.assertIsNotNone(contexto.exception.__cause__)

    def test_descuento_fuera_de_rango(self):
        sala = ReservaSala("SAL-01", "Sala Angular", 100, 20)
        self.sistema.agregar_servicio(sala)
        reserva = self.sistema.crear_reserva("CC000001", "SAL-01", 1)
        with self.assertRaises(CalculoInconsistenteError):
            reserva.confirmar(descuento=1.5)

if __name__ == "__main__":
    unittest.main(verbosity=2)
