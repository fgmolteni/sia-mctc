"""
Componente data_table: tabla reutilizable con funcionalidad avanzada.
"""
from typing import Any, Callable, Dict, List, Optional
import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace
from sia.styles.border import CommonBorders, BorderRadius


def default_actions_menu(item_data: Any) -> rx.Component:
    """Menú de acciones por defecto para data_table."""
    return rx.hstack(
        rx.button(
            rx.icon("eye", size=16),
            size="1",
            variant="ghost",
            #color_scheme="black"
        ),
        rx.button(
            rx.icon("pencil", size=16),
            size="1",
            variant="ghost",
            #color_scheme="black",
        ),
        rx.button(
            rx.icon("trash-2", size=16),
            size="1",
            variant="ghost",
            #color_scheme="black",
        ),
        spacing="4",
    )


def data_table(
    title: str,
    data: rx.Var,  # Variable de Reflex para datos dinámicos
    headers: List[str],
    render_functions: Optional[Dict[str, Callable]] = None,
    show_counter: bool = True,
    counter_text: str = "elementos",
    actions_column: bool = True,
    actions_menu: Optional[Callable] = None,
    **kwargs,
) -> rx.Component:
    """
    Componente de tabla reutilizable con funcionalidad avanzada.
    
    Args:
        title: Título de la tabla
        data: Variable de Reflex con lista de diccionarios
        headers: Lista de headers de columnas
        render_functions: Funciones de renderizado personalizadas por columna
        show_counter: Si mostrar contador de elementos
        counter_text: Texto para el contador
        actions_column: Si incluir columna de acciones
        actions_menu: Función para generar menú de acciones personalizado
        **kwargs: Propiedades adicionales para el contenedor
        
    Returns:
        rx.Component: Componente de tabla completa
    """
    if render_functions is None:
        render_functions = {}
    
    if actions_menu is None:
        actions_menu = default_actions_menu
    
    # Mapeo básico de headers a claves de datos
    header_to_key_mapping = {
        "Usuario": "name",
        "Correo": "email", 
        "Email": "email",
        "Rol": "role",
        "Estado": "status",
        "Área": "area",
        "Permisos": "permissions",
        "Último Acceso": "last_access",
        "Acciones": "actions",
    }
    
    def get_data_key(header: str) -> str:
        """Obtener clave de datos para un header."""
        return header_to_key_mapping.get(header, header.lower().replace(" ", "_"))
    
    def render_cell(row_data: rx.Var, header: str) -> rx.Component:
        """Renderizar una celda específica usando variables de Reflex."""
        data_key = get_data_key(header)
        
        # Si hay función de renderizado personalizada
        if data_key in render_functions:
            return render_functions[data_key](row_data[data_key], row_data)
        
        # Renderizado por defecto usando rx.Var
        return rx.text(row_data[data_key], color=ColorText.GRAY_700.value)
    
    def render_row(row_data: rx.Var) -> rx.Component:
        """Renderizar una fila completa usando variables de Reflex."""
        cells = []
        
        # Celdas de datos
        for header in headers:
            if header != "Acciones":
                cells.append(
                    rx.table.cell(
                        render_cell(row_data, header),
                        padding="12px 16px",
                    )
                )
        
        # Celda de acciones si está habilitada
        if actions_column and "Acciones" in headers:
            cells.append(
                rx.table.cell(
                    actions_menu(row_data),
                    padding="12px 16px",
                )
            )
        
        return rx.table.row(
            *cells,
            vertical_align="middle",
        )
    
    # Componente principal
    return rx.box(
        rx.vstack(
            # Header con título y contador
            rx.hstack(
                rx.text(
                    title,
                    font_weight=FontWeight.BOLD.value,
                    font_size="1.2em",
                    color=ColorText.GRAY_800.value,
                ),
                rx.spacer(),
                rx.cond(
                    show_counter,
                    rx.text(
                        data.length().to_string() + " de " + data.length().to_string() + f" {counter_text}",
                        font_size="0.9em",
                        color=ColorText.GRAY_500.value,
                    ),
                ),
                width="100%",
                align="center",
            ),
            # Tabla
            rx.table.root(
                # Headers
                rx.table.header(
                    rx.table.row(
                        *[
                            rx.table.column_header_cell(
                                header,
                                padding="12px 16px",
                                font_weight=FontWeight.MEDIUM.value,
                                color=ColorText.GRAY_800.value,
                                bg=Color.background_light,
                            )
                            for header in headers
                        ],
                    ),
                ),
                # Datos usando rx.foreach para variables dinámicas
                rx.table.body(
                    rx.foreach(data, render_row),
                ),
                width="100%",
                border=CommonBorders.LIGHT_SOLID,
                border_radius=BorderRadius.SMALL.value,
            ),
            width="100%",
            spacing="4",
        ),
        bg="white",
        padding=SizeSpace.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
        width="100%",
        **kwargs,
    )