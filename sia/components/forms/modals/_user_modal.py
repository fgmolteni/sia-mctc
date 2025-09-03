import reflex as rx
from sia.components.forms.inputs import (
    form_input, 
    password_input_with_strength,
    select_input,
    get_user_validation_rules,
    get_placeholder_by_field
)
from sia.components.forms.selects import form_select
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, SizeText
from sia.styles.fonts import FontWeight
from sia.styles.border import BorderRadius
from typing import Dict, List


def user_modal() -> rx.Component:
    """
    Modal para crear/editar usuarios del sistema.
    
    Funcionalidad:
    - Modo crear: form_is_editing = False
    - Modo editar: form_is_editing = True  
    - Campos: nombre, apellido, nombre_usuario, contraseña (solo crear), rol
    - Validación de campos requeridos
    - Integración con design system del proyecto
    
    Returns:
        rx.Component: Modal de usuario o None si está cerrado
    """
    # Importación tardía para evitar importación circular
    from sia.pages.usuarios import UserState
    
    # Definir opciones para el select de rol según las pruebas TDD
    role_options: List[Dict[str, str]] = [
        {"value": "usuario", "label": "Usuario"},
        {"value": "supervisor", "label": "Supervisor"}, 
        {"value": "admin", "label": "Administrador"}
    ]
    
    # Obtener reglas de validación para usuarios
    validation_rules = get_user_validation_rules()
    
    # Usar rx.cond para controlar la renderización del modal
    return rx.cond(
        UserState.show_user_modal,
        _render_modal_content(role_options, UserState, validation_rules),
        ""  # Retornar cadena vacía cuando está cerrado según las pruebas TDD
    )


def _render_modal_content(role_options: List[Dict[str, str]], UserState, validation_rules: Dict) -> rx.Component:
    """Renderiza el contenido del modal."""
    
    return rx.dialog.root(
        rx.dialog.content(
            # Header del modal
            rx.dialog.title(
                rx.hstack(
                    rx.heading(
                        rx.cond(
                            UserState.form_is_editing,
                            "Editar Usuario",
                            "Crear Usuario"
                        ),
                        font_size=SizeText.LARGE.value,
                        font_weight=FontWeight.BOLD.value,
                        color=ColorText.GRAY_800.value,
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon(tag="x", cursor="pointer")
                    ),
                    width="100%",
                    align="center",
                    padding_bottom=SizeSpace.MEDIUM.value,
                    border_bottom=f"1px solid {Color.border_light.value}",
                )
            ),
            
            # Body del modal con formulario
            rx.vstack(
                # Campo nombre
                form_input(
                    label="Nombre",
                    placeholder=get_placeholder_by_field("nombre"),
                    type="text",
                    name="nombre",
                    value=UserState.form_nombre,
                    on_change=UserState.set_form_nombre,
                    required=True,
                    validation_rules=validation_rules.get("nombre"),
                    helper_text=validation_rules.get("nombre", {}).get("helper_text"),
                    max_length=validation_rules.get("nombre", {}).get("max_length")
                ),
                
                # Campo apellido
                form_input(
                    label="Apellido",
                    placeholder=get_placeholder_by_field("apellido"),
                    type="text",
                    name="apellido", 
                    value=UserState.form_apellido,
                    on_change=UserState.set_form_apellido,
                    required=True,
                    validation_rules=validation_rules.get("apellido"),
                    helper_text=validation_rules.get("apellido", {}).get("helper_text"),
                    max_length=validation_rules.get("apellido", {}).get("max_length")
                ),
                
                # Campo nombre de usuario
                form_input(
                    label="Nombre de Usuario",
                    placeholder=get_placeholder_by_field("nombre_usuario"),
                    type="text",
                    name="nombre_usuario",
                    value=UserState.form_nombre_usuario,
                    on_change=UserState.set_form_nombre_usuario,
                    required=True,
                    validation_rules=validation_rules.get("nombre_usuario"),
                    helper_text=validation_rules.get("nombre_usuario", {}).get("helper_text"),
                    show_counter=True,
                    max_length=validation_rules.get("nombre_usuario", {}).get("max_length")
                ),
                
                # Campo email
                form_input(
                    label="Email",
                    placeholder=get_placeholder_by_field("email"),
                    type="email",
                    name="email",
                    value=UserState.form_email,
                    on_change=UserState.set_form_email,
                    required=True,
                    validation_rules=validation_rules.get("email"),
                    helper_text=validation_rules.get("email", {}).get("helper_text"),
                    show_counter=True,
                    max_length=validation_rules.get("email", {}).get("max_length")
                ),
                
                # Campo contraseña - solo en modo crear
                rx.cond(
                    ~UserState.form_is_editing,  # Solo mostrar si NO está editando
                    password_input_with_strength(
                        label="Contraseña",
                        placeholder=get_placeholder_by_field("contrasena"),
                        name="contrasena",
                        value=UserState.form_contrasena,
                        on_change=UserState.set_form_contrasena,
                        required=True,
                        helper_text="Al menos 6 caracteres, una letra y un número"
                    )
                ),
                
                # Campo rol - select
                select_input(
                    label="Rol",
                    placeholder="Seleccione un rol",
                    options=["admin", "supervisor", "usuario"],
                    name="rol",
                    value=UserState.form_rol,
                    on_change=UserState.set_form_rol,
                    required=True,
                    helper_text="Define los permisos del usuario en el sistema"
                ),
                
                spacing="6",
                width="100%",
                align="start",
                padding_y=SizeSpace.LARGE.value,
            ),
            
            # Footer del modal con botones
            rx.hstack(
                # Botón cancelar
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="outline",
                        color_scheme="gray",
                        disabled=UserState.is_loading,
                    )
                ),
                
                # Botón submit (crear o actualizar)
                rx.button(
                    rx.cond(
                        UserState.is_loading,
                        rx.hstack(
                            rx.spinner(size="2"),
                            rx.text("Procesando..."),
                            spacing="2",
                        ),
                        rx.cond(
                            UserState.form_is_editing,
                            "Actualizar Usuario",
                            "Crear Usuario"
                        )
                    ),
                    color_scheme="blue",
                    on_click=rx.cond(
                        UserState.form_is_editing,
                        UserState.update_user_submit,
                        UserState.create_user_submit
                    ),
                    disabled=UserState.is_loading,
                ),
                
                spacing="3",
                justify="end",
                width="100%",
                padding_top=SizeSpace.MEDIUM.value,
                border_top=f"1px solid {Color.border_light.value}",
            ),
            
            # Estilos del contenido del diálogo
            max_width="500px",
            width="90%",
            bg=Color.background.value,
            border_radius=BorderRadius.LARGE.value,
        ),
        open=UserState.show_user_modal,
        on_open_change=UserState.close_user_modal,
    )