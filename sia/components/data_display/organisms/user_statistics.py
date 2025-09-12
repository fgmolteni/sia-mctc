"""
Organismo de estadísticas de usuarios.
Componente que combina múltiples stat cards para mostrar métricas de usuarios.
"""
import reflex as rx
from sia.components.layout.cards import stat_card
from sia.styles.colors import Color
from sia.styles.sizes import SizeSpace
from sia.styles.fonts import FontWeight
from sia.styles.border import CommonBorders, BorderRadius


def user_statistics(stats_data: dict = None) -> rx.Component:
    """
    Organismo que muestra estadísticas de usuarios en tarjetas.
    
    Args:
        stats_data: Diccionario con estadísticas de usuarios
        
    Returns:
        rx.Component: Organismo de estadísticas
    """
    # Obtener datos del estado o usar valores por defecto
    from sia.pages.usuarios import UserState
    
    return rx.box(
        rx.vstack(
            # Header de estadísticas
            rx.hstack(
                rx.text(
                    "Estadísticas de Usuarios",
                    font_weight=FontWeight.BOLD.value,
                    font_size="1.2em",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Actualizar",
                    on_click=UserState.refresh_statistics,
                    variant="ghost",
                    size="2",
                    color_scheme="gray",
                ),
                width="100%",
                align="center",
            ),
            # Grid de estadísticas
            rx.grid(
                stat_card(
                    title="Total Usuarios",
                    value=UserState.user_statistics["total_usuarios"],
                    icon="users",
                    color_scheme="blue",
                ),
                stat_card(
                    title="Usuarios Activos",
                    value=UserState.user_statistics["activos"],
                    icon="user-check",
                    color_scheme="green",
                ),
                stat_card(
                    title="Administradores",
                    value=UserState.user_statistics["administradores"],
                    icon="shield",
                    color_scheme="purple",
                ),
                stat_card(
                    title="Supervisores",
                    value=UserState.user_statistics["supervisores"],
                    icon="user-cog",
                    color_scheme="orange",
                ),
                columns="4",
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