import reflex as rx
from sia.components.siderbar_componentes import sidebar_header, sidebar_section, sidebar_item, sidebar_collapsible_item, sidebar_footer
from sia.styles.colors import Color

def sidebar_main() -> rx.Component:
    return rx.box(
        rx.vstack(
            sidebar_header(),
            rx.vstack(
                sidebar_section("Navegación Principal"),
                sidebar_item("Dashboard", "home", "/", is_active=True),
                sidebar_item("Anticipos", "dollar-sign", "/anticipos"),
                sidebar_item("Caja", "box", "/viaticos"),
                sidebar_item("Agentes", "users", "/agentes"),
                sidebar_item("Vehiculos", "car", "/vehiculos"),
                sidebar_item("Usuarios", "user", "/users"),
                spacing="2",
                width="100%",
                padding="0 1rem",
            ),
            rx.spacer(),
            sidebar_footer(),
            height="100%",
        ),
        width="250px",
        height="100vh",
        position="sticky",
        left="0",
        top="0",
        bg="white",
        border_right=f"1px solid {rx.color('gray', 4)}",
        flex_shrink="0",
    )