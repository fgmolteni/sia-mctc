from fastapi import background
import reflex as rx
from sia.styles.sizes import SizeLogo, SizeSpace, SizeText, SizeButton
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.colors import Color

from sia.components.buttons import button_redondo

from sia.components.headers import name_app_wth_logo, only_isologo

from sia.components.menu_user import menu_user


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            only_isologo(theme="Dark",),
            rx.spacer(),
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    bg="#8A2BE2",
                    border_radius="50%",
                ),
                rx.hstack(rx.text("Personal", font_weight="medium",
                                  color="white", font_size="14px"),
                          rx.badge("adm", var="solid"),
                          ),

                align="center",
                justify="start",
                spacing="3",
                width="100%",
                padding="4px",
            ),

            rx.spacer(),
            # Botones del lado derecho

            menu_user(),
            align_items="center",
            padding_x=SizeSpace.X_LARGE.value,
        ),
        align="center",
        justify="center",
        width="100%",  # Fuerza a ocupar todo el viewport
        left="0",
        right="0",
        position="sticky",  # O "sticky" si prefieres
        top="0",
        z_index=50,
        background=Color.background.value,
        # Elimina paddings laterales si no los necesitas
    ),
