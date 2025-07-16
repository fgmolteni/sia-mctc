from fastapi import background
import reflex as rx
from components.imagen_open import open_image

from sia.styles.colors import Color

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )

img = open_image(r"./assets/logo.png")

def navbar_user() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src=img,
                        width="2em",
                        height="auto",
                        border_radius="50%",
                        background_color="white",
                    ),
                    rx.text(
                        "SIA", 
                        size="8", 
                        #weight="200", 
                        font_family="Inter",
                        
                    ),
                    align_items="center",
                    margin_left="10em",
                    padding="0.2em",
                ),
                #background="blue",
            )
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src=r"/assets/logo1.svg",
                        width="2.5em",
                        height="auto",
                        border_radius="full",
                        background_color="white",
                    ),
                    rx.heading(
                        "Reflex", size="6", weight="bold",
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon("user"),
                            size="2",
                            radius="full",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item("Settings"),
                        rx.menu.item("Earnings"),
                        rx.menu.separator(),
                        rx.menu.item("Log out"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        background="black",
        padding="1em",
        position="fixed",
        top="0px",
        z_index="1",
        width="100%",
    )