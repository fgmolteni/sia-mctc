from enum import Enum
from sia.styles.colors import Color

class BorderWidth(Enum):
    """Grosores estándar para bordes"""
    THIN = "1px"
    MEDIUM = "2px"
    THICK = "3px"
    NONE = "0px"

class BorderStyle(Enum):
    """Estilos de borde estándar"""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    NONE = "none"

class BorderRadius(Enum):
    """Radios de borde estándar"""
    NONE = "0px"
    SMALL = "5px"
    MEDIUM = "8px"
    LARGE = "10px"
    X_LARGE = "12px"
    ROUND = "50%"
    FULL = "9999px"
    DEFAULT = "25px"  # Para mantener compatibilidad

class BorderColor(Enum):
    """Colores de borde estándar"""
    LIGHT = Color.border_light.value  # #E5E7EB
    MEDIUM = Color.border_medium.value  # #D1D5DB
    GRAY_3 = "var(--gray-3)"  # Para rx.color('gray', 3)
    GRAY_4 = "var(--gray-4)"  # Para rx.color('gray', 4)
    PRIMARY = Color.primary.value
    SECONDARY = Color.secondary.value
    TRANSPARENT = "transparent"

# Funciones helper para crear bordes completos
def create_border(width: BorderWidth = BorderWidth.THIN, 
                 style: BorderStyle = BorderStyle.SOLID, 
                 color: BorderColor = BorderColor.LIGHT) -> str:
    """Crea una cadena de borde completa"""
    return f"{width.value} {style.value} {color.value}"

def create_border_bottom(width: BorderWidth = BorderWidth.THIN, 
                        style: BorderStyle = BorderStyle.SOLID, 
                        color: BorderColor = BorderColor.LIGHT) -> str:
    """Crea un borde inferior"""
    return f"{width.value} {style.value} {color.value}"

def create_border_right(width: BorderWidth = BorderWidth.THIN, 
                       style: BorderStyle = BorderStyle.SOLID, 
                       color: BorderColor = BorderColor.GRAY_4) -> str:
    """Crea un borde derecho"""
    return f"{width.value} {style.value} {color.value}"

# Bordes predefinidos más comunes
class CommonBorders:
    """Bordes predefinidos comúnmente usados"""
    LIGHT_SOLID = create_border(BorderWidth.THIN, BorderStyle.SOLID, BorderColor.LIGHT)
    MEDIUM_SOLID = create_border(BorderWidth.THIN, BorderStyle.SOLID, BorderColor.MEDIUM)
    GRAY_SOLID = create_border(BorderWidth.THIN, BorderStyle.SOLID, BorderColor.GRAY_3)
    PRIMARY_SOLID = create_border(BorderWidth.THIN, BorderStyle.SOLID, BorderColor.PRIMARY)
    SECONDARY_SOLID = create_border(BorderWidth.THIN, BorderStyle.SOLID, BorderColor.SECONDARY)
    NONE = create_border(BorderWidth.NONE, BorderStyle.NONE, BorderColor.TRANSPARENT)