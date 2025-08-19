import reflex as rx
from sia.components.forms.selects._general import select_component
from sia.components.data_display.cards import (
    card_profile, 
    info_card_profile,
    dashboard_permission_card,
    users_permission_card,
    reports_permission_card,
    vehicles_permission_card
)
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeAvatar, SizeSpace, SizeIcon, SizeText, SizeGeneral
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders, BorderRadius
from sia.components.data_display.avatars import avatar_circle
from sia.components.layout.headers import page_header, header_profiles

class ProfileState(rx.State):
    """Estado para manejar la página de perfiles."""
    current_tab: str = "general"
    
    # Modal de permisos
    show_permissions_modal: bool = False
    
    # Estados de permisos con niveles: no_acceso, ver, editar
    permission_view_dashboard: str = "ver"
    permission_manage_anticipos: str = "editar"
    permission_view_reports: str = "no_acceso"
    permission_manage_gastos: str = "editar"
    permission_manage_users: str = "no_acceso"
    permission_manage_vehicles: str = "no_acceso"
    permission_manage_agents: str = "no_acceso"
    permission_view_analytics: str = "ver"
    
    def set_tab(self, tab: str):
        """Cambiar la pestaña activa."""
        self.current_tab = tab
    
    def open_permissions_modal(self):
        """Abrir modal de permisos."""
        self.show_permissions_modal = True
    
    def close_permissions_modal(self):
        """Cerrar modal de permisos."""
        self.show_permissions_modal = False
    
    def set_permission_view_dashboard(self, value: str):
        self.permission_view_dashboard = value
    
    def set_permission_manage_anticipos(self, value: str):
        self.permission_manage_anticipos = value
    
    def set_permission_view_reports(self, value: str):
        self.permission_view_reports = value
    
    def set_permission_manage_gastos(self, value: str):
        self.permission_manage_gastos = value
    
    def set_permission_manage_users(self, value: str):
        self.permission_manage_users = value
    
    def set_permission_manage_vehicles(self, value: str):
        self.permission_manage_vehicles = value
    
    def set_permission_manage_agents(self, value: str):
        self.permission_manage_agents = value
    
    def set_permission_view_analytics(self, value: str):
        self.permission_view_analytics = value

def profile_header() -> rx.Component:
    """Header del perfil con avatar, nombre y badges - diseño horizontal elegante."""
    return rx.flex(
        # Avatar grande
        rx.flex(
            avatar_circle("Juan Perez", size=SizeAvatar.LARGE.value),
            #width="80px",
            #height="80px",
            border_radius=BorderRadius.ROUND.value,
            background=Color.secondary.value,
            align_items="center",
            justify_content="center",
            flex_shrink="0",  # No se encoja
        ),
        
        # Información del usuario
        rx.vstack(
            # Nombre del usuario
            rx.heading(
                "Juan Pérez",
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=ColorText.GRAY_800.value,
                #margin_bottom=SizeSpace.MEDIUM.value,
            ),
            
            # Badges horizontales
            rx.hstack(
                # Badge Administrador (rojo)
                rx.badge(
                    "Administrador",
                    color_scheme="red",
                    variant="soft",
                    size="2",
                    padding="0.5rem 0.75rem",
                    border_radius=BorderRadius.FULL.value,
                ),
                
                # Badge Activo (verde)
                rx.badge(
                    "Activo",
                    color_scheme="green", 
                    variant="soft",
                    size="2",
                    padding="0.5rem 0.75rem",
                    border_radius=BorderRadius.FULL.value,
                ),
                spacing="3",
                align="center",
            ),
            align_items="start",
            spacing="1",
            flex_grow="1",
        ),
        
        # Layout principal
        direction="row",
        align_items="center",
        spacing="6",
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        #margin_bottom=SizeSpace.LARGE.value,
        width="100%",
        max_width="800px",
    )

def user_info_card() -> rx.Component:
    """Tarjeta de información de usuario."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("user", size=SizeIcon.MEDIUM.value, color=ColorText.GRAY_500.value),
                rx.heading("Información General", size="4", font_weight=FontWeight.MEDIUM.value),
                spacing="2",
                align="center",
                margin_bottom=SizeSpace.LARGE.value,
            ),
            rx.grid(
                # Columna izquierda
                rx.vstack(
                    rx.vstack(
                        rx.text("Nombre completo", color=ColorText.GRAY_500.value, size="2"),
                        rx.text("Juan Pérez", font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Rol", color=ColorText.GRAY_500.value, size="2"),
                        rx.text("Administrador", font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Estado", color=ColorText.GRAY_500.value, size="2"),
                        rx.text("Activo", font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    spacing="4",
                    align="start",
                ),
                # Columna derecha
                rx.vstack(
                    rx.vstack(
                        rx.text("Email", color=ColorText.GRAY_500.value, size="2"),
                        rx.hstack(
                            rx.icon(tag="mail", size=SizeIcon.SMALL.value, color=ColorText.GRAY_500.value),
                            rx.text("juan.perez@empresa.com", font_weight=FontWeight.MEDIUM.value, size="3"),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Área", color=ColorText.GRAY_500.value, size="2"),
                        rx.text("Administración", font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Último acceso", color=ColorText.GRAY_500.value, size="2"),
                        rx.hstack(
                            rx.icon(tag="calendar", size=SizeIcon.SMALL.value, color=ColorText.GRAY_500.value),
                            rx.text("15/1/2024", font_weight=FontWeight.MEDIUM.value, size="3"),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    spacing="4",
                    align="start",
                ),
                columns="2",
                spacing="8",
                width=SizeGeneral.FULL.value,
            ),
            spacing="3",
            align="start",
            width=SizeGeneral.FULL.value,
        ),
        
        # Estilos de la tarjeta
        padding=SizeSpace.LARGE.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        background=Color.background.value,
        width=SizeGeneral.FULL.value,
        max_width="800px"
    )

def permissions_section() -> rx.Component:
    """Sección de permisos con las nuevas tarjetas de permisos"""
    return rx.vstack(
        # Título de la sección
        rx.heading(
            "Permisos y Accesos",
            font_size=SizeText.LARGE.value,
            font_weight=FontWeight.BOLD.value,
            color=ColorText.GRAY_800.value,
            margin_bottom=SizeSpace.MEDIUM.value,
        ),
        
        # Grid de tarjetas de permisos
        rx.grid(
            dashboard_permission_card(),
            users_permission_card(),
            reports_permission_card(),
            vehicles_permission_card(),
            columns="1",
            spacing="3",
            width="100%",
        ),
        
        # Propiedades del contenedor principal
        spacing="4",
        align_items="start",
        width="100%",
        max_width="800px",
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        margin_bottom=SizeSpace.LARGE.value,
    )

def header_profiles() -> rx.Component:
    return rx.box(
        page_header(
            title="Perfil de Usuario",
            subtitle="Gestiona información personal, permisos y configuraciones del perfil",
        ),
        width="100%",
        padding=f"{SizeSpace.MEDIUM.value} {SizeSpace.LARGE.value} 0 {SizeSpace.LARGE.value}",
    )

def permission_views() -> rx.Component:
    return rx.box(
                rx.vstack(
                    # Contenido principal
                    rx.box(
                        rx.vstack(
                            # Header del perfil
                            profile_header(),
                            # Cartas separadas verticalmente
                            user_info_card(),
                            # Nueva sección de permisos
                            permissions_section(),
                            spacing="3",
                            width="100%"
                        ),
                        padding=f"{SizeSpace.MEDIUM.value} {SizeSpace.LARGE.value}",
                        width="100%",
                    ),
                    
                    spacing="0",
                    width="100%",
                ),
                width="100%",
                height="100vh",
                overflow_y="auto",
                flex="1",
            )

