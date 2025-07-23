import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace

class MenuState(rx.State):
    is_menu_open: bool = False

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    def open_menu(self):
        self.is_menu_open = True

    def close_menu(self):
        self.is_menu_open = False

def menu_user() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.avatar(
                fallback="AU",
                size="3",
                radius="full",
                cursor="pointer",
                _hover={
                    "opacity": 0.95,
                },
                on_click=MenuState.toggle_menu,  # Toggle on click
                on_mouse_enter=MenuState.open_menu,  # Open on hover
            )
        ),
        rx.menu.content(
            rx.menu.item(
                rx.vstack(
                    rx.text("Admin User", font_weight=FontWeight.MEDIUM.value),
                    rx.text("admin@mctc.gob.ar", color=ColorText.SECONDARY.value),
                    align_items="start",
                    spacing="1"
                ),
            ),
            rx.menu.separator(),
            rx.menu.item("Mi Perfil", shortcut="⇧⌘P"),
            rx.menu.item("Facturación", shortcut="⌘B"),
            rx.menu.item("Configuración", shortcut="⌘S"),
            rx.menu.separator(),
            rx.menu.item("Cerrar Sesión", shortcut="⇧⌘Q", color=Color.error.value),
            width="200px",
            bg="#ff00ff",  # Fuchsia background for debugging
            z_index=9999,    # High z-index to ensure it's on top
            on_mouse_leave=MenuState.close_menu,  # Close when mouse leaves content
        ),
        open=MenuState.is_menu_open,
    )