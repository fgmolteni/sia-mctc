# Release v0.4.2

**Fecha de Release:** 2025-07-16

## Resumen

Esta release mejora la experiencia visual de la página de inicio de sesión al agregar una transición de fundido (fade-in)a la animación de fondo de Spline y estilos.

## Cambios Principales

### ✨ Nuevas Características
-**Pagina de login:**estilos definitivos de pagina de logeo.
-**Agregado de Escenas de fondo:** se agregaron escenas de fondo conectado con spline.
- **Transición de Fundido en Fondo de Login:** Se ha implementado una transición suave para la escena de fondo en la página de login (`sia/pages/login.py`). La animación ahora aparece gradualmente, mejorando la estética visual de la carga inicial.

# Release v0.4.1

**Fecha de Release:** 2025-07-15

## Resumen

Esta release se enfoca en corregir un problema de alineación en la interfaz de usuario de la página de inicio de sesión construida con Reflex.

## Cambios Principales

### 🐛 Corrección de Errores

- **Centrado de Tarjeta de Login:** Se ha corregido el componente `rx.box` en la página de login (`sia/pages/login.py`) añadiendo la propiedad `display="flex"`. Esto asegura que la tarjeta de inicio de sesión se muestre correctamente centrada tanto vertical como horizontalmente en la pantalla.

# Release v0.4.0

**Fecha de Release:** 2025-07-10

## Resumen

Esta release introduce una nueva tabla para la gestión de anticipos de viáticos, mejorando el control y seguimiento de los fondos asignados a los agentes.

## Cambios Principales

### ✨ Nuevas Características

- **Nueva Tabla `anticipos`:** Se ha añadido una nueva tabla a la base de datos para registrar los anticipos de viáticos. La tabla incluye campos para el `id_agente`, `monto`, `fecha_anticipo`, `estado` y `id_expediente`.

# Release v0.3.0

**Fecha de Release:** 2025-07-08

## Resumen

Esta release migra la carga de datos de la aplicación de archivos CSV a una base de datos PostgreSQL, mejorando la gestión y escalabilidad de los datos.

## Cambios Principales

### ✨ Nuevas Características

- **Carga de Datos desde PostgreSQL:** `app.py` ahora obtiene los datos de agentes y montos de viáticos directamente de las tablas de PostgreSQL (`agentes` y `montos_viaticos`).
- **Población de Datos Inicial:** Las tablas de la base de datos (`agentes`, `vehiculo`, `montos_viaticos`) ahora se pueblan con datos iniciales.

### 🚀 Mejoras

- **Conexión a Base de Datos con SQLAlchemy:** `components/db_connector.py` ha sido refactorizado para utilizar SQLAlchemy, proporcionando una conexión a la base de datos más robusta y eficiente.

### ⚙️ Infraestructura

- **Actualización de Imagen PostgreSQL:** `docker-compose.yml` ahora utiliza la imagen `pgvector/pgvector:pg16` para el servicio de base de datos, lo que permite el soporte de extensiones de vectores y asegura la compatibilidad.
- **Nueva Dependencia:** Se añadió `SQLAlchemy` a `requirements.txt`.
- **Documentación de Instalación de Docker:** `README.md` ha sido actualizado con instrucciones completas para la configuración de Docker para la base de datos, y el archivo redundante `INSTRUCCIONES_DOCKER.md` ha sido eliminado.


# Release v0.2.0

**Fecha de Release:** 2025-07-08

## Resumen

Esta release se centra en la transición del almacenamiento de datos basado en archivos CSV a una base de datos PostgreSQL robusta, gestionada a través de Docker. Se ha establecido la infraestructura de base de datos y el conector inicial, sentando las bases para migrar la lógica de la aplicación.

## Cambios Principales

### ✨ Nuevas Características

- **Conector de Base de Datos:** Se ha creado un nuevo módulo `components/db_connector.py` que gestiona la conexión a la base de datos PostgreSQL. Utiliza `python-dotenv` para cargar las credenciales de forma segura desde un archivo `.env`.

### ⚙️ Infraestructura

- **Base de Datos PostgreSQL con Docker:** Se ha añadido un archivo `docker-compose.yml` para desplegar un contenedor de PostgreSQL. Esto asegura un entorno de desarrollo y producción consistente y aislado.
- **Inicialización de la Base de Datos:** La base de datos se inicializa automáticamente al arrancar el contenedor, utilizando el esquema definido en `data/database.sql`.
- **Gestión de Dependencias:** Se han añadido `psycopg2-binary` y `python-dotenv` al archivo `requirements.txt` para permitir la interacción con PostgreSQL y la gestión de variables de entorno.

---

# Release v0.1.0

**Fecha de Release:** 2025-07-03

## Resumen

Esta es la primera release oficial del Sistema Interno de Administración (SIA). Introduce la funcionalidad principal para el cálculo de viáticos, la generación de reportes en PDF y una estructura de proyecto documentada y robusta.

## Cambios Principales

### ✨ Nuevas Características

- **Generación de Reportes en PDF:** Se añadió un nuevo módulo (`components/pdf_generator.py`) que utiliza `reportlab` para crear un reporte en PDF con los detalles del viaje. La aplicación ahora muestra un botón para generar y descargar este reporte después de un cálculo exitoso.
- **Documentación del Proyecto:** Se creó una base de documentación completa para facilitar el mantenimiento y la colaboración futura. Esto incluye:
    - Un `README.md` mejorado con instrucciones de instalación y uso.
    - Documentos de `ARQUITECTURA.md` y `REFERENCIA_COMPONENTES.md`.
    - Una guía de contribución (`CONTRIBUTING.md`) y una plantilla de release.

### 🐛 Corrección de Errores

- **Error de Cálculo al Inicio:** Se solucionó un error que ocurría al iniciar la aplicación, donde se intentaba calcular la distancia con campos de entrada vacíos. El cálculo ahora solo se activa cuando el usuario ingresa un origen y un destino.
- **Error de Importación de Dependencias:** Se corrigió un `ImportError` con la biblioteca `reportlab` asegurando que todas las dependencias se instalen correctamente dentro del entorno virtual del proyecto.
- **Nombres de Columnas en `cars.csv`:** Se actualizó el código en `app.py` para usar los nombres de columna correctos (`brand`, `model`) al leer el archivo de vehículos.

### 🚀 Mejoras

- **Refactorización de Constantes:** Las constantes del proyecto se movieron a `Enums` en el archivo `components/constants.py`. Esto mejora la legibilidad y reduce el riesgo de errores.
- **Aislamiento de Lógica:** La lógica de negocio (cálculos, generación de PDF) está ahora completamente encapsulada en los módulos de la carpeta `components`, separándola de la interfaz de usuario en `app.py`.

### ⚙️ Infraestructura

- **Base de Datos con Docker:** Se ha añadido un archivo `docker-compose.yml` y un archivo de entorno `.env` para configurar y levantar una base de datos PostgreSQL usando Docker. Esto facilita un entorno de desarrollo consistente y reproducible. La base de datos se inicializa con el esquema definido en `data/database.sql`.