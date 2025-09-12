import reflex as rx
from sia.pages.profiles import DynamicProfileState

def debug_profile_page() -> rx.Component:
    """Página de debug para mostrar el estado del DynamicProfileState."""
    return rx.vstack(
        rx.heading("🔍 Debug de DynamicProfileState", size="6"),
        
        rx.divider(),
        
        rx.heading("📋 Estados del Sistema", size="4"),
        rx.vstack(
            rx.hstack(
                rx.text("current_user_id: ", font_weight="bold"),
                rx.cond(
                    DynamicProfileState.current_user_id.is_none(),
                    rx.text("None", color="gray"),
                    rx.text(DynamicProfileState.current_user_id)
                ),
                spacing="1"
            ),
            rx.hstack(
                rx.text("is_loading: ", font_weight="bold"),
                rx.cond(
                    DynamicProfileState.is_loading,
                    rx.text("True", color="blue"),
                    rx.text("False", color="green")
                ),
                spacing="1"
            ),
            rx.hstack(
                rx.text("error_message: ", font_weight="bold"),
                rx.cond(
                    DynamicProfileState.error_message != "",
                    rx.text(DynamicProfileState.error_message, color="red"),
                    rx.text("(sin errores)", color="green")
                ),
                spacing="1"
            ),
            rx.hstack(
                rx.text("has_user_profile: ", font_weight="bold"),
                rx.cond(
                    DynamicProfileState.user_profile != {},
                    rx.text("True", color="green"),
                    rx.text("False", color="gray")
                ),
                spacing="1"
            ),
            align="start",
            spacing="2"
        ),
        
        rx.divider(),
        
        rx.heading("👤 Datos del Usuario", size="4"),
        rx.cond(
            DynamicProfileState.user_profile != {},
            rx.vstack(
                rx.hstack(
                    rx.text("ID: ", font_weight="bold"),
                    rx.text(DynamicProfileState.user_profile["id"]),
                    spacing="1"
                ),
                rx.hstack(
                    rx.text("Nombre: ", font_weight="bold"),
                    rx.text(DynamicProfileState.user_profile["nombre"]),
                    spacing="1"
                ),
                rx.hstack(
                    rx.text("Email: ", font_weight="bold"),
                    rx.text(DynamicProfileState.user_profile["email"]),
                    spacing="1"
                ),
                rx.hstack(
                    rx.text("Rol: ", font_weight="bold"),
                    rx.text(DynamicProfileState.user_profile["rol"]),
                    spacing="1"
                ),
                rx.hstack(
                    rx.text("Área: ", font_weight="bold"),
                    rx.text(DynamicProfileState.user_profile["area"]),
                    spacing="1"
                ),
                rx.hstack(
                    rx.text("Fecha creación: ", font_weight="bold"),
                    rx.text(DynamicProfileState.user_profile["fecha_creacion"]),
                    spacing="1"
                ),
                align="start",
                spacing="2"
            ),
            rx.text("❌ No hay datos de usuario cargados", color="red")
        ),
        
        rx.divider(),
        
        rx.heading("🔧 Acciones", size="4"),
        rx.hstack(
            rx.button(
                "Cargar manualmente",
                on_click=DynamicProfileState.on_load,
                color_scheme="blue"
            ),
            rx.button(
                "Cargar usuario ID 15",
                on_click=DynamicProfileState.load_user_profile(15),
                color_scheme="green"
            ),
            rx.button(
                "Cargar usuario ID 25",
                on_click=DynamicProfileState.load_user_profile(25),
                color_scheme="purple"
            ),
            spacing="4"
        ),
        
        spacing="6",
        padding="2rem",
        width="100%",
        max_width="800px",
        margin="0 auto"
    )