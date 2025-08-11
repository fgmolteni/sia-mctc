from enum import Enum

class Color(Enum):
    primary = "#1F1F1F"
    secondary = "#EEEEEE"
    accent = "#B6EADA"
    success = "#B6EADA"
    warning = "#EEDF7A"
    error = "#F7374F"
    info = "#6EACDA"
    background = "#ffffff"
    icon_background = "#EBF5FF"  # Fondo de iconos en stat_card
    background_light = "#F9FAFB"  # Fondo claro para tablas y contenedores
    border_light = "#E5E7EB"  # Bordes claros para inputs y selects
    border_medium = "#D1D5DB"  # Bordes medios
    icon_inactive = "#9CA3AF"  # Iconos inactivos y textos secundarios
    admin_bg = "#DBEAFE"  # Fondo para rol Administrador
    admin_icon = "#60A5FA"  # Color de iconos para acciones
    admin_text = "#2563EB"  # Texto para rol Administrador
    manager_bg = "#E9D5FF"  # Fondo para rol Manager
    manager_text = "#9333EA"  # Texto para rol Manager
    employee_bg = "#DCFCE7"  # Fondo para rol Empleado
    status_active = "#22C55E"  # Indicador de estado activo
    employee_text = "#16A34A"  # Texto para rol Empleado
    delete_icon = "#F87171"  # Icono de eliminación
    delete_text = "#EF4444"  # Texto de eliminación

class ColorText(Enum):
    PRIMARY = "#FFFFFF"
    SECONDARY = "#A0A0A0"
    TERCEARY = "#1F1F1F"
    ACCENT = "#B6EADA"
    ERROR = "#F7374F"
    OCULT = "#61677A"
    GRAY_500 = "#6B7280"
    GRAY_700 = "#374151"
    GRAY_800 = "#1F2937"
    WHITE_400 = "#FFFFFF66"


