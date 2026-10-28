# Monitor de resultados de compra de boletos de cine
UNL · Teoría de Autómatas y Computabilidad Avanzada.
Integrantes, roles y usuarios de GitHub: COMPLETAR.

## Alcance
Reconoce PPP, PPS o BBP después de ignorar V. Aceptar=patrón de seguimiento, no fraude ni compra autorizada. Alfabeto S,T,F,B,L,P,V,R. Caso=cliente-año. Procedencia original y permiso de datos no certificados: consultar datos/FUENTES.md.

## Carpetas
- automatas/: JFLAP y modelos JSON; incluye AFD mínimo reorganizado.
- datos/: preparación y documentación; datos reales solo locales.
- informe/: instrucciones para añadir los documentos finales ya entregados anteriormente.
- monitor/: construcciones, ejecución, pruebas y rendimiento.
- tablas/: transiciones, subconjuntos, particiones y resultados agregados.

## Instalación (desde la raíz del proyecto)
Python 3.10+.
```
pip install -r requirements.txt
python monitor/construir_modelos.py
python monitor/verificar.py
```

## Preparación de datos locales
Obtener el CSV de la fuente; no está incluido en el repositorio.
```
python datos/preparar_datos.py /ruta/ticket_history.csv datos/local
python monitor/monitor.py datos/local/validacion.csv --clave datos/local/clave_validacion.csv --salida tablas/resultados/detecciones_validacion.csv
python monitor/monitor.py datos/local/prueba.csv --salida tablas/resultados/detecciones_prueba.csv
```
Evaluación posterior de prueba:
```
python monitor/monitor.py datos/local/prueba.csv --clave datos/local/clave_prueba.csv --salida tablas/resultados/detecciones_prueba.csv
python monitor/benchmark.py datos/local/clave_validacion.csv datos/local/clave_prueba.csv
```
El monitor no usa etiquetas para detectar. Las claves no deben entregarse junto al archivo de prueba ciega. No subir CSV con información operacional sin revisar permisos. .gitignore no protege una selección manual de archivos en la web.

## JFLAP
Abrir automatas/04_afd_minimo_reorganizado.jff para el diseño separado. El generador ahora conserva también esta versión. Capturas y comprobación gráfica pendientes del equipo. La equivalencia programática no se presenta como ejecución JFLAP.

## Participación
Código base asistido por IA. Registrar revisión, pruebas y mejoras auténticas desde cada cuenta; no inventar aportes ni commits. Consultar REPARTO_COMMITS.md. Los documentos finales anteriores deben incorporarse a informe/; no están recuperados en esta versión.
