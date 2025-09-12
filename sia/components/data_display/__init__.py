"""
Módulo de componentes para visualización de datos.
"""
from .organisms import user_statistics, user_table
from .molecules import render_user_name, render_user_role, render_user_status, render_user_actions
from .tables import data_table
from .avatars import avatar

__all__ = [
    # Organismos
    "user_statistics",
    "user_table",
    # Moléculas
    "render_user_name",
    "render_user_role",
    "render_user_status", 
    "render_user_actions",
    # Tablas
    "data_table",
    # Avatares
    "avatar",
]