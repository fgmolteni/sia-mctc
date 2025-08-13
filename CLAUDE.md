# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SIA (Sistema Interno de Administración) is a travel expense management system for the Ministry of Science and Technology. The project has dual architecture:

1. **Legacy Streamlit App** (`app.py`) - Original travel expense calculator
2. **Modern Reflex Web App** (`sia/sia.py`) - New modular web application with user management

## Development Commands

### Running the Applications

**Streamlit Application (Legacy):**
```bash
streamlit run app.py
```

**Reflex Application (Main):**
```bash
reflex run
```

### Database Setup

**Start PostgreSQL with Docker:**
```bash
docker compose up -d
```

**Check database status:**
```bash
docker ps
```

### Dependencies

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

## Architecture

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