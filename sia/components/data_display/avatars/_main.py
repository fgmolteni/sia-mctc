import reflex as rx
from sia.styles.sizes import SizeAvatar, SizeText, SizeSpace    


def avatar(user: str, title: str, size: str) -> rx.Component:
    return rx.hstack(
        avatar_circle(user=user, size=size),
        rx.vstack(
            rx.text(user, font_size=SizeText.MEDIUM.value, weight="medium"),
            rx.text(
                title,
                font_size=SizeText.SMALL.value,
                color_scheme="gray",
            ),
            spacing="1",
            #height="100%",
            #width="auto",
            #align_items="flex-start",
        ),
        width="100%",
        align="start",
        justify="center",
        padding_y=SizeSpace.SMALL.value
    )


def avatar_circle(user: str, size: str = SizeAvatar.DEFAULT.value) -> rx.Component:
    # Extract first letter of username - simplified para evitar errores de Var
    return rx.avatar(
        fallback="U",  # Fallback fijo por ahora
        size=size,
        color_scheme="gray",
        radius="full",
    )
