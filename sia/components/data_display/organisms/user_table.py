"""
Organismo de tabla de usuarios.
Tabla completa con renderizado personalizado para datos de usuarios.
"""
import reflex as rx
from sia.components.data_display.tables import data_table
from sia.components.data_display.molecules.user_renders import (
    render_user_name,
    render_user_role,
    render_user_status,
    render_user_actions,
)


def user_table() -> rx.Component:
    """
    Organismo que muestra tabla de usuarios con renderizado personalizado.
    
    Returns:
        rx.Component: Tabla completa de usuarios
    """
    # Obtener datos del estado
    from sia.pages.usuarios import UserState
    
    # Configuración de headers
    headers = ["Usuario", "Rol", "Estado", "Área", "Permisos", "Acciones"]
    
    # Funciones de renderizado personalizadas
    render_functions = {
        "name": render_user_name,
        "role": render_user_role,
        "status": render_user_status,
        "actions": render_user_actions,
    }
    
    return data_table(
        title="Gestión de Usuarios",
        data=UserState.users_data,
        headers=headers,
        render_functions=render_functions,
        show_counter=True,
        counter_text="usuarios",
        actions_column=True,
    )