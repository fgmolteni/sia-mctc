import reflex as rx
from sia.components.form_components import form_input, form_button, form_reset_button


class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

    @rx.var
    def form_data_str(self) -> str:
        return str(self.form_data)


def forms_views() -> rx.Component:
    return rx.vstack(
        rx.form(
            form_input("Nombre", "Ingrese su nombre", "text", "nombre"),
            form_input("Correo electrónico",
                       "Ingrese su correo electrónico", "email", "email"),
            form_input("Contraseña", "Ingrese su contraseña", "password", "password"),
            rx.hstack(
                form_button("Enviar"),
                form_reset_button("Limpiar"),
                spacing="2",
            ),
            spacing="4",
            on_submit=FormState.handle_submit,
        ),
        rx.divider(),
        rx.heading("results"),
        rx.text(FormState.form_data_str)

    )
