import reflex as rx
from sia.components.forms.buttons import (
    button_general,
    button_redondo,
    button_sin_fondo,
    form_button,
    form_reset_button,
    button_icon_text_border,
    button_sin_fondo_icon
)
from sia.components.layout.sidebars import sidebar_item
from sia.components.navigation.breadcrumbs import breadcrumb, breadcrumb_item
from sia.components.navigation.steps import steps_example
from sia.views.forms_views import forms_views
def playground() -> rx.Component:
    return rx.vstack(
                
                steps_example(),
                # Main content area for the playground
                rx.heading(rx.text("Welcome to the Playground!",
                        color="white", font_size="2em")),
                forms_views(),
                align_items="start", # Align items to the start
                spacing="4", # Add some spacing between elements
                padding="20px",
                # Adjust width and margins to fit between sidebar and navbar
                width="calc(100vw - 280px - 30px)", # Total width minus sidebar and right margin
                min_height="100vh", # Ensure it takes full height
                margin_left="280px",  # Adjust for sidebar width
                margin_right="30px",
                bg="#1a1a1a",
                overflow_y="auto", # Allow scrolling if content overflows vertically
                border_radius="10px"
            )