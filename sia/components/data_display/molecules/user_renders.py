"""
Moléculas de renderizado para datos de usuarios.
Funciones de renderizado específicas para columnas de tabla de usuarios.
"""
import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText


def render_user_name(value: rx.Var, row_data: rx.Var) -> rx.Component:
    """Renderizar nombre de usuario con avatar y información adicional."""
    # Usar variables de Reflex
    avatar = row_data["avatar"]
    email = row_data["email"]  
    user_id = row_data["id"]
    
    return rx.hstack(
        # Avatar
        rx.box(
            rx.text(
                avatar,
                color="white",
                font_weight=FontWeight.BOLD.value,
                text_align="center",
                font_size=SizeText.SMALL.value,
            ),
            bg=Color.primary.value,
            border_radius="50%",
            width="32px",
            height="32px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        # Info
        rx.vstack(
            rx.link(
                rx.text(
                    value,
                    font_weight=FontWeight.MEDIUM.value,
                    color=ColorText.GRAY_800.value,
                    _hover={
                        "color": Color.primary.value,
                        "text_decoration": "underline",
                        "cursor": "pointer",
                    },
                ),
                href="/usuarios/" + user_id.to_string(),
                text_decoration="none",
            ),
            rx.text(
                email,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_500.value,
            ),
            spacing="1",
            align="start",
        ),
        spacing="3",
        align="center",
    )


def render_user_role(value: rx.Var, row_data: rx.Var) -> rx.Component:
    """Renderizar rol de usuario con badge coloreado usando rx.match para lógica condicional."""
    
    # Usar rx.match para manejar diferentes valores de rol
    return rx.match(
        value,
        ("Administrador", 
            rx.box(
                rx.text(
                    value,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    color="#2563EB",
                ),
                bg="#DBEAFE",
                padding="4px 8px",
                border_radius="6px",
                display="inline-block",
            )
        ),
        ("Supervisor",
            rx.box(
                rx.text(
                    value,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    color="#9333EA",
                ),
                bg="#E9D5FF",
                padding="4px 8px",
                border_radius="6px",
                display="inline-block",
            )
        ),
        ("Usuario",
            rx.box(
                rx.text(
                    value,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    color="#16A34A",
                ),
                bg="#DCFCE7",
                padding="4px 8px",
                border_radius="6px",
                display="inline-block",
            )
        ),
        # Caso por defecto
        rx.box(
            rx.text(
                value,
                font_size=SizeText.SMALL.value,
                font_weight=FontWeight.MEDIUM.value,
                color="#6B7280",
            ),
            bg="#F3F4F6",
            padding="4px 8px",
            border_radius="6px",
            display="inline-block",
        )
    )


def render_user_status(value: rx.Var, row_data: rx.Var) -> rx.Component:
    """Renderizar estado del usuario con indicador visual usando rx.match."""
    
    # Usar rx.match para manejar diferentes estados
    return rx.match(
        value,
        ("Activo",
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    bg="#22C55E",
                    border_radius="50%",
                ),
                rx.text(
                    value,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    color="#16A34A",
                ),
                bg="#DCFCE7",
                padding="4px 8px",
                border_radius="6px",
                spacing="2",
                align="center",
            )
        ),
        # Caso por defecto (Inactivo y otros)
        rx.hstack(
            rx.box(
                width="8px",
                height="8px",
                bg="#9CA3AF",
                border_radius="50%",
            ),
            rx.text(
                value,
                font_size=SizeText.SMALL.value,
                font_weight=FontWeight.MEDIUM.value,
                color="#6B7280",
            ),
            bg="#F3F4F6",
            padding="4px 8px",
            border_radius="6px",
            spacing="2",
            align="center",
        )
    )


def render_user_actions(value: rx.Var, row_data: rx.Var) -> rx.Component:
    """Renderizar acciones para usuario específico."""
    user_id = row_data["id"]
    
    # Para este caso, necesitamos acceso al estado
    # Usaremos imports dinámicos para evitar circular imports
    from sia.pages.usuarios import UserState
    
    return rx.hstack(
        rx.link(
            rx.button(
                rx.icon("eye", size=16),
                variant="ghost",
                size="2",
                title="Ver detalles",
            ),
            href="/usuarios/" + user_id.to_string(),
        ),
        rx.button(
            rx.icon("pencil", size=16),
            on_click=UserState.show_edit_user_modal(user_id),
            variant="ghost",
            size="2",
            title="Editar usuario",
        ),
        rx.button(
            rx.icon("trash-2", size=16),
            on_click=UserState.delete_user_action(user_id),
            variant="ghost",
            size="2",
            color_scheme="red",
            title="Eliminar usuario",
        ),
        spacing="1",
    )