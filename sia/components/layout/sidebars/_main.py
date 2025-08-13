import reflex as rx

# from sia.views.login_views import LoginState
from sia.components.data_display.avatars import avatar
from sia.styles.sizes import SizeAvatar


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
    """The footer of the sidebar."""
    return rx.vstack(
        rx.divider(),
        rx.hstack(
            rx.menu.root(
                rx.menu.trigger(
                    avatar(user="Gabriel", title="gabriel@empresa.com", size=SizeAvatar.SMALL.value),
                ),
                rx.menu.content(
                    rx.menu.item("Perfil", icon="user"),
                    rx.menu.item(
                        "Cerrar Sesión",
                        icon="log-out",
                        # on_click=LoginState.handle_logout,
                        variant="ghost",
                    ),
                ),
            ),
            rx.spacer(),
            rx.button(
                rx.icon("log-out", size=20),
                # on_click=LoginState.handle_logout,
                variant="ghost",
            ),
            width="100%",
            align="center",
            padding="1rem",
        ),
        width="100%",
    )
