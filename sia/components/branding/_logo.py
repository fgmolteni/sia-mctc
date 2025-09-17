import reflex as rx
from sia.styles.sizes import BorderRadius, SizeLogo, SizeText, SizeSpace
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.colors import Color, ColorText
from components.imagen_open import open_image

img = open_image(r"./assets/logo.png")


def name_app_wth_logo() -> rx.Component:
    """
    Componente de branding con logo a la izquierda y textos apilados verticalmente.
    Diseñado para mantener centrado y responsivo siguiendo las reglas del proyecto SIA.
    
    Returns:
        rx.Component: Logo y textos alineados horizontalmente y centrados
    """
    return rx.box(
        rx.hstack(
            # Logo a la izquierda
            rx.image(
                src=img,
                #width=SizeLogo.MEDIUM.value,
                height=SizeLogo.MEDIUM.value,
                border_radius="100%",
                background_color="white",
                flex_shrink="0",  # Evita que el logo se comprima
            ),
            # Textos apilados verticalmente al lado del logo
            rx.flex(
                rx.text(
                    "SIA",
                    font_size=SizeText.LARGE.value,
                    font_family=FontFamily.PLASTER.value,
                    font_weight=FontWeight.BOLD.value,
                    line_height="1.2",
                    margin="0",
                ),
                rx.spacer(),  # Espacio pequeño entre los textos
                rx.text(
                    "Sistema Interno de Administración",
                    font_size=SizeText.X_SMALL.value,
                    color=ColorText.GRAY_500.value,
                    font_family=FontFamily.PLASTER.value,
                    font_weight=FontWeight.NORMAL.value,
                    line_height="1.3",
                    margin="0",
                ),
                direction="column",  # Apilamiento vertical
                align="start",  # Alineación izquierda de los textos
                justify="center",  # Centrado vertical de los textos
            ),
            align="center",  # Centrado vertical de todo el contenido
            justify="start",  # Alineación horizontal desde la izquierda
            width="100%",  # Ocupa todo el ancho disponible
        ),
        display="flex",
        align_items="center",  # Asegura el centrado vertical del contenedor
        justify_content="center",  # Centra todo el componente horizontalmente
        width="100%",
        padding=SizeSpace.SMALL.value,  # Padding interno para respiración visual
    )


def only_isologo(theme: str) -> rx.Component:
    if theme == "Dark":
        background = Color.background.value
        text_color = ColorText.PRIMARY.value
    else:
        background = Color.background.value
        text_color = ColorText.TERCEARY.value

    return rx.box(
        rx.hstack(
            rx.text(
                "S",
                font_family=FontFamily.SPACE_MONO.value,
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=text_color,
            ),
            rx.text(
                "i",
                font_family=FontFamily.SPACE_MONO.value,
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                font_style="italic",
                color=ColorText.ACCENT.value,
            ),
            rx.text(
                "A",
                font_family=FontFamily.SPACE_MONO.value,
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=text_color,
            ),
            spacing="0",
            align_items="center",
            margin_left=SizeSpace.SMALL.value,
            padding=SizeSpace.SMALL.value,
        ),
        align="center",
        background=background,
        border=BorderRadius.SMALL.value,
        padding=SizeSpace.SMALL.value,
    )
