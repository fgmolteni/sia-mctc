import reflex as rx

from sia.components.layout.headers import page_header, new_user_button
from sia.views.sidebar import sidebar_main
from sia.components.forms.modals import user_modal
from sia.components.feedback.toasts import toast_container
from sia.styles.colors import Color
from sia.styles.sizes import SizeSpace


def user_management_template(
    statistics_component,
    filters_component, 
    table_component,
    notifications_component
) -> rx.Component:
    """
    Template para páginas de gestión de usuarios.
    
    Args:
        statistics_component: Componente de estadísticas 
        filters_component: Componente de filtros
        table_component: Componente de tabla
        notifications_component: Componente de notificaciones
    """
    # Importación tardía para evitar importación circular
    from sia.pages.usuarios import UserState
    
    return rx.box(
        rx.hstack(
            # Sidebar
            sidebar_main(),
            # Contenido principal
            rx.box(
                rx.vstack(
                    # Header de la página
                    rx.box(
                        page_header(
                            title="Gestión de Usuarios",
                            subtitle="Administra usuarios, roles y permisos del sistema SIA",
                            action_button=new_user_button(),
                        ),
                        width="100%",
                        padding_x=SizeSpace.LARGE.value,
                        padding_y=SizeSpace.MEDIUM.value,
                        border_bottom=f"1px solid {Color.border_light.value}",
                        bg="white",
                    ),
                    # Contenido principal con scroll
                    rx.box(
                        rx.vstack(
                            # Mensajes de notificación
                            notifications_component(),
                            # Estadísticas de usuarios
                            statistics_component(),
                            # Filtros de búsqueda
                            filters_component(),
                            # Tabla de usuarios
                            table_component(),
                            spacing="2",
                            width="100%",
                            max_width="1400px",
                            margin="0 auto",
                        ),
                        padding=SizeSpace.LARGE.value,
                        width="100%",
                        flex="1",
                        overflow_y="auto",
                    ),
                    spacing="0",
                    width="100%",
                    height="100vh",
                ),
                width="100%",
                bg=Color.background.value,
                flex="1",
            ),
            width="100%",
            height="100vh",
            overflow="hidden",
            align="start",
            spacing="0",
        ),
        # Modal de usuario
        user_modal(),
        # Contenedor de toasts
        toast_container(),
        width="100%",
        height="100vh",
        on_mount=UserState.on_load,
    )