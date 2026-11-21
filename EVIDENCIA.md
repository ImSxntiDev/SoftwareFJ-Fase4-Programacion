# Evidencia del componente práctico — Fase 4

## Portada

**Universidad Nacional Abierta y a Distancia — UNAD**  
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)  
Programa: Ingeniería de Sistemas  
Curso: Programación — Código 213023 — Grupo 213023A_2204  

**Componente práctico — Prácticas simuladas: Implementación del manejo de excepciones en aplicaciones orientadas a objetos**

Estudiante: ImSxntiDev (GitHub)  
Fecha de entrega: 22 de noviembre de 2026

---

## Introducción

Este documento presenta la evidencia del desarrollo del ejercicio *Sistema Integral de Gestión de Clientes, Servicios y Reservas* propuesto en el Anexo 3 de la Fase 4. La solución se construyó en Python 3.12 sin uso de bases de datos, con tres servicios especializados que heredan de una clase abstracta común, una entidad `Cliente` validada y encapsulada, una clase `Reserva` con control de estados y un sistema de excepciones personalizadas que garantiza que la aplicación continúe funcionando incluso cuando se presentan errores.

El desarrollo se realizó de manera independiente porque los demás integrantes del grupo iniciaron el trabajo sin avisar ni establecer contacto. Por ello se creó un repositorio público propio, con todo el código documentado línea por línea y con una ejecución secuencial verificable de 19 segmentos, de los cuales 16 son operaciones de negocio (7 correctas y 9 fallidas controladas).

---

## Enlace del repositorio en GitHub

https://github.com/ImSxntiDev/SoftwareFJ-Fase4-Programacion

Evidencias dentro del repositorio:

- `main.py`: ejecución secuencial numerada de los 19 segmentos.
- `logs/sistema.log`: registro real de eventos, errores y trazas.
- `pruebas/test_sistema.py`: 11 pruebas unitarias, todas superadas.
- `src/`: código fuente orientado a objetos, comentado línea por línea.

---

## Desarrollo y validación

La ejecución de `python main.py` produjo 19 mensajes secuenciales sin interrupciones. Se validaron, entre otros, los siguientes casos:

1. Registro correcto de cliente (`CC100001`).
2. Rechazo controlado de documento con letras.
3. Rechazo controlado de correo sin formato.
4. Rechazo controlado de parámetro faltante.
5. Creación correcta de `ReservaSala`, `AlquilerEquipos` y `AsesoriaEspecializada`.
6. Rechazo de tarifa negativa y de área de asesoría demasiado corta.
7. Reserva exitosa con cálculo sobrecargado: impuestos 19 % y descuento 10 %, costo final $107.100,0.
8. Rechazo de duración cero, doble cancelación y descuento del 150 %.
9. Error de servicio no disponible con encadenamiento de excepciones (`raise ... from ...`).
10. Procesamiento correcto de una reserva confirmada.

La ejecución de `python -m unittest discover -s pruebas -v` arrojó **11 pruebas OK**.

---

## Conclusiones

- La abstracción permitió definir contratos comunes (`Entidad`, `Servicio`) y reutilizar validaciones en las tres especializaciones.
- El polimorfismo se evidencia en `describir_servicio()` y `validar_parametros()`, implementados de forma distinta en cada servicio.
- Python no soporta sobrecarga rígida de métodos; se simuló con `@overload` para el análisis estático y parámetros opcionales en tiempo de ejecución.
- El manejo de excepciones con bloques `try/except/else/finally` y encadenamiento mantuvo la aplicación activa ante datos inválidos, parámetros faltantes, operaciones no permitidas, servicios no disponibles y cálculos inconsistentes.
- El archivo `logs/sistema.log` cumple el rol de persistencia permitido por la actividad y facilita la trazabilidad de cada evento y error.
- La ejecución secuencial y las pruebas automatizadas demuestran que el sistema es estable, modular y extensible sin necesidad de base de datos.

---

## Referencias bibliográficas (APA)

Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.

Silva, F. D. (2025). *Basics of using GitHub* [Objeto virtual de información]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75882

Van Rossum, G., & Drake Jr, F. L. (2024). *El tutorial de Python*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html

Zambrano, J. P. (2025). *Introducción al uso de GitHub* [Objeto virtual de información]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75876
