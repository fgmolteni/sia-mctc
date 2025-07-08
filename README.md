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

### Pasos de Configuración (Local)

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

### Configuración con Docker (Base de Datos)

Aquí tienes los pasos a seguir para configurar Docker y levantar la base de datos del proyecto.

1.  **Verificar Docker Desktop y la Integración con WSL**:
    *   Después de reiniciar, **Docker Desktop debería iniciarse automáticamente**. Si no lo hace, búscalo en el menú de inicio y ábrelo. Espera a que el icono de la ballena en la barra de tareas deje de animarse.
    *   Haz clic derecho en el icono de la ballena y selecciona **"Settings"** (Configuración).
    *   Ve a la sección **"Resources" > "WSL Integration"**.
    *   Asegúrate de que el interruptor para tu distribución de **Ubuntu** esté **activado**. Si no lo está, actívalo y presiona el botón **"Apply & Restart"**.

2.  **Abrir la Terminal de Ubuntu y Probar Docker**:
    Una vez confirmada la configuración, abre tu terminal de WSL Ubuntu.
    *   **Verifica la versión de Docker** para confirmar que el comando está disponible:
        ```bash
        docker --version
        ```
        *Deberías ver algo como: `Docker version 20.10.17, build 100c701`.*
    *   **Ejecuta el contenedor de prueba "hola mundo"**:
        ```bash
        docker run hello-world
        ```
        *Si todo es correcto, verás un mensaje de bienvenida de Docker.*

3.  **(¡Importante!) Configurar Docker para usar sin `sudo`**:
    Para no tener que escribir `sudo` cada vez que uses Docker, sigue estos pasos:
    *   **Añade tu usuario al grupo `docker`**:
        ```bash
        sudo usermod -aG docker $USER
        ```
    *   **¡CIERRA Y VUELVE A ABRIR LA TERMINAL!** Este paso es fundamental para que los cambios de permisos se apliquen.
    *   En la **nueva terminal**, verifica que puedes usar Docker sin `sudo`:
        ```bash
        docker run hello-world
        ```
        *Si funciona, ¡ya estás listo!*

4.  **Iniciar la Base de Datos del Proyecto**:
    Ahora que Docker está 100% configurado, vamos a levantar la base de datos de PostgreSQL.
    *   Navega al directorio de tu proyecto:
        ```bash
        cd /home/gabi/projects/SIA
        ```
    *   Ejecuta Docker Compose en modo "detached" (para que se quede corriendo en segundo plano):
        ```bash
        docker compose up -d
        ```
        *La primera vez, Docker descargará la imagen de PostgreSQL, lo que puede tardar un par de minutos.*

5.  **Confirmar que la Base de Datos está Corriendo**:
    Para asegurarte de que todo se ha iniciado correctamente, ejecuta:
    ```bash
    docker ps
    ```
    Deberías ver en la lista un contenedor con un nombre similar a `sia-db-1` y la imagen `postgres`. Esto significa que tu base de datos está activa y lista para recibir conexiones.

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
