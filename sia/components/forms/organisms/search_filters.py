import reflex as rx

from sia.components.forms.selects import select_component
from sia.styles.border import CommonBorders
from sia.styles.colors import ColorText, Color
from sia.styles.fonts import FontWeight
from sia.styles.sizes import BorderRadius, SizeSpace, SizeText


def search_filters() -> rx.Component:
    """Componente de filtros de búsqueda mejorado."""
    # Importación tardía para evitar importación circular
    from sia.pages.usuarios import UserState
    
    return rx.box(
        rx.vstack(
            # Header de filtros
            rx.hstack(
                rx.text(
                    "Filtros de Búsqueda",
                    font_weight=FontWeight.BOLD.value,
                    font_size=SizeText.LARGE.value,
                    color=ColorText.GRAY_800.value,
                ),
                rx.spacer(),
                rx.button(
                    "Limpiar filtros",
                    on_click=UserState.clear_filters,
                    variant="ghost",
                    size="2",
                    color_scheme="gray",
                ),
                width="100%",
                align="center",
            ),
            # Controles de filtro
            rx.grid(
                # Campo de búsqueda
                rx.box(
                    rx.input(
                        placeholder="Buscar por nombre, email o área...",
                        width="100%",
                        border=CommonBorders.LIGHT_SOLID,
                        border_radius=BorderRadius.SMALL.value,
                        py=SizeSpace.SMALL.value,
                        px=SizeSpace.SMALL.value,
                        _focus={"border_color": Color.primary.value},
                        value=UserState.search_term,
                        on_change=UserState.set_search_term,
                    ),
                ),
                # Filtro de rol
                select_component(
                    options=[
                        "Todos los roles",
                        "Administrador",
                        "Supervisor",
                        "Usuario",
                    ],
                    value=UserState.role_filter,
                    placeholder="Todos los roles",
                    on_change=UserState.set_role_filter,
                ),
                # Filtro de estado
                select_component(
                    options=["Todos los estados", "Activo", "Inactivo"],
                    value=UserState.status_filter,
                    placeholder="Todos los estados",
                    on_change=UserState.set_status_filter,
                ),
                columns="3",
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