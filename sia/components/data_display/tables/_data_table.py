import reflex as rx
from typing import List, Dict, Any, Optional, Callable, Union
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText, BorderRadius, SizeIcon
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders

def _get_counter_text(data: Union[List[Dict[str, Any]], rx.Var[List[Dict[str, Any]]]], counter_text: str) -> str:
    """Función auxiliar para obtener el texto del contador."""
    # Si data es una lista de Python normal
    if isinstance(data, list):
        count = len(data)
        return f"{count} de {count} {counter_text}"
    # Si data es una variable Reflex, usar el método length()
    else:
        return rx.cond(
            data,
            f"{data.length()} de {data.length()} {counter_text}",
            f"0 de 0 {counter_text}"
        )

def _render_python_list_row(row_data: Dict[str, Any], headers: List[str], render_functions: Dict[str, Callable], actions_column: bool, actions_menu: Optional[rx.Component]) -> rx.Component:
    """Renderiza una fila individual de una lista de Python normal."""
    
    # Mapeo de headers en español a claves en inglés
    header_mapping = {
        "Usuario": "name",
        "Correo": "email", 
        "Email": "email",
        "Rol": "role",
        "Área": "area",
        "Area": "area",
        "Estado": "status",
        "Permisos": "permissions",
        "Atributos": "attributes",
        "Acciones": "actions"
    }
    
    # Generar celdas para todas las columnas (excluyendo acciones si está habilitada)
    headers_to_process = headers[:-1] if actions_column else headers
    cells = []
    
    # Procesar cada header y crear su celda correspondiente
    for header in headers_to_process:
        # Obtener la clave para el header
        if isinstance(header, dict):
            key = header.get("key", header.get("label", "").lower())
        else:
            key = header_mapping.get(header, header.lower().replace(" ", "_").replace("ó", "o").replace("í", "i"))
        
        # Aplicar función de renderizado personalizada si existe
        if render_functions and key in render_functions:
            # Para listas Python, pasar directamente el valor
            cell_content = render_functions[key](row_data.get(key, ""), row_data)
        else:
            # Renderizado por defecto
            cell_content = rx.text(str(row_data.get(key, "")))
        
        cells.append(
            rx.table.cell(
                cell_content,
                padding="3",
            )
        )
    
    # Agregar columna de acciones si está habilitada
    if actions_column:
        if render_functions and "actions" in render_functions:
            action_cell = render_functions["actions"]("", row_data)
        elif actions_menu:
            action_cell = actions_menu
        else:
            action_cell = default_actions_menu(row_data)
        
        cells.append(
            rx.table.cell(
                action_cell,
                padding="3",
            )
        )
    
    return rx.table.row(
        *cells,
        vertical_align="middle",
    )

def _render_table_body(data: Union[List[Dict[str, Any]], rx.Var[List[Dict[str, Any]]]], render_func: Callable, headers: List[str], render_functions: Dict[str, Callable], actions_column: bool, actions_menu: Optional[rx.Component]) -> rx.Component:
    """Función auxiliar para renderizar el cuerpo de la tabla."""
    # Si data es una lista de Python normal, renderizar directamente
    if isinstance(data, list):
        return rx.fragment(
            *[_render_python_list_row(row, headers, render_functions, actions_column, actions_menu) for row in data]
        )
    # Si data es una variable Reflex, usar rx.foreach
    else:
        return rx.foreach(data, render_func)

def data_table(
    title: str,
    data: Union[List[Dict[str, Any]], rx.Var[List[Dict[str, Any]]]],
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
        data: Lista de diccionarios con los datos (puede ser List o rx.Var)
        headers: Lista de encabezados de columnas
        render_functions: Diccionario con funciones personalizadas para renderizar columnas específicas
        show_counter: Si mostrar el contador de elementos
        counter_text: Texto del contador
        actions_column: Si incluir columna de acciones
        actions_menu: Componente de menú de acciones personalizado
    """
    
    # Mapeo de headers en español a claves en inglés (como diccionario estático)
    header_mapping = {
        "Usuario": "name",
        "Correo": "email", 
        "Email": "email",
        "Rol": "role",
        "Área": "area",
        "Area": "area",
        "Estado": "status",
        "Permisos": "permissions",
        "Atributos": "attributes",
        "Acciones": "actions"
    }
    
    # Función para renderizar una fila individual (usada en rx.foreach)
    def render_table_row(row_data: rx.Var[Dict[str, Any]]) -> rx.Component:
        """Renderiza una fila individual de la tabla usando rx.foreach."""
        
        # Generar celdas para todas las columnas (excluyendo acciones si está habilitada)
        headers_to_process = headers[:-1] if actions_column else headers
        cells = []
        
        # Procesar cada header y crear su celda correspondiente
        for i, header in enumerate(headers_to_process):
            # Obtener la clave para el header
            key = header_mapping.get(header, header.lower().replace(" ", "_").replace("ó", "o").replace("í", "i"))
            
            # Aplicar función de renderizado personalizada si existe
            if render_functions and key in render_functions:
                # Las render functions deben manejar rx.Var internamente
                cell_content = render_functions[key](row_data[key], row_data)
            else:
                # Renderizado por defecto - manejo seguro de valores None/empty
                cell_content = rx.text(
                    rx.cond(
                        row_data[key],
                        row_data[key].to(str),
                        ""
                    )
                )
            
            cells.append(
                rx.table.cell(
                    cell_content,
                    padding="3",
                )
            )
        
        # Agregar columna de acciones si está habilitada
        if actions_column:
            # Para las funciones de render de acciones, pasar row_data directamente
            if render_functions and "actions" in render_functions:
                action_cell = render_functions["actions"]("", row_data)
            elif actions_menu:
                action_cell = actions_menu
            else:
                action_cell = default_actions_menu(row_data)
            
            cells.append(
                rx.table.cell(
                    action_cell,
                    padding="3",
                )
            )
        
        return rx.table.row(
            *cells,
            vertical_align="middle",
        )
    
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
                rx.cond(
                    show_counter,
                    rx.text(
                        _get_counter_text(data, counter_text),
                        color=ColorText.GRAY_500.value, 
                        font_size=SizeText.SMALL.value
                    ),
                ),
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
                    _render_table_body(data, render_table_row, headers, render_functions, actions_column, actions_menu),
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

def default_actions_menu(row_data: Union[Dict, rx.Var[Dict[str, Any]]]) -> rx.Component:
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