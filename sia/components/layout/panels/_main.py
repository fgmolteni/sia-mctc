import reflex as rx
from typing import Optional, List, Tuple
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, SizeIcon
from sia.styles.fonts import FontWeight
from sia.styles.border import BorderRadius, CommonBorders
from sia.components.data_display.badges import enhanced_role_badge, enhanced_status_badge

def _get_role_type(role: str) -> rx.Var:
    """Mapea el texto del rol a los tipos soportados por enhanced_role_badge."""
    role_lower = role.lower()
    return rx.cond(
        role_lower.contains("admin") | role_lower.contains("administrador"),
        "admin",
        rx.cond(
            role_lower.contains("supervisor") | role_lower.contains("manager") | role_lower.contains("jefe"),
            "supervisor",
            rx.cond(
                role_lower.contains("usuario") | role_lower.contains("empleado") | role_lower.contains("user"),
                "usuario",
                "default"
            )
        )
    )

def _get_status_type(status: str) -> rx.Var:
    """Mapea el texto del estado a los tipos soportados por enhanced_status_badge."""
    status_lower = status.lower()
    return rx.cond(
        status_lower.contains("activo") | status_lower.contains("active"),
        "active",
        rx.cond(
            status_lower.contains("inactivo") | status_lower.contains("inactive"),
            "inactive",
            rx.cond(
                status_lower.contains("pendiente") | status_lower.contains("pending"),
                "pending",
                rx.cond(
                    status_lower.contains("suspendido") | status_lower.contains("suspended"),
                    "suspended",
                    "default"
                )
            )
        )
    )


def quick_action_button(
    icon: str,
    label: str,
    action: rx.EventHandler = rx.noop,
    color_scheme: str = "blue",
    variant: str = "soft",
    size: str = "2",
    disabled: bool = False,
    tooltip: Optional[str] = None
) -> rx.Component:
    """Botón de acción rápida con icono y label."""
    button = rx.button(
        rx.icon(icon, size=SizeIcon.SMALL.value),
        label,
        on_click=action,
        variant=variant,
        color_scheme=color_scheme,
        size=size,
        disabled=disabled,
        spacing="2",
        title=rx.cond(tooltip != "", tooltip, label)
    )
    
    # Always wrap with tooltip but conditionally set content
    return rx.tooltip(
        button,
        content=rx.cond(tooltip is not None, tooltip, ""),
        side="bottom",
        disabled=(tooltip is None)
    )


def profile_action_buttons(
    user_id: str = "",
    user_email: str = "",
    is_active: bool = True,
    can_edit: bool = True,
    can_message: bool = True,
    can_disable: bool = True
) -> rx.Component:
    """Grupo de botones de acción específicos para perfil de usuario."""
    return rx.hstack(
        # Editar perfil
        rx.cond(
            can_edit,
            quick_action_button(
                icon="pen",
                label="Editar",
                action=rx.redirect(f"/users/edit/{user_id}"),
                color_scheme="blue",
                variant="soft",
                tooltip="Editar información del usuario"
            )
        ),
        
        # Enviar mensaje/email
        rx.cond(
            can_message & (user_email != ""),
            quick_action_button(
                icon="mail",
                label="Mensaje",
                action=rx.window_alert(f"Enviar mensaje a: {user_email}"),  # Placeholder
                color_scheme="green",
                variant="soft", 
                tooltip=f"Enviar mensaje a {user_email}"
            )
        ),
        
        # Activar/Desactivar usuario
        rx.cond(
            can_disable,
            quick_action_button(
                icon=rx.cond(is_active, "user-x", "user-check"),
                label=rx.cond(is_active, "Desactivar", "Activar"),
                action=rx.window_alert(rx.cond(is_active, "Desactivar usuario", "Activar usuario")),  # Placeholder
                color_scheme=rx.cond(is_active, "red", "green"),
                variant="soft",
                tooltip=rx.cond(is_active, "Desactivar usuario", "Activar usuario")
            )
        ),
        
        # Más opciones (dropdown)
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("more-horizontal", size=SizeIcon.SMALL.value),
                    variant="soft",
                    color_scheme="gray",
                    size="2",
                    title="Más opciones"
                )
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.icon("history", size=SizeIcon.SMALL.value),
                    "Ver historial",
                    on_click=rx.window_alert("Ver historial de usuario")  # Placeholder
                ),
                rx.menu.item(
                    rx.icon("shield", size=SizeIcon.SMALL.value),
                    "Permisos",
                    on_click=rx.window_alert("Gestionar permisos")  # Placeholder
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.icon("download", size=SizeIcon.SMALL.value),
                    "Exportar datos",
                    on_click=rx.window_alert("Exportar datos del usuario")  # Placeholder
                ),
                rx.menu.item(
                    rx.icon("copy", size=SizeIcon.SMALL.value),
                    "Copiar enlace",
                    on_click=rx.window_alert(f"Copiar enlace: /profiles/{user_id}")  # Placeholder
                ),
            ),
        ),
        
        spacing="2",
        align="center"
    )


def user_status_indicator(
    is_online: bool = False,
    last_activity: str = "",
    status_text: str = "Activo"
) -> rx.Component:
    """Indicador visual del estado del usuario."""
    return rx.hstack(
        # Indicador online/offline
        rx.box(
            width="8px",
            height="8px",
            border_radius=BorderRadius.ROUND.value,
            background=Color.success.value if is_online else Color.icon_inactive.value,
            box_shadow="0 0 0 2px white, 0 0 0 3px " + (Color.success.value + "40" if is_online else Color.border_light.value)
        ),
        
        # Texto de estado
        rx.vstack(
            rx.text(
                status_text,
                font_weight=FontWeight.MEDIUM.value,
                color=ColorText.GRAY_800.value,
                size="2"
            ),
            rx.cond(
                last_activity,
                rx.text(
                    f"Último acceso: {last_activity}",
                    color=ColorText.GRAY_500.value,
                    size="1"
                )
            ),
            align="start",
            spacing="0"
        ),
        
        spacing="2",
        align="center"
    )


def enhanced_profile_header(
    user_name: str = "",
    user_email: str = "",
    user_role: str = "",
    user_status: str = "Activo",
    user_id: str = "",
    avatar_component: Optional[rx.Component] = None,
    role_color: str = "blue",
    is_online: bool = False,
    last_activity: str = "",
    show_quick_actions: bool = True,
    can_edit: bool = True,
    can_message: bool = True,
    can_disable: bool = True
) -> rx.Component:
    """Header mejorado del perfil con quick actions e indicadores de estado."""
    return rx.flex(
        # Avatar con indicador de estado
        rx.box(
            avatar_component or rx.avatar(
                fallback=user_name[:2] if user_name else "U",
                size="8",
                color_scheme=role_color
            ),
            position="relative",
            _after={
                "content": '""',
                "position": "absolute",
                "bottom": "4px",
                "right": "4px", 
                "width": "16px",
                "height": "16px",
                "border_radius": "50%",
                "background": Color.success.value if is_online else Color.icon_inactive.value,
                "border": f"2px solid {Color.background.value}",
                "box_shadow": "0 0 0 1px " + (Color.success.value + "40" if is_online else Color.border_light.value)
            } if is_online or not is_online else {}
        ),
        
        # Información del usuario
        rx.vstack(
            # Nombre y estado
            rx.hstack(
                rx.heading(
                    rx.cond(user_name != "", user_name, "Usuario"),
                    size="6",
                    font_weight=FontWeight.BOLD.value,
                    color=ColorText.GRAY_800.value
                ),
                # Indicador de actividad en tiempo real
                rx.cond(
                    is_online,
                    enhanced_status_badge(
                        "En línea",
                        status="active",
                        show_icon=True,
                        size="sm",
                        variant="pulse"
                    ),
                    enhanced_status_badge(
                        "Fuera de línea",
                        status="inactive",
                        show_icon=True,
                        size="sm",
                        variant="solid"
                    )
                ),
                spacing="3",
                align="center"
            ),
            
            # Email y última actividad
            rx.hstack(
                rx.cond(
                    user_email,
                    rx.text(
                        user_email,
                        color=ColorText.GRAY_500.value,
                        size="3",
                        font_weight=FontWeight.MEDIUM.value
                    )
                ),
                rx.cond(
                    last_activity,
                    rx.text(
                        f"• Último acceso: {last_activity}",
                        color=ColorText.GRAY_500.value,
                        size="2"
                    )
                ),
                spacing="2",
                align="center",
                flex_wrap="wrap"
            ),
            
            # Rol y estado con badges mejorados
            rx.hstack(
                rx.cond(
                    user_role,
                    enhanced_role_badge(
                        user_role,
                        role=_get_role_type(user_role),
                        show_icon=True,
                        size="md",
                        variant="gradient"
                    )
                ),
                rx.cond(
                    user_status,
                    enhanced_status_badge(
                        user_status,
                        status=_get_status_type(user_status),
                        show_icon=True,
                        size="md",
                        variant="gradient"
                    )
                ),
                spacing="2",
                align="center"
            ),
            
            align_items="start",
            spacing="2",
            flex_grow="1"
        ),
        
        # Quick Actions
        rx.cond(
            show_quick_actions,
            profile_action_buttons(
                user_id=user_id,
                user_email=user_email,
                is_active=user_status == "Activo",
                can_edit=can_edit,
                can_message=can_message,
                can_disable=can_disable
            )
        ),
        
        direction="row",
        align_items="center", 
        spacing="6",
        padding=SizeSpace.LARGE.value,
        background=Color.background.value,
        border_radius=BorderRadius.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        width="100%",
        max_width="1000px",
        box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)"
    )


def quick_actions_panel(actions: List[Tuple[str, str, rx.EventHandler, str]]) -> rx.Component:
    """
    Panel de acciones rápidas genérico.
    
    Args:
        actions: Lista de tuplas (icono, label, acción, color_scheme)
    """
    return rx.hstack(
        *[
            quick_action_button(
                icon=action[0],
                label=action[1], 
                action=action[2],
                color_scheme=action[3] if len(action) > 3 else "blue"
            )
            for action in actions
        ],
        spacing="2",
        align="center"
    )