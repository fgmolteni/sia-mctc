import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, SizeText, SizeAvatar, SizeGeneral
from sia.styles.border import BorderRadius, CommonBorders
from sia.styles.fonts import FontWeight


def skeleton_box(width: str = "100%", height: str = "1rem", delay: str = "0s") -> rx.Component:
    """Componente base skeleton con animación de shimmer."""
    return rx.box(
        width=width,
        height=height,
        background=f"linear-gradient(90deg, {Color.border_medium.value} 25%, {Color.border_light.value} 50%, {Color.border_medium.value} 75%)",
        background_size="200% 100%",
        border_radius=BorderRadius.MEDIUM.value,
        animation=f"shimmer 2s infinite ease-in-out {delay}",
        style={
            "@keyframes shimmer": {
                "0%": {"background-position": "-200% 0"},
                "100%": {"background-position": "200% 0"}
            }
        }
    )


def profile_avatar_skeleton() -> rx.Component:
    """Skeleton del avatar del perfil."""
    return rx.box(
        skeleton_box(
            width=SizeAvatar.LARGE.value,
            height=SizeAvatar.LARGE.value
        ),
        border_radius=BorderRadius.ROUND.value,
        background=Color.secondary.value,
        flex_shrink="0",
    )


def profile_header_skeleton() -> rx.Component:
    """Skeleton del header del perfil con avatar y información básica."""
    return rx.flex(
        # Avatar skeleton
        profile_avatar_skeleton(),
        
        # Información del usuario skeleton
        rx.vstack(
            # Nombre skeleton (más ancho)
            skeleton_box(width="200px", height="1.75rem", delay="0.1s"),
            
            # Badges skeleton (horizontal)
            rx.hstack(
                skeleton_box(width="120px", height="2rem", delay="0.2s"),
                skeleton_box(width="80px", height="2rem", delay="0.3s"),
                spacing="3",
            ),
            align_items="start",
            spacing="3",
            flex_grow="1",
        ),
        
        # Layout principal
        direction="row",
        align_items="center",
        spacing="6",
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        width="100%",
        max_width="800px",
    )


def profile_info_skeleton() -> rx.Component:
    """Skeleton de la card de información del usuario."""
    return rx.card(
        rx.vstack(
            # Header de la sección
            rx.hstack(
                skeleton_box(width="24px", height="24px", delay="0.1s"),
                skeleton_box(width="150px", height="1.5rem", delay="0.2s"),
                spacing="2",
                align="center",
                margin_bottom=SizeSpace.LARGE.value,
            ),
            
            # Grid de información
            rx.grid(
                # Columna izquierda
                rx.vstack(
                    # Nombre completo
                    rx.vstack(
                        skeleton_box(width="120px", height="0.875rem", delay="0.3s"),
                        skeleton_box(width="180px", height="1.25rem", delay="0.4s"),
                        align="start",
                        spacing="1",
                    ),
                    # Nombre de usuario
                    rx.vstack(
                        skeleton_box(width="140px", height="0.875rem", delay="0.5s"),
                        skeleton_box(width="160px", height="1.25rem", delay="0.6s"),
                        align="start",
                        spacing="1",
                    ),
                    # DNI
                    rx.vstack(
                        skeleton_box(width="40px", height="0.875rem", delay="0.7s"),
                        skeleton_box(width="120px", height="1.25rem", delay="0.8s"),
                        align="start",
                        spacing="1",
                    ),
                    # Rol
                    rx.vstack(
                        skeleton_box(width="60px", height="0.875rem", delay="0.9s"),
                        skeleton_box(width="100px", height="1.25rem", delay="1.0s"),
                        align="start",
                        spacing="1",
                    ),
                    spacing="4",
                    align="start",
                ),
                
                # Columna derecha
                rx.vstack(
                    # Email
                    rx.vstack(
                        skeleton_box(width="50px", height="0.875rem", delay="1.1s"),
                        rx.hstack(
                            skeleton_box(width="16px", height="16px", delay="1.2s"),
                            skeleton_box(width="200px", height="1.25rem", delay="1.3s"),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    # Área
                    rx.vstack(
                        skeleton_box(width="40px", height="0.875rem", delay="1.4s"),
                        skeleton_box(width="130px", height="1.25rem", delay="1.5s"),
                        align="start",
                        spacing="1",
                    ),
                    # Fecha de registro
                    rx.vstack(
                        skeleton_box(width="140px", height="0.875rem", delay="1.6s"),
                        rx.hstack(
                            skeleton_box(width="16px", height="16px", delay="1.7s"),
                            skeleton_box(width="100px", height="1.25rem", delay="1.8s"),
                            spacing="2",
                            align="center",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    # Estado
                    rx.vstack(
                        skeleton_box(width="60px", height="0.875rem", delay="1.9s"),
                        skeleton_box(width="80px", height="1.25rem", delay="2.0s"),
                        align="start",
                        spacing="1",
                    ),
                    spacing="4",
                    align="start",
                ),
                columns="2",
                spacing="8",
                width=SizeGeneral.FULL.value,
            ),
            spacing="3",
            align="start",
            width=SizeGeneral.FULL.value,
        ),
        
        # Estilos de la tarjeta
        padding=SizeSpace.LARGE.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        background=Color.background.value,
        width=SizeGeneral.FULL.value,
        max_width="800px"
    )


def permissions_skeleton() -> rx.Component:
    """Skeleton para la sección de permisos."""
    return rx.card(
        rx.vstack(
            # Header de permisos
            rx.hstack(
                skeleton_box(width="24px", height="24px", delay="0.1s"),
                skeleton_box(width="100px", height="1.5rem", delay="0.2s"),
                spacing="2",
                align="center",
                margin_bottom=SizeSpace.MEDIUM.value,
            ),
            
            # Lista de permisos skeleton
            rx.vstack(
                *[
                    rx.hstack(
                        skeleton_box(width="20px", height="20px", delay=f"{0.3 + i * 0.1}s"),
                        skeleton_box(width=f"{150 + i * 20}px", height="1rem", delay=f"{0.4 + i * 0.1}s"),
                        spacing="3",
                        align="center",
                    )
                    for i in range(5)  # 5 permisos skeleton
                ],
                spacing="3",
                align="start",
                width="100%",
            ),
            
            spacing="4",
            align="start",
            width=SizeGeneral.FULL.value,
        ),
        padding=SizeSpace.LARGE.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        background=Color.background.value,
        width=SizeGeneral.FULL.value,
        max_width="800px"
    )


def profile_full_skeleton() -> rx.Component:
    """Skeleton completo del perfil con todas las secciones."""
    return rx.center(
        rx.vstack(
            # Texto indicativo de carga
            rx.vstack(
                skeleton_box(width="32px", height="32px", delay="0.1s"),
                skeleton_box(width="250px", height="1.25rem", delay="0.2s"),
                spacing="4",
                align="center",
                margin_bottom=SizeSpace.X_LARGE.value,
            ),
            
            # Header del perfil
            profile_header_skeleton(),
            
            # Información del usuario
            profile_info_skeleton(),
            
            # Sección de permisos
            permissions_skeleton(),
            
            spacing="6",
            width="100%",
            max_width="900px",
            align="center"
        ),
        min_height="400px",
        width="100%",
        padding=SizeSpace.LARGE.value
    )