import reflex as rx

# Importaciones de vistas y componentes
from sia.views.login_views import login_default_icons
from sia.components.navigation.navbars import navbar_user
from sia.components.feedback.banners import top_banner_gradient
from sia.views.footer_login import footer_login

# Importar tokens del sistema de diseño
from sia.styles.colors import Color
from sia.styles.sizes import SizeSpace

# Código simplificado - funciones complejas removidas para solución urgente


def login() -> rx.Component:
    """Página de login con layout simplificado con flexbox.
    
    SOLUCIÓN URGENTE: Layout simplificado para restaurar visibilidad inmediata del formulario.
    - Estructura básica con flexbox para centrado perfecto
    - Eliminación de CSS Grid complejo que causaba problemas
    - Formulario claramente visible en el centro
    """
    return rx.box(
        # Header simple
        rx.vstack(
            navbar_user(),
            top_banner_gradient(),
            spacing="0",
            width="100%"
        ),
        
        # Main content centrado con flexbox
        rx.center(
            rx.card(
                login_default_icons(),
                max_width="400px",
                padding="2em",
                border_radius="8px",
                box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)"
            ),
            min_height="70vh",
            width="100%",
            padding=SizeSpace.MEDIUM.value
        ),
        
        # Footer simple
        footer_login(),
        
        # Contenedor principal con flexbox
        min_height="100vh",
        background=Color.background.value,
        display="flex",
        flex_direction="column"
    )
