"""Punto de entrada: ejecuta de forma secuencial cada segmento del sistema."""

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

def mostrar(segmento, mensaje):
    """Muestra el resultado numerado de cada segmento ejecutado."""
    print(f"[{segmento:02d}] {mensaje}")
    return None

def ejecutar():
    """Ejecuta 19 segmentos y continúa aunque aparezcan errores controlados."""
    # Cada segmento tiene su propio bloque para que un fallo no detenga los siguientes.
    registro = RegistroEventos("logs/sistema.log")
    sistema = SistemaGestion(registro)
    mostrar(1, "Inicio de la ejecución secuencial.")

    try:
        cliente_ana = sistema.registrar_cliente("CC100001", "Ana Torres", "ana@correo.com", "3001234567")
        mostrar(2, f"Cliente válido registrado: ${cliente_ana.nombre}")
    except Exception as error:
        mostrar(2, f"ERROR inesperado: ${error}")

    try:
        sistema.registrar_cliente("ABC123", "Luis Pérez", "luis@correo.com", "3007654321")
        mostrar(3, "El registro inválido NO debió aceptarse.")
    except DatoInvalidoError as error:
        mostrar(3, f"Error controlado (documento inválido): ${error}")

    try:
        sistema.registrar_cliente("CC100002", "Luis Pérez", "correo-sin-arroba", "3007654321")
        mostrar(4, "El correo inválido NO debió aceptarse.")
    except DatoInvalidoError as error:
        mostrar(4, f"Error controlado (correo inválido): ${error}")

    try:
        sistema.registrar_cliente("CC100003", "Sofía Ruiz", None, "3105551234")
        mostrar(5, "El parámetro faltante NO debió aceptarse.")
    except ParametroFaltanteError as error:
        mostrar(5, f"Error controlado (parámetro faltante): ${error}")

    try:
        sala = ReservaSala("SAL-01", "Sala Angular", 50000, 20)
        sistema.agregar_servicio(sala)
        mostrar(6, f"Servicio válido creado: ${sala.describir_servicio()}")
    except DatoInvalidoError as error:
        mostrar(6, f"ERROR inesperado: ${error}")

    try:
        ReservaSala("SAL-02", "Sala Inválida", -100, 10)
        mostrar(7, "La tarifa negativa NO debió aceptarse.")
    except DatoInvalidoError as error:
        mostrar(7, f"Error controlado (tarifa negativa): ${error}")

    try:
        equipo = AlquilerEquipos("EQ-01", "Video Beam", 35000, 5)
        sistema.agregar_servicio(equipo)
        mostrar(8, f"Servicio válido creado: ${equipo.describir_servicio()}")
    except DatoInvalidoError as error:
        mostrar(8, f"ERROR inesperado: ${error}")

    try:
        AsesoriaEspecializada("ASE-00", "Asesoría", 80000, "POO")
        mostrar(9, "El área inválida NO debió aceptarse.")
    except DatoInvalidoError as error:
        mostrar(9, f"Error controlado (área inválida): ${error}")

    try:
        asesoria = AsesoriaEspecializada("ASE-01", "Asesoría POO", 80000, "Programación")
        sistema.agregar_servicio(asesoria)
        mostrar(10, f"Servicio válido creado: ${asesoria.describir_servicio()}")
    except DatoInvalidoError as error:
        mostrar(10, f"ERROR inesperado: ${error}")

    try:
        reserva_exitosa = sistema.crear_reserva("CC100001", "SAL-01", 2)
        costo = reserva_exitosa.confirmar(impuestos=0.19, descuento=0.10)
        mostrar(11, f"Reserva exitosa confirmada por $${costo} (estado: ${reserva_exitosa.estado}).")
    except Exception as error:
        mostrar(11, f"ERROR inesperado: ${error}")

    try:
        sistema.crear_reserva("CC100001", "SAL-01", 0)
        mostrar(12, "La duración cero NO debió aceptarse.")
    except ReservaInvalidaError as error:
        mostrar(12, f"Error controlado (duración cero): ${error}")

    try:
        reserva_exitosa.cancelar()
        mostrar(13, f"Reserva cancelada correctamente (estado: ${reserva_exitosa.estado}).")
    except OperacionNoPermitidaError as error:
        mostrar(13, f"ERROR inesperado: ${error}")

    try:
        reserva_exitosa.cancelar()
        mostrar(14, "La segunda cancelación NO debió permitirse.")
    except OperacionNoPermitidaError as error:
        mostrar(14, f"Error controlado (doble cancelación): ${error}")

    try:
        equipo_no_disponible = AlquilerEquipos("EQ-02", "Cámara Pro", 40000, 2, False)
        sistema.agregar_servicio(equipo_no_disponible)
        reserva_fallida = sistema.crear_reserva("CC100001", "EQ-02", 1)
        reserva_fallida.confirmar()
        mostrar(15, "La confirmación NO debió lograrse.")
    except ServicioNoDisponibleError as error:
        mostrar(15, f"Error controlado y encadenado: ${error} | causa: ${error.__cause__}")

    try:
        reserva_calculo = sistema.crear_reserva("CC100001", "ASE-01", 1)
        reserva_calculo.confirmar(descuento=1.5)
        mostrar(16, "El descuento inválido NO debió aceptarse.")
    except CalculoInconsistenteError as error:
        mostrar(16, f"Error controlado (descuento inválido): ${error}")

    try:
        reserva_procesada = sistema.crear_reserva("CC100001", "ASE-01", 3)
        reserva_procesada.confirmar(impuestos=0.19)
        estado_final = reserva_procesada.procesar()
        mostrar(17, f"Reserva procesada correctamente (estado: ${estado_final}).")
    except (OperacionNoPermitidaError, ServicioNoDisponibleError) as error:
        mostrar(17, f"ERROR inesperado: ${error}")

    mostrar(18, f"Fin. Clientes: ${len(sistema.clientes)} | Servicios: ${len(sistema.servicios)} | Reservas: ${len(sistema.reservas)}")
    mostrar(19, "El archivo logs/sistema.log contiene todos los eventos y errores.")
    return sistema

if __name__ == "__main__":
    ejecutar()
