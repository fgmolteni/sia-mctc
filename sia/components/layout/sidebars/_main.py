import reflex as rx

from sia.views.login_views import LoginState
from sia.components.data_display.avatars.avatar_circle import avatar_circle
from sia.components.data_display.badges.enhanced_badges import enhanced_role_badge
from sia.components.data_display.cards.profile_cards import info_card_profile
from sia.styles.sizes import SizeText
from sia.styles.colors import ColorText
from sia.styles.fonts import FontWeight


def sidebar_header() -> rx.Component:
    """The header of the sidebar."""
    return rx.vstack(
        rx.hstack(
            rx.icon("layout-grid", size=28),
            rx.vstack(
                rx.heading("SIA", size="5"),
                # rx.text("Gestión Empresarial", size="2", color_scheme="gray"),
                align_items="flex-start",
                spacing="1",
            ),
            align="center",
            justify="center",
            spacing="2",
        ),
        align="center",
        justify="center",
        padding="1rem",
        width="100%",

    )


def sidebar_section(title: str) -> rx.Component:
    """A section title for the sidebar."""
    return rx.text(
        title,
        size="2",
        weight="medium",
        padding="0.75rem 1rem",
        color_scheme="gray",
    )


def sidebar_item(
    text: str, icon: str, href: str, is_active: bool = False
) -> rx.Component:
    """A single item in the sidebar."""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20),
            rx.text(text, size="3"),
            width="100%",
            padding="0.75rem 1rem",
            align="center",
            spacing="3",
            bg=rx.cond(is_active, rx.color("accent", 4), "transparent"),
            color=rx.cond(is_active, rx.color("accent", 11), rx.color("gray", 11)),
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border_radius": "0.375rem",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_sub_item(text: str, href: str, is_active: bool = False) -> rx.Component:
    """A sub-item for a collapsible sidebar section."""
    return rx.link(
        rx.hstack(
            rx.text(text, size="3"),
            width="100%",
            padding="0.5rem 1rem",
            padding_left="3.5rem",  # Indent sub-items
            align="center",
            bg=rx.cond(is_active, rx.color("accent", 4), "transparent"),
            color=rx.cond(is_active, rx.color("accent", 11), rx.color("gray", 11)),
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border_radius": "0.375rem",
            },
        ),
        href=href,
        underline="none",
        width="100%",
    )


def sidebar_collapsible_item(text: str, icon: str, sub_items: list) -> rx.Component:
    """A collapsible item in the sidebar with sub-items."""
    return rx.accordion.root(
        rx.accordion.item(
            value=text,
            header=rx.accordion.trigger(
                rx.hstack(
                    rx.icon(icon, size=20),
                    rx.text(text, size="3", weight="medium"),
                    rx.spacer(),
                    width="100%",
                    padding="0.75rem 1rem",
                    align="center",
                    spacing="3",
                    color=rx.color("gray", 11),
                    style={
                        "_hover": {
                            "bg": rx.color("accent", 4),
                            "color": rx.color("accent", 11),
                        },
                        "border_radius": "0.375rem",
                    },
                ),
            ),
            content=rx.vstack(
                *[
                    sidebar_sub_item(item["text"], item["href"])
                    for item in sub_items
                ],
                spacing="1",
                width="100%",
                padding_y="0.5rem",
            ),
        ),
        collapsible=True,
        width="100%",
        type="single",
    )


def sidebar_footer() -> rx.Component:
    """
    Footer mejorado del sidebar con información dinámica del usuario usando variables de Reflex.
    Integra componentes del sistema de diseño y funcionalidad completamente reactiva.
    """
    return rx.cond(
        LoginState.is_logged_in,
        # Usuario logueado - mostrar información completa
        rx.vstack(
            rx.divider(),
            rx.hstack(
                # Avatar dinámico usando variables de Reflex con fallback
                avatar_circle(
                    name=rx.cond(
                        LoginState.user_name != "",
                        LoginState.user_name,
                        "Usuario"
                    ),
                    size="40px",
                ),
                # Información del usuario con variables reactivas y fallbacks
                rx.vstack(
                    # Nombre del usuario (reactivo) con fallback
                    rx.text(
                        rx.cond(
                            LoginState.user_name != "",
                            LoginState.user_name,
                            "Usuario"
                        ),
                        font_weight=FontWeight.MEDIUM.value,
                        font_size=SizeText.MEDIUM.value,
                        color=ColorText.GRAY_800.value,
                        white_space="nowrap",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        max_width="140px",
                    ),
                    # Rol con badge mejorado usando rx.match
                    rx.match(
                        LoginState.user_role,
                        ("admin", 
                            enhanced_role_badge(
                                text="Admin",
                                role="admin",
                                show_icon=True,
                            )
                        ),
                        ("supervisor",
                            enhanced_role_badge(
                                text="Manager", 
                                role="supervisor",
                                show_icon=True,
                            )
                        ),
                        ("usuario",
                            enhanced_role_badge(
                                text="Usuario",
                                role="usuario", 
                                show_icon=True,
                            )
                        ),
                        # Caso por defecto con fallback mejorado
                        enhanced_role_badge(
                            text="Usuario",
                            role="usuario",
                            show_icon=True,
                        )
                    ),
                    spacing="2",
                    align="start",
                    flex="1",
                ),
                # Menú contextual mejorado
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.icon("more-vertical", size=16),
                            variant="ghost",
                            size="2",
                            title="Opciones de usuario",
                        ),
                    ),
                    rx.menu.content(
                        # Información dinámica del usuario con fallbacks usando rx.box
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    rx.cond(
                                        LoginState.user_email != "",
                                        LoginState.user_email,
                                        "Sin email"
                                    ),
                                    font_size=SizeText.SMALL.value,
                                    color=ColorText.GRAY_500.value,
                                ),
                                rx.text(
                                    rx.cond(
                                        LoginState.last_access != "",
                                        "Último acceso: " + LoginState.last_access,
                                        "Primer acceso"
                                    ),
                                    font_size=SizeText.X_SMALL.value,
                                    color=ColorText.GRAY_500.value,
                                ),
                                spacing="1",
                                align="start",
                            ),
                            padding="8px 12px",
                            border_bottom="1px solid",
                            border_color=ColorText.GRAY_500.value,
                        ),
                        rx.menu.separator(),
                        # Enlace al perfil usando ID dinámico con validación
                        rx.cond(
                            LoginState.current_user_id > 0,
                            rx.menu.item(
                                "Mi Perfil",
                                icon="user",
                                on_click=rx.redirect("/users/profile/" + LoginState.current_user_id.to_string()),
                            ),
                            rx.menu.item(
                                "Perfil no disponible",
                                icon="user",
                                disabled=True,
                            ),
                        ),
                        rx.menu.item(
                            "Configuración",
                            icon="settings", 
                            on_click=rx.redirect("/settings"),
                        ),
                        rx.menu.separator(),
                        # Logout funcional
                        rx.menu.item(
                            "Cerrar Sesión",
                            icon="log-out",
                            on_click=LoginState.handle_logout,
                            color_scheme="red",
                        ),
                    ),
                ),
                width="100%",
                align="center", 
                spacing="3",
                padding="1rem",
            ),
            width="100%",
        ),
        # Usuario no logueado - mostrar login rápido
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.text(
                    "Iniciar sesión",
                    font_size=SizeText.SMALL.value,
                    color=ColorText.GRAY_500.value,
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("log-in", size=16),
                    on_click=rx.redirect("/login"),
                    variant="ghost",
                    size="2",
                ),
                width="100%",
                align="center",
                padding="1rem",
            ),
            width="100%",
        )
    )


def sidebar_footer_expanded() -> rx.Component:
    """
    Footer expandido del sidebar usando variables de Reflex y info_card_profile completo.
    Alternativa para interfaces que requieren información detallada del usuario.
    """
    return rx.cond(
        LoginState.is_logged_in,
        # Usuario logueado - versión expandida
        rx.vstack(
            rx.divider(),
            rx.box(
                info_card_profile(
                    name=LoginState.user_name,
                    email=LoginState.user_email,
                    role=rx.match(
                        LoginState.user_role,
                        ("admin", "Administrador"),
                        ("supervisor", "Supervisor"),
                        ("usuario", "Usuario"),
                        "Usuario",  # Fallback por defecto
                    ),
                    area="Ministerio C&T",
                    avatar_initial=LoginState.avatar_initial,
                    status="Activo",
                ),
                padding="1rem",
                width="100%",
            ),
            # Panel de acciones rápidas con variables reactivas
            rx.hstack(
                rx.button(
                    rx.icon("user", size=16),
                    "Perfil",
                    on_click=rx.redirect("/users/profile/" + LoginState.current_user_id.to_string()),
                    variant="ghost",
                    size="2",
                    flex="1",
                ),
                rx.button(
                    rx.icon("log-out", size=16),
                    "Salir",
                    on_click=LoginState.handle_logout,
                    variant="ghost",
                    size="2",
                    color_scheme="red",
                    flex="1",
                ),
                width="100%",
                padding="0 1rem 1rem 1rem",
                spacing="2",
            ),
            width="100%",
        ),
        # Usuario no logueado - versión compacta para login
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.text(
                    "Necesitas iniciar sesión",
                    font_size=SizeText.SMALL.value,
                    color=ColorText.GRAY_500.value,
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("log-in", size=16),
                    "Login",
                    on_click=rx.redirect("/login"),
                    variant="outline",
                    size="2",
                ),
                width="100%",
                align="center",
                padding="1rem",
            ),
            width="100%",
        )
    )
