import reflex as rx
from typing import Optional

from sia.views.sidebar import sidebar_main
from sia.components.layout.headers import header_profiles, page_header
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeAvatar, SizeSpace, SizeIcon, SizeText, SizeGeneral
from sia.styles.border import CommonBorders, BorderRadius
from sia.components.data_display.avatars import avatar_circle
from sia.views.layout_profiles import permission_views, permissions_section, ProfileState
from components.db_users import get_user_by_id
from sia.models.validation import User


class DynamicProfileState(ProfileState):
    """
    Estado para manejar perfiles dinámicos de usuarios cargados desde la base de datos.
    
    Extiende ProfileState añadiendo funcionalidad para cargar datos específicos 
    de usuario desde los parámetros de la ruta usando router.page.params.get("user_id").
    """
    
    # Estados de datos del usuario
    user_data: Optional[User] = None
    user_id_param: Optional[str] = None
    
    # Estados de carga y error
    is_loading: bool = False
    error_message: str = ""
    has_error: bool = False
    
    # Método on_load para cargar datos cuando se accede a la página
    async def on_load(self):
        """Carga los datos del usuario cuando se accede a la página."""
        try:
            # Obtener el user_id desde los parámetros de la ruta
            self.user_id_param = self.router.page.params.get("user_id", "")
            
            if not self.user_id_param:
                self.has_error = True
                self.error_message = "No se proporcionó ID de usuario"
                self.is_loading = False
                return
            
            # Validar que el user_id sea un número válido
            try:
                user_id = int(self.user_id_param)
            except ValueError:
                self.has_error = True
                self.error_message = "ID de usuario inválido"
                self.is_loading = False
                return
            
            # Establecer estado de carga
            self.is_loading = True
            self.has_error = False
            self.error_message = ""
            
            # Cargar datos del usuario desde la base de datos
            success, message, user = get_user_by_id(user_id)
            
            if success and user:
                self.user_data = user
                self.has_error = False
                self.error_message = ""
            else:
                self.has_error = True
                self.error_message = message or "Usuario no encontrado"
                self.user_data = None
            
        except Exception as e:
            self.has_error = True
            self.error_message = f"Error al cargar datos del usuario: {str(e)}"
            self.user_data = None
        
        finally:
            self.is_loading = False
    
    # Propiedades computadas para obtener información formateada del usuario
    @rx.var
    def get_user_full_name(self) -> str:
        """Retorna el nombre completo del usuario."""
        if self.user_data:
            return f"{self.user_data.nombre} {self.user_data.apellido}"
        return "Usuario no encontrado"
    
    @rx.var
    def get_user_email(self) -> str:
        """Retorna el email del usuario."""
        if self.user_data:
            return self.user_data.email
        return ""
    
    @rx.var
    def get_user_role(self) -> str:
        """Retorna el rol del usuario formatado."""
        if self.user_data:
            role_translations = {
                "admin": "Administrador",
                "supervisor": "Supervisor",
                "usuario": "Usuario"
            }
            return role_translations.get(self.user_data.rol, self.user_data.rol.title())
        return ""
    
    @rx.var
    def get_user_dni(self) -> str:
        """Retorna el DNI del usuario formateado."""
        if self.user_data and self.user_data.dni:
            # Formatear DNI con puntos (ej: 12.345.678)
            dni_str = str(self.user_data.dni)
            if len(dni_str) == 8:
                return f"{dni_str[:2]}.{dni_str[2:5]}.{dni_str[5:]}"
            elif len(dni_str) == 7:
                return f"{dni_str[:1]}.{dni_str[1:4]}.{dni_str[4:]}"
            else:
                return dni_str
        return "No especificado"
    
    @rx.var
    def get_user_username(self) -> str:
        """Retorna el nombre de usuario."""
        if self.user_data:
            return self.user_data.nombre_usuario
        return ""
    
    @rx.var
    def get_user_creation_date(self) -> str:
        """Retorna la fecha de creación formateada."""
        if self.user_data and self.user_data.fecha_creacion:
            return self.user_data.fecha_creacion.strftime("%d/%m/%Y")
        return "No disponible"
    
    @rx.var
    def get_user_status(self) -> str:
        """Retorna el estado del usuario (siempre 'Activo' por ahora)."""
        if self.user_data:
            return "Activo"
        return "Inactivo"
    
    @rx.var
    def get_user_role_badge_color(self) -> str:
        """Retorna el color del badge según el rol del usuario."""
        if self.user_data:
            color_mapping = {
                "admin": "red",
                "supervisor": "orange", 
                "usuario": "blue"
            }
            return color_mapping.get(self.user_data.rol, "gray")
        return "gray"
    
    @rx.var
    def has_user_data(self) -> bool:
        """Verifica si hay datos de usuario cargados."""
        return self.user_data is not None
    
    @rx.var
    def get_user_area(self) -> str:
        """Retorna el área del usuario basada en su rol."""
        if self.user_data:
            area_mapping = {
                "admin": "Administración",
                "supervisor": "Supervisión",
                "usuario": "Operaciones"
            }
            return area_mapping.get(self.user_data.rol, "Sin asignar")
        return "Sin asignar"
    
    @rx.var
    def get_user_last_access(self) -> str:
        """Retorna información del último acceso (mock por ahora)."""
        if self.user_data:
            # Por ahora retornamos la fecha de creación como último acceso
            # En el futuro se puede implementar un tracking real de accesos
            return self.get_user_creation_date()
        return "Nunca"


# Componentes dinámicos para perfil de usuario

def dynamic_profile_header() -> rx.Component:
    """Header dinámico del perfil con avatar, nombre y badges usando datos reales."""
    return rx.flex(
        # Avatar grande
        rx.flex(
            avatar_circle(DynamicProfileState.get_user_full_name, size=SizeAvatar.LARGE.value),
            border_radius=BorderRadius.ROUND.value,
            background=Color.secondary.value,
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        
        # Información del usuario
        rx.vstack(
            # Nombre del usuario
            rx.heading(
                DynamicProfileState.get_user_full_name,
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=ColorText.GRAY_800.value,
            ),
            
            # Badges horizontales
            rx.hstack(
                # Badge Rol (color dinámico basado en el rol)
                rx.badge(
                    DynamicProfileState.get_user_role,
                    color_scheme=DynamicProfileState.get_user_role_badge_color,
                    variant="soft",
                    size="2",
                    padding="0.5rem 0.75rem",
                    border_radius=BorderRadius.FULL.value,
                ),
                
                # Badge Estado (siempre verde por ahora)
                rx.badge(
                    DynamicProfileState.get_user_status,
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
        width="100%",
        max_width="800px",
    )

def dynamic_user_info_card() -> rx.Component:
    """Tarjeta de información de usuario dinámica."""
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
                        rx.text(DynamicProfileState.get_user_full_name, font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Nombre de usuario", color=ColorText.GRAY_500.value, size="2"),
                        rx.text(DynamicProfileState.get_user_username, font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("DNI", color=ColorText.GRAY_500.value, size="2"),
                        rx.text(DynamicProfileState.get_user_dni, font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Rol", color=ColorText.GRAY_500.value, size="2"),
                        rx.text(DynamicProfileState.get_user_role, font_weight=FontWeight.MEDIUM.value, size="3"),
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
                            rx.text(DynamicProfileState.get_user_email, font_weight=FontWeight.MEDIUM.value, size="3"),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Área", color=ColorText.GRAY_500.value, size="2"),
                        rx.text(DynamicProfileState.get_user_area, font_weight=FontWeight.MEDIUM.value, size="3"),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Fecha de registro", color=ColorText.GRAY_500.value, size="2"),
                        rx.hstack(
                            rx.icon(tag="calendar", size=SizeIcon.SMALL.value, color=ColorText.GRAY_500.value),
                            rx.text(DynamicProfileState.get_user_creation_date, font_weight=FontWeight.MEDIUM.value, size="3"),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Estado", color=ColorText.GRAY_500.value, size="2"),
                        rx.text(DynamicProfileState.get_user_status, font_weight=FontWeight.MEDIUM.value, size="3"),
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

def loading_state() -> rx.Component:
    """Componente de estado de carga."""
    return rx.center(
        rx.vstack(
            rx.spinner(size="3", color=Color.primary.value),
            rx.text(
                "Cargando información del usuario...",
                color=ColorText.GRAY_500.value,
                font_weight=FontWeight.MEDIUM.value,
                size="3"
            ),
            spacing="4",
            align="center"
        ),
        min_height="400px",
        width="100%"
    )

def error_state() -> rx.Component:
    """Componente de estado de error."""
    return rx.center(
        rx.vstack(
            rx.icon("alert-triangle", size=48, color="red"),
            rx.heading(
                "Error al cargar el perfil",
                size="6",
                color=ColorText.GRAY_800.value,
                font_weight=FontWeight.BOLD.value
            ),
            rx.text(
                DynamicProfileState.error_message,
                color=ColorText.GRAY_500.value,
                size="3",
                text_align="center"
            ),
            rx.button(
                rx.icon("arrow-left", size=SizeIcon.SMALL.value),
                "Volver a usuarios",
                on_click=rx.redirect("/users"),
                variant="soft",
                color_scheme="blue",
                size="3"
            ),
            spacing="4",
            align="center"
        ),
        min_height="400px",
        width="100%",
        padding=SizeSpace.LARGE.value
    )

def back_to_users_button() -> rx.Component:
    """Botón para volver a la página de usuarios."""
    return rx.button(
        rx.icon("arrow-left", size=SizeIcon.SMALL.value),
        "Volver a usuarios",
        on_click=rx.redirect("/users"),
        variant="soft",
        color_scheme="blue",
        size="3",
        margin_bottom=SizeSpace.MEDIUM.value
    )

def dynamic_header_profiles() -> rx.Component:
    """Header dinámico para perfil de usuario específico."""
    return rx.box(
        page_header(
            title=rx.cond(
                DynamicProfileState.has_user_data,
                rx.text("Perfil de ", DynamicProfileState.get_user_full_name),
                "Perfil de Usuario"
            ),
            subtitle="Información detallada del usuario seleccionado",
            back_button=True,
            redirect="/users"
        ),
        width="100%",
        padding=f"{SizeSpace.MEDIUM.value} {SizeSpace.LARGE.value} 0 {SizeSpace.LARGE.value}",
    )

def dynamic_user_profile_page() -> rx.Component:
    """Página dinámica de perfil de usuario que carga datos específicos usando DynamicProfileState."""
    return rx.box(
        rx.hstack(
            sidebar_main(),
            rx.flex(
                # Header dinámico
                dynamic_header_profiles(),
                
                # Contenido principal con estados condicionales
                rx.box(
                    rx.vstack(
                        # Botón volver siempre visible (excepto en loading)
                        rx.cond(
                            ~DynamicProfileState.is_loading,
                            back_to_users_button(),
                            rx.box()  # Espacio vacío cuando está cargando
                        ),
                        
                        # Estados condicionales del contenido
                        rx.cond(
                            DynamicProfileState.is_loading,
                            loading_state(),
                            rx.cond(
                                DynamicProfileState.has_error,
                                error_state(),
                                # Estado de éxito - mostrar perfil completo
                                rx.vstack(
                                    # Header del perfil dinámico
                                    dynamic_profile_header(),
                                    # Información del usuario dinámico
                                    dynamic_user_info_card(),
                                    # Sección de permisos (reutilizamos la existente)
                                    permissions_section(),
                                    spacing="3",
                                    width="100%",
                                    max_width="800px",
                                    align="center"
                                )
                            )
                        ),
                        spacing="0",
                        width="100%",
                        align="center"
                    ),
                    padding=f"{SizeSpace.MEDIUM.value} {SizeSpace.LARGE.value}",
                    width="100%",
                ),
                
                direction="column",
                overflow="hidden",
                flex="1",
                background=Color.background_light.value,
                height="100vh",
            ),
            width="100%",
            height="100vh",
            align="start",
            spacing="0",
        ),
        width="100%",
        height="100vh",
        background=Color.background_light.value
    )

def profiles_page() -> rx.Component:
    """Página principal de perfiles con sistema de tabs."""
    return rx.box(
        rx.hstack(
            sidebar_main(),
            rx.flex(
                header_profiles(),
                permission_views(),
                direction="column",
                overflow="hidden",
                flex="1",
                background=Color.background_light.value,
                height="100vh",
            ),
            width="100%",
            height="100vh",
            align="start",
            spacing="0",
        ),
        width="100%",
        height="100vh",
        background=Color.background_light.value,
    )