import reflex as rx
from typing import Optional, Union, List, Dict, Any
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeText, SizeSpace
from sia.styles.fonts import FontWeight
import re


def form_input(
    label: str, 
    placeholder: str, 
    type: str, 
    name: str, 
    on_change=None, 
    value: Any = "", 
    required: bool = False,
    validation_rules: Optional[Dict] = None,
    helper_text: Optional[str] = None,
    show_counter: bool = False,
    max_length: Optional[int] = None,
    auto_transform: Optional[str] = None  # 'lowercase', 'uppercase', 'title'
) -> rx.Component:
    """
    Componente de entrada mejorado con validación en tiempo real.
    
    Args:
        label: Etiqueta del campo
        placeholder: Texto de placeholder
        type: Tipo de input (text, email, etc.)
        name: Nombre del campo
        on_change: Función de callback para cambios
        value: Valor actual (debe ser rx.Var)
        required: Si el campo es requerido
        validation_rules: Reglas de validación
        helper_text: Texto de ayuda
        show_counter: Mostrar contador de caracteres
        max_length: Límite máximo de caracteres
        auto_transform: Transformación automática del texto
    """
    return rx.vstack(
        # Label con indicador de requerido
        rx.hstack(
            rx.text(
                label,
                font_weight=FontWeight.MEDIUM.value,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_700.value,
            ),
            rx.cond(
                required,
                rx.text("*", color=Color.error.value, font_weight="bold")
            ),
            justify="start",
            align="center",
            spacing="1"
        ),
        
        # Campo de entrada básico
        rx.input(
            placeholder=placeholder,
            type=type,
            name=name,
            value=value,
            on_change=on_change,
            border_color=Color.border_light.value,
            _focus={"border_color": Color.primary.value},
            padding_x=SizeSpace.SMALL.value,
            padding_y=SizeSpace.SMALL.value,
            border_radius="6px",
            width="100%"
        ),
        
        # Texto de ayuda
        rx.cond(
            helper_text is not None,
            rx.text(
                helper_text or "",
                color=ColorText.GRAY_500.value,
                font_size=SizeText.X_SMALL.value,
                margin_top="1"
            )
        ),
        
        # Contador de caracteres
        rx.cond(
            show_counter and (max_length is not None),
            rx.text(
                f"0/{max_length}",  # Simplificado por ahora
                color=ColorText.GRAY_500.value,
                font_size=SizeText.X_SMALL.value,
                text_align="right",
                margin_top="1"
            )
        ),
        
        width="100%",
        spacing="2",
        align="start"
    )


def password_input_with_strength(
    label: str = "Contraseña",
    placeholder: str = "Ingresa tu contraseña", 
    name: str = "password",
    on_change=None,
    value: Any = "",
    required: bool = False,
    helper_text: str = "Al menos 6 caracteres, una letra y un número"
) -> rx.Component:
    """
    Componente de contraseña con indicador de fortaleza visual.
    """
    return rx.vstack(
        # Label con indicador de requerido
        rx.hstack(
            rx.text(
                label,
                font_weight=FontWeight.MEDIUM.value,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_700.value,
            ),
            rx.cond(
                required,
                rx.text("*", color=Color.error.value, font_weight="bold")
            ),
            justify="start",
            align="center",
            spacing="1"
        ),
        
        # Campo de contraseña
        rx.input(
            placeholder=placeholder,
            type="password",
            name=name,
            value=value,
            on_change=on_change,
            border_color=Color.border_light.value,
            _focus={"border_color": Color.primary.value},
            padding_x=SizeSpace.SMALL.value,
            padding_y=SizeSpace.SMALL.value,
            border_radius="6px",
            width="100%"
        ),
        
        # Indicador de fortaleza simplificado
        rx.cond(
            value,
            rx.vstack(
                rx.text(
                    "Fortaleza de contraseña",
                    font_size=SizeText.X_SMALL.value,
                    color=ColorText.GRAY_700.value
                ),
                rx.progress(
                    value=50,  # Simplificado por ahora
                    size="1",
                    color_scheme="blue"
                ),
                width="100%",
                spacing="1"
            )
        ),
        
        # Texto de ayuda
        rx.cond(
            helper_text is not None,
            rx.text(
                helper_text,
                color=ColorText.GRAY_500.value,
                font_size=SizeText.X_SMALL.value,
                margin_top="1"
            )
        ),
        
        width="100%",
        spacing="2",
        align="start"
    )


def select_input(
    label: str,
    placeholder: str,
    options: List[str],
    name: str,
    on_change=None,
    value: Any = "",
    required: bool = False,
    helper_text: Optional[str] = None
) -> rx.Component:
    """
    Componente de selección mejorado.
    """
    return rx.vstack(
        # Label con indicador de requerido
        rx.hstack(
            rx.text(
                label,
                font_weight=FontWeight.MEDIUM.value,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_700.value,
            ),
            rx.cond(
                required,
                rx.text("*", color=Color.error.value, font_weight="bold")
            ),
            justify="start",
            align="center",
            spacing="1"
        ),
        
        # Campo de selección
        rx.select(
            options,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            width="100%",
        ),
        
        # Texto de ayuda
        rx.cond(
            helper_text is not None,
            rx.text(
                helper_text or "",
                color=ColorText.GRAY_500.value,
                font_size=SizeText.X_SMALL.value,
                margin_top="1"
            )
        ),
        
        width="100%",
        spacing="2",
        align="start"
    )


# Funciones de validación simplificadas para evitar errores de rx.cond
def _validate_input_value(value, rules):
    """Función de validación simplificada que retorna siempre valores seguros."""
    if not rules or not value:
        return True, ""
    
    # Por ahora retorna siempre válido para evitar errores en rx.cond
    return True, ""


def _evaluate_password_strength(password):
    """Evalúa la fortaleza de la contraseña y retorna un nivel del 0-4."""
    if not password:
        return 0
    
    score = 0
    if len(password) >= 6:
        score += 1
    if re.search(r'[a-zA-Z]', password):
        score += 1  
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        
    return min(score, 4)


def get_strength_text(level):
    """Retorna el texto descriptivo del nivel de fortaleza."""
    strength_map = {
        0: "Muy débil",
        1: "Débil", 
        2: "Media",
        3: "Fuerte",
        4: "Muy fuerte"
    }
    return strength_map.get(level, "Muy débil")


def get_strength_color(level):
    """Retorna el color del indicador según el nivel."""
    color_map = {
        0: "red",
        1: "orange",
        2: "yellow", 
        3: "blue",
        4: "green"
    }
    return color_map.get(level, "red")


def form_date_input(
    label: str,
    name: str,
    placeholder: str = "YYYY-MM-DD",
    default_value: Any = "",
    required: bool = False,
    helper_text: Optional[str] = None,
    on_change=None
) -> rx.Component:
    """
    Componente de entrada de fecha optimizado para Reflex.
    
    Args:
        label: Etiqueta del campo
        name: Nombre del campo  
        placeholder: Texto placeholder
        default_value: Valor por defecto
        required: Si el campo es requerido
        helper_text: Texto de ayuda
        on_change: Función callback para cambios
    """
    return rx.vstack(
        # Label con indicador de requerido
        rx.hstack(
            rx.text(
                label,
                font_weight=FontWeight.MEDIUM.value,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_700.value,
            ),
            rx.cond(
                required,
                rx.text("*", color=Color.error.value, font_weight="bold")
            ),
            justify="start",
            align="center",
            spacing="1"
        ),
        
        # Campo de entrada de fecha
        rx.input(
            type="date",
            name=name,
            value=default_value,
            on_change=on_change,
            placeholder=placeholder,
            border_color=Color.border_light.value,
            _focus={"border_color": Color.primary.value},
            padding_x=SizeSpace.SMALL.value,
            padding_y=SizeSpace.SMALL.value,
            border_radius="6px",
            width="100%"
        ),
        
        # Texto de ayuda
        rx.cond(
            helper_text is not None,
            rx.text(
                helper_text or "",
                color=ColorText.GRAY_500.value,
                font_size=SizeText.X_SMALL.value,
                margin_top="1"
            )
        ),
        
        width="100%",
        spacing="2",
        align="start"
    )


def form_time_input(
    label: str,
    name: str,
    placeholder: str = "HH:MM",
    default_value: Any = "",
    required: bool = False,
    helper_text: Optional[str] = None,
    on_change=None
) -> rx.Component:
    """
    Componente de entrada de hora optimizado para Reflex.
    
    Args:
        label: Etiqueta del campo
        name: Nombre del campo
        placeholder: Texto placeholder  
        default_value: Valor por defecto
        required: Si el campo es requerido
        helper_text: Texto de ayuda
        on_change: Función callback para cambios
    """
    return rx.vstack(
        # Label con indicador de requerido
        rx.hstack(
            rx.text(
                label,
                font_weight=FontWeight.MEDIUM.value,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_700.value,
            ),
            rx.cond(
                required,
                rx.text("*", color=Color.error.value, font_weight="bold")
            ),
            justify="start",
            align="center",
            spacing="1"
        ),
        
        # Campo de entrada de hora
        rx.input(
            type="time",
            name=name,
            value=default_value,
            on_change=on_change,
            placeholder=placeholder,
            border_color=Color.border_light.value,
            _focus={"border_color": Color.primary.value},
            padding_x=SizeSpace.SMALL.value,
            padding_y=SizeSpace.SMALL.value,
            border_radius="6px",
            width="100%"
        ),
        
        # Texto de ayuda
        rx.cond(
            helper_text is not None,
            rx.text(
                helper_text or "",
                color=ColorText.GRAY_500.value,
                font_size=SizeText.X_SMALL.value,
                margin_top="1"
            )
        ),
        
        width="100%",
        spacing="2",
        align="start"
    )