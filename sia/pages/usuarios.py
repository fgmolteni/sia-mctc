
import reflex as rx
from sia.views.sidebar import sidebar_main
from sia.components.header import page_header, new_user_button
from sia.components.form_components import form_input, form_select
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeAvatar, SizeText, SizeButton, SizeIcon, BorderRadius
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders
from sia.components.select_components import select_component
from sia.components.avartar import avatar_circle

class UserState(rx.State):
    """Estado para manejar la página de usuarios."""
    users_data: list = []
    
    def load_users(self):
        """Cargar datos de usuarios."""
        # Por ahora usamos datos estáticos, pero aquí se podría conectar a la base de datos
        self.users_data = [
            {"initials": "JP", "name": "Juan Pérez", "email": "juan.perez@empresa.com", "role": "Administrador", "area": "Administración", "status": "Activo", "permissions": "5 permisos", "attributes": "5 atributos", "last_access": "15/1/2024"},
            {"initials": "MG", "name": "María García", "email": "maria.garcia@empresa.com", "role": "Manager", "area": "Ventas", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "14/1/2024"},
            {"initials": "CL", "name": "Carlos López", "email": "carlos.lopez@empresa.com", "role": "Empleado", "area": "Marketing", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "13/1/2024"},
            {"initials": "AM", "name": "Ana Martínez", "email": "ana.martinez@empresa.com", "role": "Empleado", "area": "RRHH", "status": "Inactivo", "permissions": "3 permisos", "attributes": "3 atributos", "last_access": "10/1/2024"},
        ]
    
    def load_profiles(self):
        """Cargar datos de perfiles de usuarios."""
        # Método para cargar perfiles, por ahora puede estar vacío o cargar datos específicos
        pass

from sia.styles.sizes import SizeText, SizeButton, SizeIcon, BorderRadius, SizeSpace

def stat_card(title: str, value: str, icon: str, icon_color: str = "white.400") -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(
                    title,
                    color=ColorText.GRAY_500.value,
                    font_size=SizeText.MEDIUM.value,
                    font_weight=FontWeight.MEDIUM.value
                ),
                rx.spacer(),
                rx.icon(
                    tag=icon,
                    size=SizeIcon.LARGE.value,
                    color=icon_color,
                    #background_color=Color.icon_background.value,
                    padding=SizeSpace.SMALL.value,
                    border_radius=BorderRadius.SMALL.value,
                ),
                align="start",
                width="100%",
                spacing="5",
            ),
            rx.spacer(),
            rx.heading(
                value,
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                align="left",
                justify="end",
                width="100%"
            ),
            width="100%",
            align="start",
            spacing="3"
        ),
        width_min="250px",
        width="100%",
        height="120px",
        padding=SizeSpace.MEDIUM.value
    )

def search_filters() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "Filtros de Búsqueda",
                font_weight=FontWeight.BOLD.value,
                font_size=SizeText.LARGE.value,
                color=ColorText.GRAY_800.value,
                align_self="start",
                mb="3",
            ),
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.input(
                            placeholder="Buscar por nombre, email o área...",
                            width="100%",
                            border=CommonBorders.LIGHT_SOLID,
                            border_radius=BorderRadius.SMALL.value,
                            py=SizeSpace.SMALL.value,
                            px=SizeSpace.SMALL.value,
                            _focus={"border_color": Color.icon_inactive.value},
                        ),
                        width="60%",
                    ),
                rx.spacer(),
                rx.hstack(
                    select_component(
                        "Todos los roles",
                        ["Todos los roles", "Administrador", "Manager", "Empleado"],
                    ),
                    select_component(
                        "Todos los estados",
                        ["Todos los estados", "Activo", "Inactivo"],
                    ),
                    spacing="4",
                    width="40%",
                    align_items='end',
                ),
                width='40%',
                #align_items='end',
                ),
                width='100%',
            ),
            width="100%",
            spacing="3",
            border_radius=BorderRadius.SMALL.value,
            border=CommonBorders.LIGHT_SOLID,
            padding=SizeSpace.MEDIUM.value,
        ),
        align='start',
        width="100%",
        height="auto",
        bg="white",
        mb="4",
    )

def user_table() -> rx.Component:
    users_data = [
        {"initials": "JP", "name": "Juan Pérez", "email": "juan.perez@empresa.com", "role": "Administrador", "area": "Administración", "status": "Activo", "permissions": "5 permisos", "attributes": "5 atributos", "last_access": "15/1/2024"},
        {"initials": "MG", "name": "María García", "email": "maria.garcia@empresa.com", "role": "Manager", "area": "Ventas", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "14/1/2024"},
        {"initials": "CL", "name": "Carlos López", "email": "carlos.lopez@empresa.com", "role": "Empleado", "area": "Marketing", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "13/1/2024"},
        {"initials": "AM", "name": "Ana Martínez", "email": "ana.martinez@empresa.com", "role": "Empleado", "area": "RRHH", "status": "Inactivo", "permissions": "3 permisos", "attributes": "3 atributos", "last_access": "10/1/2024"},
    ]
    table_headers = ["Usuario", "Rol", "Área", "Estado", "Permisos", "Atributos", "Último Acceso", "Acciones"]

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Lista de Usuarios", font_weight=FontWeight.BOLD.value, font_size=SizeText.LARGE.value, color="gray.800"),
                rx.spacer(),
                rx.text("4 de 4 usuarios mostrados", color=ColorText.GRAY_500.value, font_size=SizeText.SMALL.value),
                width="100%",
                mb="4",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        *[rx.table.column_header_cell(header, font_weight=FontWeight.MEDIUM.value, text_align="left", padding="3") for header in table_headers],
                        bg=Color.background_light.value,
                    ),
                ),
                rx.table.body(
                    *[rx.table.row(
                        # usuario
                        rx.table.cell(
                            rx.hstack(
                                avatar_circle(
                                    user=user["initials"],
                                    size=SizeAvatar.SMALL.value,
                                ),
                                rx.vstack(
                                    rx.text(user["name"], font_weight=FontWeight.MEDIUM.value),
                                    rx.text(user["email"], color=ColorText.GRAY_500.value, font_size="2"),
                                    align="start",
                                    spacing="0",
                                ),
                                spacing="3",
                            ),
                            padding="3",
                        ),
                        # Rol
                        rx.table.cell(
                            rx.box(
                                rx.badge(
                                    user["role"],
                                    color=Color.admin_text.value if user["role"] == "Administrador" else Color.manager_text.value if user["role"] == "Manager" else Color.employee_text.value,
                                    bg=Color.admin_bg.value if user["role"] == "Administrador" else Color.manager_bg.value if user["role"] == "Manager" else Color.employee_bg.value,
                                    px="2",
                                    py="1",
                                    border_radius=BorderRadius.DEFAULT.value,
                                    font_weight=FontWeight.MEDIUM.value,
                                ),
                            ),
                            padding="3",
                        ),
                        # Area
                        rx.table.cell(user["area"], padding="3"),
                        # Estado
                        rx.table.cell(
                            rx.hstack(
                                rx.box(width="8px", height="8px", bg=Color.status_active.value if user["status"] == "Activo" else Color.icon_inactive.value, border_radius=BorderRadius.DEFAULT.value),
                                rx.text(user["status"]),
                                spacing="2",
                                align_items="center",
                            ),
                            padding="3",
                        ),
                        rx.table.cell(rx.hstack(rx.icon(tag="shield", color=Color.icon_inactive.value, size=SizeIcon.SMALL.value), rx.text(user["permissions"]), spacing="2"), padding="3"),
                        rx.table.cell(rx.hstack(rx.icon(tag="badge-check", color=Color.icon_inactive.value, size=SizeIcon.SMALL.value), rx.text(user["attributes"]), spacing="2"), padding="3"),
                        rx.table.cell(user["last_access"], padding="3"),
                        rx.table.cell(
                            rx.menu.root(
                                rx.menu.trigger(
                                    rx.button(rx.icon(tag="ellipsis-vertical", color=Color.icon_inactive.value, size=SizeIcon.MEDIUM.value), color="white", bg="white")
                                ),
                                rx.menu.content(
                                    rx.menu.item(rx.link(rx.hstack(rx.icon(tag="user", color=Color.icon_inactive.value, size=SizeIcon.MEDIUM.value), rx.text("Ver Perfil"), spacing="2"), href="/users/profiles")),
                                    rx.menu.item(rx.hstack(rx.icon(tag="pencil", color=Color.admin_icon.value, size=SizeIcon.MEDIUM.value), rx.text("Modificar"), spacing="2")),
                                    rx.menu.separator(),
                                    rx.menu.item(rx.hstack(rx.icon(tag="trash-2", color=Color.delete_icon.value, size=SizeIcon.MEDIUM.value), rx.text("Eliminar"), spacing="2"), color=Color.delete_text.value),
                                ),
                            ),
                            padding="3",
                        ),
                        vertical_align="middle",
                    ) for user in users_data],
                ),
                width="100%",
                border_radius=BorderRadius.SMALL.value,
                border=CommonBorders.LIGHT_SOLID,
            ),
            width="100%",
            align_items="start",
        ),
        width="100%",
        bg="white",
        padding="1.5rem",
        border_radius=BorderRadius.SMALL.value,
        border=CommonBorders.LIGHT_SOLID,
    )

def statistics_cards_users() -> rx.Component:
    """Returns a horizontal stack of statistics cards showing user metrics."""
    return rx.hstack(
        
            stat_card(
                title="Total Usuarios",
                value="4", 
                icon="user-check",
            ),
        
        
            stat_card(
                title="Activos",
                value="3",
                icon="check",
                icon_color="green.400"
            ),
        
        
            stat_card(
                title="Administradores", 
                value="1",
                icon="shield",
                icon_color="purple.400"
            ),
        
        
            stat_card(
                title="Managers",
                value="1", 
                icon="briefcase",
                icon_color="orange.400"
            ),
        spacing="6",
        justify="start",
        width="100%",
    )

def users_page() -> rx.Component:
    return rx.box(
        rx.hstack(
            sidebar_main(),
            rx.box(
                rx.vstack(
                    rx.box(
                        page_header(
                            title="Gestión de Usuarios",
                            subtitle="Administra usuarios, permisos y atributos del sistema",
                            action_button=new_user_button(),
                        ),
                        width="100%",
                        padding=f"{SizeSpace.MEDIUM.value} {SizeSpace.LARGE.value} 0 {SizeSpace.LARGE.value}",
                    ),
                    rx.box(
                        rx.vstack(
                            statistics_cards_users(),
                            search_filters(),
                            user_table(),
                            spacing="4",
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
                bg=Color.background_light.value,
                flex="1",
            ),
            width="100%",
            height="100vh",
            overflow="hidden",
            align="start",
            spacing="0",
        ),
        width="100%",
        height="100vh",
    )
