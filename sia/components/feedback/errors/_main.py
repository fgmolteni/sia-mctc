import reflex as rx
from typing import Optional, Callable
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, SizeIcon, SizeText
from sia.styles.fonts import FontWeight
from sia.styles.border import BorderRadius, CommonBorders


def contextual_error(
    title: str,
    message: str,
    error_type: str = "generic",
    primary_action: Optional[tuple] = None,
    secondary_action: Optional[tuple] = None,
    show_details: bool = False,
    details: str = ""
) -> rx.Component:
    """
    Componente de error contextualizado.
    
    Args:
        title: Título del error
        message: Mensaje principal del error
        error_type: Tipo de error (network, not_found, permission, generic)
        primary_action: Tupla (texto, función) para acción principal
        secondary_action: Tupla (texto, función) para acción secundaria
        show_details: Si mostrar detalles técnicos
        details: Detalles técnicos del error
    """
    
    # Configuración por tipo de error
    error_configs = {
        "network": {
            "icon": "wifi-off",
            "color": "orange",
            "bg_color": Color.warning.value + "20",
            "border_color": Color.warning.value
        },
        "not_found": {
            "icon": "user-x",
            "color": "blue", 
            "bg_color": Color.info.value + "20",
            "border_color": Color.info.value
        },
        "permission": {
            "icon": "shield-alert",
            "color": "red",
            "bg_color": Color.error.value + "20",
            "border_color": Color.error.value
        },
        "generic": {
            "icon": "alert-triangle",
            "color": "gray",
            "bg_color": Color.background_light.value,
            "border_color": Color.border_light.value
        }
    }
    
    config = error_configs.get(error_type, error_configs["generic"])
    
    return rx.center(
        rx.card(
            rx.vstack(
                # Header con icono y título
                rx.vstack(
                    rx.box(
                        rx.icon(
                            config["icon"], 
                            size=48,
                            color=config["color"]
                        ),
                        padding=SizeSpace.MEDIUM.value,
                        background=config["bg_color"],
                        border_radius=BorderRadius.ROUND.value,
                        border=f"2px solid {config['border_color']}"
                    ),
                    rx.heading(
                        title,
                        size="6",
                        color=ColorText.GRAY_800.value,
                        font_weight=FontWeight.BOLD.value,
                        text_align="center"
                    ),
                    align="center",
                    spacing="4"
                ),
                
                # Mensaje principal
                rx.text(
                    message,
                    color=ColorText.GRAY_500.value,
                    size="3",
                    text_align="center",
                    max_width="400px",
                    line_height="1.6"
                ),
                
                # Detalles técnicos (opcional)
                rx.cond(
                    show_details & (details != ""),
                    rx.box(
                        rx.text(
                            "Detalles técnicos:",
                            color=ColorText.GRAY_500.value,
                            size="2",
                            font_weight=FontWeight.MEDIUM.value,
                            margin_bottom=SizeSpace.SMALL.value
                        ),
                        rx.code(
                            details,
                            background=Color.background_light.value,
                            padding=SizeSpace.SMALL.value,
                            border_radius=BorderRadius.MEDIUM.value,
                            width="100%",
                            font_size="0.8rem",
                            color=ColorText.GRAY_700.value
                        ),
                        margin_top=SizeSpace.SMALL.value
                    )
                ),
                
                # Botones de acción
                rx.hstack(
                    # Acción secundaria (si existe)
                    rx.cond(
                        secondary_action is not None,
                        rx.button(
                            secondary_action[0] if secondary_action else "",
                            on_click=secondary_action[1] if secondary_action else rx.noop,
                            variant="soft",
                            color_scheme="gray",
                            size="3"
                        ) if secondary_action else rx.fragment()
                    ),
                    
                    # Acción principal (si existe)
                    rx.cond(
                        primary_action is not None,
                        rx.button(
                            rx.icon("arrow-left", size=SizeIcon.SMALL.value),
                            primary_action[0] if primary_action else "",
                            on_click=primary_action[1] if primary_action else rx.noop,
                            variant="solid",
                            color_scheme=config["color"],
                            size="3"
                        ) if primary_action else rx.fragment()
                    ),
                    
                    spacing="3",
                    justify="center"
                ),
                
                spacing="6",
                align="center",
                max_width="500px"
            ),
            padding=f"{SizeSpace.X_LARGE.value}",
            border_radius=BorderRadius.LARGE.value,
            background=Color.background.value,
            border=CommonBorders.LIGHT_SOLID,
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
        ),
        min_height="400px",
        width="100%",
        padding=SizeSpace.LARGE.value
    )


def network_error_with_retry(
    retry_action: Callable = None,
    attempts=0,
    max_attempts=3
) -> rx.Component:
    """Error de red con retry automático."""
    return contextual_error(
        title="Error de conexión",
        message=rx.cond(
            attempts > 0,
            f"No se pudo cargar la información del usuario. Intento {attempts}/{max_attempts}.",
            "No se pudo cargar la información del usuario."
        ),
        error_type="network",
        primary_action=("Reintentar", retry_action or rx.noop),
        secondary_action=("Volver a usuarios", rx.redirect("/users")),
        show_details=attempts >= 2,
        details=f"Error de red después de varios intentos. Verifique su conexión a internet."
    )


def user_not_found_error(
    user_id: str = "",
    back_action: Callable = None
) -> rx.Component:
    """Error específico para usuario no encontrado."""
    return contextual_error(
        title="Usuario no encontrado",
        message=rx.cond(
            user_id != "",
            f"El usuario con ID {user_id} no existe o no tienes permisos para verlo.",
            "El usuario solicitado no existe o no tienes permisos para verlo."
        ),
        error_type="not_found",
        primary_action=("Ver todos los usuarios", back_action or rx.redirect("/users")),
        secondary_action=("Reportar problema", rx.noop),
        show_details=(user_id != ""),
        details=rx.cond(user_id != "", f"ID de usuario: {user_id}", "")
    )


def generic_error_with_actions(
    error_message: str,
    technical_details: str = "",
    retry_action: Callable = None
) -> rx.Component:
    """Error genérico con acciones contextuales."""
    return contextual_error(
        title="Error al cargar el perfil", 
        message=rx.cond(error_message != "", error_message, "Ocurrió un error inesperado al cargar la información."),
        error_type="generic",
        primary_action=("Volver a usuarios", rx.redirect("/users")),
        secondary_action=("Reintentar", retry_action),
        show_details=(technical_details != ""),
        details=technical_details
    )