"""Punto de entrada: ejecuta de forma secuencial cada segmento del sistema."""  # Docstring del programa.

from src.registro import RegistroEventos  # Importa el gestor del archivo de logs.
from src.servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada  # Importa los tres servicios.
from src.sistema import SistemaGestion  # Importa la fachada del sistema.
from src.excepciones import (  # Importa las excepciones propias que se van a controlar.
    DatoInvalidoError,  # Error de dato inválido.
    ParametroFaltanteError,  # Error de parámetro faltante.
    OperacionNoPermitidaError,  # Error de operación no permitida.
    ServicioNoDisponibleError,  # Error de servicio no disponible.
    CalculoInconsistenteError,  # Error de cálculo inconsistente.
    ReservaInvalidaError,  # Error de reserva inválida.
)


def mostrar(segmento, mensaje):  # Imprime el avance de cada segmento en consola.
    """Muestra el resultado numerado de cada segmento ejecutado."""  # Documentación.
    print(f"[{segmento:02d}] {mensaje}")  # Imprime el número de segmento y su mensaje.
    return None  # Devuelve None de forma explícita.


def ejecutar():  # Ejecuta todas las operaciones en orden secuencial.
    """Ejecuta 16 segmentos y continúa aunque aparezcan errores controlados."""  # Documentación.
    registro = RegistroEventos("logs/sistema.log")  # Crea el registrador de eventos y errores.
    sistema = SistemaGestion(registro)  # Crea el sistema usando ese registrador.
    mostrar(1, "Inicio de la ejecución secuencial.")  # Segmento 1: aviso de inicio.

    try:  # Segmento 2: registro válido de cliente.
        cliente_ana = sistema.registrar_cliente("CC100001", "Ana Torres", "ana@correo.com", "3001234567")  # Registro válido.
        mostrar(2, f"Cliente válido registrado: {cliente_ana.nombre}")  # Muestra el cliente creado.
    except Exception as error:  # Captura cualquier error imprevisto en el segmento.
        mostrar(2, f"ERROR inesperado: {error}")  # Muestra el error imprevisto.

    try:  # Segmento 3: registro inválido de cliente (documento con letras).
        sistema.registrar_cliente("ABC123", "Luis Pérez", "luis@correo.com", "3007654321")  # Intento inválido.
        mostrar(3, "El registro inválido NO debió aceptarse.")  # Alerta si no se detecta el error.
    except DatoInvalidoError as error:  # Captura el error esperado de dato inválido.
        mostrar(3, f"Error controlado (documento inválido): {error}")  # Muestra el error controlado.

    try:  # Segmento 4: registro inválido de cliente (correo mal formado).
        sistema.registrar_cliente("CC100002", "Luis Pérez", "correo-sin-arroba", "3007654321")  # Correo inválido.
        mostrar(4, "El correo inválido NO debió aceptarse.")  # Alerta si no se detecta el error.
    except DatoInvalidoError as error:  # Captura el error esperado.
        mostrar(4, f"Error controlado (correo inválido): {error}")  # Muestra el error controlado.

    try:  # Segmento 5: parámetro faltante en el registro.
        sistema.registrar_cliente("CC100003", "Sofía Ruiz", None, "3105551234")  # Falta el correo.
        mostrar(5, "El parámetro faltante NO debió aceptarse.")  # Alerta si no se detecta el error.
    except ParametroFaltanteError as error:  # Captura el error esperado.
        mostrar(5, f"Error controlado (parámetro faltante): {error}")  # Muestra el error controlado.

    try:  # Segmento 6: creación correcta de ReservaSala.
        sala = ReservaSala("SAL-01", "Sala Angular", 50000, 20)  # Crea una sala válida.
        sistema.agregar_servicio(sala)  # Agrega la sala al sistema.
        mostrar(6, f"Servicio válido creado: {sala.describir_servicio()}")  # Muestra la descripción polimórfica.
    except DatoInvalidoError as error:  # Captura un posible error de validación.
        mostrar(6, f"ERROR inesperado: {error}")  # Muestra el error.

    try:  # Segmento 7: creación incorrecta de ReservaSala (tarifa negativa).
        ReservaSala("SAL-02", "Sala Inválida", -100, 10)  # Intento inválido de tarifa.
        mostrar(7, "La tarifa negativa NO debió aceptarse.")  # Alerta si no se detecta el error.
    except DatoInvalidoError as error:  # Captura el error esperado.
        mostrar(7, f"Error controlado (tarifa negativa): {error}")  # Muestra el error controlado.

    try:  # Segmento 8: creación correcta de AlquilerEquipos.
        equipo = AlquilerEquipos("EQ-01", "Video Beam", 35000, 5)  # Crea un equipo válido.
        sistema.agregar_servicio(equipo)  # Agrega el equipo al sistema.
        mostrar(8, f"Servicio válido creado: {equipo.describir_servicio()}")  # Muestra la descripción polimórfica.
    except DatoInvalidoError as error:  # Captura un posible error de validación.
        mostrar(8, f"ERROR inesperado: {error}")  # Muestra el error.

    try:  # Segmento 9: creación incorrecta de AsesoriaEspecializada (área muy corta).
        AsesoriaEspecializada("ASE-00", "Asesoría", 80000, "POO")  # Área con menos de cuatro caracteres.
        mostrar(9, "El área inválida NO debió aceptarse.")  # Alerta si no se detecta el error.
    except DatoInvalidoError as error:  # Captura el error esperado.
        mostrar(9, f"Error controlado (área inválida): {error}")  # Muestra el error controlado.

    try:  # Segmento 10: creación correcta de AsesoriaEspecializada.
        asesoria = AsesoriaEspecializada("ASE-01", "Asesoría POO", 80000, "Programación")  # Crea asesoría válida.
        sistema.agregar_servicio(asesoria)  # Agrega la asesoría al sistema.
        mostrar(10, f"Servicio válido creado: {asesoria.describir_servicio()}")  # Muestra descripción polimórfica.
    except DatoInvalidoError as error:  # Captura un posible error de validación.
        mostrar(10, f"ERROR inesperado: {error}")  # Muestra el error.

    try:  # Segmento 11: reserva exitosa con cálculo sobrecargado (impuestos y descuento).
        reserva_exitosa = sistema.crear_reserva("CC100001", "SAL-01", 2)  # Crea reserva de dos horas.
        costo = reserva_exitosa.confirmar(impuestos=0.19, descuento=0.10)  # Confirma con impuestos y descuento.
        mostrar(11, f"Reserva exitosa confirmada por ${costo} (estado: {reserva_exitosa.estado}).")  # Muestra resultado.
    except Exception as error:  # Captura cualquier error inesperado del segmento.
        mostrar(11, f"ERROR inesperado: {error}")  # Muestra el error.

    try:  # Segmento 12: reserva fallida por duración cero.
        sistema.crear_reserva("CC100001", "SAL-01", 0)  # Duración inválida.
        mostrar(12, "La duración cero NO debió aceptarse.")  # Alerta si no se detecta el error.
    except ReservaInvalidaError as error:  # Captura el error esperado.
        mostrar(12, f"Error controlado (duración cero): {error}")  # Muestra el error controlado.

    try:  # Segmento 13: cancelación de una reserva confirmada.
        reserva_exitosa.cancelar()  # Cancela la reserva del segmento 11.
        mostrar(13, f"Reserva cancelada correctamente (estado: {reserva_exitosa.estado}).")  # Muestra el estado.
    except OperacionNoPermitidaError as error:  # Captura un posible error de estado.
        mostrar(13, f"ERROR inesperado: {error}")  # Muestra el error.

    try:  # Segmento 14: intento de cancelar una reserva ya cancelada.
        reserva_exitosa.cancelar()  # Segunda cancelación (no permitida).
        mostrar(14, "La segunda cancelación NO debió permitirse.")  # Alerta si no se detecta el error.
    except OperacionNoPermitidaError as error:  # Captura el error esperado.
        mostrar(14, f"Error controlado (doble cancelación): {error}")  # Muestra el error controlado.

    try:  # Segmento 15: servicio no disponible durante la confirmación (excepción encadenada).
        equipo_no_disponible = AlquilerEquipos("EQ-02", "Cámara Pro", 40000, 2, False)  # Servicio no disponible.
        sistema.agregar_servicio(equipo_no_disponible)  # Agrega el servicio al sistema.
        reserva_fallida = sistema.crear_reserva("CC100001", "EQ-02", 1)  # Crea la reserva.
        reserva_fallida.confirmar()  # Intenta confirmar y falla por disponibilidad.
        mostrar(15, "La confirmación NO debió lograrse.")  # Alerta si no se detecta el error.
    except ServicioNoDisponibleError as error:  # Captura el error propio encadenado.
        mostrar(15, f"Error controlado y encadenado: {error} | causa: {error.__cause__}")  # Muestra causa.

    try:  # Segmento 16: cálculo inconsistente (descuento fuera de rango).
        reserva_calculo = sistema.crear_reserva("CC100001", "ASE-01", 1)  # Crea reserva de asesoría.
        reserva_calculo.confirmar(descuento=1.5)  # Descuento mayor al 100 % (inválido).
        mostrar(16, "El descuento inválido NO debió aceptarse.")  # Alerta si no se detecta el error.
    except CalculoInconsistenteError as error:  # Captura el error esperado.
        mostrar(16, f"Error controlado (descuento inválido): {error}")  # Muestra el error controlado.

    try:  # Segmento 17: procesamiento correcto de una reserva confirmada.
        reserva_procesada = sistema.crear_reserva("CC100001", "ASE-01", 3)  # Crea otra reserva de asesoría.
        reserva_procesada.confirmar(impuestos=0.19)  # Confirma con impuestos.
        estado_final = reserva_procesada.procesar()  # Procesa la reserva confirmada.
        mostrar(17, f"Reserva procesada correctamente (estado: {estado_final}).")  # Muestra el estado final.
    except (OperacionNoPermitidaError, ServicioNoDisponibleError) as error:  # Captura errores esperados.
        mostrar(17, f"ERROR inesperado: {error}")  # Muestra el error.

    mostrar(18, f"Fin. Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas: {len(sistema.reservas)}")  # Resumen final.
    mostrar(19, "El archivo logs/sistema.log contiene todos los eventos y errores.")  # Indica dónde está el log.
    return sistema  # Devuelve el sistema para posibles verificaciones posteriores.


if __name__ == "__main__":  # Punto de entrada estándar de Python.
    ejecutar()  # Ejecuta la secuencia completa de segmentos.
