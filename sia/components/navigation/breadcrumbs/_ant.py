import reflex as rx
from typing import List, Dict, Any, Optional
from sia.styles.colors import Color, ColorText


class AntBreadcrumb(rx.Component):
    library = "antd"
    tag = "Breadcrumb"
    items: rx.Var[List[Dict[str, Any]]]
    separator: rx.Var[str]
    
    def get_default_style(self):
        return {
            "background_color": Color.GRAY_100.value,
            "padding": "8px 12px",
            "border_radius": "6px",
            "color": ColorText.GRAY_600.value,
            ".ant-breadcrumb-separator": {
                 "color": "black",
                 "font_weight": "700",
                 "font_size": "14px"
             },
            ".ant-breadcrumb-link": {
                "color": ColorText.GRAY_600.value,
                "&:hover": {
                    "color": Color.BLUE_500.value
                }
            }
        }


class AntBreadcrumbItem(rx.Component):
    library = "antd"
    tag = "Breadcrumb.Item"
    href: rx.Var[str]
    colorText: rx.Var[str]
    separator: rx.Var[str]
    
    def get_default_style(self):
        return {
            "color": ColorText.GRAY_600.value,
            "&:hover": {
                "color": Color.BLUE_500.value
            }
        }


# Create instances of the components
breadcrumb = AntBreadcrumb.create
breadcrumb_item = AntBreadcrumbItem.create

# Helper function to create breadcrumb with items prop
def create_breadcrumb(items_list, separator="/", custom_style=None):
    """Create a breadcrumb with items prop instead of child components.
    
    Args:
        items_list: List of dictionaries with breadcrumb item properties
        separator: Custom separator character
        custom_style: Custom CSS styles
        
    Returns:
        Breadcrumb component with items prop
    """
    style = custom_style or {}
    return breadcrumb(items=items_list, separator=separator, style=style)


def create_breadcrumb_themed(items_list, theme="default", separator="/"):
    """Create a themed breadcrumb with predefined color schemes.
    
    Args:
        items_list: List of dictionaries with breadcrumb item properties
        theme: Theme name (admin, manager, employee, default)
        separator: Custom separator character
        
    Returns:
        Breadcrumb component with themed styling
    """
    themes = {
        "admin": {
            "background_color": Color.BLUE_50.value,
            "color": ColorText.BLUE_700.value,
            "border": f"1px solid {Color.BLUE_200.value}",
            ".ant-breadcrumb-separator": {
                  "color": "black",
                  "font_weight": "800",
                  "font_size": "16px"
              },
            ".ant-breadcrumb-link": {
                "color": ColorText.BLUE_700.value,
                "&:hover": {
                    "color": Color.BLUE_800.value
                }
            }
        },
        "manager": {
            "background_color": Color.GREEN_50.value,
            "color": ColorText.GREEN_700.value,
            "border": f"1px solid {Color.GREEN_200.value}",
            ".ant-breadcrumb-separator": {
                  "color": "black",
                  "font_weight": "800",
                  "font_size": "16px"
              },
            ".ant-breadcrumb-link": {
                "color": ColorText.GREEN_700.value,
                "&:hover": {
                    "color": Color.GREEN_800.value
                }
            }
        },
        "employee": {
            "background_color": Color.GRAY_50.value,
            "color": ColorText.GRAY_700.value,
            "border": f"1px solid {Color.GRAY_200.value}",
            ".ant-breadcrumb-separator": {
                  "color": "black",
                  "font_weight": "800",
                  "font_size": "16px"
              },
            ".ant-breadcrumb-link": {
                "color": ColorText.GRAY_700.value,
                "&:hover": {
                    "color": Color.GRAY_800.value
                }
            }
        }
    }
    
    base_style = {
        "padding": "8px 12px",
        "border_radius": "6px",
        "margin_bottom": "4px"
    }
    
    theme_style = themes.get(theme, {})
    final_style = {**base_style, **theme_style}
    
    return breadcrumb(items=items_list, separator=separator, style=final_style)
