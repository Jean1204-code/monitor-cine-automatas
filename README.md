# Monitor de resultados de compra de boletos de cine

Proyecto de la Evaluación Sumativa 1 (Unidad 1) de **Teoría de Autómatas y Computabilidad Avanzada**, Universidad Nacional de Loja.
Docente: Ing. Genoveva Suing Albito.

## Integrantes

| Integrante | Rol | GitHub |
|---|---|---|
| Jossibel Pérez | Documentadora (informe y presentación) | Jossibel |
| David Toledo | Responsable del modelo formal (AFND, AFD y JFLAP) | |
| Isauro Rivera | Responsable de datos y pruebas | |
| Jean Encalada | Desarrollador del monitor | Jean1204-code |

## Qué hace

Cada operación de compra de un boleto termina con un resultado (orden exitosa, pago fallido desde el banco, sin respuesta del banco, etc.). Agrupamos las operaciones de cada cliente por año, las convertimos en una cadena y el monitor busca tres patrones:

| Patrón | Qué indica |
|---|---|
| PPP | Tres pagos fallidos desde el banco seguidos |
| PPS | Una compra exitosa justo después de dos fallos |
| BBP | Dos faltas de respuesta del banco seguidas de un fallo |

V (verificar cuenta) es el evento irrelevante: se ignora antes de buscar los patrones. Una alerta es un caso para revisar, no un fraude confirmado.

Alfabeto (sale de `status_detail.csv`): S orden exitosa · T pago vencido · F fondos insuficientes · B sin respuesta del banco · L contraseña bloqueada · P pago fallido desde el banco · V verificar cuenta · R transacción limitada.

## Carpetas

- `datos/`: `preparar_datos.py` (limpieza, casos cliente-año, muestreo con semilla 2026), `FUENTES.md` y los archivos `validacion.csv` y `prueba.csv`.
- `automatas/`: los autómatas en JFLAP (`.jff`) y en JSON: AFND de cada patrón, unión con ε, AFND sin ε, AFD y AFD mínimo.
- `monitor/`: `automata.py` (construcciones y simuladores), `construir_modelos.py`, `monitor.py`, `verificar.py` y `benchmark.py`.
- `tablas/`: tablas de transiciones, subconjuntos, refinamiento y resultados.
- `interfaz/`: interfaz web hecha con Streamlit para cargar un CSV y ver las alertas.
- `informe/`: informe técnico en PDF y Word.

## Cómo ejecutarlo

Necesita Python 3.10 o superior, pandas y (para la interfaz) Streamlit.

```
pip install -r requirements.txt
python monitor/construir_modelos.py
python monitor/verificar.py
python monitor/monitor.py datos/validacion.csv --clave datos/clave_validacion.csv --salida tablas/resultados/detecciones_validacion.csv
python monitor/monitor.py datos/prueba.csv --salida tablas/resultados/detecciones_prueba.csv
```

Para abrir la interfaz web:

```
streamlit run interfaz/app.py
```

Para regenerar los datos desde la fuente original:

```
python datos/preparar_datos.py /ruta/ticket_history.csv datos/local
```

La clave de la prueba se entrega por separado; el monitor no usa etiquetas para detectar.

## Resultados

| Conjunto | VP | FP | FN | VN | Precisión | Exhaustividad |
|---|---|---|---|---|---|---|
| Validación (300) | 54 | 0 | 0 | 246 | 1,000 | 1,000 |
| Prueba (50) | 9 | 0 | 0 | 41 | 1,000 | 1,000 |

El AFD de la construcción de subconjuntos tiene 41 estados y el mínimo 6.

## Uso de IA

Parte del código base se hizo con apoyo de herramientas de IA (Perplexity y Claude). El equipo lo revisó, lo ejecutó y puede explicar cada parte.
