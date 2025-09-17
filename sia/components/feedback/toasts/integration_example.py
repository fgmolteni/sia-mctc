"""
Ejemplo de integración del sistema de toasts en el proyecto SIA.

Este archivo muestra diferentes formas de usar el sistema de toasts
en páginas y componentes de la aplicación.
"""

import reflex as rx
from typing import List

# Imports del sistema de toasts
from . import (
    toast_container,
    ToastState,
    show_toast_success,
    show_toast_error,
    show_toast_warning,
    show_toast_info,
    ToastType
)


class ExamplePageState(rx.State):
    """Estado de ejemplo que demuestra el uso de toasts."""
    
    users: List[str] = ["Usuario 1", "Usuario 2", "Usuario 3"]
    
    def handle_save_user(self):
        """Ejemplo de guardado de usuario con toast de éxito."""
        try:
            # Simular lógica de guardado
            success = True  # En tu código real, esto vendría de la base de datos
            
            if success:
                show_toast_success("Usuario guardado exitosamente")
            else:
                show_toast_error("Error al guardar el usuario")
                
        except Exception as e:
            show_toast_error(f"Error inesperado: {str(e)}")
    
    def handle_delete_user(self, user_id: str):
        """Ejemplo de eliminación con toast de advertencia y error."""
        try:
            # Mostrar advertencia antes de eliminar
            show_toast_warning("Eliminando usuario...")
            
            # Simular eliminación
            deleted = False  # En tu código real, aquí iría la lógica de eliminación
            
            if deleted:
                show_toast_success("Usuario eliminado correctamente")
            else:
                show_toast_error("No se pudo eliminar el usuario")
                
        except Exception as e:
            show_toast_error(f"Error al eliminar: {str(e)}")
    
    def handle_load_data(self):
        """Ejemplo de carga de datos con toast informativo."""
        # Mostrar información de carga
        show_toast_info("Cargando datos...")
        
        try:
            # Simular carga
            data_loaded = True
            
            if data_loaded:
                show_toast_success("Datos cargados correctamente")
            else:
                show_toast_warning("Algunos datos no pudieron cargarse")
                
        except Exception as e:
            show_toast_error("Error al cargar los datos")
    
    def handle_validation_error(self):
        """Ejemplo con errores de validación persistentes."""
        # Errores críticos que no se auto-dismiss
        ToastState.show_error(
            "Error crítico: Revisar configuración del sistema",
            auto_dismiss=False  # El usuario debe cerrar manualmente
        )
    
    def handle_advanced_toast(self):
        """Ejemplo de toast avanzado con configuración personalizada."""
        ToastState.add_toast(
            message="Operación completada con advertencias",
            toast_type=ToastType.WARNING,
            auto_dismiss=True,
            dismiss_timeout=8000,  # 8 segundos
            on_dismiss=lambda: print("Toast de advertencia cerrado")
        )


def example_page() -> rx.Component:
    """
    Página de ejemplo que demuestra el uso del sistema de toasts.
    
    Incluye el contenedor de toasts y varios botones para probar
    diferentes tipos de notificaciones.
    """
    return rx.vstack(
        # Header de la página
        rx.heading("Ejemplo del Sistema de Toasts", size="8"),
        rx.text("Prueba diferentes tipos de notificaciones", color="gray"),
        
        # Botones de ejemplo
        rx.hstack(
            rx.button(
                "Guardar Usuario",
                on_click=ExamplePageState.handle_save_user,
                color_scheme="green"
            ),
            rx.button(
                "Eliminar Usuario", 
                on_click=lambda: ExamplePageState.handle_delete_user("user-1"),
                color_scheme="red"
            ),
            rx.button(
                "Cargar Datos",
                on_click=ExamplePageState.handle_load_data,
                color_scheme="blue"
            ),
            spacing="3"
        ),
        
        rx.hstack(
            rx.button(
                "Error Crítico",
                on_click=ExamplePageState.handle_validation_error,
                color_scheme="red",
                variant="outline"
            ),
            rx.button(
                "Toast Avanzado",
                on_click=ExamplePageState.handle_advanced_toast,
                color_scheme="orange"
            ),
            spacing="3"
        ),
        
        # Información sobre toasts activos
        rx.cond(
            ToastState.has_toasts(),
            rx.text(
                f"Toasts activos: {ToastState.get_toasts_count()}",
                color="blue"
            ),
            rx.text("No hay toasts activos", color="gray")
        ),
        
        # IMPORTANTE: Incluir el contenedor de toasts
        toast_container(),
        
        spacing="5",
        padding="4",
        align="center",
        min_height="100vh"
    )


# Integración en páginas existentes del proyecto SIA
def integrate_toasts_in_existing_page():
    """
    Ejemplo de cómo integrar toasts en una página existente del proyecto SIA.
    
    Solo necesitas:
    1. Importar las funciones que necesites
    2. Añadir toast_container() a tu layout
    3. Usar show_toast_* en tus event handlers
    """
    
    # Importar en tu página existente
    from sia.components.feedback.toasts import toast_container, show_toast_success
    from sia.pages.usuarios import UserState  # Tu estado existente
    
    # En tu event handler existente, agregar toasts:
    def enhanced_create_user_submit(self):
        """Versión mejorada con toasts del método create_user_submit."""
        try:
            # Tu lógica existente de creación de usuario
            success = True  # Resultado de tu lógica
            
            if success:
                show_toast_success("Usuario creado exitosamente")
                # Limpiar formulario, cerrar modal, etc.
            else:
                show_toast_error("Error al crear el usuario")
                
        except Exception as e:
            show_toast_error(f"Error inesperado: {str(e)}")
    
    # En tu componente de página, agregar el contenedor:
    def your_existing_page():
        return rx.vstack(
            # Tu contenido existente
            rx.heading("Usuarios"),
            # ... resto del contenido
            
            # Añadir al final (o donde prefieras)
            toast_container(),
            
            spacing="4"
        )


# CSS adicional para integración con el tema SIA
INTEGRATION_CSS = """
/* Integración con el tema SIA */
.toast-container {
    font-family: var(--font-family-base, 'Inter', system-ui, sans-serif);
}

.toast-item {
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* Animaciones mejoradas para SIA */
@keyframes sia-toast-entrance {
    from {
        transform: translateX(100%) scale(0.95);
        opacity: 0;
    }
    to {
        transform: translateX(0) scale(1);
        opacity: 1;
    }
}

.toast-item {
    animation: sia-toast-entrance 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Responsive mejorado para SIA */
@media (max-width: 640px) {
    .toast-container {
        top: env(safe-area-inset-top, 10px);
        left: env(safe-area-inset-left, 10px);
        right: env(safe-area-inset-right, 10px);
    }
}
"""
</content>
</invoke>