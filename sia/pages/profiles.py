import reflex as rx

from sia.views.sidebar import sidebar_main
from sia.components.layout.headers import page_header, header_profiles
from sia.views.layout_profiles import (
    ProfileState,
    profile_header,
    user_info_card,
    permissions_section
)
from sia.styles.sizes import SizeSpace
from sia.styles.colors import Color, ColorText
from sia.views.layout_profiles import permission_views
from sia.components.layout.headers import header_profiles


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