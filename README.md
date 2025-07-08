# Sistema Interno de Administración (SIA)

Sistema para el control, registro y cálculo de viáticos del Ministerio de Ciencia y Tecnología.

## Descripción General

Sistema interno de administración (SIA) es una aplicación web interna construida con Streamlit que facilita la gestión y calculo de viáticos. Permite a los usuarios:

- Registrar expedientes de viaje.
- Seleccionar agentes y vehículos.
- Calcular la distancia y duración de un viaje utilizando direcciones de origen y destino.
- Determinar la cantidad de días correspondientes para el pago de viáticos.
- Generar un reporte en formato PDF con los detalles del viaje.

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo local.

### Prerrequisitos

- Python 3.10 o superior
- `pip` y `venv`

### Pasos de Configuración

1.  **Clona el repositorio (si aplica):**
    ```bash
    git clone https://github.com/fgmolteni/sia-mctc.git
    cd SIA
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *En Windows, usa ` .venv\Scripts\activate `.*

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Cómo Ejecutar la Aplicación

Una vez que el entorno esté configurado y las dependencias instaladas, puedes iniciar la aplicación con el siguiente comando:

```bash
streamlit run app.py
```

Esto iniciará un servidor local y abrirá la aplicación en tu navegador web.

## Estructura del Proyecto

- **`app.py`**: El punto de entrada de la aplicación Streamlit. Contiene la lógica de la interfaz de usuario.
- **`requirements.txt`**: Lista de las dependencias de Python.
- **`data/`**: Contiene los archivos CSV (`agent.csv`, `cars.csv`) que funcionan como base de datos.
- **`components/`**: Módulos de Python con la lógica de negocio principal.
- **`docs/`**: Documentación del proyecto.