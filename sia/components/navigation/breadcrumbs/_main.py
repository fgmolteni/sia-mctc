import reflex as rx
from typing import Optional
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, SizeIcon, SizeText
from sia.styles.fonts import FontWeight
from sia.styles.border import BorderRadius


def profile_breadcrumbs(
    user_name: str = "",
    user_id: str = "",
    show_user_info: bool = True,
    back_url: str = "/users"
) -> rx.Component:
    """
    Breadcrumbs específicos para páginas de perfil de usuario.
    
    Args:
        user_name: Nombre completo del usuario
        user_id: ID del usuario
        show_user_info: Si mostrar información adicional del usuario
        back_url: URL de retorno (por defecto /users)
    """
    return rx.box(
        rx.hstack(
            # Breadcrumbs principales usando hstack
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon("home", size=SizeIcon.SMALL.value),
                        "Inicio",
                        spacing="2",
                        align="center"
                    ),
                    href="/dashboard",
                    color=ColorText.GRAY_500.value,
                    _hover={"color": ColorText.GRAY_700.value}
                ),
                rx.icon("chevron-right", size=12, color=ColorText.GRAY_500.value),
                rx.link(
                    rx.hstack(
                        rx.icon("users", size=SizeIcon.SMALL.value),
                        "Usuarios", 
                        spacing="2",
                        align="center"
                    ),
                    href=back_url,
                    color=ColorText.GRAY_500.value,
                    _hover={"color": ColorText.GRAY_700.value}
                ),
                rx.icon("chevron-right", size=12, color=ColorText.GRAY_500.value),
                rx.hstack(
                    rx.icon("user", size=SizeIcon.SMALL.value),
                    rx.text(
                        user_name if user_name else f"Usuario #{user_id}" if user_id else "Perfil",
                        color=ColorText.GRAY_800.value,
                        font_weight=FontWeight.MEDIUM.value,
                        max_width="200px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap"
                    ),
                    spacing="2",
                    align="center"
                ),
                spacing="2",
                align="center"
            ),
            
            # Información adicional del usuario (opcional)
            rx.cond(
                show_user_info and user_id,
                rx.hstack(
                    rx.box(width="1px", height="20px", background=ColorText.GRAY_500.value),
                    rx.badge(
                        f"ID: {user_id}",
                        variant="soft",
                        color_scheme="gray",
                        size="1",
                        padding="0.25rem 0.5rem"
                    ),
                    spacing="3",
                    align="center"
                )
            ),
            
            spacing="4",
            align="center",
            flex_wrap="wrap"
        ),
        padding=f"{SizeSpace.MEDIUM.value} {SizeSpace.LARGE.value}",
        background=Color.background.value,
        border_bottom=f"1px solid {Color.border_light.value}",
        width="100%"
    )


def dynamic_breadcrumbs(
    user_name: rx.Var[str],
    user_id: rx.Var[str],
    is_loading: rx.Var[bool] = False,
    has_error: rx.Var[bool] = False,
    back_url: str = "/users"
) -> rx.Component:
    """
    Breadcrumbs dinámicos que se actualizan según el estado del perfil.
    
    Args:
        user_name: Variable reactiva con el nombre del usuario
        user_id: Variable reactiva con el ID del usuario  
        is_loading: Variable reactiva de estado de carga
        has_error: Variable reactiva de estado de error
        back_url: URL de retorno
    """
    return rx.box(
        rx.hstack(
            # Breadcrumbs principales usando hstack
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon("home", size=SizeIcon.SMALL.value),
                        "Inicio",
                        spacing="2",
                        align="center"
                    ),
                    href="/dashboard",
                    color=ColorText.GRAY_500.value,
                    _hover={"color": ColorText.GRAY_700.value}
                ),
                rx.icon("chevron-right", size=12, color=ColorText.GRAY_500.value),
                rx.link(
                    rx.hstack(
                        rx.icon("users", size=SizeIcon.SMALL.value),
                        "Usuarios", 
                        spacing="2",
                        align="center"
                    ),
                    href=back_url,
                    color=ColorText.GRAY_500.value,
                    _hover={"color": ColorText.GRAY_700.value}
                ),
                rx.icon("chevron-right", size=12, color=ColorText.GRAY_500.value),
                rx.hstack(
                    rx.icon("user", size=SizeIcon.SMALL.value),
                    
                    # Contenido dinámico basado en estado
                    rx.cond(
                        is_loading,
                        rx.hstack(
                            rx.spinner(size="1", color=ColorText.GRAY_500.value),
                            rx.text(
                                "Cargando...",
                                color=ColorText.GRAY_500.value,
                                font_style="italic"
                            ),
                            spacing="2",
                            align="center"
                        ),
                        rx.cond(
                            has_error,
                            rx.text(
                                "Error al cargar",
                                color=Color.error.value,
                                font_weight=FontWeight.MEDIUM.value
                            ),
                            rx.text(
                                rx.cond(
                                    user_name != "",
                                    user_name,
                                    rx.cond(
                                        user_id != "",
                                        f"Usuario #{user_id}",
                                        "Perfil"
                                    )
                                ),
                                color=ColorText.GRAY_800.value,
                                font_weight=FontWeight.MEDIUM.value,
                                max_width="200px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap"
                            )
                        )
                    ),
                    
                    spacing="2",
                    align="center"
                ),
                spacing="2",
                align="center"
            ),
            
            # Estado visual y acciones rápidas
            rx.hstack(
                rx.box(width="1px", height="20px", background=ColorText.GRAY_500.value),
                
                # Indicador de estado
                rx.cond(
                    is_loading,
                    rx.badge(
                        rx.icon("loader", size=10, className="animate-spin"),
                        "Cargando",
                        variant="soft",
                        color_scheme="blue",
                        size="1",
                        spacing="1"
                    ),
                    rx.cond(
                        has_error,
                        rx.badge(
                            rx.icon("triangle-alert", size=10),
                            "Error",
                            variant="soft", 
                            color_scheme="red",
                            size="1",
                            spacing="1"
                        ),
                        rx.cond(
                            user_id != "",
                            rx.badge(
                                f"ID: {user_id}",
                                variant="soft",
                                color_scheme="green",
                                size="1"
                            )
                        )
                    )
                ),
                
                # Botón de acción rápida
                rx.cond(
                    has_error,
                    rx.button(
                        rx.icon("refresh-cw", size=12),
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                        title="Reintentar carga"
                    ),
                    rx.cond(
                        user_name != "",
                        rx.button(
                            rx.icon("external-link", size=12),
                            size="1", 
                            variant="ghost",
                            color_scheme="gray",
                            title="Abrir en nueva ventana"
                        )
                    )
                ),
                
                spacing="2",
                align="center"
            ),
            
            spacing="4",
            align="center",
            flex_wrap="wrap",
            justify="between"
        ),
        padding=f"{SizeSpace.SMALL.value} {SizeSpace.LARGE.value}",
        background=Color.background.value,
        border_bottom=f"1px solid {Color.border_light.value}",
        width="100%",
        position="sticky",
        top="0",
        z_index="10",
        backdrop_filter="blur(8px)"
    )