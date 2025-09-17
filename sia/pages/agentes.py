import reflex as rx
from sia.views.agent import agent_view
from sia.views.sidebar import sidebar_main


def agentes_pages() -> rx.Component:
    return rx.hstack(
        sidebar_main(),
        agent_view(),
        spacing="7",
        width="100%",
        height="100vh",
        background=rx.color("gray", 2),
    )