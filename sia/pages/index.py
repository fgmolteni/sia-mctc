import reflex as rx
from sia.views.sidebar import sidebar_main
#from sia.pages.usuarios import users_page

def index() -> rx.Component:
    return rx.hstack(
        sidebar_main(),
        rx.box(

            rx.heading("Bienvenidos al Sistema Interno de Administración", size="8"),
            rx.text("Ministerio de Ciencia y Tecnología"),
            align="center",
            justify="center",
            width="100%",
            padding="2rem",
        ),
        spacing="7",
        width="100%",
        height="100vh",
        background=rx.color("gray", 2),
    )