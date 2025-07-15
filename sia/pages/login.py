import reflex as rx
from sia.views.login_views import login_default_icons






def login() -> rx.Component:    
    return rx.box(
        rx.vstack(
            login_default_icons(),
            width="100%",
            height="100vh",
            display="flex",
            align_items="center",
            justify_content="center",
    ),
    
    )

