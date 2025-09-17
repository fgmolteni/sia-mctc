import reflex as rx
from typing import Optional

from sia.views.sidebar import sidebar_main
from sia.components.layout.headers import header_profiles
from sia.styles.colors import Color
from sia.views.layout_profiles import permission_views


class DynamicProfileState(rx.State):
    """Estado para manejar perfiles dinámicos de usuarios."""
    
    # ID del usuario actual
    current_user_id: Optional[int] = None
    
    # Datos del perfil del usuario
    user_profile: dict = {}
    
    # Estado de carga
    is_loading: bool = False
    error_message: str = ""
    
    def load_user_profile(self, user_id: int):
        """Cargar perfil de usuario específico."""
        self.is_loading = True
        self.current_user_id = user_id
        self.error_message = ""
        
        try:
            # TODO: Implementar carga real desde base de datos
            # Por ahora usamos datos de ejemplo
            self.user_profile = {
                "id": user_id,
                "nombre": f"Usuario {user_id}",
                "email": f"usuario{user_id}@mctc.gov.py",
                "rol": "usuario",
                "area": "Ministerio C&T",
                "fecha_creacion": "2024-01-01",
            }
            
        except Exception as e:
            self.error_message = f"Error al cargar perfil: {str(e)}"
        finally:
            self.is_loading = False
    
    def on_load(self):
        """Ejecutar al cargar la página."""
        # Cargar perfil por defecto si hay ID en la ruta
        if self.current_user_id:
            self.load_user_profile(self.current_user_id)


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


def dynamic_user_profile_page() -> rx.Component:
    """Página de perfil dinámico para usuarios específicos."""
    return rx.box(
        rx.hstack(
            sidebar_main(),
            rx.flex(
                # Header dinámico con información del usuario
                rx.box(
                    rx.cond(
                        DynamicProfileState.is_loading,
                        rx.text("Cargando perfil..."),
                        rx.cond(
                            DynamicProfileState.error_message != "",
                            rx.text(
                                DynamicProfileState.error_message,
                                color="red",
                            ),
                            rx.vstack(
                                rx.text(
                                    DynamicProfileState.user_profile["nombre"],
                                    font_size="1.5em",
                                    font_weight="bold",
                                ),
                                rx.text(
                                    DynamicProfileState.user_profile["email"],
                                    color="gray",
                                ),
                                spacing="2",
                                align="start",
                            ),
                        ),
                    ),
                    padding="1rem",
                    border_bottom="1px solid #E5E7EB",
                ),
                # Contenido del perfil
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
        on_mount=DynamicProfileState.on_load,
    )
