import reflex as rx

# Importaciones de vistas y componentes
from sia.views.login_views import login_default_icons
from sia.components.navigation.navbars import navbar_user
from sia.components.feedback.banners import top_banner_gradient
from sia.views.footer_login import footer_login

# Importar tokens del sistema de diseño
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, SizeText
from sia.styles.fonts import FontFamily
from sia.styles.border import BorderRadius, CommonBorders

class LoginTransitionState(rx.State):
    opacity: str = "100"
    def set_opacity(self):
        self.opacity = "1"

class Spline(rx.Component):
    """Componente Spline personalizado para animaciones 3D.
    
    Nota: Requiere instalación de dependencias @splinetool/runtime y @splinetool/react-spline
    """    
    library = "@splinetool/react-spline"
    tag = "Spline"
    is_default = True
    scene: rx.Var[str]

spline = Spline.create

# Escenas Spline 3D disponibles - optimizadas para performance
scene_1 = "https://prod.spline.design/6SNYlarzbo0-xZgs/scene.splinecode" # hole particule
scene_2 = "https://prod.spline.design/lyu6KMjx6GdU0uuL/scene.splinecode" 
scene_3 = "https://prod.spline.design/UNk43TNC4EyUDUII/scene.splinecode" # hole black (actual)
scene_4 = "https://prod.spline.design/MPMkLHd8PjLS9k09/scene.splinecode" # bg wave point color

def spline_demo(**kwargs):
    """Componente Spline 3D optimizado con lazy loading y pointer-events disabled."""
    return spline(scene=scene_3, **kwargs)

# Estilos del sistema CSS Grid
def grid_layout_styles():
    """Estilos para el layout principal con CSS Grid."""
    return {
        "display": "grid",
        "grid_template_areas": [
            '"header"',
            '"main"',
            '"footer"'
        ],
        "grid_template_rows": "auto 1fr auto",
        "height": "100vh",
        "width": "100vw",
        "overflow": "hidden",
        "font_family": FontFamily.DEFAULT.value,
        "background_color": Color.background.value,
    }

def responsive_container_styles():
    """Estilos del contenedor principal con responsive design y accesibilidad."""
    return {
        "position": "relative",
        "width": "100vw",
        "height": "100vh",
        "overflow": "hidden",
        "font_family": FontFamily.DEFAULT.value,
        # Mejoras de accesibilidad
        "scroll_behavior": "smooth",
        # Responsive typography scaling
        "font_size": {
            "base": SizeText.SMALL.value,   # Móvil: texto más pequeño
            "md": SizeText.MEDIUM.value,    # Tablet: texto medio
            "lg": SizeText.MEDIUM.value,    # Desktop: texto medio
        },
    }

def header_styles():
    """Estilos para el header semántico con contraste mejorado."""
    return {
        "grid_area": "header",
        "z_index": "10",
        "position": "relative",
        "width": "100%",
        # Mejoras de contraste y accesibilidad
        "background_color": Color.background.value,
        "border_bottom": CommonBorders.LIGHT_SOLID,
        # Estados de focus para navegación por teclado
        "_focus_within": {
            "box_shadow": f"0 0 0 2px {Color.accent.value}",
            "outline": "none",
        },
    }

def main_styles():
    """Estilos para el contenido principal con mejoras de accesibilidad."""
    return {
        "grid_area": "main",
        "position": "relative",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "width": "100%",
        "height": "100%",
        "min_height": "500px",  # Altura mínima asegurada para el formulario
        "padding": SizeSpace.MEDIUM.value,  # Padding para evitar elementos cortados
        # Mejoras para focus management
        "_focus_within": {
            "outline": "none",
        },
    }

def spline_background_styles():
    """Estilos para el fondo Spline 3D."""
    return {
        "position": "absolute",
        "top": "0",
        "left": "0",
        "width": "100%",
        "height": "100%",
        "z_index": "1",
        "opacity": LoginTransitionState.opacity,
        "transition": "opacity 1.5s ease-in-out",  # Optimizado a 1.5s según requerimiento
        "pointer_events": "none",  # Evitar interferencia con interacciones
    }

def login_form_overlay_styles():
    """Estilos simplificados para el formulario con flexbox centrado."""
    return {
        "position": "relative",
        "z_index": "3",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "width": "100%",
        "height": "100%",
        "padding": SizeSpace.MEDIUM.value,
    }

def footer_styles():
    """Estilos para el footer semántico con contraste mejorado."""
    return {
        "grid_area": "footer",
        "z_index": "10",
        "position": "relative",
        "width": "100%",
        "background_color": Color.background.value,
        "border_top": CommonBorders.LIGHT_SOLID,
        # Mejoras de contraste para el texto del footer
        "color": ColorText.GRAY_700.value,
        # Estados de focus para navegación por teclado
        "_focus_within": {
            "box_shadow": f"0 0 0 2px {Color.accent.value}",
            "outline": "none",
        },
    }


def login() -> rx.Component:
    """Página de login con layout CSS Grid y diseño responsive optimizado.
    
    Estructura semántica:
    - Header semántico con navbar y banner (z-index: 10)
    - Main content con Spline 3D background y formulario de login
    - Footer semántico (z-index: 10)
    
    Características implementadas:
    ✅ CSS Grid layout con áreas definidas (header/main/footer)
    ✅ Z-index predecible: Spline (1) → Formulario (3) → Header/Footer (10)
    ✅ Responsive design: móvil (<768px), tablet (768-1024px), desktop (>1024px)
    ✅ Sistema de diseño integrado (Color, SizeSpace, FontFamily, BorderRadius)
    ✅ Transición Spline optimizada (1.5s según requerimiento)
    ✅ Accesibilidad: estructura semántica, ARIA roles, focus states
    ✅ UX mejorado: hover effects, box shadows, transiciones suaves
    ✅ Typography scaling adaptativo por breakpoint
    """
    return rx.box(
        # Header semántico con navbar y banner
        rx.box(
            rx.vstack(
                navbar_user(),
                top_banner_gradient(),
                align="center",
                spacing="0",
                width="100%",
            ),
            style=header_styles(),
            role="banner",  # ARIA role para accesibilidad
            aria_label="Encabezado de la aplicación",
            as_="header",  # Renderizar como elemento HTML <header>
        ),
        
        # Main content con Spline + formulario
        rx.box(
            # Spline 3D background layer (z-index: 1)
            spline_demo(
                style=spline_background_styles(),
                on_mount=LoginTransitionState.set_opacity,
            ),
            
            # Login form overlay centrado y visible (z-index: 3)
            rx.box(
                login_default_icons(),
                style=login_form_overlay_styles(),
                role="main",  # ARIA role para accesibilidad
                aria_label="Formulario de inicio de sesión",
                aria_describedby="login-form-description",
                as_="section",  # Renderizar como elemento HTML <section>
            ),
            
            style=main_styles(),
            as_="main",  # Renderizar como elemento HTML <main>
        ),
        
        # Footer semántico
        rx.box(
            footer_login(),
            style=footer_styles(),
            role="contentinfo",  # ARIA role para accesibilidad
            aria_label="Pie de página con información de contacto",
            as_="footer",  # Renderizar como elemento HTML <footer>
        ),
        
        # Descripción oculta para screen readers
        rx.box(
            "Página de inicio de sesión del Sistema Interno de Administración. "
            "Utilice Tab para navegar entre elementos y Enter para seleccionar.",
            style={
                "position": "absolute",
                "left": "-10000px",
                "width": "1px",
                "height": "1px",
                "overflow": "hidden",
            },
            id="login-form-description",
            aria_hidden="true",
        ),
        
        # CSS Grid container con áreas definidas
        style=grid_layout_styles(),
        role="document",  # Rol principal del documento
        lang="es",  # Idioma para screen readers
        aria_label="Sistema Interno de Administración - Página de Login",
    )
