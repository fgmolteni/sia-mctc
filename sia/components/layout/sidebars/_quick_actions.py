"""
Quick Actions Sidebar para desktop.

Este módulo proporciona un sidebar flotante con acciones contextuales
que solo es visible en pantallas de escritorio (>= 1024px).
"""

import reflex as rx
from typing import Optional, List, Dict, Any

from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeIcon, SizeText, SizeSpace
from sia.styles.border import BorderRadius, CommonBorders


class QuickActionsState(rx.State):
    """Estado para manejar el quick actions sidebar."""
    
    # Estado de visibilidad
    is_visible: bool = True
    is_expanded: bool = False
    
    # Estados de acciones
    is_editing: bool = False
    
    def toggle_sidebar(self):
        """Alternar visibilidad del sidebar."""
        self.is_visible = not self.is_visible
    
    def toggle_expand(self):
        """Alternar expansión del sidebar."""
        self.is_expanded = not self.is_expanded
    
    def start_editing(self):
        """Iniciar modo de edición."""
        self.is_editing = True
    
    def cancel_editing(self):
        """Cancelar modo de edición."""
        self.is_editing = False
    
    def duplicate_profile(self):
        """Duplicar perfil actual."""
        # TODO: Implementar lógica de duplicación
        pass
    
    def export_profile(self):
        """Exportar perfil actual."""
        # TODO: Implementar lógica de exportación
        pass
    
    def print_profile(self):
        """Imprimir perfil actual."""
        # TODO: Implementar lógica de impresión
        pass
    
    def share_profile(self):
        """Compartir perfil actual."""
        # TODO: Implementar lógica de compartir
        pass


def quick_action_button(
    icon: str,
    label: str,
    description: str,
    action: Any,
    color: str = "blue",
    is_expanded: bool = False,
    is_destructive: bool = False,
    animation_delay: str = "0s"
) -> rx.Component:
    """
    Botón de acción rápida con tooltip y animaciones.
    
    Args:
        icon: Nombre del icono
        label: Etiqueta del botón
        description: Descripción para tooltip
        action: Función a ejecutar al hacer click
        color: Color scheme del botón
        is_expanded: Si el sidebar está expandido
        is_destructive: Si es una acción destructiva
        animation_delay: Delay para animación
        
    Returns:
        Componente del botón
    """
    
    # Mapeo de colores
    color_map = {
        "blue": {
            "bg": Color.info.value,
            "hover_bg": "#2563EB",
            "border": "#3B82F6"
        },
        "green": {
            "bg": Color.success.value,
            "hover_bg": "#16A34A", 
            "border": "#22C55E"
        },
        "orange": {
            "bg": Color.warning.value,
            "hover_bg": "#EA580C",
            "border": "#F97316"
        },
        "red": {
            "bg": Color.error.value,
            "hover_bg": "#DC2626",
            "border": "#EF4444"
        },
        "purple": {
            "bg": "#8B5CF6",
            "hover_bg": "#7C3AED",
            "border": "#A855F7"
        }
    }
    
    colors = color_map.get(color, color_map["blue"])
    
    # Create button component
    button_component = rx.button(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=SizeIcon.SMALL.value,
                color="white",
                transition="all 0.2s ease-in-out"
            ),
            rx.cond(
                is_expanded,
                rx.text(
                    label,
                    color="white",
                    size="2",
                    font_weight=FontWeight.MEDIUM.value,
                    transition="all 0.2s ease-in-out"
                ),
                rx.box()
            ),
            spacing="2",
            align="center",
            width="100%",
            justify=rx.cond(is_expanded, "start", "center")
        ),
        
        # Estilos del botón
        background=colors["bg"],
        border=f"1px solid {colors['border']}",
        width=rx.cond(is_expanded, "100%", "44px"),
        height="44px",
        min_height="44px",
        border_radius=BorderRadius.MEDIUM.value,
        cursor="pointer",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        
        _hover={
            "background": colors["hover_bg"],
            "transform": "scale(1.05)",
            "box_shadow": f"0 4px 12px {colors['bg']}40"
        },
        
        _active={
            "transform": "scale(0.98)"
        },
        
        on_click=action,
        
        # Animación de entrada
        animation=f"slideInFromRight 0.4s ease-out {animation_delay} both",
        style={
            "@keyframes slideInFromRight": {
                "0%": {
                    "opacity": "0",
                    "transform": "translateX(20px)"
                },
                "100%": {
                    "opacity": "1",
                    "transform": "translateX(0)"
                }
            }
        }
    )
    
    # Always show tooltip but with dynamic content
    return rx.tooltip(
        button_component,
        content=rx.cond(
            is_expanded,
            "",  # Empty content when expanded (tooltip won't show)
            f"{label}: {description}"
        ),
        side="left",
        delay_duration=500,
        skip_delay_duration=100,
        disabled=is_expanded  # Disable tooltip when expanded
    )


def sidebar_toggle_button(is_visible: bool = True) -> rx.Component:
    """
    Botón para alternar visibilidad del sidebar.
    
    Args:
        is_visible: Si el sidebar está visible
        
    Returns:
        Componente del botón toggle
    """
    return rx.button(
        rx.icon(
            tag=rx.cond(is_visible, "chevron-right", "chevron-left"),
            size=SizeIcon.SMALL.value,
            color="white",
            transition="transform 0.2s ease-in-out"
        ),
        
        # Estilos del botón
        position="absolute",
        top="20px",
        left="-16px",
        width="32px",
        height="32px",
        border_radius=BorderRadius.ROUND.value,
        background=Color.info.value,
        border="2px solid white",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        cursor="pointer",
        z_index="1001",
        transition="all 0.2s ease-in-out",
        
        _hover={
            "background": "#2563EB",
            "transform": "scale(1.1)"
        },
        
        on_click=QuickActionsState.toggle_sidebar
    )


def quick_actions_sidebar() -> rx.Component:
    """
    Sidebar flotante con acciones rápidas para desktop.
    
    Returns:
        Componente del sidebar completo
    """
    
    return rx.cond(
        # Solo mostrar en desktop (>= 1024px) y si está visible
        QuickActionsState.is_visible,
        rx.box(
            # Botón de toggle
            sidebar_toggle_button(QuickActionsState.is_visible),
            
            # Contenido del sidebar
            rx.box(
                rx.vstack(
                    # Header del sidebar
                    rx.hstack(
                        rx.box(
                            rx.icon(
                                tag="zap",
                                size=SizeIcon.MEDIUM.value,
                                color=Color.info.value
                            ),
                            padding="6px",
                            border_radius=BorderRadius.SMALL.value,
                            background=Color.icon_background.value
                        ),
                        rx.cond(
                            QuickActionsState.is_expanded,
                            rx.vstack(
                                rx.text(
                                    "Acciones",
                                    font_weight=FontWeight.MEDIUM.value,
                                    color=ColorText.GRAY_800.value,
                                    size="3"
                                ),
                                rx.text(
                                    "Rápidas",
                                    color=ColorText.GRAY_500.value,
                                    size="2"
                                ),
                                spacing="0",
                                align="start"
                            ),
                            rx.box()
                        ),
                        rx.button(
                            rx.icon(
                                tag=rx.cond(
                                    QuickActionsState.is_expanded,
                                    "chevron-left",
                                    "chevron-right"
                                ),
                                size=SizeIcon.SMALL.value,
                                color=ColorText.GRAY_500.value
                            ),
                            variant="ghost",
                            size="1",
                            on_click=QuickActionsState.toggle_expand
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                        margin_bottom=SizeSpace.MEDIUM.value
                    ),
                    
                    # Separador
                    rx.box(
                        width="100%",
                        height="1px",
                        background=Color.border_light.value,
                        margin_bottom=SizeSpace.MEDIUM.value
                    ),
                    
                    # Botones de acción principales
                    quick_action_button(
                        icon="pen",
                        label="Editar",
                        description="Modificar información del perfil",
                        action=QuickActionsState.start_editing,
                        color="blue",
                        is_expanded=QuickActionsState.is_expanded,
                        animation_delay="0.1s"
                    ),
                    
                    quick_action_button(
                        icon="copy",
                        label="Duplicar",
                        description="Crear copia del perfil actual",
                        action=QuickActionsState.duplicate_profile,
                        color="green",
                        is_expanded=QuickActionsState.is_expanded,
                        animation_delay="0.2s"
                    ),
                    
                    # Separador
                    rx.box(
                        width="100%",
                        height="1px",
                        background=Color.border_light.value,
                        margin=f"{SizeSpace.MEDIUM.value} 0"
                    ),
                    
                    # Botones de exportación
                    quick_action_button(
                        icon="download",
                        label="Exportar",
                        description="Descargar datos del perfil",
                        action=QuickActionsState.export_profile,
                        color="orange",
                        is_expanded=QuickActionsState.is_expanded,
                        animation_delay="0.3s"
                    ),
                    
                    quick_action_button(
                        icon="printer",
                        label="Imprimir",
                        description="Generar versión imprimible",
                        action=QuickActionsState.print_profile,
                        color="purple",
                        is_expanded=QuickActionsState.is_expanded,
                        animation_delay="0.4s"
                    ),
                    
                    quick_action_button(
                        icon="share",
                        label="Compartir",
                        description="Compartir enlace del perfil",
                        action=QuickActionsState.share_profile,
                        color="blue",
                        is_expanded=QuickActionsState.is_expanded,
                        animation_delay="0.5s"
                    ),
                    
                    # Espaciador
                    rx.box(flex="1"),
                    
                    # Footer con información
                    rx.cond(
                        QuickActionsState.is_expanded,
                        rx.box(
                            rx.text(
                                "Acciones contextuales",
                                color=ColorText.GRAY_500.value,
                                size="1",
                                text_align="center",
                                width="100%"
                            ),
                            margin_top=SizeSpace.MEDIUM.value,
                            padding_top=SizeSpace.SMALL.value,
                            border_top=f"1px solid {Color.border_light.value}"
                        ),
                        rx.box()
                    ),
                    
                    spacing="2",
                    align=rx.cond(QuickActionsState.is_expanded, "start", "center"),
                    width="100%",
                    height="100%"
                ),
                
                # Estilos del contenedor del sidebar
                background=Color.background.value,
                border=CommonBorders.LIGHT_SOLID,
                border_radius=BorderRadius.LARGE.value,
                padding=SizeSpace.MEDIUM.value,
                width=rx.cond(QuickActionsState.is_expanded, "200px", "76px"),
                height="100%",
                min_height="400px",
                max_height="600px",
                box_shadow="0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                backdrop_filter="blur(8px)",
                transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                overflow="hidden"
            ),
            
            # Posicionamiento fijo del sidebar
            position="fixed",
            top="50%",
            right="20px",
            transform="translateY(-50%)",
            z_index="1000",
            
            # Animación de entrada del sidebar completo
            animation="slideInFromRightSidebar 0.6s ease-out",
            style={
                "@keyframes slideInFromRightSidebar": {
                    "0%": {
                        "opacity": "0",
                        "transform": "translateY(-50%) translateX(100%)"
                    },
                    "100%": {
                        "opacity": "1",
                        "transform": "translateY(-50%) translateX(0)"
                    }
                },
                # Media query para ocultar en móvil/tablet
                "@media (max-width: 1023px)": {
                    "display": "none"
                }
            }
        ),
        
        # Botón flotante minimalista cuando está oculto
        rx.button(
            rx.icon(
                tag="zap",
                size=SizeIcon.SMALL.value,
                color="white"
            ),
            
            # Estilos del botón flotante
            position="fixed",
            top="50%",
            right="20px", 
            transform="translateY(-50%)",
            width="44px",
            height="44px",
            border_radius=BorderRadius.ROUND.value,
            background=Color.info.value,
            border="2px solid white",
            box_shadow="0 4px 12px rgba(0, 0, 0, 0.15)",
            cursor="pointer",
            z_index="1000",
            transition="all 0.2s ease-in-out",
            
            _hover={
                "background": "#2563EB",
                "transform": "translateY(-50%) scale(1.1)"
            },
            
            on_click=QuickActionsState.toggle_sidebar,
            
            # Ocultar en móvil/tablet
            style={
                "@media (max-width: 1023px)": {
                    "display": "none"
                }
            }
        )
    )