import reflex as rx
from sia.views.layout_profiles import (
    # Componentes estáticos (originales)
    permission_views,
    header_profiles,
    
    # Componentes dinámicos (nuevos)
    dynamic_permission_views,
    DynamicProfileState,
    get_permissions_by_role
)

class ProfileDemoState(DynamicProfileState):
    """Estado extendido para la demostración con datos de diferentes roles."""
    
    current_demo_user: str = "admin"  # admin, supervisor, user
    
    def switch_to_admin(self):
        """Cambiar a perfil de administrador."""
        self.current_demo_user = "admin"
        self.user_name = "María González"
        self.user_email = "maria.gonzalez@empresa.com"
        self.user_role = "Administrador"
        self.user_area = "Dirección General"
        self.user_status = "Activo"
        self.last_login = "05/09/2024"
        self.user_dni = "87654321"
    
    def switch_to_supervisor(self):
        """Cambiar a perfil de supervisor."""
        self.current_demo_user = "supervisor"
        self.user_name = "Carlos Méndez"
        self.user_email = "carlos.mendez@empresa.com"
        self.user_role = "Supervisor"
        self.user_area = "Supervisión de Gastos"
        self.user_status = "Activo"
        self.last_login = "04/09/2024"
        self.user_dni = "12348765"
    
    def switch_to_user(self):
        """Cambiar a perfil de usuario básico."""
        self.current_demo_user = "user"
        self.user_name = "Ana Torres"
        self.user_email = "ana.torres@empresa.com"
        self.user_role = "Usuario"
        self.user_area = "Contabilidad"
        self.user_status = "Activo"
        self.last_login = "03/09/2024"
        self.user_dni = "56781234"


def profile_demo_page() -> rx.Component:
    """Página de demostración que muestra componentes estáticos y dinámicos."""
    return rx.vstack(
        # Header de la página
        header_profiles(),
        
        # Controles de demostración
        rx.box(
            rx.vstack(
                rx.heading("Demostración de Componentes Dinámicos", size="5"),
                rx.text(
                    "Esta página muestra la diferencia entre componentes estáticos y dinámicos. "
                    "Usa los botones para cambiar entre diferentes roles y ver cómo cambian los permisos.",
                    color="gray",
                    size="3"
                ),
                rx.hstack(
                    rx.button(
                        "Ver como Administrador",
                        on_click=ProfileDemoState.switch_to_admin,
                        color_scheme=rx.cond(
                            ProfileDemoState.current_demo_user == "admin",
                            "red", "gray"
                        ),
                        variant=rx.cond(
                            ProfileDemoState.current_demo_user == "admin",
                            "solid", "soft"
                        )
                    ),
                    rx.button(
                        "Ver como Supervisor", 
                        on_click=ProfileDemoState.switch_to_supervisor,
                        color_scheme=rx.cond(
                            ProfileDemoState.current_demo_user == "supervisor",
                            "orange", "gray"
                        ),
                        variant=rx.cond(
                            ProfileDemoState.current_demo_user == "supervisor",
                            "solid", "soft"
                        )
                    ),
                    rx.button(
                        "Ver como Usuario",
                        on_click=ProfileDemoState.switch_to_user,
                        color_scheme=rx.cond(
                            ProfileDemoState.current_demo_user == "user",
                            "blue", "gray"
                        ),
                        variant=rx.cond(
                            ProfileDemoState.current_demo_user == "user",
                            "solid", "soft"
                        )
                    ),
                    spacing="3",
                    justify="center"
                ),
                spacing="4",
                align="center",
                padding="2rem",
            ),
            background="white",
            border="1px solid #e5e7eb",
            border_radius="0.5rem",
            margin_bottom="2rem"
        ),
        
        # Contenido principal con componentes dinámicos
        dynamic_permission_views(ProfileDemoState),
        
        # Separador
        rx.divider(margin="2rem 0"),
        
        # Información de referencia de permisos
        rx.box(
            rx.vstack(
                rx.heading("Referencia de Permisos por Rol", size="4"),
                rx.text("Esta tabla muestra cómo se asignan los permisos según el rol:", color="gray"),
                
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Funcionalidad"),
                            rx.table.column_header_cell("Administrador"),
                            rx.table.column_header_cell("Supervisor"), 
                            rx.table.column_header_cell("Usuario"),
                        ),
                    ),
                    rx.table.body(
                        rx.table.row(
                            rx.table.cell("Dashboard"),
                            rx.table.cell(rx.badge("Editar", color_scheme="green", size="1")),
                            rx.table.cell(rx.badge("Ver", color_scheme="blue", size="1")),
                            rx.table.cell(rx.badge("Ver", color_scheme="blue", size="1")),
                        ),
                        rx.table.row(
                            rx.table.cell("Gestión de Usuarios"),
                            rx.table.cell(rx.badge("Editar", color_scheme="green", size="1")),
                            rx.table.cell(rx.badge("Ver", color_scheme="blue", size="1")),
                            rx.table.cell(rx.badge("Sin Acceso", color_scheme="red", size="1")),
                        ),
                        rx.table.row(
                            rx.table.cell("Reportes"),
                            rx.table.cell(rx.badge("Editar", color_scheme="green", size="1")),
                            rx.table.cell(rx.badge("Ver", color_scheme="blue", size="1")),
                            rx.table.cell(rx.badge("Sin Acceso", color_scheme="red", size="1")),
                        ),
                        rx.table.row(
                            rx.table.cell("Gestión de Gastos"),
                            rx.table.cell(rx.badge("Editar", color_scheme="green", size="1")),
                            rx.table.cell(rx.badge("Editar", color_scheme="green", size="1")),
                            rx.table.cell(rx.badge("Ver", color_scheme="blue", size="1")),
                        ),
                    ),
                    variant="surface",
                    width="100%"
                ),
                spacing="3",
                padding="2rem",
            ),
            background="white",
            border="1px solid #e5e7eb", 
            border_radius="0.5rem",
            margin="2rem 0"
        ),
        
        width="100%",
        spacing="0",
        on_load=ProfileDemoState.switch_to_admin  # Cargar admin por defecto
    )