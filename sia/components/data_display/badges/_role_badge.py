import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import BorderRadius
from typing import Literal

def role_badge(
    text: str,
    role: Literal["admin", "manager", "employee", "default"] = "default",
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
        "manager": {
            "color": Color.manager_text.value,
            "bg": Color.manager_bg.value
        },
        "employee": {
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

def status_badge(
    text: str,
    status: Literal["active", "inactive", "pending", "success", "warning", "error"] = "active",
    show_dot: bool = True,
    **kwargs
) -> rx.Component:
    """Badge component for displaying status with optional status dot.
    
    Args:
        text: The text to display in the badge
        status: The status type that determines the color scheme
        show_dot: Whether to show a colored dot indicator
        **kwargs: Additional props to pass to the container
    
    Returns:
        A styled status badge component
    """
    
    # Define color schemes for different statuses
    status_schemes = {
        "active": {
            "color": Color.employee_text.value,
            "bg": Color.employee_bg.value,
            "dot_color": Color.status_active.value
        },
        "inactive": {
            "color": ColorText.GRAY_700.value,
            "bg": Color.background_light.value,
            "dot_color": Color.icon_inactive.value
        },
        "pending": {
            "color": ColorText.GRAY_800.value,
            "bg": Color.warning.value,
            "dot_color": Color.warning.value
        },
        "success": {
            "color": Color.employee_text.value,
            "bg": Color.employee_bg.value,
            "dot_color": Color.status_active.value
        },
        "warning": {
            "color": ColorText.GRAY_800.value,
            "bg": Color.warning.value,
            "dot_color": Color.warning.value
        },
        "error": {
            "color": ColorText.TERCEARY.value,
            "bg": Color.error.value,
            "dot_color": Color.error.value
        }
    }
    
    scheme = status_schemes.get(status, status_schemes["active"])
    
    if show_dot:
        return rx.hstack(
            rx.box(
                width="8px",
                height="8px",
                bg=scheme["dot_color"],
                border_radius=BorderRadius.DEFAULT.value
            ),
            rx.text(
                text,
                color=scheme["color"],
                font_weight=FontWeight.MEDIUM.value
            ),
            spacing="2",
            align_items="center",
            **kwargs
        )
    else:
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