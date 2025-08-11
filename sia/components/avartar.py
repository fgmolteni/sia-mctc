import reflex as rx
from sia.styles.sizes import SizeAvatar, SizeText

def avatar(user:str, size: str) -> rx.Component:
    return rx.hstack(
                avatar_circle(user=user),
                rx.vstack(
                    rx.text(user, fomt_size=SizeText.MEDIUM.value, weight="medium"),
                    rx.text("Administración", font_size=SizeText.SMALL.value, color_scheme="gray"),
                    spacing="1",
                    align_items="flex-start",
                    justify="center",
                ),
                width="100%",
            )

def avatar_circle(user: str, size: str = SizeAvatar.DEFAULT.value) -> rx.Component:
    # Extract first letter of username
    first_letter = user[0].upper() if user else "?"
    return rx.avatar(
        fallback=first_letter,
        size=size,
        color_scheme="gray",
        radius="full",
    )
