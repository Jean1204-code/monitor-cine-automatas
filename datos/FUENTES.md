# De dónde salen los datos

Descargamos `ticket_history.csv` y `status_detail.csv` desde la carpeta enlazada en el repositorio https://github.com/ngthuylinh3003/Movie_Ticket_Python, que los presenta como transacciones de una aplicación de venta de entradas.

No pudimos verificar quién es la empresa original ni la licencia de los datos, y otro repositorio que usa las mismas tablas (https://github.com/QL-KHANG/movie-ticket-analysis) indica que fueron simuladas para un proyecto de aprendizaje. Por eso no los presentamos como datos reales de una empresa, ni de Loja ni de Ecuador.

## Cómo los preparamos

- Quitamos 102 filas duplicadas exactas.
- Ordenamos por cliente, fecha y ticket_id.
- Cada caso es un cliente en un año (cliente-año); conservamos los grupos de 3 a 20 operaciones, sin recortarlos. Quedan 3 937 casos, 153 con alerta (3,89 %).
- Con semilla 2026 armamos una muestra con 18 % de alertas: 300 casos de validación y 50 de prueba, con un solo caso por cliente y sin clientes repetidos entre ambos archivos. Aseguramos dos casos de P3 en validación y uno en prueba porque es muy escaso.
- Las etiquetas se calculan con una búsqueda de texto después de quitar las V, sin usar los autómatas.
- Los identificadores de cliente se reemplazan por códigos locales; las fechas se conservan.
