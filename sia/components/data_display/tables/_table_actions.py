import reflex as rx
from typing import List, Dict, Any
from sia.styles.sizes import SizeIcon
from sia.styles.colors import Color

def table_actions_menu(
    actions: List[Dict[str, Any]],
    row_data: Dict = None
) -> rx.Component:
    """
    Componente para crear menús de acciones personalizados.
    
    Args:
        actions: Lista de diccionarios con las acciones
                Formato: [{
                    "label": "Texto",
                    "icon": "icon-name",
                    "color": "color",
                    "href": "url" (opcional),
                    "on_click": function (opcional),
                    "separator_after": bool (opcional)
                }]
        row_data: Datos de la fila para contexto
    """
    
    menu_items = []
    
    for action in actions:
        # Crear el contenido del item
        item_content = rx.hstack(
            rx.icon(
                tag=action.get("icon", "circle"),
                color=action.get("color", Color.icon_inactive.value),
                size=SizeIcon.MEDIUM.value
            ),
            rx.text(action["label"]),
            spacing="2"
        )
        
        # Crear el item del menú
        if action.get("href"):
            menu_item = rx.menu.item(
                rx.link(item_content, href=action["href"]),
                color=action.get("text_color")
            )
        else:
            menu_item = rx.menu.item(
                item_content,
                on_click=action.get("on_click"),
                color=action.get("text_color")
            )
        
        menu_items.append(menu_item)
        
        # Agregar separador si se especifica
        if action.get("separator_after", False):
            menu_items.append(rx.menu.separator())
    
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
        rx.menu.content(*menu_items),
    )