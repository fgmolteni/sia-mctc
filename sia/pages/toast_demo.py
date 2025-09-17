"""
Página de demostración del sistema de toasts de SIA.

Esta página permite probar todas las funcionalidades del sistema de toasts,
incluyendo auto-dismiss, diferentes tipos y timeouts personalizados.
"""

import reflex as rx
from sia.components.feedback.toasts._state import ToastState
from sia.components.feedback.toasts._types import ToastType
from sia.components.feedback.toasts._container import toast_container


class ToastDemoState(rx.State):
    """Estado para la página de demostración de toasts."""
    
    # Contador para mensajes únicos
    message_counter: int = 0
    
    def show_success_toast(self):
        """Muestra un toast de éxito con auto-dismiss."""
        self.message_counter += 1
        ToastState.show_success(f"¡Operación exitosa #{self.message_counter}!")
    
    def show_error_toast(self):
        """Muestra un toast de error sin auto-dismiss."""
        self.message_counter += 1
        ToastState.show_error(
            f"Error en el sistema #{self.message_counter}. Revisar logs.",
            auto_dismiss=False
        )
    
    def show_warning_toast(self):
        """Muestra un toast de advertencia con auto-dismiss."""
        self.message_counter += 1
        ToastState.show_warning(f"Advertencia: Acción requerida #{self.message_counter}")
    
    def show_info_toast(self):
        """Muestra un toast informativo con auto-dismiss."""
        self.message_counter += 1
        ToastState.show_info(f"Información del sistema #{self.message_counter}")
    
    def show_custom_toast(self):
        """Muestra un toast con configuración personalizada."""
        self.message_counter += 1
        ToastState.add_toast(
            message=f"Toast personalizado #{self.message_counter} (10 segundos)",
            toast_type=ToastType.INFO,
            auto_dismiss=True,
            dismiss_timeout=10000  # 10 segundos
        )
    
    def show_multiple_toasts(self):
        """Muestra varios toasts rápidamente para probar el sistema."""
        base_count = self.message_counter
        ToastState.show_success(f"Éxito #{base_count + 1}")
        ToastState.show_warning(f"Advertencia #{base_count + 2}")
        ToastState.show_info(f"Info #{base_count + 3}")
        ToastState.show_error(f"Error #{base_count + 4}", auto_dismiss=False)
        self.message_counter += 4
    
    def clear_all_toasts(self):
        """Elimina todos los toasts activos."""
        ToastState.dismiss_all_toasts()


def toast_demo() -> rx.Component:
    """
    Página de demostración del sistema de toasts.
    
    Incluye botones para probar diferentes tipos de toasts,
    configuraciones personalizadas y el comportamiento de auto-dismiss.
    
    Returns:
        rx.Component: Página de demostración completa
    """
    return rx.fragment(
        # Contenedor de toasts (debe estar en todas las páginas que usen toasts)
        toast_container(),
        
        # Contenido de la página
        rx.container(
            rx.vstack(
                # Encabezado
                rx.heading(
                    "Demostración del Sistema de Toasts",
                    size="8",
                    margin_bottom="2"
                ),
                rx.text(
                    "Prueba todas las funcionalidades del sistema de toasts de SIA",
                    color="gray",
                    margin_bottom="6"
                ),
                
                # Sección: Tipos básicos de toast
                rx.card(
                    rx.vstack(
                        rx.heading("Tipos Básicos de Toast", size="6"),
                        rx.text(
                            "Los toasts de éxito, advertencia e info se auto-eliminan después de 4 segundos. "
                            "Los toasts de error permanecen hasta ser cerrados manualmente.",
                            color="gray",
                            margin_bottom="4"
                        ),
                        rx.hstack(
                            rx.button(
                                "✓ Éxito",
                                on_click=ToastDemoState.show_success_toast,
                                color_scheme="green",
                                size="2"
                            ),
                            rx.button(
                                "✕ Error",
                                on_click=ToastDemoState.show_error_toast,
                                color_scheme="red",
                                size="2"
                            ),
                            rx.button(
                                "⚠ Advertencia",
                                on_click=ToastDemoState.show_warning_toast,
                                color_scheme="orange",
                                size="2"
                            ),
                            rx.button(
                                "ℹ Información",
                                on_click=ToastDemoState.show_info_toast,
                                color_scheme="blue",
                                size="2"
                            ),
                            spacing="3",
                            wrap="wrap"
                        ),
                        spacing="4",
                        align="start"
                    ),
                    padding="4",
                    width="100%"
                ),
                
                # Sección: Configuración personalizada
                rx.card(
                    rx.vstack(
                        rx.heading("Configuración Personalizada", size="6"),
                        rx.text(
                            "Toast con timeout personalizado de 10 segundos en lugar de los 4 segundos por defecto.",
                            color="gray",
                            margin_bottom="4"
                        ),
                        rx.hstack(
                            rx.button(
                                "Toast 10 segundos",
                                on_click=ToastDemoState.show_custom_toast,
                                color_scheme="purple",
                                size="2"
                            ),
                            spacing="3"
                        ),
                        spacing="4",
                        align="start"
                    ),
                    padding="4",
                    width="100%"
                ),
                
                # Sección: Prueba de múltiples toasts
                rx.card(
                    rx.vstack(
                        rx.heading("Prueba de Múltiples Toasts", size="6"),
                        rx.text(
                            "Prueba el comportamiento con múltiples toasts simultáneos y el límite máximo de 5 toasts.",
                            color="gray",
                            margin_bottom="4"
                        ),
                        rx.hstack(
                            rx.button(
                                "Múltiples Toasts",
                                on_click=ToastDemoState.show_multiple_toasts,
                                color_scheme="cyan",
                                size="2"
                            ),
                            rx.button(
                                "Limpiar Todos",
                                on_click=ToastDemoState.clear_all_toasts,
                                color_scheme="gray",
                                size="2",
                                variant="soft"
                            ),
                            spacing="3"
                        ),
                        spacing="4",
                        align="start"
                    ),
                    padding="4",
                    width="100%"
                ),
                
                # Sección: Información del sistema
                rx.card(
                    rx.vstack(
                        rx.heading("Información del Sistema", size="6"),
                        rx.unordered_list(
                            rx.list_item("Auto-dismiss: Los toasts se eliminan automáticamente después del tiempo configurado"),
                            rx.list_item("Hover-pause: Al pasar el mouse sobre un toast, se pausa el auto-dismiss"),
                            rx.list_item("Dismiss manual: Todos los toasts pueden cerrarse manualmente con el botón X"),
                            rx.list_item("Límite máximo: Se mantienen máximo 5 toasts simultáneos (FIFO)"),
                            rx.list_item("Animaciones: Entrada desde la derecha, salida hacia la derecha"),
                            rx.list_item("Responsive: Posicionamiento adaptativo en dispositivos móviles")
                        ),
                        spacing="4",
                        align="start"
                    ),
                    padding="4",
                    width="100%"
                ),
                
                spacing="6",
                align="start",
                width="100%"
            ),
            padding="4",
            max_width="800px"
        )
    )