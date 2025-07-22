import reflex as rx
from sia.components.buttons import *
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.sizes import *

from sia.styles.colors import Color,Color

from sia.components.siderbar_componentes import sidebar_item, sidebar_items
from sia.components.ant_breadcrumb import breadcrumb, breadcrumb_item
from sia.components.ant_steps import steps_example
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