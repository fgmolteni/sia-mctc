
import reflex as rx
from sia.views.sidebar import sidebar_main
from sia.components.layout.headers import page_header, new_user_button
from sia.components.forms.inputs import form_input
from sia.components.forms.selects import form_select
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeAvatar, SizeText, SizeButton, SizeIcon, BorderRadius
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders
from sia.components.forms.selects import select_component
from sia.components.data_display.avatars import avatar_circle, avatar
from sia.components.data_display.badges import role_badge, status_badge
from sia.components.data_display.cards import stat_card
from sia.components.data_display.tables import data_table, table_actions_menu

class UserState(rx.State):
    """Estado para manejar la página de usuarios."""
    users_data: list = []
    
    def load_users(self):
        """Cargar datos de usuarios."""
        # Por ahora usamos datos estáticos, pero aquí se podría conectar a la base de datos
        self.users_data = [
            {"name": "Juan Pérez", "email": "juan.perez@empresa.com", "role": "Administrador", "area": "Administración", "status": "Activo", "permissions": "5 permisos", "attributes": "5 atributos", "last_access": "15/1/2024"},
            {"name": "María García", "email": "maria.garcia@empresa.com", "role": "Manager", "area": "Ventas", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "14/1/2024"},
            {"name": "Carlos López", "email": "carlos.lopez@empresa.com", "role": "Empleado", "area": "Marketing", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "13/1/2024"},
            {"name": "Ana Martínez", "email": "ana.martinez@empresa.com", "role": "Empleado", "area": "RRHH", "status": "Inactivo", "permissions": "3 permisos", "attributes": "3 atributos", "last_access": "10/1/2024"},
        ]
    
    def load_profiles(self):
        """Cargar datos de perfiles de usuarios."""
        # Método para cargar perfiles, por ahora puede estar vacío o cargar datos específicos
        pass

from sia.styles.sizes import SizeText, SizeButton, SizeIcon, BorderRadius, SizeSpace

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
        {"name": "Juan Pérez", "email": "juan.perez@empresa.com", "area": "Administración", "status": "Activo", "permissions": "5 permisos", "attributes": "5 atributos", "last_access": "15/1/2024"},
        {"name": "María García", "email": "maria.garcia@empresa.com", "area": "Ventas", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "14/1/2024"},
        {"name": "Carlos López", "email": "carlos.lopez@empresa.com", "area": "Marketing", "status": "Activo", "permissions": "4 permisos", "attributes": "3 atributos", "last_access": "13/1/2024"},
        {"name": "Ana Martínez", "email": "ana.martinez@empresa.com", "area": "RRHH", "status": "Inactivo", "permissions": "3 permisos", "attributes": "3 atributos", "last_access": "10/1/2024"},
    ]
    
    # Funciones de renderizado personalizadas
    def render_user_column(value, row_data):
        return rx.hstack(
            avatar_circle(user=row_data["name"], size=SizeAvatar.DEFAULT.value),
            rx.vstack(
                rx.text(row_data["name"], font_size=SizeText.MEDIUM.value, weight="medium"),
                #rx.text(row_data["email"], font_size=SizeText.SMALL.value, color="gray.500"),
                spacing="1",
                align="start",
                justify="center",
            ),
            spacing="3",
            align="center",
            #justify="center",
            width="100%"
        )
    
    def render_role_column(value, row_data):
        return role_badge(
            text=row_data["role"],
            #role="admin" if row_data["role"] == "Administrador" else "manager" if row_data["role"] == "Manager" else "employee"
        )
    
    def render_status_column(value, row_data):
        return status_badge(
            text=row_data["status"],
            status="active" if row_data["status"] == "Activo" else "inactive",
            show_dot=True
        )
    
    def render_permissions_column(value, row_data):
        return rx.hstack(
            rx.icon(tag="shield", color=Color.icon_inactive.value, size=SizeIcon.SMALL.value),
            rx.text(row_data["permissions"]),
            spacing="2"
        )
    
    def render_attributes_column(value, row_data):
        return rx.hstack(
            rx.icon(tag="badge-check", color=Color.icon_inactive.value, size=SizeIcon.SMALL.value),
            rx.text(row_data["attributes"]),
            spacing="2"
        )
    
    # Acciones personalizadas
    user_actions = [
        {
            "label": "Ver Perfil",
            "icon": "user",
            "href": "/users/profiles",
            "text_color": ColorText.PRIMARY.value,
            "color": Color.icon_inactive.value
        },
        {
            "label": "Modificar",
            "icon": "pencil",
            "color": Color.icon_inactive.value
        },
        {
            "label": "Eliminar",
            "icon": "trash-2",
            "color": Color.delete_icon.value,
            "text_color": Color.delete_text.value,
            "separator_after": True
        }
    ]
    
    return data_table(
        title="Lista de Usuarios",
        data=users_data,
        headers=["Usuario", "Email","Área", "Estado", "Permisos", "Acciones"],
        render_functions={
            "name": render_user_column,
            "role": render_role_column,
            "status": render_status_column,
            "permissions": render_permissions_column,
            "attributes": render_attributes_column,
        },
        actions_menu=table_actions_menu(user_actions),
        counter_text="usuarios mostrados"
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
