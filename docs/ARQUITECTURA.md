# Arquitectura del Sistema

Este documento describe la arquitectura de alto nivel del Sistema Interno de Administración (SIA).

## Componentes Principales

El sistema está diseñado con una estructura modular simple, separando la interfaz de usuario de la lógica de negocio.

### 1. Interfaz de Usuario (`app.py`)

- **Tecnología:** Streamlit
- **Responsabilidad:** Es el punto de entrada de la aplicación y gestiona toda la interacción con el usuario.
- **Funciones:**
    - Muestra los campos de entrada para los datos del viaje (expediente, agente, fechas, ubicaciones).
    - Orquesta las llamadas a los módulos de `components` para realizar cálculos.
    - Muestra los resultados al usuario.
    - Genera y ofrece la descarga de reportes en PDF.

### 2. Lógica de Negocio (`components/`)

Esta carpeta contiene módulos de Python reutilizables, cada uno con una responsabilidad específica.

- **`constants.py`**: Centraliza valores fijos y constantes (como límites de distancia o porcentajes) para mantener la consistencia y facilitar futuras modificaciones.
- **`distance_calculator.py`**: Se encarga de calcular la distancia y la duración de un viaje entre dos puntos geográficos. Utiliza servicios externos como Nominatim (para geocodificación) y OSRM (para el cálculo de rutas).
- **`date_calculator.py`**: Contiene la lógica para calcular la cantidad de días de viáticos basándose en las fechas y horas de inicio y fin del viaje.
- **`pdf_generator.py`**: Genera un documento PDF a partir de los datos procesados. Utiliza la biblioteca `reportlab`.

### 3. Almacenamiento de Datos (`data/`)

- **Tecnología:** Archivos CSV planos.
- **Responsabilidad:** Actúa como una base de datos simple para almacenar información sobre agentes y vehículos.
    - `agent.csv`: Contiene la lista de agentes, sus categorías y otros detalles.
    - `cars.csv`: Contiene información sobre los vehículos disponibles.
- **Ventaja:** Para el estado actual del proyecto, los archivos CSV son fáciles de gestionar y no requieren un motor de base de datos complejo.

## Flujo de Datos

1.  El usuario introduce los datos en la interfaz de `app.py`.
2.  `app.py` llama a las funciones en los módulos de `components` para procesar los datos (calcular distancia, días, etc.).
3.  Los módulos de `components` leen datos de los archivos en `data/` si es necesario.
4.  Los resultados se devuelven a `app.py`, que los muestra al usuario.
5.  Si el usuario lo solicita, `app.py` utiliza `pdf_generator.py` para crear un reporte que se puede descargar.
