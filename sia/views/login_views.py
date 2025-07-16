import reflex as rx
from components.imagen_open import open_image

img = open_image("/home/subco/project/sia-mctc/assets/logo.png")

def login_default_icons() -> rx.Component:
    return rx.box(
        rx.card(
        rx.vstack(
            # Logo and title
            rx.center(
                
                rx.heading(
                    "Bienvenido",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            # Username input
            rx.vstack(
                rx.text(
                    "Usuario/Email",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                    color="white",
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="user@correo.com",
                    type="email",
                    size="3",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            # Password input
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Contraseña",
                        size="3",
                        weight="medium",
                        color="white",
                    ),
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Ingrese su contraseña",
                    type="password",
                    size="3",
                    width="100%",
                ),
                
                rx.vstack(
                    rx.link(
                        "Olvide mi contraseña",
                        href="#",
                        size="3",
                    ),
                    justify="between",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.button("Sign in", size="3", width="100%"),
            
        ),
        max_width="28em",
        size="5",
        width="100%",
        
        ),
        display="flex",
        flex_direction="column",
        #background_color=rx.color("orange"),
        align="center",
        justify_content="center",   
    )