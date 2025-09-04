# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Instrucciones de Idioma

**IMPORTANTE**: Todas las respuestas y comunicaciones con el usuario deben ser en español. El equipo de desarrollo trabaja en español y prefiere recibir explicaciones, documentación y mensajes de error en este idioma.

## Descripción del Proyecto

SIA (Sistema Interno de Administración) es un sistema de gestión de viáticos para el Ministerio de Ciencia y Tecnología. El proyecto tiene arquitectura dual:

1. **Aplicación Streamlit Legacy** (`app.py`) - Calculadora original de viáticos
2. **Aplicación Web Reflex Moderna** (`sia/sia.py`) - Nueva aplicación web modular con gestión de usuarios

## Comandos de Desarrollo

### Configuración del Entorno

**Crear y activar entorno virtual:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

**Instalar dependencias de Python:**
```bash
pip install -r requirements.txt
```

### Configuración de Base de Datos

**Iniciar PostgreSQL con Docker:**
```bash
docker compose up -d
```

**Verificar estado de la base de datos:**
```bash
docker ps
```

**Verificar logs de la base de datos:**
```bash
docker compose logs db
```

**Detener la base de datos:**
```bash
docker compose down
```

### Ejecutar las Aplicaciones

**Aplicación Reflex (Principal):**
```bash
reflex run
```

**Aplicación Streamlit (Legacy):**
```bash
streamlit run app.py
```

### Testing y Desarrollo

**Ejecutar test de logging (ejemplo disponible):**
```bash
python test_logging.py
```

## Arquitectura

### Reflex Application Structure (`sia/`)

- **`sia.py`** - Main application entry point with routing
- **`pages/`** - Page components (dashboard, login, users, profiles, etc.)
- **`views/`** - Complex view logic and state management
- **`components/`** - Reusable UI components organized by category:
  - `branding/` - Logo and brand elements
  - `data_display/` - Tables, avatars, badges, menus, timelines
  - `feedback/` - Banners and notifications
  - `forms/` - Input components, buttons, selects
  - `layout/` - Headers, sidebars, cards
  - `navigation/` - Breadcrumbs, navbars, steps
- **`styles/`** - Design system (colors, fonts, sizes, borders)

### Legacy Components (`components/`)

Business logic modules for travel expense calculations:
- **`db_*.py`** - Database operations (users, agents, vehicles, expenses)
- **`distance_calculator.py`** - Geographic distance/duration calculations
- **`date_calculator.py`** - Travel day calculations for expense purposes  
- **`pdf_generator.py`** - PDF report generation
- **`converter.py`** - Number to text/currency conversion

### Database

- **PostgreSQL con pgvector** - Base de datos principal (containerizada con Docker)
- **Connection** - Gestionada a través de `components/db_connector.py`
- **Schema** - Ubicado en `database/schema.sql`
- **Migración** - Script de migración CSV a SQL en `database/migrate_csv_to_sql.py`
- **Configuración** - Variables de entorno en `.env`:
  - `DATABASE_URL=postgresql://user_sia:password_sia@localhost:5432/db_sia`
  - Puerto: 5432 (PostgreSQL estándar)

## Code Patterns

### Reflex Components
- Use `rx.Component` return type annotations
- Follow atomic design principles (atoms → molecules → organisms)
- Organize by functionality in component subdirectories
- Import styles from `sia.styles.*` modules

### State Management
- Each major feature has its own State class (UserState, AgentState, etc.)
- State classes inherit from `rx.State`
- Use `on_load` handlers for data fetching

### Database Operations
- Use `get_db_engine()` for connections
- Always dispose engines after use
- SQL queries return pandas DataFrames
- Error handling for connection failures

## Design System

The project uses a comprehensive design system located in `sia/styles/`:
- **Colors** - Consistent color palette
- **Fonts** - Typography scale and weights  
- **Sizes** - Standardized dimensions
- **Borders** - Border radius and styling

## Key Dependencies

- **Reflex** (0.8.1) - Main web framework
- **Streamlit** - Legacy interface framework
- **PostgreSQL/psycopg2** - Database connectivity
- **Pandas** - Data manipulation
- **ReportLab** - PDF generation
- **Geopy/Requests** - Geographic calculations

## Configuración del Proyecto

### Configuración de Reflex

- **rxconfig.py** - Configuración principal con plugins TailwindV4 y Sitemap
- **Assets** - Directorio `assets/` para archivos estáticos
- **Styles** - Sistema de diseño modular en `sia/styles/`

### Logging

- **Configuración** - `components/logging/logger_config.py`
- **Logs** - Directorio `logs/` para archivos de log
- **Test** - `test_logging.py` para verificar funcionamiento

## Development Notes

- El proyecto está en transición de Streamlit a Reflex
- Los reportes PDF se generan en el directorio `report/`
- La rama `feature/implement-reflex` contiene la nueva implementación
- Usar variables de entorno para credenciales de base de datos
- El proyecto incluye datos de ejemplo en `data/` (agent.csv, cars.csv)
- no quiero que hagas referencias claude o claude-code cuando hagas un commit o documentacion