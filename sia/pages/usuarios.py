
from typing import Any, Optional

import reflex as rx

from components.db_users import (
    create_user,
    delete_user,
    get_all_users,
    get_user_statistics,
    search_users,
    update_user,
)
from sia.components.data_display.avatars import avatar_circle
from sia.components.data_display.badges import role_badge, status_badge
from sia.components.data_display.cards import stat_card
from sia.components.data_display.tables import data_table
from sia.components.forms.modals import user_modal
from sia.components.forms.selects import select_component
from sia.components.layout.headers import new_user_button, page_header
from sia.models.validation import User, UserCreate, UserUpdate
from sia.styles.border import CommonBorders
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import BorderRadius, SizeAvatar, SizeIcon, SizeText
from sia.views.sidebar import sidebar_main


class UserState(rx.State):
    """Estado para manejar la página de usuarios con integración a PostgreSQL."""

    # Lista de usuarios actual
    users_data: list[dict[str, Any]] = []

    # Estados de loading y error
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # Estadísticas
    user_statistics: dict[str, int] = {}

    # Filtros
    search_term: str = ""
    role_filter: str = ""
    status_filter: str = ""

    # Modal de usuario
    show_user_modal: bool = False
    selected_user_id: Optional[int] = None

    # Formulario de usuario
    form_nombre: str = ""
    form_apellido: str = ""
    form_nombre_usuario: str = ""
    form_contrasena: str = ""
    form_rol: str = "usuario"
    form_is_editing: bool = False

    def _convert_user_to_display_format(self, user: User) -> dict[str, Any]:
        """Convierte un modelo User de Pydantic al formato esperado por la UI.
        """
        # Mapear roles para display
        role_display_map = {
            "admin": "Administrador",
            "supervisor": "Supervisor",
            "usuario": "Usuario",
        }

        return {
            "id": user.id,
            "name": f"{user.nombre} {user.apellido}",
            "email": user.nombre_usuario,  # Usando nombre_usuario como email para display
            "role": role_display_map.get(user.rol, user.rol.title()),
            "area": "Ministerio C&T",  # Por ahora área fija
            "status": "Activo",  # Por ahora todos activos
            "permissions": "Sistema completo",  # Por ahora permisos genéricos
            "attributes": f"Rol: {user.rol}",
            "last_access": user.fecha_creacion.strftime("%d/%m/%Y") if user.fecha_creacion else "N/A",
            "avatar": user.nombre[0].upper() if user.nombre else "U",
            "actions": "",
        }

    def load_users(self):
        """Cargar usuarios desde la base de datos."""
        self.is_loading = True
        self.error_message = ""

        try:
            # Llamar a la función de la base de datos
            success, message, users = get_all_users()

            if success:
                # Convertir usuarios al formato de display
                self.users_data = [
                    self._convert_user_to_display_format(user)
                    for user in users
                ]
                self.success_message = f"Se cargaron {len(users)} usuarios exitosamente"
                self.error_message = ""
            else:
                self.users_data = []
                self.error_message = f"Error al cargar usuarios: {message}"
                self.success_message = ""

        except Exception as e:
            self.users_data = []
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False

    def load_statistics(self):
        """Cargar estadísticas de usuarios."""
        try:
            success, message, stats = get_user_statistics()

            if success:
                self.user_statistics = stats
            else:
                self.user_statistics = {
                    "total_usuarios": 0,
                    "activos": 0,
                    "administradores": 0,
                    "supervisores": 0,
                    "usuarios": 0,
                }
        except Exception:
            self.user_statistics = {
                "total_usuarios": 0,
                "activos": 0,
                "administradores": 0,
                "supervisores": 0,
                "usuarios": 0,
            }

    def search_users_filtered(self):
        """Buscar usuarios con filtros aplicados."""
        self.is_loading = True
        self.error_message = ""

        try:
            # Procesar filtros para enviar a la BD
            # Mapear valores de UI a valores de BD
            role_filter_map = {
                "Administrador": "admin",
                "Supervisor": "supervisor",
                "Usuario": "usuario",
                "Todos los roles": "",
                "": "",
            }

            status_filter_map = {
                "Activo": "active",
                "Inactivo": "inactive",
                "Todos los estados": "",
                "": "",
            }

            db_role_filter = role_filter_map.get(self.role_filter, "")
            db_status_filter = status_filter_map.get(self.status_filter, "")

            success, message, users = search_users(
                search_term=self.search_term,
                role_filter=db_role_filter,
                status_filter=db_status_filter,
            )

            if success:
                self.users_data = [
                    self._convert_user_to_display_format(user)
                    for user in users
                ]
                self.success_message = f"Se encontraron {len(users)} usuarios"
                self.error_message = ""
            else:
                self.users_data = []
                self.error_message = f"Error en búsqueda: {message}"
                self.success_message = ""

        except Exception as e:
            self.users_data = []
            self.error_message = f"Error inesperado en búsqueda: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False

    def set_search_term(self, term: str):
        """Establecer término de búsqueda."""
        self.search_term = term
        # Auto filtrar cuando se cambia el término
        return self.search_users_filtered()

    def set_role_filter(self, role: str):
        """Establecer filtro de rol."""
        self.role_filter = role
        # Auto filtrar cuando se cambia el rol
        return self.search_users_filtered()

    def set_status_filter(self, status: str):
        """Establecer filtro de estado."""
        self.status_filter = status
        # Auto filtrar cuando se cambia el estado
        return self.search_users_filtered()

    def clear_filters(self):
        """Limpiar todos los filtros."""
        self.search_term = ""
        self.role_filter = ""
        self.status_filter = ""

    def show_create_user_modal(self):
        """Mostrar modal para crear usuario."""
        self.show_user_modal = True
        self.form_is_editing = False
        self._clear_form()

    def show_edit_user_modal(self, user_id: int):
        """Mostrar modal para editar usuario."""
        self.show_user_modal = True
        self.form_is_editing = True
        self.selected_user_id = user_id
        self._load_user_to_form(user_id)

    def close_user_modal(self):
        """Cerrar modal de usuario."""
        self.show_user_modal = False
        self.selected_user_id = None
        self._clear_form()

    def _clear_form(self):
        """Limpiar formulario."""
        self.form_nombre = ""
        self.form_apellido = ""
        self.form_nombre_usuario = ""
        self.form_contrasena = ""
        self.form_rol = "usuario"

    def _load_user_to_form(self, user_id: int):
        """Cargar datos del usuario al formulario para edición."""
        # Buscar el usuario en los datos actuales
        for user_display in self.users_data:
            if user_display.get("id") == user_id:
                # Separar nombre completo
                full_name = user_display.get("name", "")
                name_parts = full_name.split(" ", 1)
                self.form_nombre = name_parts[0] if len(name_parts) > 0 else ""
                self.form_apellido = name_parts[1] if len(name_parts) > 1 else ""
                self.form_nombre_usuario = user_display.get("email", "")

                # Mapear rol de display a rol de BD
                role_map = {
                    "Administrador": "admin",
                    "Supervisor": "supervisor",
                    "Usuario": "usuario",
                }
                display_role = user_display.get("role", "Usuario")
                self.form_rol = role_map.get(display_role, "usuario")
                break

    def create_user_submit(self):
        """Crear nuevo usuario."""
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            # Crear objeto UserCreate
            user_data = UserCreate(
                nombre=self.form_nombre,
                apellido=self.form_apellido,
                nombre_usuario=self.form_nombre_usuario,
                contrasena=self.form_contrasena,
                rol=self.form_rol,
            )

            success, message, user_id = create_user(user_data)

            if success:
                self.success_message = message
                self.error_message = ""
                self.show_user_modal = False
                self._clear_form()
                # Recargar usuarios
                self.load_users()
                self.load_statistics()
            else:
                self.error_message = message
                self.success_message = ""

        except Exception as e:
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False

    def update_user_submit(self):
        """Actualizar usuario existente."""
        if not self.selected_user_id:
            return

        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            # Crear objeto UserUpdate solo con campos modificados
            update_data = {}
            if self.form_nombre:
                update_data["nombre"] = self.form_nombre
            if self.form_apellido:
                update_data["apellido"] = self.form_apellido
            if self.form_nombre_usuario:
                update_data["nombre_usuario"] = self.form_nombre_usuario
            if self.form_rol:
                update_data["rol"] = self.form_rol

            user_data = UserUpdate(**update_data)

            success, message, updated_user = update_user(self.selected_user_id, user_data)

            if success:
                self.success_message = message
                self.error_message = ""
                self.show_user_modal = False
                self._clear_form()
                self.selected_user_id = None
                # Recargar usuarios
                self.load_users()
                self.load_statistics()
            else:
                self.error_message = message
                self.success_message = ""

        except Exception as e:
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False

    def delete_user_action(self, user_id: int):
        """Eliminar usuario."""
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            success, message = delete_user(user_id)

            if success:
                self.success_message = message
                self.error_message = ""
                # Recargar usuarios y estadísticas
                self.load_users()
                self.load_statistics()
            else:
                self.error_message = message
                self.success_message = ""

        except Exception as e:
            self.error_message = f"Error inesperado: {e!s}"
            self.success_message = ""

        finally:
            self.is_loading = False

    def clear_messages(self):
        """Limpiar mensajes de éxito y error."""
        self.success_message = ""
        self.error_message = ""

    def load_profiles(self):
        """Cargar perfiles de usuario."""
        # Por ahora es un método placeholder

    # Métodos setter para los campos del formulario
    def set_form_nombre(self, nombre: str):
        """Establecer nombre en el formulario."""
        self.form_nombre = nombre

    def set_form_apellido(self, apellido: str):
        """Establecer apellido en el formulario."""
        self.form_apellido = apellido

    def set_form_nombre_usuario(self, nombre_usuario: str):
        """Establecer nombre de usuario en el formulario."""
        self.form_nombre_usuario = nombre_usuario

    def set_form_contrasena(self, contrasena: str):
        """Establecer contraseña en el formulario."""
        self.form_contrasena = contrasena

    def set_form_rol(self, rol: str):
        """Establecer rol en el formulario."""
        self.form_rol = rol

    def load_test_data(self):
        """Cargar datos de prueba."""
        self.users_data = [
            {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@mctc.gov.py",
                "role": "Administrador",
                "area": "Ministerio C&T",
                "status": "Activo",
                "permissions": "Sistema completo",
                "attributes": "Rol: admin",
                "avatar": "J"
            },
            {
                "id": 2,
                "name": "María García",
                "email": "maria@mctc.gov.py", 
                "role": "Usuario",
                "area": "Ministerio C&T",
                "status": "Activo",
                "permissions": "Solo lectura",
                "attributes": "Rol: usuario",
                "avatar": "M"
            }
        ]

    def on_load(self):
        """Ejecutar al cargar la página."""
        self.load_test_data()
        return []

from sia.styles.sizes import SizeSpace


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
                            value=UserState.search_term,
                            on_change=UserState.set_search_term,
                        ),
                        width="60%",
                    ),
                rx.spacer(),
                rx.hstack(
                    select_component(
                        options=["Todos los roles", "Administrador", "Supervisor", "Usuario"],
                        value=UserState.role_filter,
                        placeholder="Todos los roles",
                        on_change=UserState.set_role_filter,
                    ),
                    select_component(
                        options=["Todos los estados", "Activo", "Inactivo"],
                        value=UserState.status_filter,
                        placeholder="Todos los estados",
                        on_change=UserState.set_status_filter,
                    ),
                    spacing="4",
                    width="40%",
                    align_items="end",
                ),
                width="40%",
                ),
                width="100%",
            ),
            width="100%",
            spacing="3",
            border_radius=BorderRadius.SMALL.value,
            border=CommonBorders.LIGHT_SOLID,
            padding=SizeSpace.MEDIUM.value,
        ),
        align="start",
        width="100%",
        height="auto",
        bg="white",
        mb="4",
    )

def user_table() -> rx.Component:
    # Funciones de renderizado personalizadas
    def render_user_column(value, row_data):
        return rx.hstack(
            rx.text("👤", font_size="24px"),  # Emoji simple como avatar temporal
            rx.vstack(
                rx.text(row_data.name, font_size=SizeText.MEDIUM.value, weight="medium"),
                rx.text(row_data.email, font_size=SizeText.SMALL.value, color="gray.500"),
                spacing="1",
                align="start",
                justify="center",
            ),
            spacing="3",
            align="center",
            width="100%",
        )

    def render_role_column(value, row_data):
        # Usamos rx.match para mapear el rol de display a rol para badge
        return rx.match(
            row_data.role,
            ("Administrador", role_badge(text="Administrador", role="admin")),
            ("Supervisor", role_badge(text="Supervisor", role="supervisor")),
            ("Usuario", role_badge(text="Usuario", role="usuario")),
            role_badge(text=row_data.role, role="default")  # fallback
        )

    def render_status_column(value, row_data):
        return rx.match(
            row_data.status,
            ("Activo", status_badge(text="Activo", status="active", show_dot=True)),
            status_badge(text=row_data.status, status="inactive", show_dot=True)  # fallback
        )

    def render_permissions_column(value, row_data):
        return rx.hstack(
            rx.icon(tag="shield", color=Color.icon_inactive.value, size=SizeIcon.SMALL.value),
            rx.text(row_data.permissions),
            spacing="2",
        )

    def render_attributes_column(value, row_data):
        return rx.hstack(
            rx.icon(tag="badge-check", color=Color.icon_inactive.value, size=SizeIcon.SMALL.value),
            rx.text(row_data.attributes),
            spacing="2",
        )

    def render_actions_column(value, row_data):
        return rx.hstack(
            rx.button(
                rx.icon(tag="pencil", size=SizeIcon.SMALL.value),
                on_click=UserState.show_edit_user_modal(row_data.id),
                variant="ghost",
                size="2",
                color_scheme="blue",
            ),
            rx.button(
                rx.icon(tag="trash-2", size=SizeIcon.SMALL.value),
                on_click=UserState.delete_user_action(row_data.id),
                variant="ghost",
                size="2",
                color_scheme="red",
            ),
            spacing="1",
        )

    return rx.cond(
        UserState.is_loading,
        rx.box(
            rx.spinner(size="3"),
            rx.text("Cargando usuarios...", mt="4"),
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
            height="200px",
        ),
        # Tabla de usuarios simplificada para debug
        rx.box(
            rx.text("Lista de Usuarios", font_weight="bold", font_size="lg", mb="4"),
            rx.text(f"Usuarios cargados: {UserState.users_data.length()}", mb="4"),
            rx.cond(
                UserState.users_data.length() > 0,
                # Tabla con usuarios
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Usuario"),
                            rx.table.column_header_cell("Email"),
                            rx.table.column_header_cell("Rol"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Acciones"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            UserState.users_data,
                            lambda user: rx.table.row(
                                rx.table.cell(user.name),
                                rx.table.cell(user.email),
                                rx.table.cell(user.role),
                                rx.table.cell(user.status),
                                rx.table.cell("Acciones"),
                            )
                        )
                    ),
                    width="100%",
                    border="1px solid #e2e8f0",
                    border_radius="8px",
                ),
                # Estado vacío
                rx.box(
                    rx.vstack(
                        rx.icon("users", size=48, color="gray.400"),
                        rx.text("No hay usuarios registrados", font_size="lg", font_weight="medium", color="gray.700"),
                        rx.text("Agrega el primer usuario para empezar a gestionar el sistema", color="gray.500", text_align="center"),
                        spacing="4",
                        align="center",
                        justify="center",
                        py="12",
                    ),
                    width="100%",
                    text_align="center",
                    border="2px dashed #e2e8f0",
                    border_radius="8px",
                    bg="gray.50",
                )
            ),
            width="100%",
            bg="white",
            p="6",
            border_radius="8px",
            border="1px solid #e2e8f0",
        ),
    )

def statistics_cards_users() -> rx.Component:
    """Returns a horizontal stack of statistics cards showing user metrics."""
    return rx.hstack(
        stat_card(
            title="Total Usuarios",
            value=str(UserState.user_statistics.get("total_usuarios", 0)),
            icon="user-check",
        ),
        stat_card(
            title="Activos",
            value=str(UserState.user_statistics.get("activos", 0)),
            icon="check",
            icon_color="green.400",
        ),
        stat_card(
            title="Administradores",
            value=str(UserState.user_statistics.get("administradores", 0)),
            icon="shield",
            icon_color="purple.400",
        ),
        stat_card(
            title="Supervisores",
            value=str(UserState.user_statistics.get("supervisores", 0)),
            icon="briefcase",
            icon_color="orange.400",
        ),
        spacing="6",
        justify="start",
        width="100%",
    )

def notification_messages() -> rx.Component:
    """Componente para mostrar mensajes de éxito y error."""
    return rx.box(
        # Mensaje de éxito
        rx.cond(
            UserState.success_message != "",
            rx.callout(
                UserState.success_message,
                icon="check",
                color_scheme="green",
                mb="4",
            ),
        ),
        # Mensaje de error
        rx.cond(
            UserState.error_message != "",
            rx.callout(
                UserState.error_message,
                icon="triangle-alert",
                color_scheme="red",
                mb="4",
            ),
        ),
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
                            notification_messages(),
                            statistics_cards_users(),
                            search_filters(),
                            user_table(),
                            spacing="4",
                            width="100%",
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

        # Modal de usuario
        user_modal(),

        width="100%",
        height="100vh",
        on_mount=UserState.on_load,
    )
