import reflex as rx
from typing import List, Dict, Any, Optional, Callable
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText, BorderRadius, SizeSpace, SizeIcon
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders

def data_table(
    title: str,
    data: List[Dict[str, Any]],
    headers: List[str],
    render_functions: Dict[str, Callable] = None,
    show_counter: bool = True,
    counter_text: str = "elementos mostrados",
    actions_column: bool = True,
    actions_menu: Optional[rx.Component] = None,
    **kwargs
) -> rx.Component:
    """
    Componente de tabla reutilizable para mostrar datos tabulares.
    
    Args:
        title: Título de la tabla
        data: Lista de diccionarios con los datos
        headers: Lista de encabezados de columnas
        render_functions: Diccionario con funciones personalizadas para renderizar columnas específicas
        show_counter: Si mostrar el contador de elementos
        counter_text: Texto del contador
        actions_column: Si incluir columna de acciones
        actions_menu: Componente de menú de acciones personalizado
    """
    
    # Función por defecto para renderizar celdas
    def default_cell_renderer(value: Any, key: str, row_data: Dict) -> rx.Component:
        if render_functions and key in render_functions:
            return render_functions[key](value, row_data)
        return rx.text(str(value))
    
    # Generar filas de la tabla
    def generate_table_rows():
        rows = []
        for row_data in data:
            cells = []
            
            # Obtener las claves de los datos para mapear con headers
            data_keys = list(row_data.keys())
            
            # Generar celdas para cada columna (excluyendo acciones si está habilitada)
            headers_to_process = headers[:-1] if actions_column else headers
            
            for i, header in enumerate(headers_to_process):
                # Extraer clave del header si es un diccionario
                if isinstance(header, dict):
                    key = header.get("key")
                    header_label = header.get("label", key)
                else:
                    # Intentar mapear el header con una clave de datos
                    key = None
                    header_label = header
                    if i < len(data_keys):
                        key = data_keys[i]
                    else:
                        # Buscar por nombre similar
                        header_lower = header.lower().replace(" ", "_").replace("ó", "o").replace("í", "i")
                        for data_key in data_keys:
                            if data_key.lower() == header_lower:
                                key = data_key
                                break
                
                value = row_data.get(key, "") if key else ""
                cell_content = default_cell_renderer(value, key or header_label, row_data)
                
                cells.append(
                    rx.table.cell(
                        cell_content,
                        padding="3",
                    )
                )
            
            # Agregar columna de acciones si está habilitada
            if actions_column:
                action_cell = actions_menu if actions_menu else default_actions_menu(row_data)
                cells.append(
                    rx.table.cell(
                        action_cell,
                        padding="3",
                    )
                )
            
            rows.append(
                rx.table.row(
                    *cells,
                    vertical_align="middle",
                )
            )
        
        return rows
    
    return rx.box(
        rx.vstack(
            # Header con título y contador
            rx.hstack(
                rx.text(
                    title, 
                    font_weight=FontWeight.BOLD.value, 
                    font_size=SizeText.LARGE.value, 
                    color="gray.800"
                ),
                rx.spacer(),
                rx.text(
                    f"{len(data)} de {len(data)} {counter_text}", 
                    color=ColorText.GRAY_500.value, 
                    font_size=SizeText.SMALL.value
                ) if show_counter else rx.fragment(),
                width="100%",
                mb="4",
            ),
            # Tabla
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        *[rx.table.column_header_cell(
                            header.get("label", header) if isinstance(header, dict) else header, 
                            font_weight=FontWeight.MEDIUM.value, 
                            text_align="left", 
                            padding="3"
                        ) for header in headers],
                        bg=Color.background_light.value,
                    ),
                ),
                rx.table.body(
                    *generate_table_rows(),
                ),
                width="100%",
                border_radius=BorderRadius.SMALL.value,
                border=CommonBorders.LIGHT_SOLID,
            ),
            width="100%",
            align_items="start",
        ),
        width="100%",
        bg="white",
        padding="1.5rem",
        border_radius=BorderRadius.SMALL.value,
        border=CommonBorders.LIGHT_SOLID,
        **kwargs
    )

def default_actions_menu(row_data: Dict) -> rx.Component:
    """Menú de acciones por defecto."""
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon(
                    tag="ellipsis-vertical", 
                    color=Color.icon_inactive.value, 
                    size=SizeIcon.MEDIUM.value
                ), 
                color="white", 
                bg="white"
            )
        ),
        rx.menu.content(
            rx.menu.item(
                rx.hstack(
                    rx.icon(tag="eye", color=Color.icon_inactive.value, size=SizeIcon.MEDIUM.value), 
                    rx.text("Ver"), 
                    spacing="2"
                )
            ),
            rx.menu.item(
                rx.hstack(
                    rx.icon(tag="pencil", color=Color.admin_icon.value, size=SizeIcon.MEDIUM.value), 
                    rx.text("Editar"), 
                    spacing="2"
                )
            ),
            rx.menu.separator(),
            rx.menu.item(
                rx.hstack(
                    rx.icon(tag="trash-2", color=Color.delete_icon.value, size=SizeIcon.MEDIUM.value), 
                    rx.text("Eliminar"), 
                    spacing="2"
                ), 
                color=Color.delete_text.value
            ),
        ),
    )