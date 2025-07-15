import reflex as rx
from sia.views.sidebar import sidebar_top_profile


def index() -> rx.Component:    
    return rx.box(
        sidebar_top_profile(),
    )

