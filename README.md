# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Curso:** Programación (213023A_2204) — UNAD  
**Fase:** 4 — Componente práctico: Prácticas simuladas  
**Estudiante:** Santiago David Martinez Hernandez  
**Repositorio público:** https://github.com/ImSxntiDev/SoftwareFJ-Fase4-Programacion  
**Lenguaje:** Python 3.12 · **Base de datos:** ninguna · **Dependencias externas:** ninguna

> Este proyecto se desarrolló de forma individual con autorización escrita del Ing. Alexander López Téllez, docente del curso. La constancia correspondiente se publicará en el foro del grupo 41 y el repositorio queda abierto para que cualquier compañero pueda revisarlo o continuarlo. Se utilizó apoyo de inteligencia artificial para organizar y revisar fragmentos; el diseño, la ejecución y las pruebas fueron realizados por el estudiante.

---

## 1. Objetivo

Implementar, usando programación orientada a objetos, un sistema estable y robusto para gestionar **clientes**, **servicios** y **reservas** de la empresa **Software FJ**, aplicando de forma rigurosa:

- Abstracción
- Encapsulación
- Herencia
- Polimorfismo
- Métodos sobrecargados (simulados con `typing.overload` y parámetros opcionales)
- Manejo avanzado de excepciones (propias, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...`)
- Registro de eventos y errores en un archivo de log (único mecanismo de persistencia permitido)

---

## 2. Estructura del proyecto

```text
SoftwareFJ_Fase4/
├── main.py                    # Ejecución secuencial de 19 segmentos
├── README.md                  # Este documento
├── EVIDENCIA_Fase4_SantiagoDavidMartinezHernandez.pdf  # Documento PDF para entrega
├── requirements.txt           # Sin dependencias externas
├── .gitignore                 # Archivos generados por Python
├── logs/
│   └── sistema.log            # Log generado con eventos y errores reales
├── src/
│   ├── __init__.py
│   ├── excepciones.py         # 7 excepciones personalizadas
│   ├── registro.py            # Registro centralizado en logs/sistema.log
│   ├── entidades.py           # Entidad (abstracta) y Cliente
│   ├── servicios.py           # Servicio (abstracta) + 3 servicios concretos
│   ├── reserva.py             # Reserva con estados y manejo de excepciones
│   └── sistema.py             # SistemaGestion: listas internas sin BD
└── pruebas/
    ├── __init__.py
    └── test_sistema.py        # 11 pruebas unitarias ejecutadas en orden
```

---

## 3. Cómo ejecutar

No se necesita instalar paquetes adicionales. Desde la raíz del repositorio:

```bash
python --version              # Debe ser Python 3.12 o superior
python main.py                # Ejecuta los 19 segmentos en orden
python -m unittest discover -s pruebas -v   # Ejecuta las 11 verificaciones
```

Salida esperada de `python main.py`: 19 mensajes numerados que muestran registros válidos e inválidos, servicios correctos e incorrectos, reservas exitosas y fallidas, cancelaciones, excepción encadenada y procesamiento final. El programa **no se detiene** ante los errores: los captura, los registra y continúa.

Todos los eventos y errores quedan en `logs/sistema.log` con el formato:

```text
2026-11-21 10:55:07,789 | ERROR | Registro de cliente fallido: ...
2026-11-21 10:55:07,789 | INFO  | Reserva confirmada: CC100001 -> SAL-01
```

---

## 4. Cobertura de los requisitos de la guía

| Requisito del anexo / guía | Dónde se evidencia |
|---|---|
| Clase abstracta de entidades generales | `src/entidades.py` → `Entidad(ABC)` |
| Cliente con validaciones y encapsulación | `src/entidades.py` → `Cliente` (documento, nombre, correo y teléfono validados; atributos privados + `@property`) |
| Clase abstracta `Servicio` | `src/servicios.py` → `Servicio(Entidad, ABC)` |
| Tres servicios especializados con herencia y polimorfismo | `ReservaSala`, `AlquilerEquipos`, `AsesoriaEspecializada` (sobrescriben `validar_parametros` y `describir_servicio`) |
| Métodos sobrecargados | `Servicio.calcular_costo` con tres firmas `@overload` y una implementación con parámetros opcionales |
| Clase `Reserva` con confirmar / cancelar / procesar | `src/reserva.py` |
| Excepciones personalizadas | `src/excepciones.py` (7 clases derivadas de `ErrorSoftwareFJ`) |
| `try/except`, `try/except/else`, `try/except/finally` | `SistemaGestion.registrar_cliente`, `Reserva.confirmar`, `Reserva.procesar` |
| Encadenamiento de excepciones | `Reserva.confirmar` → `raise ServicioNoDisponibleError(...) from error` |
| Archivo de logs | `src/registro.py` + `logs/sistema.log` |
| Sin base de datos | Solo listas internas en `SistemaGestion` y un archivo de texto para logs |
| Al menos 10 operaciones completas | 19 segmentos en `main.py` (7 válidas y 9 fallidas controladas, más inicio y resumen) |
| Documentación del código | Docstrings en módulos, clases y métodos y comentarios `#` breves en puntos clave |
| Ejecución secuencial y correcciones | `main.py` numerado + `pruebas/test_sistema.py` con 11 pruebas en orden |

---

## 5. Resultado de la ejecución verificada

- `python main.py` → **19/19 segmentos ejecutados**, 0 errores no controlados.
- `python -m unittest discover -s pruebas -v` → **11/11 pruebas OK**.
- Log generado: `logs/sistema.log` con INFO, ERROR y trazas de excepción.

---

## 6. Referencias

- Van Rossum, G., & Drake Jr, F. L. (2024). *El tutorial de Python*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
- Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.
- Zambrano, J. P. (2025). *Introducción al uso de GitHub* [OVI]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75876
- Silva, F. D. (2025). *Basics of using GitHub* [OVI]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75882
