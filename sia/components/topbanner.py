import reflex as rx

def top_banner_gradient() -> rx.Component:
        return rx.box(
            rx.flex(
                rx.text(
                    "Sistema Interno de Administración. ",
                    rx.link(
                        "Read the release notes.",
                        href="#",
                        underline="always",
                        display="inline",
                        underline_offset="2px",
                    ),
                    align_items=["start", "center"],
                    margin="auto",
                    spacing="3",
                    weight="medium",
                ),
            ),
            z_index="50",
            width="100%",
            position="fixer"
        )
        