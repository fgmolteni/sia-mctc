# Arquitectura del Sistema

Este documento describe la arquitectura de alto nivel del Sistema Interno de Administración (SIA).

## Componentes Principales

El sistema tiene una arquitectura dual con dos aplicaciones principales:

### 1. Aplicación Reflex Moderna (Aplicación Principal)

- **Tecnología:** Reflex 0.8.1
- **Ubicación:** `sia/`
- **Responsabilidad:** Sistema de gestión integral con administración de usuarios y cálculo de viáticos
- **Funciones:**
    - Gestión completa de usuarios con perfiles dinámicos
    - Sistema de autenticación y autorización
    - Cálculo avanzado de viáticos con validaciones
    - Interfaz de usuario moderna y responsiva
    - Generación de reportes en PDF
    - Dashboard con métricas y estadísticas

#### Estructura de la Aplicación Reflex

- **`sia.py`** - Punto de entrada principal con enrutamiento
- **`pages/`** - Componentes de páginas (dashboard, login, usuarios, perfiles, etc.)
- **`views/`** - Lógica de vistas complejas y gestión de estado
- **`components/`** - Componentes de UI reutilizables organizados por categoría:
  - `branding/` - Logo y elementos de marca
  - `data_display/` - Tablas, avatares, badges, menús, cronogramas
  - `feedback/` - Banners y notificaciones
  - `forms/` - Componentes de entrada, botones, selectores
  - `layout/` - Headers, sidebars, tarjetas
  - `navigation/` - Breadcrumbs, navbars, pasos
- **`styles/`** - Sistema de diseño (colores, fuentes, tamaños, bordes)

### 2. Aplicación Streamlit Legacy

- **Tecnología:** Streamlit
- **Ubicación:** `app.py`
- **Responsabilidad:** Calculadora original de viáticos (mantenida para compatibilidad)
- **Funciones:**
    - Cálculo básico de viáticos
    - Interfaz simplificada para cálculos rápidos
    - Generación de reportes básicos en PDF

### 3. Lógica de Negocio (`components/`)

Esta carpeta contiene módulos de Python reutilizables compartidos entre ambas aplicaciones:

#### Operaciones de Base de Datos
- **`db_*.py`** - Operaciones de base de datos (usuarios, agentes, vehículos, gastos)
- **`db_connector.py`** - Gestión de conexiones a PostgreSQL

#### Cálculos de Negocio
- **`distance_calculator.py`** - Cálculos de distancia y duración geográfica
- **`date_calculator.py`** - Cálculos de días de viáticos
- **`pdf_generator.py`** - Generación de reportes PDF
- **`converter.py`** - Conversión de números a texto/moneda

#### Configuración y Utilidades
- **`constants.py`** - Valores fijos y constantes del sistema
- **`logging/`** - Configuración de sistema de logging

### 4. Sistema de Base de Datos

- **Tecnología:** PostgreSQL con pgvector (containerizada con Docker)
- **Responsabilidad:** Almacenamiento persistente de todos los datos del sistema
- **Esquemas:**
    - Usuarios y perfiles dinámicos
    - Agentes y categorías
    - Vehículos y asignaciones
    - Gastos y viáticos
    - Configuraciones del sistema
- **Configuración:** Variables de entorno en `.env`
- **Puerto:** 5432 (PostgreSQL estándar)

### 5. Datos Legacy (`data/`)

- **Tecnología:** Archivos CSV (en proceso de migración)
- **Contenido:**
    - `agent.csv`: Datos históricos de agentes
    - `cars.csv`: Información de vehículos
- **Estado:** Mantenidos para compatibilidad durante la transición

## Flujo de Datos

### Aplicación Reflex (Principal)
1. El usuario accede a través del sistema de autenticación en `sia.py`
2. Las páginas en `pages/` gestionan la interacción del usuario
3. Las vistas en `views/` manejan la lógica de estado compleja
4. Los componentes en `components/` proporcionan UI reutilizable
5. La lógica de negocio en `components/db_*.py` interactúa con PostgreSQL
6. Los cálculos se realizan mediante módulos especializados
7. Los resultados se presentan a través del sistema de componentes
8. Los reportes se generan y se ofrecen para descarga

### Aplicación Streamlit (Legacy)
1. El usuario introduce datos en la interfaz de `app.py`
2. `app.py` llama a funciones en los módulos de `components/`
3. Los módulos leen datos de PostgreSQL o archivos CSV según disponibilidad
4. Los resultados se devuelven y se muestran al usuario
5. Los reportes PDF se generan bajo demanda

## Sistema de Diseño

La aplicación Reflex utiliza un sistema de diseño comprensivo ubicado en `sia/styles/`:
- **Colores** - Paleta de colores consistente
- **Fuentes** - Escala tipográfica y pesos
- **Tamaños** - Dimensiones estandarizadas
- **Bordes** - Radio de bordes y estilos

## Lógica de Negocios

### Reglas de Cálculo de Viáticos

El sistema implementa las siguientes reglas para el cálculo de viáticos:

#### Límites y Restricciones
- **Distancia mínima:** 60 km para que aplique el cálculo de viáticos
- **Límite de taxi:** Máximo 20% del total de viáticos
- **Días para rendición:** 3 días hábiles posterior al viaje

#### Categorías y Escalas
Las categorías de personal siguen la escala ministerial:
- **Ministro:** Categoría I
- **Subsecretario:** Categoría II
- **Director:** Categoría II  
- **Agente:** Categoría IV

#### Ajustes por Provisiones
Los viáticos se ajustan según las provisiones del viaje:
- **Con alojamiento y comida:** 25% del valor base
- **Solo con alojamiento:** 50% del valor base
- **Solo con comida:** 75% del valor base
- **Sin provisiones:** 100% del valor base

### Gestión de Usuarios

#### Sistema de Autenticación
- **Encriptación:** bcrypt para contraseñas
- **Validación:** Pydantic para datos de entrada
- **Unicidad:** Por nombre_usuario, email y DNI

#### Perfiles Dinámicos
- **Roles:** Administrador, Manager, Empleado
- **Permisos:** Sistema granular basado en roles
- **Auditoría:** Registro completo de acciones y cambios

#### Validaciones de Seguridad
- **Contraseñas:** Requisitos de complejidad
- **Sesiones:** Gestión segura con timeouts
- **Logs:** Registro de eventos de seguridad

### Cálculos Geográficos

#### Distancias y Rutas
- **Geocodificación:** Nominatim para conversión de direcciones
- **Cálculo de rutas:** OSRM para distancias y duraciones
- **Validación:** Verificación de puntos geográficos válidos

#### Cálculo de Días
- **Días completos:** Basado en fechas de inicio y fin
- **Horas parciales:** Cálculo proporcional para días incompletos
- **Fines de semana:** Consideración en el cálculo total

## Sistema de Diseño y Reglas de UI/UX

### Paleta de Colores

#### Colores Primarios
- **Primary:** `#1F1F1F` - Color principal del sistema
- **Secondary:** `#EEEEEE` - Color secundario
- **Accent:** `#B6EADA` - Color de acento y éxito
- **Background:** `#FFFFFF` - Fondo principal

#### Colores de Estado
- **Success:** `#B6EADA` - Acciones exitosas
- **Warning:** `#EEDF7A` - Advertencias
- **Error:** `#F7374F` - Errores y eliminaciones
- **Info:** `#6EACDA` - Información general

#### Colores de Roles
- **Administrador:** Fondo `#DBEAFE`, Texto `#2563EB`
- **Manager:** Fondo `#E9D5FF`, Texto `#9333EA`
- **Empleado:** Fondo `#DCFCE7`, Texto `#16A34A`

### Tipografía

#### Familias de Fuentes
- **Principal:** Inter, sans-serif
- **Monospace:** Space Mono, monospace
- **Display:** Major Mono Display, monospace
- **Código:** Inconsolata, monospace

#### Pesos de Fuente
- **Light:** 300 - Textos secundarios
- **Normal:** 400 - Texto base
- **Medium:** 500 - Énfasis moderado
- **Bold:** 700 - Títulos y elementos importantes

### Componentes y Patrones

#### Principios de Diseño Atómico
- **Átomos:** Elementos básicos (botones, inputs, iconos)
- **Moléculas:** Combinaciones simples (form fields, search bars)
- **Organismos:** Secciones complejas (headers, tablas, modales)

#### Convenciones de Componentes
- **Nomenclatura:** PascalCase para componentes
- **Props:** Tipado estricto con TypeScript/Pydantic
- **Estados:** Gestión centralizada con Reflex State
- **Responsividad:** Mobile-first approach

#### Espaciado y Layout
- **Grid System:** Basado en CSS Grid y Flexbox
- **Breakpoints:** Responsive design estándar
- **Margins/Padding:** Sistema de espaciado consistente
- **Bordes:** Radio estandarizado en `sia/styles/border.py`

### Reglas de Interacción

#### Feedback Visual
- **Loading States:** Skeletons y spinners para cargas
- **Hover Effects:** Transiciones suaves en elementos interactivos
- **Focus States:** Indicadores claros para navegación por teclado
- **Error States:** Mensajes claros y constructivos

#### Navegación
- **Breadcrumbs:** Para ubicación en la jerarquía
- **Sidebar:** Navegación principal colapsible
- **Steps:** Para procesos multi-etapa
- **Modales:** Para acciones destructivas o formularios complejos

#### Accesibilidad
- **Contraste:** Cumplimiento de WCAG 2.1 AA
- **Semántica:** HTML semántico correcto
- **Teclado:** Navegación completa sin mouse
- **Screen Readers:** Etiquetas y roles ARIA apropiados

## Estado de Migración

El proyecto está actualmente en transición de Streamlit a Reflex:
- ✅ **Completado:** Infraestructura base de Reflex, sistema de componentes, gestión de usuarios
- 🚧 **En Progreso:** Migración completa de funcionalidades de cálculo
- 📋 **Pendiente:** Deprecación gradual de la aplicación Streamlit legacy
