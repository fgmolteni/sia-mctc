"""
Template de sidebar que utiliza el organismo de navegación.
Mantiene compatibilidad con la implementación anterior.
"""
import reflex as rx
from sia.components.layout.organisms import sidebar_navigation


def sidebar_main() -> rx.Component:
    """
    Template principal del sidebar utilizando el organismo de navegación.
    Mantiene la misma interfaz que la implementación anterior para 
    compatibilidad con páginas existentes.
    
    Returns:
        rx.Component: Sidebar de navegación principal
    """
    return sidebar_navigation()