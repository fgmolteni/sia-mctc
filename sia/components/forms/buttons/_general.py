from typing import Callable

import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.sizes import BorderRadius, SizeSpace


def button_general(text: str, on_click: Callable = None) -> rx.Component:
    return rx.button(
        text,
        on_click=on_click,
    )


def button_redondo(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.button(
            rx.text(
                text,
                font_family=FontFamily.DEFAULT.value,
                font_weight=FontWeight.MEDIUM.value,
                color=ColorText.PRIMARY.value,
            ),
            variant="outline",
            # color_scheme= Color.info.value,
            border_radius=BorderRadius.DEFAULT.value,
            border=F"1px solid {ColorText.PRIMARY.value}",
            bg=Color.background.value,
            _hover={
                "bg": Color.primary.value,
                "color": ColorText.PRIMARY.value,
                "border": f"1px solid {ColorText.SECONDARY.value}",
            },
            px="16px",
            py="8px",
            width="100%",
        ),
        href=url,
        padding=SizeSpace.SMALL.value,
        width="100%",
    )


def button_sin_fondo(text: str):
    return rx.link(
        rx.button(
            "Feedback",
            size="1",
            variant="ghost",
            color_scheme="gray",
            font_family=FontFamily.DEFAULT.value,
            font_weight="500",
            color="#9ca3af",
            bg="transparent",
            _hover={"bg": Color.background.value, "color": ColorText.PRIMARY.value},
            px="16px",
            py="8px",
            font_size="14px",
            width="100%",
        ),
        width="100%",
    )


def form_button(text: str, on_click=None) -> rx.Component:
    return rx.button(text, type_="submit", on_click=on_click)


def form_reset_button(text: str) -> rx.Component:
    return rx.button(text, type_="reset")
