import reflex as rx
from components.imagen_open import open_image
from sia.components.forms.buttons import button_general
from sia.styles.colors import ColorText
from sia.styles.sizes import SizeText
from sia.styles.fonts import FontWeight
from components.db_users import verify_user

img = open_image("/home/subco/project/sia-mctc/assets/logo.png")

class LoginState(rx.State):
    """Estado para manejar el formulario de login."""
    email: str = ""
    password: str = ""
    error_message: str = ""
    is_logged_in: bool = False

    async def handle_login(self):
        """Maneja el intento de login."""
        user_id = verify_user(self.email, self.password)
        if user_id:
            self.is_logged_in = True
            self.error_message = ""
            # Redirigir a la página principal o dashboard
            return rx.redirect("/")
        else:
            self.error_message = "Usuario o contraseña incorrectos."
            self.is_logged_in = False

    def handle_logout(self):
        self.is_logged_in = False
        return rx.redirect("/login")

    

def login_default_icons() -> rx.Component:
    return rx.box(
        rx.card(
            rx.vstack(
                # Logo and title
                rx.center(
                    rx.heading(
                        "Bienvenido",
                        font_size=SizeText.X_LARGE.value,
                        as_="h2",
                        text_align="center",
                        width="100%",
                        font_weight=FontWeight.BOLD.value,
                        color=ColorText.PRIMARY.value,
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                # Username input
                rx.vstack(
                    rx.text(
                        "Usuario/Email",
                        font_size=SizeText.MEDIUM.value,
                        font_weight=FontWeight.MEDIUM.value,
                        text_align="left",
                        width="100%",
                        color=ColorText.PRIMARY.value,
                    ),
                    rx.input(
                        rx.input.slot(rx.icon(tag="user")),
                        placeholder="user@correo.com",
                        type="email",
                        size="3",
                        width="100%",
                        on_change=LoginState.set_email,
                        value=LoginState.email,
                    ),
                    spacing="2",
                    width="100%",
                ),
                # Password input
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Contraseña",
                            font_size=SizeText.MEDIUM.value,
                            font_weight=FontWeight.MEDIUM.value,
                            color=ColorText.PRIMARY.value,
                        ),
                    ),
                    rx.input(
                        rx.input.slot(rx.icon(tag="lock")),
                        placeholder="Ingrese su contraseña",
                        type="password",
                        size="3",
                        width="100%",
                        on_change=LoginState.set_password,
                        value=LoginState.password,
                    ),
                    rx.vstack(
                        rx.link(
                            "Olvide mi contraseña",
                            href="#",
                            font_size=SizeText.SMALL.value,
                            color=ColorText.ACCENT.value,
                        ),
                        justify="between",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                button_general("Sign in", on_click=LoginState.handle_login),
                rx.cond(
                    LoginState.error_message != "",
                    rx.text(LoginState.error_message, color="red")
                ),
                
            ),
            max_width="28em",
            size="5",
            width="100%",
        ),
        display="flex",
        flex_direction="column",
        align="center",
        justify_content="center",   
    )
