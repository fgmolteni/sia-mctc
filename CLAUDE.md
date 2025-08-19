# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Instrucciones de Idioma

**IMPORTANTE**: Todas las respuestas y comunicaciones con el usuario deben ser en español. El equipo de desarrollo trabaja en español y prefiere recibir explicaciones, documentación y mensajes de error en este idioma.

## Descripción del Proyecto

SIA (Sistema Interno de Administración) es un sistema de gestión de viáticos para el Ministerio de Ciencia y Tecnología. El proyecto tiene arquitectura dual:

1. **Aplicación Streamlit Legacy** (`app.py`) - Calculadora original de viáticos
2. **Aplicación Web Reflex Moderna** (`sia/sia.py`) - Nueva aplicación web modular con gestión de usuarios

## Comandos de Desarrollo

### Ejecutar las Aplicaciones

**Aplicación Streamlit (Legacy):**
```bash
streamlit run app.py
```

**Aplicación Reflex (Principal):**
```bash
reflex run
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

### Dependencias

**Instalar dependencias de Python:**
```bash
pip install -r requirements.txt
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

- **PostgreSQL** - Primary database (Docker containerized)
- **Connection** - Managed through `components/db_connector.py`
- **Schema** - Located in `database/schema.sql`

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

## Development Notes

- The project is transitioning from Streamlit to Reflex
- Database credentials should be managed via environment variables
- PDF reports are generated to the `report/` directory
- Asset files are served from `assets/` directory
- The current branch `feature/implement-reflex` contains the new Reflex implementation