
from typing import Any, Optional

import reflex as rx

from components.logging import get_sia_logger
from components.db_users import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
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
from sia.components.forms.inputs import apply_auto_transform
from sia.styles.border import CommonBorders
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import BorderRadius, SizeAvatar, SizeIcon, SizeText
from sia.views.sidebar import sidebar_main


# Logger fuera del estado (no serializable)
logger = get_sia_logger('pages.usuarios')

class UserState(rx.State):
    """Estado para manejar la página de usuarios con integración a PostgreSQL."""

    # Lista de usuarios actual
    users_data: list[dict[str, Any]] = []

    # Estados de loading y error
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # Estadísticas
    user_statistics: dict[str, int] = {
        "total_usuarios": 0,
        "activos": 0,
        "administradores": 0,
        "supervisores": 0,
        "usuarios": 0,
    }

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
    form_email: str = ""
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
            "email": user.email,  # Usando el campo email real
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
        return []

    def load_statistics(self):
        """Cargar estadísticas de usuarios."""
        try:
            success, message, stats = get_user_statistics()

            if success and stats:
                # Actualizar solo los valores que están presentes
                for key, value in stats.items():
                    if key in self.user_statistics:
                        self.user_statistics[key] = value
                logger.info(f"Estadísticas cargadas exitosamente: {stats}")
            else:
                logger.error(f"Error al cargar estadísticas: {message}")
                # No reinicializar si ya hay datos previos
                if not any(self.user_statistics.values()):
                    self.user_statistics = {
                        "total_usuarios": 0,
                        "activos": 0,
                        "administradores": 0,
                        "supervisores": 0,
                        "usuarios": 0,
                    }
        except Exception as e:
            logger.error(f"Excepción al cargar estadísticas: {e}")
            # Solo reinicializar si no hay datos previos
            if not any(self.user_statistics.values()):
                self.user_statistics = {
                    "total_usuarios": 0,
                    "activos": 0,
                    "administradores": 0,
                    "supervisores": 0,
                    "usuarios": 0,
                }
        return []

    def refresh_statistics(self):
        """Forzar actualización de estadísticas."""
        logger.info("Refrescando estadísticas manualmente")
        return self.load_statistics()

    def debug_statistics(self):
        """Método de debug para mostrar estadísticas en consola."""
        logger.info(f"Estado actual de user_statistics: {self.user_statistics}")
        try:
            success, message, stats = get_user_statistics()
            logger.info(f"Resultado directo de get_user_statistics(): success={success}, stats={stats}")
        except Exception as e:
            logger.error(f"Error en debug_statistics: {e}")
        return []

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
        self.form_email = ""
        self.form_contrasena = ""
        self.form_rol = "usuario"

    def _load_user_to_form(self, user_id: int):
        """Cargar datos del usuario al formulario para edición."""
        try:
            # Obtener usuario directamente de la base de datos para tener datos precisos
            success, message, user = get_user_by_id(user_id)
            
            if success and user:
                self.form_nombre = user.nombre
                self.form_apellido = user.apellido
                self.form_nombre_usuario = user.nombre_usuario
                self.form_email = user.email
                self.form_rol = user.rol
                # No cargar contraseña por seguridad
                self.form_contrasena = ""
            else:
                logger.error(f"Error al cargar usuario para edición: {message}")
                self.error_message = f"Error al cargar usuario: {message}"
                
        except Exception as e:
            logger.error(f"Error inesperado al cargar usuario {user_id}: {e}")
            self.error_message = f"Error inesperado: {e}"

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
                email=self.form_email,
                contrasena=self.form_contrasena,
                rol=self.form_rol,
            )

            success, message, user_id = create_user(user_data)

            if success:
                self.success_message = message
                self.error_message = ""
                self.show_user_modal = False
                self._clear_form()
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
            if self.form_email:
                update_data["email"] = self.form_email
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
        # Aplicar transformación automática (capitalizar)
        self.form_nombre = apply_auto_transform(nombre, 'title')

    def set_form_apellido(self, apellido: str):
        """Establecer apellido en el formulario."""
        # Aplicar transformación automática (capitalizar)
        self.form_apellido = apply_auto_transform(apellido, 'title')

    def set_form_nombre_usuario(self, nombre_usuario: str):
        """Establecer nombre de usuario en el formulario."""
        # Aplicar transformación automática (minúsculas)
        self.form_nombre_usuario = apply_auto_transform(nombre_usuario, 'lowercase')

    def set_form_email(self, email: str):
        """Establecer email en el formulario."""
        # Aplicar transformación automática (minúsculas)
        self.form_email = apply_auto_transform(email, 'lowercase')

    def set_form_contrasena(self, contrasena: str):
        """Establecer contraseña en el formulario."""
        # No aplicar transformación para contraseñas (mantener original)
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
        yield self.load_users()
        yield self.load_statistics()

from sia.styles.sizes import SizeSpace


def search_filters() -> rx.Component:
    """Componente de filtros de búsqueda mejorado."""
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
                    options=["Todos los roles", "Administrador", "Supervisor", "Usuario"],
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

def user_table() -> rx.Component:
    """Tabla de usuarios usando el componente data_table reutilizable."""
    
    # Funciones de renderizado para columnas personalizadas
    def render_user_column(value, row_data):
        """Renderiza la columna de usuario con avatar y info."""
        if isinstance(row_data, dict):
            # Para listas Python
            return rx.hstack(
                # avatar_circle(user=row_data.get("avatar", "U"), size="2"),
                rx.vstack(
                    rx.text(value, font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value),
                    rx.text(row_data.get("email", ""), font_size=SizeText.SMALL.value, color=ColorText.GRAY_500.value),
                    spacing="1",
                    align="start",
                    justify="center",
                ),
                spacing="3",
                align="center",
            )
        else:
            # Para variables Reflex
            return rx.hstack(
                # avatar_circle(user=row_data.avatar, size="6"),
                rx.vstack(
                    rx.text(value, font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value),
                    rx.text(row_data.email, font_size=SizeText.SMALL.value, color=ColorText.GRAY_500.value),
                    spacing="1",
                    align="start",
                    justify="center",
                ),
                spacing="3",
                align="center",
            )

    def render_role_column(value, row_data):
        """Renderiza la columna de rol con badge."""
        role_map = {
            "Administrador": "admin",
            "Supervisor": "supervisor", 
            "Usuario": "usuario"
        }
        
        if isinstance(value, str):
            # Para listas Python
            role_key = role_map.get(value, "default")
            return role_badge(text=value, role=role_key)
        else:
            # Para variables Reflex - usar rx.match
            return rx.match(
                value,
                ("Administrador", role_badge(text="Administrador", role="admin")),
                ("Supervisor", role_badge(text="Supervisor", role="supervisor")),
                ("Usuario", role_badge(text="Usuario", role="usuario")),
                role_badge(text=value, role="default")  # fallback
            )

    def render_status_column(value, row_data):
        """Renderiza la columna de estado con badge."""
        if isinstance(value, str):
            # Para listas Python
            status_map = {
                "Activo": "active",
                "Inactivo": "inactive"
            }
            status_key = status_map.get(value, "inactive")
            return status_badge(text=value, status=status_key, show_dot=True)
        else:
            # Para variables Reflex - usar rx.match
            return rx.match(
                value,
                ("Activo", status_badge(text="Activo", status="active", show_dot=True)),
                status_badge(text=value, status="inactive", show_dot=True)  # fallback
            )

    def render_actions_column(value, row_data):
        """Renderiza la columna de acciones con botones."""
        # Para listas Python, row_data es un dict
        # Para variables Reflex, row_data es rx.Var
        if isinstance(row_data, dict):
            user_id = row_data.get("id")
            return rx.hstack(
                rx.button(
                    rx.icon(tag="pencil", size=SizeIcon.SMALL.value),
                    on_click=UserState.show_edit_user_modal(user_id),
                    variant="solid",
                    size="2",
                    color_scheme="blue",
                ),
                rx.button(
                    rx.icon(tag="trash", size=SizeIcon.SMALL.value), 
                    on_click=UserState.delete_user_action(user_id),
                    variant="solid",
                    size="2",
                    color_scheme="red",
                ),
                spacing="4",
            )
        else:
            # Para variables Reflex
            return rx.hstack(
                rx.button(
                    rx.icon(tag="pencil", size=SizeIcon.SMALL.value),
                    on_click=lambda: UserState.show_edit_user_modal(row_data.id),
                    variant="ghost",
                    size="2",
                    color_scheme="blue",
                ),
                rx.button(
                    rx.icon(tag="trash", size=SizeIcon.SMALL.value), 
                    on_click=lambda: UserState.delete_user_action(row_data.id),
                    variant="ghost",
                    size="2",
                    color_scheme="red",
                ),
                spacing="1",
            )

    # Headers para la tabla
    headers = ["Usuario", "Rol", "Estado", "Acciones"]
    
    # Funciones de renderizado
    render_functions = {
        "name": render_user_column,
        "role": render_role_column,
        "status": render_status_column,
        "actions": render_actions_column,
    }

    return data_table(
        title="Usuarios del Sistema",
        data=UserState.users_data,
        headers=headers,
        render_functions=render_functions,
        show_counter=True,
        counter_text="usuarios",
        actions_column=True
    )

def statistics_cards_users() -> rx.Component:
    """Returns a horizontal stack of statistics cards showing user metrics."""
    return rx.vstack(
        # Header con botón de refresh
        rx.hstack(
            rx.heading(
                "Estadísticas de Usuarios",
                font_size=SizeText.LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=ColorText.GRAY_800.value,
            ),
            rx.spacer(),
            rx.button(
                rx.icon("refresh-ccw", size=SizeIcon.SMALL.value),
                "Actualizar",
                on_click=UserState.refresh_statistics,
                variant="ghost",
                size="2",
                color_scheme="blue",
            ),
            rx.button(
                rx.icon("bug", size=SizeIcon.SMALL.value),
                "Debug",
                on_click=UserState.debug_statistics,
                variant="ghost",
                size="2",
                color_scheme="orange",
            ),
            width="100%",
            align="center",
        ),
        # Tarjetas de estadísticas
        rx.hstack(
            stat_card(
                title="Total Usuarios",
                value=UserState.user_statistics["total_usuarios"].to(str),
                icon="user_check",
            ),
            stat_card(
                title="Activos",
                value=UserState.user_statistics["activos"].to(str),
                icon="check",
                icon_color="green.400",
            ),
            stat_card(
                title="Administradores",
                value=UserState.user_statistics["administradores"].to(str),
                icon="shield",
                icon_color="purple.400",
            ),
            stat_card(
                title="Supervisores",
                value=UserState.user_statistics["supervisores"].to(str),
                icon="briefcase",
                icon_color="orange.400",
            ),
            spacing="6",
            justify="start",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )

def notification_messages() -> rx.Component:
    """Componente mejorado para mostrar mensajes de éxito y error."""
    return rx.vstack(
        # Mensaje de éxito
        rx.cond(
            UserState.success_message != "",
            rx.callout(
                rx.hstack(
                    rx.text(UserState.success_message),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=UserState.clear_messages,
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                    align="center",
                ),
                icon="check_check",
                color_scheme="green",
                width="100%",
            ),
        ),
        # Mensaje de error
        rx.cond(
            UserState.error_message != "",
            rx.callout(
                rx.hstack(
                    rx.text(UserState.error_message),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=UserState.clear_messages,
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                    align="center",
                ),
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
        ),
        # Indicador de carga
        rx.cond(
            UserState.is_loading,
            rx.callout(
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text("Procesando..."),
                    spacing="3",
                    align="center",
                ),
                icon="info",
                color_scheme="blue",
                width="100%",
            ),
        ),
        spacing="3",
        width="100%",
    )


def users_page() -> rx.Component:
    """Página principal de gestión de usuarios con diseño mejorado."""
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
                            notification_messages(),
                            
                            # Estadísticas de usuarios
                            statistics_cards_users(),
                            
                            # Filtros de búsqueda
                            search_filters(),
                            
                            # Tabla de usuarios
                            user_table(),
                            
                            spacing="6",
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
        
        width="100%",
        height="100vh",
        on_mount=UserState.on_load,
    )
