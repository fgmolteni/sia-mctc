import reflex as rx
from sia.components.forms.selects._general import select_component
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace, SizeText, SizeIcon
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders, BorderRadius

from sia.components.forms.selects import select_component

class PermissionCardState(rx.State):
    """Estado para manejar las tarjetas de permisos"""
    
    def set_permission_level(self, card_id: str, level: str):
        """Actualizar el nivel de permiso para una tarjeta específica"""
        # Aquí puedes agregar lógica para guardar el estado
        pass

def permission_card(
    title: str,
    subtitle: str, 
    permission_level: str = "ver",
    card_id: str = "default",
    description: str = "Información adicional sobre este permiso"
    ) -> rx.Component:
    """
    Tarjeta de permisos con selector de estado y hover informativo.
    
    Args:
        title: Título principal de la tarjeta
        subtitle: Subtítulo descriptivo
        permission_level: Nivel de permiso actual ("no_acceso", "ver", "editar")
        card_id: ID único para la tarjeta
        description: Descripción que aparece en hover
    """
    
    # Opciones del selector
    permission_options = ["Sin Acceso", "Ver", "Editar"]
    permission_values = ["no_acceso", "ver", "editar"]
    
    # Colores basados en el nivel de permiso
    def get_permission_color(level: str) -> str:
        colors = {
            "no_acceso": "red",
            "ver": "blue", 
            "editar": "green"
        }
        return colors.get(level, "gray")
    
    return rx.card(
        rx.flex(
            # Contenido principal
            rx.vstack(
                # Título principal
                rx.hstack(
                    rx.heading(
                    title,
                    font_size=SizeText.LARGE.value,
                    font_weight=FontWeight.BOLD.value,
                    color=ColorText.GRAY_800.value,
                    ),
                    rx.icon("info", size=SizeIcon.MEDIUM.value),
                    align="center",
                    spacing="1",
                    margin_bottom="0.25rem",
                ),
                rx.hstack(
                # Subtítulo
                    rx.text(
                        subtitle,
                        font_size=SizeText.MEDIUM.value,
                        color=ColorText.GRAY_500.value,
                    ),
                    

                    align_items="center",
                    spacing="2",
                    flex_grow="1",
                ),
            ),
            # Selector de estado
            rx.box(
                select_component("Seleccionar nivel", permission_options),
                width="120px",
            ),
            direction="row",
            align_items="center",
            justify_content="space-between",
            width="100%",
        ),
        
        # Estilos de la tarjeta
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.LARGE.value,
        width="100%",
    )

def dashboard_permission_card() -> rx.Component:
    """Tarjeta específica para permisos de Dashboard"""
    return permission_card(
        title="Dashboard",
        subtitle="Ver Dashboard",
        permission_level="ver",
        card_id="dashboard",
        description="Acceso al panel principal con métricas y estadísticas del sistema. Incluye visualización de reportes y datos generales."
    )

def users_permission_card() -> rx.Component:
    """Tarjeta específica para permisos de Usuarios"""
    return permission_card(
        title="Gestión de Usuarios",
        subtitle="Administrar Usuarios",
        permission_level="editar",
        card_id="users",
        description="Crear, editar y eliminar usuarios del sistema. Gestionar roles y permisos de acceso."
    )

def reports_permission_card() -> rx.Component:
    """Tarjeta específica para permisos de Reportes"""
    return permission_card(
        title="Reportes",
        subtitle="Generar Reportes",
        permission_level="no_acceso",
        card_id="reports",
        description="Generar y descargar reportes de viáticos, gastos y estadísticas del sistema."
    )

def vehicles_permission_card() -> rx.Component:
    """Tarjeta específica para permisos de Vehículos"""
    return permission_card(
        title="Vehículos",
        subtitle="Gestionar Vehículos",
        permission_level="ver",
        card_id="vehicles",
        description="Visualizar y administrar la flota de vehículos disponibles para comisiones oficiales."
    )