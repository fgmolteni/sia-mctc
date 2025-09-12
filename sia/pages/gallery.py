import reflex as rx
from sia.components.layout.headers import page_header
from sia.components.forms.buttons import (
    button_general,
    button_redondo,
    button_sin_fondo,
    form_button,
    form_reset_button,
    button_icon_text_border,
    button_sin_fondo_icon,
)
from sia.components.data_display.cards import card_profile, info_card_profile
from sia.components.data_display.avatars import avatar, avatar_circle
from sia.components.data_display.badges import role_badge, status_badge
from sia.components.layout.cards import stat_card
# Imports temporalmente comentados hasta implementar componentes faltantes
# from sia.components.data_display.menus import menu_user
# from sia.components.data_display.timelines import timeline
from sia.components.data_display.tables import data_table
# from sia.components.navigation.steps import steps_example
# from sia.components.navigation.breadcrumbs import breadcrumb
# from sia.components.forms.inputs import form_input, form_date_input, form_time_input
# from sia.components.forms.selects import form_select, select_component
# from sia.components.feedback.banners import top_banner_gradient
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeSpace, BorderRadius


def _create_section(title: str, description: str, content: rx.Component) -> rx.Component:
    """Helper function to create a consistent section layout."""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                title,
                size="6",
                color=ColorText.TERCEARY.value,
                font_weight="600"
            ),
            rx.spacer(),
            width="100%",
            align_items="center",
        ),
        rx.text(
            description,
            color=ColorText.GRAY_500.value,
            size="3",
            margin_bottom=SizeSpace.MEDIUM.value
        ),
        rx.box(
            content,
            background=Color.background_light.value,
            border_radius=BorderRadius.SMALL.value,
            border=f"1px solid {Color.border_light.value}",
            padding=SizeSpace.LARGE.value,
            width="100%"
        ),
        spacing="4",
        width="100%",
        margin_bottom=SizeSpace.X_LARGE.value
    )


def gallery_page() -> rx.Component:
    """A page to display all the refactored components."""
    return rx.vstack(
        # Header principal
        page_header(
            title="Galería de Componentes", 
            subtitle="Un lugar para ver y probar todos los componentes reutilizables del sistema."
        ),
        
        # Contenido principal
        rx.container(
            rx.vstack(
                # Sección Banners
                _create_section(
                     "Banners",
                     "Componentes de banner para destacar información importante",
                     rx.vstack(
                         top_banner_gradient(),
                         spacing="4"
                     )
                 ),

                # Sección Headers
                _create_section(
                     "Headers",
                     "Cabeceras de página con títulos, subtítulos y botones de acción",
                     rx.vstack(
                         page_header(
                             title="Header de Página", 
                             subtitle="Este es un subtítulo de ejemplo", 
                             action_button=button_general(text="Acción")
                         ),
                         spacing="4"
                     )
                 ),

                # Sección Cards
                _create_section(
                    "Cards",
                    "Tarjetas para mostrar información de manera organizada",
                    rx.grid(
                        card_profile(title="Perfil Básico", value="$1,234.56", user_initials="CP"),
                        info_card_profile(
                            title="Tarjeta de Información",
                            content=rx.text("Este es el contenido principal de la tarjeta."),
                            icon="info",
                            badge_text="Activo",
                            show_footer=True,
                            footer_text="Última actualización: hace 2 horas"
                        ),
                        columns="2",
                         spacing="5",
                         width="100%"
                    )
                ),

                # Sección Buttons
                _create_section(
                    "Buttons",
                    "Botones con diferentes estilos y funcionalidades",
                    rx.vstack(
                        rx.text("Botones básicos:", font_weight="500", color=ColorText.GRAY_700.value),
                        rx.flex(
                             button_general("General"),
                             button_redondo("Redondo", url="#"),
                             button_sin_fondo("Sin Fondo"),
                             form_button("Submit"),
                             form_reset_button("Reset"),
                             spacing="4",
                             wrap="wrap",
                             gap="4"
                         ),
                        rx.text("Botones con iconos:", font_weight="500", color=ColorText.GRAY_700.value, margin_top=SizeSpace.LARGE.value),
                        rx.flex(
                             button_icon_text_border(text="Icono y Borde", icon="star"),
                             button_sin_fondo_icon(text="Icono Sin Fondo", icon="heart", url="#", color="red", hover_bg="lightgray"),
                             spacing="4",
                             wrap="wrap",
                             gap="4"
                         ),
                        spacing="4",
                         width="100%",
                         align_items="start"
                    )
                ),

                # Sección Avatars & Menus
                _create_section(
                    "Avatars & Menus",
                    "Avatares de usuario y menús desplegables",
                    rx.hstack(
                        rx.vstack(
                            #rx.text("Avatares:", font_weight="500", color=ColorText.GRAY_700.value),
                            rx.hstack(
                                 avatar(user="Juan Perez", title="juan.perez@empresa.com", size="5"),
                                 avatar_circle(user="JP", size="7"),
                                 spacing="4"
                             ),
                            align_items="start",
                            justify="center",
                        ),
                        rx.vstack(
                            rx.text("Menús:", font_weight="500", color=ColorText.GRAY_700.value),
                            menu_user(),
                            align_items="start"
                        ),
                        spacing="6",
                        align_items="start",
                        justify="center",
                        width="100%"
                    )
                ),

                # Sección Badges
                _create_section(
                    "Badges",
                    "Indicadores visuales para roles, estados y categorías",
                    rx.vstack(
                        rx.vstack(
                            rx.text("Badges de Roles:", font_weight="500", color=ColorText.GRAY_700.value),
                            rx.hstack(
                                role_badge(text="Administrador", role="admin"),
                                role_badge(text="Manager", role="manager"),
                                role_badge(text="Empleado", role="employee"),
                                role_badge(text="Por Defecto", role="default"),
                                spacing="4",
                                wrap="wrap"
                            ),
                            align_items="start",
                            spacing="2"
                        ),
                        rx.vstack(
                            rx.text("Badges de Estado:", font_weight="500", color=ColorText.GRAY_700.value),
                            rx.hstack(
                                status_badge(text="Activo", status="active", show_dot=True),
                                status_badge(text="Inactivo", status="inactive", show_dot=True),
                                status_badge(text="Pendiente", status="pending", show_dot=True),
                                status_badge(text="Éxito", status="success", show_dot=False),
                                status_badge(text="Advertencia", status="warning", show_dot=False),
                                status_badge(text="Error", status="error", show_dot=False),
                                spacing="4",
                                wrap="wrap"
                            ),
                            align_items="start",
                            spacing="2"
                        ),
                        spacing="6",
                        width="100%",
                        align_items="start"
                    )
                ),

                # Sección Statistics Cards
                _create_section(
                    "Statistics Cards",
                    "Tarjetas de estadísticas reutilizables para mostrar métricas",
                    rx.grid(
                        stat_card(
                            title="Total Usuarios",
                            value="124",
                            icon="users",
                            icon_color="blue.400"
                        ),
                        stat_card(
                            title="Ventas del Mes",
                            value="$45,230",
                            icon="trending_up",
                            icon_color="green.400"
                        ),
                        stat_card(
                            title="Pedidos Pendientes",
                            value="18",
                            icon="clock",
                            icon_color="orange.400"
                        ),
                        stat_card(
                            title="Productos Activos",
                            value="89",
                            icon="package",
                            icon_color="purple.400"
                        ),
                        columns="4",
                        spacing="4",
                        width="100%"
                    )
                ),

                # Sección Inputs & Selects
                _create_section(
                    "Inputs & Selects",
                    "Campos de entrada y selectores para formularios",
                    rx.grid(
                        form_input(label="Nombre", placeholder="Ingrese su nombre", type="text", name="name"),
                        form_date_input(label="Fecha", name="date"),
                        form_time_input(label="Hora", name="time"),
                        form_select(label="Opción", name="option", options=["Opción 1", "Opción 2"]),
                        select_component(placeholder="Selección Custom", options=["A", "B"]),
                        columns="3",
                         spacing="5",
                         width="100%"
                    )
                ),

                # Sección Tables
                _create_section(
                    "Data Tables",
                    "Tablas de datos reutilizables con acciones personalizables",
                    rx.vstack(
                        data_table(
                            title="Ejemplo de Tabla",
                            data=[
                                {"id": 1, "name": "Juan Pérez", "role": "admin", "status": "active", "email": "juan@example.com"},
                                {"id": 2, "name": "María García", "role": "user", "status": "inactive", "email": "maria@example.com"},
                                {"id": 3, "name": "Carlos López", "role": "moderator", "status": "active", "email": "carlos@example.com"}
                            ],
                            headers=[
                                {"key": "name", "label": "Nombre"},
                                {"key": "role", "label": "Rol"},
                                {"key": "status", "label": "Estado"},
                                {"key": "email", "label": "Email"}
                            ],
                            render_functions={
                                "role": lambda value, _row: role_badge(
                                    text=value.capitalize(),
                                    role=value if value in ["admin", "manager", "employee"] else "default",
                                ),
                                "status": lambda value, _row: status_badge(
                                    text=value.capitalize(),
                                    status=value,
                                ),
                            },
                            actions=[
                                {"label": "Ver", "icon": "eye", "color": "blue"},
                                {"label": "Editar", "icon": "edit", "color": "green"},
                                {"separator": True},
                                {"label": "Eliminar", "icon": "trash", "color": "red"}
                            ],
                            show_counter=True
                        ),
                        spacing="4",
                        width="100%"
                    )
                ),

                # Sección Navigation Elements
                _create_section(
                    "Navigation Elements",
                    "Elementos de navegación como breadcrumbs, steps y timeline",
                    rx.vstack(
                        rx.vstack(
                            rx.text("Breadcrumbs:", font_weight="500", color=ColorText.GRAY_700.value),
                            breadcrumb(items=[
                                {"title": rx.icon(tag="home"), "href": "#"},
                                {"title": rx.text("Galería"), "href": "#"},
                                {"title": rx.text("Navegación")}
                            ]),
                            align_items="start",
                             spacing="2"
                        ),
                        rx.vstack(
                            rx.text("Steps:", font_weight="500", color=ColorText.GRAY_700.value),
                            steps_example(),
                            align_items="start",
                             spacing="2"
                        ),
                        rx.vstack(
                            rx.text("Timeline:", font_weight="500", color=ColorText.GRAY_700.value),
                            timeline(items=[
                                {"children": rx.text("Paso 1"), "color": "green"},
                                {"children": rx.text("Paso 2"), "color": "blue"},
                                {"children": rx.text("Paso 3"), "color": "red"},
                            ]),
                            align_items="start",
                             spacing="2"
                        ),
                        spacing="6",
                         width="100%",
                         align_items="start"
                    )
                ),

                spacing="6",
                 width="100%"
            ),
            max_width="1200px",
            padding_x=SizeSpace.LARGE.value,
            padding_y=SizeSpace.X_LARGE.value
        ),
        align="center",
        padding="50px",
        width="100%",
        background=Color.background.value,
        min_height="100vh"
    )
