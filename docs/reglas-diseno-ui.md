# Reglas de Diseño UI/UX - Sistema SIA

Guía de diseño para el Sistema Interno de Administración (SIA) del Ministerio de Ciencia y Tecnología.

## Principios
- **Consistencia**: Variables de estilo de `sia/styles/`, patrones uniformes
- **Claridad**: Jerarquía visual, información organizada, feedback inmediato  
- **Accesibilidad**: WCAG 2.1 AA, navegación por teclado, etiquetas semánticas

## Sistema de Colores

### Paleta Principal
```python
# Colores primarios
primary = "#1F1F1F"          # Negro principal
primary_dark = "#0F0F0F"     # Negro hover
secondary = "#EEEEEE"        # Gris claro
background = "#ffffff"       # Fondo principal
background_light = "#F9FAFB" # Fondo contenedores

# Colores semánticos
accent = "#B6EADA"          # Verde agua (success)
success = "#B6EADA"         # Verde éxito
warning = "#EEDF7A"         # Amarillo advertencia
error = "#F7374F"           # Rojo error
info = "#6EACDA"            # Azul información
```

### Colores Funcionales
```python
# Bordes
border_light = "#E5E7EB"    # Bordes suaves
border_medium = "#D1D5DB"   # Bordes medios

# Roles y estados
admin_bg = "#DBEAFE"        # Fondo administrador
admin_text = "#2563EB"      # Texto administrador
manager_bg = "#E9D5FF"      # Fondo supervisor
manager_text = "#9333EA"    # Texto supervisor
employee_bg = "#DCFCE7"     # Fondo usuario
employee_text = "#16A34A"   # Texto usuario
status_active = "#22C55E"   # Estado activo
```

**Uso**: Primary (headers, botones), Secondary (backgrounds, disabled), Accent/Success (confirmaciones), Warning (alertas), Error (errores), Info (información)

## Tipografía

### Familia de Fuentes
```python
DEFAULT = "Inter, sans-serif"           # Principal
SPACE_MONO = "Space Mono, monospace"   # Código/datos
INCONSOLATA = "Inconsolata, monospace" # Alternativa monospace
```

### Pesos y Tamaños
```python
# Pesos
LIGHT = "300"     # Texto secundario
NORMAL = "400"    # Texto base
MEDIUM = "500"    # Énfasis suave
BOLD = "700"      # Títulos, llamadas a la acción

# Tamaños
X_SMALL = "0.6em"  # Metadatos, timestamps
SMALL = "0.8em"    # Labels, texto secundario
MEDIUM = "1em"     # Texto base
LARGE = "1.2em"    # Subtítulos
X_LARGE = "2em"    # Títulos principales
```

**Jerarquía**: Títulos página (X_LARGE+BOLD+gray.800), Subtítulos (LARGE+MEDIUM+gray.500), Títulos sección (LARGE+BOLD+gray.800), Texto base (MEDIUM+NORMAL+gray.700), Secundario (SMALL+NORMAL+gray.500), Metadatos (X_SMALL+NORMAL+gray.400)

## Espaciado y Layout

### Sistema de Espaciado
```python
SMALL = "0.2em"   # 3-4px - Entre elementos relacionados
MEDIUM = "1em"    # 16px - Separación estándar
LARGE = "2em"     # 32px - Separaciones mayores
X_LARGE = "4em"   # 64px - Secciones principales
```

### Grid System
- **Contenedor principal**: max-width 1400px, centrado
- **Sidebar**: ancho fijo 280px
- **Contenido principal**: flex-grow 1
- **Cards/componentes**: grid responsive con gaps de 24px

### Layout de Páginas
```
┌─────────────────────────────────────────┐
│ Header Fijo (página)                    │
├─────────┬───────────────────────────────┤
│         │ Contenido Principal           │
│ Sidebar │ ├─ Estadísticas (optional)    │
│ Fijo    │ ├─ Filtros (optional)         │
│         │ ├─ Tabla/Contenido principal  │
│         │ └─ Paginación (optional)      │
└─────────┴───────────────────────────────┘
```

## Arquitectura de Páginas

### Estructura Estándar
- **Layout Fijo**: `height="100vh"`
- **Sidebar**: 280px, persistente
- **Header**: fijo con `border_bottom`, separación visual
- **Contenido**: scrolleable `overflow_y="auto"`, centrado `max_width="1400px"`
- **Overlays**: modales y toasts separados
- **Orden**: notification_messages() → statistics_cards() → filters_component() → main_content() → pagination()
```

### Características Clave

1. **Layout Fijo**: `height="100vh"` para ocupar toda la pantalla
2. **Sidebar Persistente**: `sidebar_main()` siempre presente
3. **Header con Border**: Separación visual clara del contenido
4. **Contenido Scrolleable**: `overflow_y="auto"` solo en la zona de contenido
5. **Max-width Centrado**: `max_width="1400px", margin="0 auto"`
6. **Overlays Separados**: Modales y toasts fuera del flujo principal
7. **Carga de Datos**: `on_mount` para inicialización automática

### Orden de Contenido Estándar

```python
# Dentro del contenido scrolleable:
1. notification_messages()    # Mensajes de estado
2. statistics_cards()         # Métricas y estadísticas  
3. filters_component()        # Filtros y búsqueda
4. main_content()            # Contenido principal (tabla/cards)
5. pagination() (opcional)    # Paginación si aplica
```

### Reglas de Implementación

- **Siempre usar** `on_mount` para cargar datos iniciales
- **Header fijo** con `border_bottom` para separación visual
- **Contenido centrado** con `max_width="1400px"`
- **Spacing="0"** entre secciones principales para control preciso
- **Toast container** siempre presente para notificaciones
- **Background consistente**: `bg=Color.background.value`

## Componentes y Patrones

### 1. Page Header
```python
def page_header(title, subtitle, action_button=None, back_button=False)
```
- **Estructura**: título + subtítulo + botón de acción opcional
- **Título**: X_LARGE + BOLD + gray.800
- **Subtítulo**: MEDIUM + NORMAL + gray.500
- **Botón de acción**: alineado a la derecha, estilo primary

### 2. Cards y Contenedores
```python
# Propiedades estándar
border_radius = "5px"
border = "1px solid #E5E7EB"
padding = "1em"
background = "white"
```

#### Stat Cards
- **Tamaño**: min-width 250px, height 120px
- **Estructura**: título + valor + ícono
- **Colores**: título gray.500, valor gray.800 + bold

#### Info Cards
- **Header opcional**: título + badge + acciones
- **Contenido**: flexible, cualquier rx.Component
- **Footer opcional**: metadatos + acciones secundarias

### 3. Tablas
```python
# Componente data_table estándar
headers = ["Usuario", "Rol", "Estado", "Acciones"]
render_functions = {
    "column_name": custom_render_function
}
```
- **Header**: MEDIUM + MEDIUM weight + gray.800
- **Filas**: alternar background white/gray.50
- **Padding**: celdas 12px vertical, 16px horizontal
- **Acciones**: íconos 16px con hover states

#### Patrones de Tabla Avanzados

Renderizado personalizado por columna implementado en `usuarios.py`:

```python
def advanced_table() -> rx.Component:
    """Tabla con renderizado personalizado por columna."""
    
    # Función de renderizado para columna principal con enlace
    def render_main_column(value, row_data):
        if isinstance(row_data, dict):
            item_id = row_data.get("id")
            return rx.vstack(
                rx.link(
                    rx.text(
                        value,
                        font_weight=FontWeight.MEDIUM.value,
                        color=ColorText.GRAY_800.value,
                        _hover={
                            "color": Color.primary.value,
                            "text_decoration": "underline",
                            "cursor": "pointer",
                        },
                    ),
                    href=f"/items/{item_id}",  # Navegación dinámica
                    text_decoration="none",
                ),
                rx.text(
                    row_data.get("subtitle", ""),
                    font_size=SizeText.SMALL.value,
                    color=ColorText.GRAY_500.value,
                ),
                spacing="1",
                align="start",
            )
    
    # Función de renderizado para badges
    def render_badge_column(value, row_data):
        badge_mapping = {
            "Activo": ("active", "green"),
            "Inactivo": ("inactive", "gray"),
        }
        status, color = badge_mapping.get(value, ("default", "gray"))
        return enhanced_status_badge(value, status=status, show_icon=True)
    
    # Función de renderizado para acciones
    def render_actions_column(value, row_data):
        if isinstance(row_data, dict):
            item_id = row_data.get("id")
            return rx.hstack(
                rx.link(
                    rx.button(rx.icon("eye"), variant="ghost", size="2"),
                    href=f"/items/{item_id}",
                ),
                rx.button(
                    rx.icon("pencil"), 
                    on_click=PageState.edit_item(item_id),
                    variant="ghost", 
                    size="2"
                ),
                rx.button(
                    rx.icon("trash"), 
                    on_click=PageState.delete_item(item_id),
                    variant="ghost", 
                    size="2",
                    color_scheme="red"
                ),
                spacing="1",
            )
    
    # Configuración de la tabla
    headers = ["Item Principal", "Estado", "Acciones"]
    render_functions = {
        "name": render_main_column,      # Columna con enlaces
        "status": render_badge_column,   # Columna con badges
        "actions": render_actions_column, # Columna de acciones
    }
    
    return data_table(
        title="Título de la Tabla",
        data=PageState.items_data,
        headers=headers,
        render_functions=render_functions,
        show_counter=True,
        counter_text="elementos",
        actions_column=True,
    )
```

#### Tipos de Renderizado Estándar

**Columna Principal con Enlaces:**
- Título principal con hover effects
- Subtítulo opcional en texto pequeño
- Link dinámico a página de detalle
- Transiciones suaves en hover

**Columna de Badges:**
- Mapeo de valores a tipos de badge
- Colores consistentes por estado
- Íconos opcionales integrados

**Columna de Acciones:**
- Ver (eye) + Editar (pencil) + Eliminar (trash)
- Espaciado uniforme entre botones
- Color scheme específico para acciones destructivas
- Tamaño estándar "2" para todos los botones

#### Manejo Dual Python/Reflex

```python
def render_column(value, row_data):
    if isinstance(row_data, dict):
        # Para listas Python estáticas
        return render_dict_data(value, row_data)
    else:
        # Para variables Reflex dinámicas
        return rx.match(
            value,
            ("valor1", render_case_1()),
            ("valor2", render_case_2()),
            render_default(),  # fallback
        )
```

### 4. Formularios y Inputs

#### Input Fields
```python
# Propiedades estándar
border = "1px solid #E5E7EB"
border_radius = "5px"
padding = "8px 12px"
focus_border = primary_color
error_border = error_color
```

#### Estados de Validación
- **Normal**: border gray.300
- **Focus**: border primary + box-shadow
- **Error**: border red + mensaje de error debajo
- **Success**: border green + checkmark opcional
- **Disabled**: background gray.100 + color gray.400

#### Estados de Formulario Avanzados

Patrón completo implementado en `usuarios.py` con validación en tiempo real y transformaciones automáticas:

```python
class FormState(rx.State):
    # Campos del formulario
    form_nombre: str = ""
    form_email: str = ""
    form_dni: str = ""
    
    # Estados de error específicos por campo
    has_nombre_error: bool = False
    has_email_error: bool = False
    has_dni_error: bool = False
    
    # Mensajes de error específicos
    nombre_error_message: str = ""
    email_error_message: str = ""
    dni_error_message: str = ""
    
    # Estado general de validación
    form_errors: dict[str, str] = {}
    has_validation_errors: bool = False
    
    def validate_field(self, field_name: str, value: str):
        """Validación en tiempo real por campo."""
        is_valid, error_message = validate_field_value(
            field_name, value, get_validation_rules()
        )
        
        # Actualizar estado específico del campo
        if field_name == "nombre":
            self.has_nombre_error = not is_valid
            self.nombre_error_message = error_message if not is_valid else ""
        
        # Actualizar diccionario general de errores
        if is_valid:
            if field_name in self.form_errors:
                new_errors = self.form_errors.copy()
                del new_errors[field_name]
                self.form_errors = new_errors
        else:
            new_errors = self.form_errors.copy()
            new_errors[field_name] = error_message
            self.form_errors = new_errors
        
        self.has_validation_errors = len(self.form_errors) > 0
    
    def set_form_nombre(self, nombre: str):
        """Setter con transformación automática y validación."""
        # 1. Aplicar transformación automática
        self.form_nombre = apply_auto_transform(nombre, "title")
        # 2. Validar en tiempo real
        self.validate_field("nombre", self.form_nombre)
    
    def set_form_email(self, email: str):
        """Setter con transformación y validación."""
        self.form_email = apply_auto_transform(email, "lowercase")
        self.validate_field("email", self.form_email)
    
    def set_form_dni(self, dni: str):
        """Setter con limpieza y validación específica."""
        import re
        dni_clean = re.sub(r"[^\d]", "", dni)  # Solo números
        self.form_dni = dni_clean
        self.validate_field("dni", self.form_dni)
    
    def validate_all_fields(self):
        """Validación completa antes del submit."""
        self.validate_field("nombre", self.form_nombre)
        self.validate_field("email", self.form_email)
        if self.form_dni.strip():  # Campo opcional
            self.validate_field("dni", self.form_dni)
```

#### Transformaciones Automáticas Estándar

```python
# Importar función de transformación
from sia.components.forms.inputs import apply_auto_transform

# Tipos de transformación disponibles:
apply_auto_transform(value, "title")     # Capitalizar palabras
apply_auto_transform(value, "lowercase") # Minúsculas
apply_auto_transform(value, "uppercase") # Mayúsculas
```

**Casos de Uso:**
- **Nombres/Apellidos**: `title` para capitalización correcta
- **Emails/Usernames**: `lowercase` para consistencia
- **DNI/Números**: Limpieza con regex personalizada
- **Códigos**: `uppercase` para estandarización

#### Patrón de Validación Dual

**1. Validación Específica por Campo:**
```python
# Estados booleanos para UI inmediata
has_nombre_error: bool = False
nombre_error_message: str = ""
```

**2. Validación General del Formulario:**
```python
# Diccionario para lógica de negocio
form_errors: dict[str, str] = {}
has_validation_errors: bool = False
```

#### Flujo de Validación Completo

1. **Input del Usuario** → Transformación automática
2. **Transformación** → Validación individual del campo  
3. **Validación** → Actualización de estados específicos
4. **Estados UI** → Feedback visual inmediato
5. **Submit** → Validación completa de todos los campos

#### Reglas de Implementación

- **Setters personalizados** para todos los campos del formulario
- **Transformación antes de validación** en cada setter
- **Estados duales**: específicos por campo + general del formulario
- **Validación en tiempo real** en `on_change` de inputs
- **Limpieza de errores** cuando el campo se vuelve válido
- **Prevención de submit** cuando `has_validation_errors = True`

### 5. Sistema de Filtros Dinámicos

Patrón estándar para filtros con búsqueda en tiempo real implementado en `usuarios.py`:

```python
def filters_component() -> rx.Component:
    """Componente de filtros con auto-búsqueda."""
    return rx.box(
        rx.vstack(
            # Header con botón limpiar
            rx.hstack(
                rx.text("Filtros de Búsqueda", font_weight=FontWeight.BOLD.value),
                rx.spacer(),
                rx.button(
                    "Limpiar filtros",
                    on_click=PageState.clear_filters,
                    variant="ghost",
                    size="2",
                    color_scheme="gray",
                ),
                width="100%",
                align="center",
            ),
            # Grid de filtros (3 columnas estándar)
            rx.grid(
                # Campo de búsqueda (columna 1)
                rx.input(
                    placeholder="Buscar por nombre, email...",
                    width="100%",
                    border=CommonBorders.LIGHT_SOLID,
                    value=PageState.search_term,
                    on_change=PageState.set_search_term,  # Auto-filtrado
                ),
                # Filtro categórico 1 (columna 2)
                select_component(
                    options=["Todas las opciones", "Opción 1", "Opción 2"],
                    value=PageState.filter_1,
                    on_change=PageState.set_filter_1,  # Auto-filtrado
                ),
                # Filtro categórico 2 (columna 3)
                select_component(
                    options=["Todos los estados", "Activo", "Inactivo"],
                    value=PageState.filter_2,
                    on_change=PageState.set_filter_2,  # Auto-filtrado
                ),
                columns="3",  # Siempre 3 columnas
                spacing="4",
                width="100%",
            ),
            width="100%",
            spacing="4",
        ),
        bg="white",
        border_radius=BorderRadius.SMALL.value,
        border=CommonBorders.LIGHT_SOLID,
        padding=SizeSpace.MEDIUM.value,
        width="100%",
        mb="4",
    )
```

#### Características del Estado

```python
class PageState(rx.State):
    # Filtros
    search_term: str = ""
    filter_1: str = ""
    filter_2: str = ""
    
    def set_search_term(self, term: str):
        self.search_term = term
        return self.apply_filters()  # Auto-filtrado inmediato
    
    def set_filter_1(self, value: str):
        self.filter_1 = value
        return self.apply_filters()  # Auto-filtrado inmediato
    
    def clear_filters(self):
        self.search_term = ""
        self.filter_1 = ""
        self.filter_2 = ""
        return self.apply_filters()
    
    def apply_filters(self):
        # Mapear valores UI a base de datos
        ui_to_db_mapping = {
            "Todas las opciones": "",
            "Opción 1": "db_value_1",
        }
        
        # Aplicar filtros con mapeo
        db_filter = ui_to_db_mapping.get(self.filter_1, "")
        # Ejecutar búsqueda filtrada...
```

#### Reglas de Implementación

- **Grid 3 columnas**: búsqueda + 2 filtros categóricos
- **Auto-filtrado**: `on_change` ejecuta filtros inmediatamente
- **Mapeo UI→DB**: convertir valores de display a valores de base de datos
- **Botón limpiar**: siempre presente y funcional
- **Placeholder específico**: describir qué campos se buscan
- **Estilo consistente**: card blanca con borde y padding estándar

### 6. Modales
```python
# Estructura estándar
- Overlay: rgba(0,0,0,0.5)
- Container: max-width 500px, centrado
- Header: título + botón cerrar
- Body: contenido del formulario
- Footer: botones de acción
```

### 6. Navegación

#### Sidebar
- **Ancho**: 280px fijo
- **Background**: white
- **Border**: right 1px solid gray.200
- **Items**: padding 12px, hover background gray.50
- **Iconos**: 20px, gray.400 normal, primary activo

#### Breadcrumbs
```python
# Estructura: Inicio > Sección > Página actual
separator = "/"
current_page_style = "bold + primary_color"
links_style = "normal + gray.500"
```

### 7. Badges y Estados

#### Role Badges
```python
# Estilos por rol
admin = {"bg": "#DBEAFE", "color": "#2563EB"}
supervisor = {"bg": "#E9D5FF", "color": "#9333EA"} 
usuario = {"bg": "#DCFCE7", "color": "#16A34A"}
```

#### Status Badges
```python
# Activo: verde + punto
active = {"bg": "green.100", "color": "green.700", "dot": "green.400"}
# Inactivo: gris + punto
inactive = {"bg": "gray.100", "color": "gray.700", "dot": "gray.400"}
```

### 8. Botones

#### Jerarquía de Botones
1. **Primary**: background black, color white, hover gray.800
2. **Secondary**: background gray.200, color gray.700, hover gray.300
3. **Ghost/Outline**: background transparent, border gray.300, hover gray.50
4. **Destructive**: background red.500, color white, hover red.600

#### Tamaños
- **Small**: padding 6px 12px, text 14px
- **Medium**: padding 8px 16px, text 16px (defecto)
- **Large**: padding 12px 24px, text 18px

## Estados de UI

### Loading States
- **Skeleton**: componentes grises pulsantes mientras cargan datos
- **Spinner**: para acciones en progreso
- **Disabled**: botones y campos deshabilitados con opacity 0.6

### Empty States
- **Sin datos**: mensaje + ilustración + call-to-action
- **Búsqueda sin resultados**: mensaje + sugerencias
- **Error de carga**: mensaje + botón retry

### Interactive States
- **Hover**: transición suave 150ms
- **Active**: feedback visual inmediato
- **Focus**: outline accesible para navegación por teclado
- **Disabled**: indica claramente elementos no interactuables

## Responsive Design

### Breakpoints
```css
sm: 640px   /* Móvil grande */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop pequeño */
xl: 1280px  /* Desktop grande */
```

### Comportamiento Adaptativo
- **Móvil (< 768px)**: sidebar colapsa a overlay, cards en columna única
- **Tablet (768-1024px)**: sidebar visible, grid 2 columnas
- **Desktop (> 1024px)**: layout completo, grid 3+ columnas

### Navegación Móvil
- Botón hamburguesa para mostrar sidebar
- Menú overlay con backdrop
- Toque para cerrar fuera del menú

## Accesibilidad

### Contraste de Color
- Texto normal: mínimo 4.5:1
- Texto grande: mínimo 3:1
- Componentes interactivos: mínimo 3:1

### Navegación por Teclado
- Todos los elementos interactivos focalizables
- Orden lógico de tabulación
- Indicadores de focus visibles
- Shortcuts de teclado para acciones principales

### Lectores de Pantalla
- Alt text en imágenes informativas
- Labels asociados a inputs
- Roles ARIA apropiados
- Estados dinámicos anunciados

## Microinteracciones

### Transiciones Estándar
```css
transition: all 0.15s ease-in-out;  /* Hover, focus */
transition: opacity 0.2s ease;      /* Aparición/desaparición */
transition: transform 0.15s ease;   /* Movimiento */
```

### Animaciones de Carga
- Fade in para contenido nuevo
- Skeleton loading para tablas y listas
- Progress bars para procesos largos

### Feedback Interactivo
- Botones: hover + active states
- Inputs: focus ring + validación en tiempo real
- Links: subrayado en hover
- Cards: sombra suave en hover

## Toast Notifications

### Tipos y Colores
- **Success**: background green.100, border green.400, icon check-circle
- **Error**: background red.100, border red.400, icon x-circle  
- **Warning**: background yellow.100, border yellow.400, icon alert-triangle
- **Info**: background blue.100, border blue.400, icon info-circle

### Comportamiento
- Posición: esquina superior derecha
- Duración: 4-6 segundos (éxito/info), manual (error/warning)
- Máximo 3 toasts simultáneos
- Animación: slide in desde la derecha

## Patrones de Validación

### Validación en Tiempo Real
- Validar campo por campo al perder focus
- Mostrar errores inmediatamente
- Confirmar correcciones con color verde

### Mensajes de Error
- Específicos y accionables
- Ubicados directamente bajo el campo
- Color error + ícono de alerta
- Texto en español claro y directo

### Estados de Formulario
- Submit deshabilitado si hay errores
- Loading state durante envío
- Toast confirmation al completar
- Limpiar formulario después del éxito

## Implementación Técnica

### Importaciones Estándar
```python
# Estilos base
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight, FontFamily
from sia.styles.sizes import SizeText, SizeIcon, SizeSpace, BorderRadius
from sia.styles.border import CommonBorders

# Componentes base
from sia.components.layout.headers import page_header
from sia.components.data_display.tables import data_table
from sia.components.data_display.cards import stat_card, info_card_profile
```

### Estructura de Componentes
```python
def component_name(props) -> rx.Component:
    """
    Descripción del componente y su propósito.
    
    Args:
        props: descripción de parámetros
    
    Returns:
        rx.Component: componente configurado
    """
    return rx.container(
        # Estructura del componente
        width="100%",
        padding=SizeSpace.MEDIUM.value,
    )
```

### Convenciones de Naming
- Componentes: `snake_case` para funciones
- Props: nombres descriptivos en español cuando sea necesario
- Estados: prefijo `is_`, `has_`, `show_` para booleans
- Handlers: prefijo `on_`, `handle_`, sufijo `_action`

## Transformación de Datos UI/Backend

### Patrón de Conversión Backend → UI

Implementado en `usuarios.py` para transformar modelos Pydantic a formato de tabla:

```python
def _convert_to_display_format(self, backend_item: PydanticModel) -> dict[str, Any]:
    """Convierte modelo backend al formato esperado por la UI."""
    
    # 1. Mapeo de valores para display
    display_mapping = {
        "admin": "Administrador",
        "supervisor": "Supervisor", 
        "usuario": "Usuario",
    }
    
    # 2. Formateo de datos complejos
    formatted_date = (
        backend_item.fecha_creacion.strftime("%d/%m/%Y") 
        if backend_item.fecha_creacion 
        else "N/A"
    )
    
    # 3. Campos calculados para UI
    full_name = f"{backend_item.nombre} {backend_item.apellido}"
    avatar_initial = backend_item.nombre[0].upper() if backend_item.nombre else "U"
    
    # 4. Estructura final para tabla/UI
    return {
        "id": backend_item.id,
        "name": full_name,                    # Campo combinado
        "email": backend_item.email,
        "role": display_mapping.get(          # Valor mapeado
            backend_item.rol, 
            backend_item.rol.title()
        ),
        "status": "Activo",                   # Estado calculado
        "last_access": formatted_date,        # Fecha formateada
        "avatar": avatar_initial,             # Campo calculado
        "area": "Ministerio C&T",            # Valor por defecto
    }
```

### Tipos de Transformación Estándar

#### 1. Mapeo de Valores
```python
# Backend → Display
role_mapping = {
    "admin": "Administrador",
    "user": "Usuario", 
    "manager": "Supervisor"
}
```

#### 2. Formateo de Fechas
```python
# Fecha ISO → Display localizado
formatted_date = date_obj.strftime("%d/%m/%Y") if date_obj else "No disponible"
```

#### 3. Campos Combinados
```python
# Múltiples campos → Campo único
full_name = f"{item.first_name} {item.last_name}"
```

#### 4. Campos Calculados
```python
# Lógica de negocio → Valor UI
avatar = item.name[0].upper() if item.name else "?"
status = "Activo" if item.is_active else "Inactivo"
```

#### 5. Valores por Defecto
```python
# Fallbacks para campos opcionales  
area = item.department or "Sin asignar"
phone = item.phone or "No especificado"
```

### Patrón Inverso: UI → Backend

```python
def _convert_form_to_backend(self) -> BackendModel:
    """Convierte datos del formulario al modelo backend."""
    
    # Mapeo inverso UI → Backend
    ui_to_backend_roles = {
        "Administrador": "admin",
        "Supervisor": "supervisor", 
        "Usuario": "usuario"
    }
    
    # Limpieza y conversión de tipos
    dni_value = int(self.form_dni.strip()) if self.form_dni.strip() else None
    
    return BackendModel(
        nombre=self.form_nombre.strip(),
        apellido=self.form_apellido.strip(),
        email=self.form_email.lower().strip(),
        dni=dni_value,
        rol=ui_to_backend_roles.get(self.form_rol, "usuario")
    )
```

### Reglas de Implementación

- **Función privada** `_convert_*_format()` para cada entidad
- **Mapeos bidireccionales** para valores categóricos  
- **Formateo consistente** de fechas usando strftime
- **Campos calculados** para mejorar UX
- **Valores por defecto** para campos opcionales
- **Validación de tipos** en conversión inversa
- **Limpieza de datos** antes de enviar al backend

## Checklist de Implementación

### Antes de Crear Componentes
- [ ] ¿Existe un componente similar que pueda reutilizar?
- [ ] ¿Estoy usando las variables de estilo correctas?
- [ ] ¿El componente es responsive?
- [ ] ¿Tiene estados de hover/focus/disabled apropiados?

### Antes de Crear Páginas
- [ ] ¿Sigue el layout estándar (sidebar + header + contenido)?
- [ ] ¿Tiene page_header consistente?
- [ ] ¿Incluye estadísticas relevantes si aplica?
- [ ] ¿Los filtros y búsquedas están bien ubicados?

### Arquitectura de Páginas Complejas
- [ ] ¿Implementa estructura de 3 columnas (sidebar + main + content)?
- [ ] ¿Usa `overflow_y="auto"` en contenedores que requieren scroll?
- [ ] ¿Los breadcrumbs están posicionados correctamente bajo el header?
- [ ] ¿Incluye `toast_container()` para notificaciones?
- [ ] ¿Usa `on_mount` para carga inicial de datos?

### Sistema de Filtros Dinámicos
- [ ] ¿Los filtros están alineados horizontalmente en 3 columnas?
- [ ] ¿Cada filtro tiene `on_change` conectado al estado?
- [ ] ¿Los filtros se aplican automáticamente sin botón "Buscar"?
- [ ] ¿Los dropdowns tienen opciones "Todos" como valor por defecto?
- [ ] ¿Los filtros de texto incluyen debouncing para performance?

### Patrones de Tabla Avanzados
- [ ] ¿Usa `render_functions` para personalizar columnas específicas?
- [ ] ¿Incluye columna de acciones con menú contextual?
- [ ] ¿Las funciones de render manejan tanto listas Python como rx.Var?
- [ ] ¿Los badges y estados usan colores consistentes del design system?
- [ ] ¿Incluye contador de elementos mostrados?

### Estados de Formulario Avanzados
- [ ] ¿Implementa validación en tiempo real con auto-transformación?
- [ ] ¿Usa `apply_auto_transform` para campos como email y DNI?
- [ ] ¿Maneja estados duales (campo_error + has_campo_error)?
- [ ] ¿Incluye indicadores visuales de carga (spinners, disabled states)?
- [ ] ¿Los mensajes de error son específicos y útiles?

### Integración de Modales
- [ ] ¿Usa `rx.cond` para controlar visibilidad?
- [ ] ¿Incluye lógica de cierre en múltiples puntos (X, overlay, ESC)?
- [ ] ¿Los formularios dentro del modal son independientes del estado principal?
- [ ] ¿Implementa estados de carga específicos para el modal?
- [ ] ¿Valida y limpia datos antes de envío?

### Transformación de Datos
- [ ] ¿Implementa funciones `_convert_*_format()` para cada entidad?
- [ ] ¿Usa mapeos bidireccionales para valores categóricos?
- [ ] ¿Aplica formateo consistente de fechas y números?
- [ ] ¿Incluye campos calculados para mejorar UX?
- [ ] ¿Limpia y valida datos antes de enviar al backend?

### Testing de Accesibilidad
- [ ] Navegación completa por teclado
- [ ] Contraste de colores adecuado
- [ ] Textos alt en imágenes
- [ ] Labels en todos los inputs
- [ ] Estructura semántica HTML correcta

## Mantenimiento y Evolución

### Actualización del Sistema
- Todos los cambios al sistema de diseño deben documentarse aquí
- Nuevos componentes deben seguir estos patrones
- Refactorizaciones deben mantener compatibilidad con patrones existentes

### Revisión de Código
- Verificar adherencia a estas reglas en code reviews
- Validar uso correcto de componentes reutilizables
- Confirmar implementación de estados de error y loading

---

## Implementación de Atomic Design

### Estructura de Componentes por Niveles

El proyecto SIA ha implementado completamente el patrón Atomic Design, organizando los componentes en una jerarquía clara:

#### **Átomos** (`sia/components/atoms/`)
Elementos UI más básicos e indivisibles:
- **Badges**: `role_badge`, `status_badge` - Estados y roles con colores consistentes
- **Botones**: Botones individuales con estados (hover, focus, disabled)
- **Inputs**: Campos de entrada básicos (text, email, password)
- **Iconos**: Iconografía consistente del sistema

#### **Moléculas** (`sia/components/molecules/`)
Combinaciones simples de átomos que forman componentes funcionales:
- **Funciones de Renderizado**: `user_renders.py` - Renderizado específico por columna
- **Campos de Formulario**: Input + label + validación como unidad
- **Tarjetas Simples**: Combinaciones de texto + ícono + badge

```python
# Ejemplo: Renderizado de información de usuario (molécula)
def render_user_info(value, row_data):
    """Combina avatar + nombre + email como una unidad funcional."""
    return rx.hstack(
        avatar_atom(user=row_data.get("avatar")),
        rx.vstack(
            rx.text(value, font_weight=FontWeight.MEDIUM.value),
            rx.text(row_data.get("email"), color=ColorText.GRAY_500.value),
        ),
    )
```

#### **Organismos** (`sia/components/organisms/`)
Secciones completas que combinan múltiples moléculas:

**Organismos de Formularios** (`forms/organisms/`):
- `search_filters.py` - Panel completo de filtros con múltiples campos de búsqueda

**Organismos de Visualización** (`data_display/organisms/`):
- `user_statistics.py` - Panel de estadísticas con múltiples tarjetas métricas
- `user_table.py` - Tabla completa con headers, datos y acciones

**Organismos de Retroalimentación** (`feedback/organisms/`):
- `notifications.py` - Sistema completo de mensajes (éxito, error, loading)

```python
# Ejemplo: Organismo de estadísticas
def user_statistics() -> rx.Component:
    """Organismo que combina múltiples stat_cards con header y acciones."""
    return rx.vstack(
        statistics_header_molecule(),  # Molécula: título + botones refresh
        rx.hstack(
            stat_card("Total", value, icon),      # Átomo reutilizable
            stat_card("Activos", value, icon),   # Átomo reutilizable
            stat_card("Admins", value, icon),    # Átomo reutilizable
        ),
    )
```

#### **Plantillas** (`sia/components/templates/`)
Estructuras de layout que organizan organismos:

- `user_management.py` - Template completo para páginas CRUD con:
  - Layout sidebar + contenido principal
  - Header fijo con separador visual
  - Área de contenido scrolleable centrada
  - Overlays para modales y toasts

```python
# Ejemplo: Template de gestión
def user_management_template(
    statistics_component,
    filters_component,
    table_component,
    notifications_component
) -> rx.Component:
    """Template que define la estructura estándar de páginas CRUD."""
    return layout_structure(
        sidebar=sidebar_main(),
        header=page_header_organism(),
        content=scrolleable_content(
            notifications_component(),  # Organismo
            statistics_component(),     # Organismo
            filters_component(),        # Organismo  
            table_component(),          # Organismo
        ),
        overlays=[modal_component(), toast_container()],
    )
```

#### **Páginas** (`sia/pages/`)
Instancias específicas de templates con datos y estado:

```python
# Ejemplo: Página usando atomic design
def users_page() -> rx.Component:
    """Página que instancia template con componentes específicos."""
    return user_management_template(
        statistics_component=user_statistics,    # Organismo específico
        filters_component=search_filters,        # Organismo específico
        table_component=user_table,              # Organismo específico
        notifications_component=notifications,   # Organismo específico
    )
```

### Beneficios de la Implementación

#### **1. Reutilización Máxima**
- Los átomos (badges, botones) se reutilizan en múltiples organismos
- Las moléculas (renders, cards) son aplicables a diferentes entidades
- Los organismos (filtros, tablas) son reutilizables para agentes, vehículos, etc.
- Las plantillas proporcionan estructura consistente

#### **2. Mantenimiento Simplificado**
- Cambios en átomos se propagan automáticamente
- Cada nivel tiene responsabilidades específicas y limitadas
- Debugging aislado por componente
- Testing unitario por nivel

#### **3. Escalabilidad**
- Nuevas páginas reutilizan organismos existentes
- Nuevos organismos combinan moléculas/átomos existentes
- Patrones establecidos para cualquier nueva funcionalidad

#### **4. Consistencia Visual**
- Design system aplicado desde átomos hasta páginas
- Patrones de interacción uniformes
- Jerarquía visual mantenida en todos los niveles

### Convenciones de Nomenclatura

#### **Archivos y Directorios**
- **No redundancia**: Los directorios ya indican el nivel (`atoms/`, `molecules/`, etc.)
- **Nombres descriptivos**: `search_filters.py` en lugar de `search_filters_organism.py`
- **Agrupación temática**: Por funcionalidad (`forms/`, `data_display/`, `feedback/`)

#### **Funciones y Componentes**
```python
# Átomos: función simple
def role_badge(text: str, role: str) -> rx.Component

# Moléculas: función con contexto específico  
def render_user_info(value, row_data) -> rx.Component

# Organismos: función de sección completa
def user_statistics() -> rx.Component

# Templates: función de estructura de layout
def user_management_template(...) -> rx.Component
```

### Migración y Refactorización

#### **Proceso Aplicado en usuarios.py**
1. **Antes**: 1186 líneas con todo mezclado
2. **Identificación**: Separar átomos, moléculas, organismos mezclados
3. **Extracción**: Mover cada función a su nivel correcto
4. **Reorganización**: Crear estructura de directorios atomic
5. **Después**: ~150 líneas (solo estado + página principal)

#### **Resultado de la Refactorización**
- ✅ **Funcionalidad idéntica**: Toda la lógica se mantiene
- ✅ **Código organizado**: Cada componente en su nivel correcto  
- ✅ **Reutilización habilitada**: Componentes disponibles para otras páginas
- ✅ **Mantenimiento simplificado**: Responsabilidades separadas y claras

### Reglas de Implementación Atomic Design

#### **Al crear nuevos componentes:**
1. **Identificar nivel**: ¿Es átomo, molécula, organismo o template?
2. **Verificar reutilización**: ¿Existe un componente similar?
3. **Ubicar correctamente**: En el directorio que corresponde a su nivel
4. **Nombrar descriptivamente**: Sin redundancia del nivel en el nombre
5. **Documentar dependencias**: Imports claros y específicos

#### **Al refactorizar código existente:**
1. **Analizar complejidad**: Identificar qué elementos están mezclados
2. **Extraer por niveles**: Comenzar con átomos, luego moléculas, organismos
3. **Mantener funcionalidad**: Testing continuo durante la migración
4. **Actualizar imports**: Corregir todas las referencias a componentes movidos

**Nota**: Este documento es la fuente de verdad para el diseño UI/UX del Sistema SIA. Cualquier desviación debe estar justificada y documentada. Para implementación de Atomic Design, consultar la refactorización exitosa en `sia/pages/usuarios.py` y la nueva estructura de `sia/components/`.