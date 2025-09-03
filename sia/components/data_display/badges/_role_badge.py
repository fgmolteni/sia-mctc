import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import BorderRadius
from typing import Literal

def role_badge(
    text: str,
    role: Literal["admin", "supervisor", "usuario", "default"] = "default",
    **kwargs
) -> rx.Component:
    """Badge component for displaying user roles with appropriate colors.
    
    Args:
        text: The text to display in the badge
        role: The role type that determines the color scheme
        **kwargs: Additional props to pass to the badge
    
    Returns:
        A styled badge component
    """
    
    # Define color schemes for different roles
    color_schemes = {
        "admin": {
            "color": Color.admin_text.value,
            "bg": Color.admin_bg.value
        },
        "supervisor": {
            "color": Color.manager_text.value,
            "bg": Color.manager_bg.value
        },
        "usuario": {
            "color": Color.employee_text.value,
            "bg": Color.employee_bg.value
        },
        "default": {
            "color": ColorText.GRAY_700.value,
            "bg": Color.background_light.value
        }
    }
    
    scheme = color_schemes.get(role, color_schemes["default"])
    
    return rx.badge(
        text,
        color=scheme["color"],
        bg=scheme["bg"],
        px="2",
        py="1",
        border_radius=BorderRadius.DEFAULT.value,
        font_weight=FontWeight.MEDIUM.value,
        **kwargs
    )

