# Referencia de Componentes

Este documento proporciona una descripción detallada de cada módulo ubicado en la carpeta `components/`.

---

### `constants.py`

- **Propósito:** Centralizar todas las constantes y valores de configuración fijos utilizados en la aplicación.
- **Contenido:**
    - **`LimitesViaje (Enum)`**: Agrupa constantes relacionadas con las reglas de los viajes, como `DISTANCIA_MINIMA_VIATICOS` y `DIAS_PARA_RENDICION`.
    - **`PorcentajesAjuste (Enum)`**: Define los porcentajes de ajuste para los viáticos en diferentes escenarios (ej. con alojamiento, con comida).
    - **`CATEGORIAS_EXCEPTAS_COMPROBANTES`**: Una lista de los cargos que están exentos de ciertas reglas.
- **Uso:** Se importa en otros módulos para asegurar que las reglas de negocio se apliquen de manera consistente.

---

### `date_calculator.py`

- **Propósito:** Manejar todos los cálculos relacionados con fechas y horas para determinar la duración de un viaje y los días de viáticos correspondientes.
- **Funciones Principales:**
    - **`calculate_travel_expenses(...)`**: Toma las fechas y horas de inicio y fin, junto con la distancia, para calcular el número de días que se deben pagar como viáticos, aplicando las reglas de negocio definidas en `constants.py`.

---

### `distance_calculator.py`

- **Propósito:** Calcular la distancia y la duración estimada de un viaje en automóvil entre dos direcciones.
- **Funciones Principales:**
    - **`get_driving_distance_and_time(address1, address2)`**: 
        1.  Toma dos direcciones en formato de texto.
        2.  Utiliza `geopy` con Nominatim para convertir las direcciones en coordenadas geográficas (latitud, longitud).
        3.  Realiza una solicitud a la API pública de OSRM (Open Source Routing Machine) para obtener la ruta por carretera.
        4.  Devuelve una tupla con la distancia en kilómetros y la duración del viaje en horas.

---

### `pdf_generator.py`

- **Propósito:** Crear y guardar reportes en formato PDF.
- **Funciones Principales:**
    - **`create_pdf(file_path, content)`**:
        1.  Toma una ruta de archivo y una lista de strings.
        2.  Utiliza la biblioteca `reportlab` para generar un documento PDF.
        3.  Escribe cada string de la lista de contenido como una línea en el PDF.
        4.  Guarda el archivo en la ruta especificada.
