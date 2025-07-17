import reflex as rx
from sia.views.sidebar import sidebar_top_profile
from sia.components.navbar import navbar_user

def index() -> rx.Component:    
    return rx.box(
        navbar_user(),
    )

