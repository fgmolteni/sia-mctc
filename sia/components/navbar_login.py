import reflex as rx

from sia.styles.colors import Color
from sia.styles.sizes import SizeLogo, SizeText
from sia.styles.fonts import FontFamily, FontWeight

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value), href=url
    )

def navbar_user() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        width=SizeLogo.MEDIUM.value,
                        height="auto",
                        border_radius="50%",
                        background_color="white",
                    ),
                    rx.text(
                        "SIA",
                        font_size=SizeText.X_LARGE.value,
                        font_family=FontFamily.DEFAULT.value,
                        font_weight= FontWeight.MEDIUM.value,
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
                        width=SizeLogo.MEDIUM.value,
                        height="auto",
                        border_radius="full",
                        background_color="white",
                    ),
                    rx.heading(
                        "Reflex", font_size=SizeText.X_LARGE.value, 
                        font_weight=FontWeight.BOLD.value,
                    ),
                    align_items="center",

                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon(tag="user"),
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
        background=Color.background.value,
        padding="1em",
        position="fixed",
        top="0px",
        z_index="1",
        width="100%",
        opacity="0.8",
    )