import reflex as rx
from sia.views.sidebar import sidebar_main
from sia.components.header import header_profiles
from sia.components.cards import card_profile, info_card_profile
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace, SizeIcon, SizeText
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders, BorderRadius
from sia.components.avartar import avatar_circle

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
    """Header del perfil con avatar, nombre y badges."""
    return rx.flex(
        # Información del usuario
        rx.flex(
            rx.vstack(
                avatar_circle("Juan Perez"),
                rx.heading(
                    "Juan Pérez",
                    font_size=SizeText.LARGE.value,
                    margin_left=SizeSpace.MEDIUM.value,
                ),
                rx.hstack(
                    rx.text(
                    "Administrador",
                    font_size=SizeText.MEDIUM.value,
                    color="gray",
                    width="60px", 
                    min_margin_top="0.75rem",
                    margin_bottom="1rem",
                    ),
                    rx.badge(
                        rx.icon(tag="shield"),
                        rx.text("Administrador"),
                        color_scheme="red",
                        size="1",
                        variant="soft",
                        padding="0.5em 0.75em",
                    ),
                ),
                align_items="center",
                gap="2",
            ),
        ),
            
        rx.flex(
            rx.badge(
                "Administrador",
                color=ColorText.PRIMARY.value,
                bg=Color.admin_bg.value,
                px="2",
                py="1",
                border_radius=BorderRadius.DEFAULT.value,
                font_weight=FontWeight.MEDIUM.value,
            ),
            gap="3",
            margin_top="0.5rem",
        ),
        # Botones de acción alineados
        rx.flex(
            rx.button(
                rx.icon("pencil"),
                "Editar Perfil",
                variant="outline",
                size="3",
                _hover={"background_color": "gray.50"},
            ),
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.icon(tag="settings"),
                        "Configurar",
                        variant="solid",
                        size="3",
                        _hover={"background_color": "blue.600"},
                    ),
                ),
                rx.menu.content(
                    rx.menu.item(
                        rx.icon(tag="user"),
                        "Ver Perfil Completo",
                        gap="2",
                    ),
                    rx.menu.item(
                        rx.icon(tag="key"),
                        "Cambiar Contraseña",
                        gap="2",
                    ),
                    rx.menu.separator(),
                    rx.menu.item(
                        rx.icon(tag="trash"),
                        "Eliminar Cuenta",
                        color="red",
                        gap="2",
                    ),
                ),
            ),
            direction="row",
            align_items="center",
            justify_content="flex-end",
            gap="3",
        ),
        direction="row",
        align_items="center",
        gap="4",
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border_radius=BorderRadius.MEDIUM.value,
        border=CommonBorders.LIGHT_SOLID,
        margin_bottom=SizeSpace.LARGE.value,
    )

def general_tab_content() -> rx.Component:
    """Contenido de la pestaña General."""
    return rx.vstack(
        rx.hstack(
            rx.icon("user", size=20),
            rx.heading("Información General", size="4", font_weight="medium"),
            spacing="2",
            align="center",
        ),
        rx.grid(
            # Columna izquierda
            rx.vstack(
                rx.vstack(
                    rx.text("Nombre completo", color="gray.500", size="2"),
                    rx.text("Juan Pérez", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Rol", color="gray.500", size="2"),
                    rx.text("Administrador", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Estado", color="gray.500", size="2"),
                    rx.text("Activo", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                spacing="6",
                align="start",
            ),
            # Columna derecha
            rx.vstack(
                rx.vstack(
                    rx.text("Email", color="gray.500", size="2"),
                    rx.hstack(
                    rx.icon(tag="mail"),
                    rx.text("juan.perez@empresa.com", font_weight="medium", size="3"),
                    spacing="2",
                ),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Área", color="gray.500", size="2"),
                    rx.text("Administración", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Último acceso", color="gray.500", size="2"),
                    rx.hstack(
                    rx.icon(tag="calendar"),
                    rx.text("15/1/2024", font_weight="medium", size="3"),
                    spacing="2",
                ),
                    align="start",
                    spacing="1",
                ),
                spacing="6",
                align="start",
            ),
            columns="2",
            spacing="8",
            width="100%",
        ),
        spacing="6",
        align="start",
        width="100%",
    )

def permissions_tab_content() -> rx.Component:
    """Contenido de la pestaña Permisos."""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="shield"),
            rx.heading("Permisos del Usuario", size="4", font_weight="medium"),
            rx.spacer(),
            rx.button(
                rx.icon(tag="pencil", color="gray.400"),
                "Gestionar Permisos",
                variant="solid",
                color_scheme="blue",
                size="3",
                gap="2",
                on_click=ProfileState.open_permissions_modal,
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.cond(
            ProfileState.show_permissions_modal,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="settings"),
                        rx.heading("Editar niveles de acceso", size="4", font_weight="medium"),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x"),
                            "Cerrar",
                            variant="ghost",
                            on_click=ProfileState.close_permissions_modal,
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Ver Dashboard", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_view_dashboard,
                                on_change=ProfileState.set_permission_view_dashboard,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Gestionar Anticipos", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_manage_anticipos,
                                on_change=ProfileState.set_permission_manage_anticipos,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Ver Reportes", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_view_reports,
                                on_change=ProfileState.set_permission_view_reports,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Gestionar Gastos", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_manage_gastos,
                                on_change=ProfileState.set_permission_manage_gastos,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Gestionar Usuarios", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_manage_users,
                                on_change=ProfileState.set_permission_manage_users,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Gestionar Vehículos", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_manage_vehicles,
                                on_change=ProfileState.set_permission_manage_vehicles,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Gestionar Agentes", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_manage_agents,
                                on_change=ProfileState.set_permission_manage_agents,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Ver Analítica", color="gray.500", size="2"),
                            rx.select(
                                ["no_acceso", "ver", "editar"],
                                value=ProfileState.permission_view_analytics,
                                on_change=ProfileState.set_permission_view_analytics,
                            ),
                            align="start",
                            spacing="2",
                        ),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button("Guardar", variant="solid", color_scheme="blue", on_click=ProfileState.close_permissions_modal),
                        rx.button("Cancelar", variant="soft", on_click=ProfileState.close_permissions_modal),
                        justify="end",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                position="fixed",
                top="10%",
                left="50%",
                transform="translateX(-50%)",
                z_index="9999",
                background=Color.background.value,
                border=CommonBorders.LIGHT_SOLID,
                border_radius=BorderRadius.MEDIUM.value,
                box_shadow="0 10px 25px rgba(0,0,0,0.15)",
                padding=SizeSpace.LARGE.value,
                width="min(800px, 90vw)",
            ),
        ),
        rx.grid(
            info_card_profile(
                title="Ver Dashboard",
                icon="layout-dashboard",
                content=rx.text(
                    ProfileState.permission_view_dashboard,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Gestionar Anticipos",
                icon="folder-cog",
                content=rx.text(
                    ProfileState.permission_manage_anticipos,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Ver Reportes",
                icon="file-bar-chart",
                content=rx.text(
                    ProfileState.permission_view_reports,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Gestionar Gastos",
                icon="wallet",
                content=rx.text(
                    ProfileState.permission_manage_gastos,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Gestionar Usuarios",
                icon="users",
                content=rx.text(
                    ProfileState.permission_manage_users,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Gestionar Vehículos",
                icon="car",
                content=rx.text(
                    ProfileState.permission_manage_vehicles,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Gestionar Agentes",
                icon="users-2",
                content=rx.text(
                    ProfileState.permission_manage_agents,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            info_card_profile(
                title="Ver Analítica",
                icon="bar-chart-3",
                content=rx.text(
                    ProfileState.permission_view_analytics,
                    color="gray.600",
                    size="3",
                ),
                show_header=True,
                show_footer=False,
            ),
            columns="3",
            spacing="4",
            width="100%",
        ),
        spacing="6",
        align="start",
        width="100%",
    )

def attributes_tab_content() -> rx.Component:
    """Contenido de la pestaña Atributos."""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="settings"),
            rx.heading("Atributos ABAC", size="4", font_weight="medium"),
            rx.spacer(),
            rx.button(
                rx.icon(tag="pencil", color="gray.400"),
                "Gestionar Atributos",
                variant="solid",
                color_scheme="blue",
                size="3",
                gap="2",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.grid(
            # Columna izquierda
            rx.vstack(
                rx.vstack(
                    rx.text("Department", color="gray.500", size="2"),
                    rx.text("Administración", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Location", color="gray.500", size="2"),
                    rx.text("oficina central", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Cost Center", color="gray.500", size="2"),
                    rx.text("ADM001", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                spacing="6",
                align="start",
            ),
            # Columna derecha
            rx.vstack(
                rx.vstack(
                    rx.text("Level", color="gray.500", size="2"),
                    rx.text("senior", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Clearance Level", color="gray.500", size="2"),
                    rx.text("high", font_weight="medium", size="3"),
                    align="start",
                    spacing="1",
                ),
                spacing="6",
                align="start",
            ),
            columns="2",
            spacing="8",
            width="100%",
        ),
        spacing="6",
        align="start",
        width="100%",
    )

def activity_tab_content() -> rx.Component:
    """Contenido de la pestaña Actividad."""
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="calendar"),
            rx.heading("Actividad Reciente", size="4", font_weight="medium"),
            spacing="2",
            align="center",
        ),
        rx.vstack(
            rx.vstack(
                rx.text("Último inicio de sesión", color="gray.500", size="2"),
                rx.text("15/1/2024, 7:30:00", font_weight="medium", size="3"),
                align="start",
                spacing="1",
            ),
            rx.vstack(
                rx.text("Cuenta creada", color="gray.500", size="2"),
                rx.text("Información no disponible", font_weight="medium", size="3"),
                align="start",
                spacing="1",
            ),
            rx.vstack(
                rx.text("Última modificación", color="gray.500", size="2"),
                rx.text("Información no disponible", font_weight="medium", size="3"),
                align="start",
                spacing="1",
            ),
            spacing="6",
            align="start",
            width="100%",
        ),
        spacing="6",
        align="start",
        width="100%",
    )

def profiles_page() -> rx.Component:
    """Página principal de perfiles con sistema de tabs."""
    return rx.box(
        rx.hstack(
            sidebar_main(),
            rx.box(
                rx.vstack(
                    # Barra de botones superior con iconos nativos de Reflex
                    card_profile("Nombre", "Juan Pérez", "JP"),
                    rx.flex(
                        rx.button(
                            rx.icon(tag="arrow-left", size=SizeIcon.MEDIUM.value),
                            "Volver",
                            #variant="ghost",
                            background=Color.background_light.value,
                            #color=ColorText.primary.value,
                            #border_radius=BorderRadius.SMALL.value,
                        ),
                    
                        direction="row",
                        align_items="center",
                        gap="3",
                        width="100%",
                        padding="0.75rem 1.25rem",
                        #border_bottom=CommonBorders.LIGHT_SOLID,
                        background=Color.background_light.value,
                    ),
                    # Header del perfil
                    rx.box(
                        profile_header(),
                        padding="0 1rem",
                        width="100%",
                    ),
                    # Cartas separadas verticalmente
                    rx.vstack(
                        # Carta General
                        info_card_profile(
                            title="General",
                            content=general_tab_content(),
                            icon="home",
                            badge_text=None,
                            actions=None,
                            show_header=True,
                            show_footer=False,
                        ),
                        # Carta Permisos
                        rx.box(
                            rx.flex(
                                rx.icon("lock", size=16, color="#10b981"),
                                rx.text("Permisos", font_weight="600", font_size="1.1rem"),
                                gap="3",
                                align_items="center",
                                mb="4",
                            ),
                            permissions_tab_content(),
                            background=Color.background.value,
                            padding=SizeSpace.X_LARGE.value,
                            margin=SizeSpace.MEDIUM.value,
                            border_radius=BorderRadius.MEDIUM.value,
                            box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
                            border=CommonBorders.LIGHT_SOLID,
                            width="100%",
                        ),
                        # Carta Atributos
                        rx.box(
                            rx.flex(
                                rx.icon("tag", size=16, color="#f59e0b"),
                                rx.text("Atributos", font_weight="600", font_size="1.1rem"),
                                gap="3",
                                align_items="center",
                                mb="4",
                            ),
                            attributes_tab_content(),
                            background=Color.background.value,
                            padding=SizeSpace.X_LARGE.value,
                            margin=SizeSpace.MEDIUM.value,
                            border_radius=BorderRadius.MEDIUM.value,
                            box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
                            border=CommonBorders.LIGHT_SOLID,
                            width="100%",
                        ),
                        # Carta Actividad
                        rx.box(
                            rx.flex(
                                rx.icon("activity", size=16, color="#ef4444"),
                                rx.text("Actividad", font_weight="600", font_size="1.1rem"),
                                gap="3",
                                align_items="center",
                                mb="4",
                            ),
                            activity_tab_content(),
                            background=Color.background.value,
                            padding=SizeSpace.X_LARGE.value,
                            margin=SizeSpace.MEDIUM.value,
                            border_radius=BorderRadius.MEDIUM.value,
                            box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
                            border=CommonBorders.LIGHT_SOLID,
                            width="100%",
                        ),
                        spacing="6",
                        padding="0 1rem",
                        width="100%",
                    ),
                    spacing="0",
                    width="100%",
                ),
                width="100%",
                min_height="100vh",
            ),
            spacing="0",
            width="100%",
        ),
        width="100%",
        height="100vh",
        background=Color.background_light.value,
    )
