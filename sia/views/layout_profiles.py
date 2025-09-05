import reflex as rx
from typing import Dict, Optional
from sia.components.data_display.cards import (
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


class DynamicProfileState(rx.State):
    """Estado dinámico para manejar perfiles con datos reales de usuarios."""
    
    # Información del usuario
    user_name: str = ""
    user_email: str = ""
    user_role: str = ""
    user_area: str = ""
    user_status: str = ""
    last_login: str = ""
    user_dni: str = ""
    
    # Estado de carga
    is_loading: bool = False
    
    def load_user_data(self, user_id: Optional[int] = None):
        """Cargar datos del usuario desde la base de datos."""
        self.is_loading = True
        # TODO: Implementar carga real desde BD
        # Por ahora usamos datos de ejemplo
        if user_id:
            # Simulamos datos específicos del usuario
            self.user_name = f"Usuario {user_id}"
            self.user_email = f"usuario{user_id}@empresa.com"
        else:
            # Datos por defecto
            self.user_name = "Juan Pérez"
            self.user_email = "juan.perez@empresa.com"
        
        self.user_role = "Administrador"
        self.user_area = "Administración"
        self.user_status = "Activo"
        self.last_login = "15/1/2024"
        self.user_dni = "12345678"
        self.is_loading = False


def get_permissions_by_role(role: str) -> Dict[str, str]:
    """
    Devuelve los permisos apropiados según el rol del usuario.
    
    Args:
        role: Rol del usuario ('Admin', 'Supervisor', 'Usuario')
    
    Returns:
        Dict con los permisos y sus niveles ('no_acceso', 'ver', 'editar')
    """
    permissions_map = {
        "Admin": {
            "view_dashboard": "editar",
            "manage_anticipos": "editar",
            "view_reports": "editar",
            "manage_gastos": "editar",
            "manage_users": "editar",
            "manage_vehicles": "editar",
            "manage_agents": "editar",
            "view_analytics": "editar"
        },
        "Administrador": {  # Alias para Admin
            "view_dashboard": "editar",
            "manage_anticipos": "editar",
            "view_reports": "editar",
            "manage_gastos": "editar",
            "manage_users": "editar",
            "manage_vehicles": "editar",
            "manage_agents": "editar",
            "view_analytics": "editar"
        },
        "Supervisor": {
            "view_dashboard": "ver",
            "manage_anticipos": "editar",
            "view_reports": "ver",
            "manage_gastos": "editar",
            "manage_users": "ver",
            "manage_vehicles": "ver",
            "manage_agents": "ver",
            "view_analytics": "ver"
        },
        "Usuario": {
            "view_dashboard": "ver",
            "manage_anticipos": "ver",
            "view_reports": "no_acceso",
            "manage_gastos": "ver",
            "manage_users": "no_acceso",
            "manage_vehicles": "no_acceso",
            "manage_agents": "no_acceso",
            "view_analytics": "no_acceso"
        }
    }
    
    return permissions_map.get(role, permissions_map["Usuario"])

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


def dynamic_profile_header(state: DynamicProfileState) -> rx.Component:
    """Header dinámico del perfil que muestra información real del usuario."""
    
    def get_role_color(role: str) -> str:
        """Determina el color del badge según el rol."""
        role_colors = {
            "Administrador": "red",
            "Supervisor": "orange", 
            "Usuario": "blue"
        }
        return role_colors.get(role, "gray")
    
    def get_status_color(status: str) -> str:
        """Determina el color del badge según el estado."""
        status_colors = {
            "Activo": "green",
            "Inactivo": "red",
            "Suspendido": "orange"
        }
        return status_colors.get(status, "gray")
    
    return rx.flex(
        # Avatar grande
        rx.flex(
            avatar_circle(
                rx.cond(state.user_name != "", state.user_name, "Usuario"),
                size=SizeAvatar.LARGE.value
            ),
            border_radius=BorderRadius.ROUND.value,
            background=Color.secondary.value,
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        
        # Información del usuario dinámica
        rx.cond(
            state.is_loading,
            # Estado de carga
            rx.vstack(
                rx.skeleton(height="2rem", width="200px"),
                rx.hstack(
                    rx.skeleton(height="1.5rem", width="100px"),
                    rx.skeleton(height="1.5rem", width="80px"),
                    spacing="3",
                ),
                spacing="2",
                align="start",
            ),
            # Contenido normal
            rx.vstack(
                # Nombre del usuario dinámico
                rx.heading(
                    rx.cond(state.user_name != "", state.user_name, "Sin nombre"),
                    font_size=SizeText.X_LARGE.value,
                    font_weight=FontWeight.BOLD.value,
                    color=ColorText.GRAY_800.value,
                ),
                
                # Badges dinámicos
                rx.hstack(
                    # Badge Rol dinámico
                    rx.badge(
                        rx.cond(state.user_role != "", state.user_role, "Sin rol"),
                        color_scheme=rx.cond(
                            state.user_role == "Administrador", "red",
                            rx.cond(
                                state.user_role == "Supervisor", "orange",
                                rx.cond(state.user_role == "Usuario", "blue", "gray")
                            )
                        ),
                        variant="soft",
                        size="2",
                        padding="0.5rem 0.75rem",
                        border_radius=BorderRadius.FULL.value,
                    ),
                    
                    # Badge Estado dinámico
                    rx.badge(
                        rx.cond(state.user_status != "", state.user_status, "Inactivo"),
                        color_scheme=rx.cond(
                            state.user_status == "Activo", "green",
                            rx.cond(
                                state.user_status == "Inactivo", "red", 
                                rx.cond(state.user_status == "Suspendido", "orange", "gray")
                            )
                        ),
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
            )
        ),
        
        # Layout principal
        direction="row",
        align_items="center",
        spacing="6",
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
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


def dynamic_profile_card(state: DynamicProfileState) -> rx.Component:
    """Tarjeta de información de usuario dinámica que usa datos reales del estado."""
    return rx.card(
        rx.cond(
            state.is_loading,
            # Estado de carga
            rx.vstack(
                rx.spinner(size="3"),
                rx.text("Cargando información del usuario...", 
                       color=ColorText.GRAY_500.value, size="2"),
                spacing="3",
                align="center",
                padding=SizeSpace.LARGE.value,
            ),
            # Contenido normal
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
                            rx.text(
                                rx.cond(state.user_name != "", state.user_name, "Sin nombre"),
                                font_weight=FontWeight.MEDIUM.value, size="3"
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("DNI", color=ColorText.GRAY_500.value, size="2"),
                            rx.text(
                                rx.cond(state.user_dni != "", state.user_dni, "No especificado"),
                                font_weight=FontWeight.MEDIUM.value, size="3"
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Rol", color=ColorText.GRAY_500.value, size="2"),
                            rx.text(
                                rx.cond(state.user_role != "", state.user_role, "Sin rol asignado"),
                                font_weight=FontWeight.MEDIUM.value, size="3"
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Estado", color=ColorText.GRAY_500.value, size="2"),
                            rx.badge(
                                rx.cond(state.user_status != "", state.user_status, "Inactivo"),
                                color_scheme=rx.cond(
                                    state.user_status == "Activo", "green",
                                    rx.cond(state.user_status == "Inactivo", "red", "gray")
                                ),
                                variant="soft",
                                size="1"
                            ),
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
                                rx.text(
                                    rx.cond(state.user_email != "", state.user_email, "Sin email"),
                                    font_weight=FontWeight.MEDIUM.value, size="3"
                                ),
                                spacing="2",
                                align="center",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Área", color=ColorText.GRAY_500.value, size="2"),
                            rx.text(
                                rx.cond(state.user_area != "", state.user_area, "Sin área asignada"),
                                font_weight=FontWeight.MEDIUM.value, size="3"
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Último acceso", color=ColorText.GRAY_500.value, size="2"),
                            rx.hstack(
                                rx.icon(tag="calendar", size=SizeIcon.SMALL.value, color=ColorText.GRAY_500.value),
                                rx.text(
                                    rx.cond(state.last_login != "", state.last_login, "Nunca"),
                                    font_weight=FontWeight.MEDIUM.value, size="3"
                                ),
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
            )
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


def dynamic_permission_card(
    title: str,
    subtitle: str,
    permission_level: str,
    description: str = "Información adicional sobre este permiso"
) -> rx.Component:
    """
    Tarjeta de permisos dinámica que muestra el nivel basado en el rol del usuario.
    
    Args:
        title: Título principal de la tarjeta
        subtitle: Subtítulo descriptivo
        permission_level: Nivel de permiso ("no_acceso", "ver", "editar")
        description: Descripción del permiso
    """
    
    # Función para obtener color según el nivel
    def get_permission_color(level: str) -> str:
        colors = {
            "no_acceso": "red",
            "ver": "blue", 
            "editar": "green"
        }
        return colors.get(level, "gray")
    
    # Función para obtener texto del nivel
    def get_permission_text(level: str) -> str:
        texts = {
            "no_acceso": "Sin Acceso",
            "ver": "Solo Ver",
            "editar": "Editar"
        }
        return texts.get(level, "Sin Definir")
    
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
                    rx.icon("info", size=SizeIcon.MEDIUM.value, color=ColorText.GRAY_400.value),
                    align="center",
                    spacing="1",
                    margin_bottom="0.25rem",
                ),
                # Subtítulo
                rx.text(
                    subtitle,
                    font_size=SizeText.MEDIUM.value,
                    color=ColorText.GRAY_500.value,
                ),
                align="start",
                spacing="1",
            ),
            # Badge de nivel de permiso
            rx.badge(
                get_permission_text(permission_level),
                color_scheme=get_permission_color(permission_level),
                variant="soft",
                size="2",
                padding="0.5rem 0.75rem",
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


def dynamic_permissions_section(state: DynamicProfileState) -> rx.Component:
    """Sección de permisos dinámica que usa los permisos basados en el rol del usuario."""
    
    return rx.vstack(
        # Título de la sección
        rx.heading(
            "Permisos y Accesos",
            font_size=SizeText.LARGE.value,
            font_weight=FontWeight.BOLD.value,
            color=ColorText.GRAY_800.value,
            margin_bottom=SizeSpace.MEDIUM.value,
        ),
        
        # Indicador de estado de carga
        rx.cond(
            state.is_loading,
            rx.vstack(
                rx.spinner(size="2"),
                rx.text("Cargando permisos...", color=ColorText.GRAY_500.value, size="2"),
                spacing="2",
                align="center",
                padding=SizeSpace.MEDIUM.value,
            ),
            # Grid de tarjetas de permisos dinámicas
            rx.vstack(
                # Información del rol
                rx.hstack(
                    rx.icon("shield-check", size=SizeIcon.SMALL.value, color=ColorText.GRAY_500.value),
                    rx.text(
                        rx.cond(
                            state.user_role != "",
                            f"Permisos para rol: {state.user_role}",
                            "Rol no definido - usando permisos mínimos"
                        ),
                        color=ColorText.GRAY_600.value,
                        size="2",
                        font_weight=FontWeight.MEDIUM.value
                    ),
                    spacing="2",
                    align="center",
                    margin_bottom=SizeSpace.MEDIUM.value,
                ),
                
                # Tarjetas de permisos
                rx.grid(
                    # Dashboard
                    dynamic_permission_card(
                        title="Dashboard",
                        subtitle="Ver panel principal",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "ver", "ver")
                        ),
                        description="Acceso al panel principal con métricas y estadísticas"
                    ),
                    
                    # Usuarios
                    dynamic_permission_card(
                        title="Gestión de Usuarios",
                        subtitle="Administrar usuarios",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "ver", "no_acceso")
                        ),
                        description="Crear, editar y eliminar usuarios del sistema"
                    ),
                    
                    # Reportes
                    dynamic_permission_card(
                        title="Reportes",
                        subtitle="Generar reportes",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "ver", "no_acceso")
                        ),
                        description="Generar y descargar reportes de viáticos y gastos"
                    ),
                    
                    # Vehículos
                    dynamic_permission_card(
                        title="Vehículos",
                        subtitle="Gestionar vehículos",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "ver", "no_acceso")
                        ),
                        description="Visualizar y administrar flota de vehículos"
                    ),
                    
                    # Agentes
                    dynamic_permission_card(
                        title="Agentes",
                        subtitle="Gestionar agentes",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "ver", "no_acceso")
                        ),
                        description="Administrar agentes del ministerio"
                    ),
                    
                    # Gastos
                    dynamic_permission_card(
                        title="Gestión de Gastos",
                        subtitle="Administrar gastos",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "editar", "ver")
                        ),
                        description="Gestionar gastos y liquidaciones de viáticos"
                    ),
                    
                    # Analytics
                    dynamic_permission_card(
                        title="Análisis",
                        subtitle="Ver estadísticas",
                        permission_level=rx.cond(
                            state.user_role == "Administrador", "editar",
                            rx.cond(state.user_role == "Supervisor", "ver", "no_acceso")
                        ),
                        description="Acceso a análisis y estadísticas avanzadas"
                    ),
                    
                    columns="1",
                    spacing="3",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            )
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


def dynamic_permission_views(state: DynamicProfileState) -> rx.Component:
    """Vista de perfiles dinámicos que usa los componentes con datos reales."""
    return rx.box(
        rx.vstack(
            # Contenido principal con componentes dinámicos
            rx.box(
                rx.vstack(
                    # Header dinámico del perfil
                    dynamic_profile_header(state),
                    # Tarjeta de información dinámica
                    dynamic_profile_card(state),
                    # Sección de permisos dinámica
                    dynamic_permissions_section(state),
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
        # Cargar datos al inicializar
        on_load=state.load_user_data
    )

