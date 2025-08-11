import reflex as rx
from sia.components.navbar_login import navbar_user
from sia.components.topbanner import top_banner_gradient
from sia.views.footer_login import footer_login
from sia.components.buttons import button_general
from sia.styles.colors import ColorText
from sia.styles.sizes import SizeText
from sia.styles.fonts import FontWeight
from components.db_users import add_user

class UserControlState(rx.State):
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    rol: str = "usuario" # Default role
    message: str = ""

    def handle_register(self):
        if not self.nombre or not self.apellido or not self.email or not self.password or not self.confirm_password:
            self.message = "Todos los campos son obligatorios."
            return
        if self.password != self.confirm_password:
            self.message = "Las contraseñas no coinciden."
            return
        
        user_id = add_user(self.nombre, self.apellido, self.email, self.password, self.rol)
        if user_id:
            self.message = "Usuario registrado exitosamente."
            self.nombre = ""
            self.apellido = ""
            self.email = ""
            self.password = ""
            self.confirm_password = ""
            self.rol = "usuario"

def user_control() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar_user(),
            top_banner_gradient(),
            align_items="center",
        ),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading("Registro de Usuarios", font_size=SizeText.X_LARGE.value, as_="h2", text_align="center", width="100%", font_weight=FontWeight.BOLD.value, color=ColorText.PRIMARY.value),
                    rx.vstack(
                        rx.text("Nombre", font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value, text_align="left", width="100%", color=ColorText.PRIMARY.value),
                        rx.input(
                            placeholder="Ingrese su nombre",
                            type="text",
                            size="3",
                            width="100%",
                            on_change=UserControlState.set_nombre,
                            value=UserControlState.nombre,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Apellido", font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value, text_align="left", width="100%", color=ColorText.PRIMARY.value),
                        rx.input(
                            placeholder="Ingrese su apellido",
                            type="text",
                            size="3",
                            width="100%",
                            on_change=UserControlState.set_apellido,
                            value=UserControlState.apellido,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Email", font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value, text_align="left", width="100%", color=ColorText.PRIMARY.value),
                        rx.input(
                            placeholder="user@correo.com",
                            type="email",
                            size="3",
                            width="100%",
                            on_change=UserControlState.set_email,
                            value=UserControlState.email,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Contraseña", font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value, text_align="left", width="100%", color=ColorText.PRIMARY.value),
                        rx.input(
                            placeholder="Ingrese su contraseña",
                            type="password",
                            size="3",
                            width="100%",
                            on_change=UserControlState.set_password,
                            value=UserControlState.password,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Confirmar Contraseña", font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value, text_align="left", width="100%", color=ColorText.PRIMARY.value),
                        rx.input(
                            placeholder="Confirme su contraseña",
                            type="password",
                            size="3",
                            width="100%",
                            on_change=UserControlState.set_confirm_password,
                            value=UserControlState.confirm_password,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Rol (opcional, por defecto 'usuario')", font_size=SizeText.MEDIUM.value, font_weight=FontWeight.MEDIUM.value, text_align="left", width="100%", color=ColorText.PRIMARY.value),
                        rx.input(
                            placeholder="Ingrese el rol (ej. admin, usuario)",
                            type="text",
                            size="3",
                            width="100%",
                            on_change=UserControlState.set_rol,
                            value=UserControlState.rol,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    button_general("Registrar", on_click=UserControlState.handle_register),
                    rx.cond(
                        UserControlState.message != "",
                        rx.text(UserControlState.message, color="red")
                    ),
                ),
                max_width="28em",
                size="5",
                width="100%",
            ),
            width="100vw",
            height="100vh",
            position="absolute",
            top="0",
            left="0",
            z_index="1",
        ),
        footer_login(),
        position="relative",
        width="100vw",
        height="100vh",
        overflow="hidden",
    )
