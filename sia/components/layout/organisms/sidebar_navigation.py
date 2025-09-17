"""
Organismo de navegación sidebar siguiendo principios de Atomic Design.
Combina átomos y moléculas del sistema para crear la navegación principal.
"""
import reflex as rx
from typing import List, Dict, Any
from sia.components.layout.sidebars import sidebar_header, sidebar_section, sidebar_item, sidebar_footer


# Configuración por defecto de la navegación principal
DEFAULT_NAVIGATION_CONFIG = [
    {
        "section": "Navegación Principal",
        "items": [
            {"text": "Inicio", "icon": "home", "href": "/"},
            {"text": "Anticipos", "icon": "dollar-sign", "href": "/anticipos"},
            {"text": "Agentes", "icon": "users", "href": "/agentes"},
            {"text": "Usuarios", "icon": "user", "href": "/users"},
        ]
    }
]


def sidebar_navigation_config() -> List[Dict[str, Any]]:
    """
    Retorna la configuración por defecto de navegación.
    Puede ser sobrescrita para diferentes páginas o contextos.
    
    Returns:
        List[Dict]: Configuración de secciones e ítems de navegación
    """
    return DEFAULT_NAVIGATION_CONFIG


def sidebar_navigation(
    navigation_config: List[Dict[str, Any]] = None,
    width: str = "250px",
    show_footer: bool = True,
) -> rx.Component:
    """
    Organismo principal de navegación sidebar.
    
    Combina moléculas y átomos existentes para crear la navegación completa:
    - sidebar_header(): Molécula del header con logo
    - sidebar_section(): Átomo de título de sección  
    - sidebar_item(): Átomo de ítem de navegación
    - sidebar_footer(): Molécula del footer con info de usuario
    
    Args:
        navigation_config: Configuración de navegación personalizada
        width: Ancho del sidebar (default: "250px")
        show_footer: Mostrar footer con info de usuario (default: True)
        
    Returns:
        rx.Component: Organismo completo de navegación sidebar
    """
    # Usar configuración por defecto si no se proporciona una
    if navigation_config is None:
        navigation_config = sidebar_navigation_config()
    
    # Construir contenido de navegación dinámicamente
    navigation_content = []
    
    for section in navigation_config:
        # Agregar título de sección si existe
        if "section" in section and section["section"]:
            navigation_content.append(
                sidebar_section(section["section"])
            )
        
        # Agregar ítems de la sección
        for item in section.get("items", []):
            navigation_content.append(
                sidebar_item(
                    text=item["text"],
                    icon=item["icon"], 
                    href=item["href"],
                    is_active=item.get("is_active", False)
                )
            )
    
    # Construir estructura completa del sidebar
    sidebar_content = [
        sidebar_header(),
        rx.vstack(
            *navigation_content,
            spacing="2",
            width="100%",
            padding="0 1rem",
        ),
        rx.spacer(),
    ]
    
    # Agregar footer si está habilitado
    if show_footer:
        sidebar_content.append(sidebar_footer())
    
    return rx.box(
        rx.vstack(
            *sidebar_content,
            height="100%",
        ),
        width=width,
        height="100vh",
        position="sticky",
        left="0",
        top="0",
        bg="white",
        border_right=f"1px solid {rx.color('gray', 4)}",
        flex_shrink="0",
    )


def sidebar_navigation_compact(
    navigation_config: List[Dict[str, Any]] = None,
) -> rx.Component:
    """
    Versión compacta del sidebar para pantallas pequeñas.
    
    Args:
        navigation_config: Configuración de navegación personalizada
        
    Returns:
        rx.Component: Sidebar compacto sin footer
    """
    return sidebar_navigation(
        navigation_config=navigation_config,
        width="60px",
        show_footer=False,
    )


def sidebar_navigation_custom(
    sections: List[Dict[str, Any]],
    width: str = "280px",
) -> rx.Component:
    """
    Sidebar con configuración completamente personalizada.
    
    Args:
        sections: Lista de secciones con configuración específica
        width: Ancho personalizado del sidebar
        
    Returns:
        rx.Component: Sidebar personalizado
    """
    return sidebar_navigation(
        navigation_config=sections,
        width=width,
        show_footer=True,
    )