import reflex as rx
from sia.components.forms.inputs import form_input
from sia.components.forms.buttons import form_button
from components.db_agents import add_agent, get_all_agents
from sia.views.sidebar import sidebar_main as sidebar

class AgentState(rx.State):
    """Estado para manejar el formulario de añadir agente."""
    # Campos del formulario
    nombre: str = ""
    apellido: str = ""
    cargo: str = ""
    dni: str = ""
    categoria: str = ""

    # Datos de la tabla de agentes
    agents_data: list[list[str]] = []

    # Mensaje de feedback para el usuario
    feedback_message: str = ""
    feedback_success: bool = False

    async def on_load(self):
        """Carga los agentes existentes al cargar la página."""
        self.agents_data = self.get_agents_list()

    def get_agents_list(self) -> list[list[str]]:
        df = get_all_agents()
        if not df.empty:
            # Convertir DataFrame a lista de listas para rx.data_table
            # Asegurarse de que el ID también se incluya si es necesario para la tabla
            return df.values.tolist()
        return []

    def handle_submit(self):
        """Gestiona el envío del formulario para crear un nuevo agente."""
        if not all([self.nombre, self.apellido, self.dni]):
            self.feedback_message = "Los campos Nombre, Apellido y DNI son obligatorios."
            self.feedback_success = False
            return

        success = add_agent(
            nombre=self.nombre,
            apellido=self.apellido,
            cargo=self.cargo,
            dni=self.dni,
            categoria=self.categoria
        )

        if success:
            self.feedback_message = f"¡Agente {self.nombre} {self.apellido} añadido con éxito!"
            self.feedback_success = True
            # Limpiar formulario
            self.nombre = ""
            self.apellido = ""
            self.cargo = ""
            self.dni = ""
            self.categoria = ""
            # Recargar la lista de agentes
            self.agents_data = self.get_agents_list()
        else:
            self.feedback_message = "Error al añadir el agente. Verifique que el DNI no esté duplicado."
            self.feedback_success = False


def agent_form() -> rx.Component:
    """Renderiza el formulario para añadir un nuevo agente."""
    return rx.box(
        rx.form.root(
            rx.vstack(
                rx.hstack(
                    form_input("Nombre", "", "text", "nombre",
                               on_change=AgentState.set_nombre, value=AgentState.nombre),
                    form_input("Apellido", "", "text", "apellido",
                               on_change=AgentState.set_apellido, value=AgentState.apellido),
                ),
                rx.hstack(
                    form_input("DNI", "", "text", "dni",
                               on_change=AgentState.set_dni, value=AgentState.dni),
                ),
                rx.divider(),
                rx.hstack(

                    form_input("Cargo", "", "text", "cargo",
                               on_change=AgentState.set_cargo, value=AgentState.cargo),
                    form_input("Categoría", "", "text", "categoria",
                               on_change=AgentState.set_categoria, value=AgentState.categoria),
                ),
                form_button("Añadir Agente",
                            on_click=lambda: AgentState.handle_submit()),
                spacing="4",
            ),
        ),
        # Mensaje de feedback
        rx.cond(
            AgentState.feedback_message != "",
            rx.text(
                AgentState.feedback_message,
                color=rx.cond(AgentState.feedback_success, "green", "red"),
                margin_top="1em"
            )
        ),
        #width="100%",
        padding="20px",
        border="1px solid #444",
        border_radius="10px",
    )

def agent_view() -> rx.Component:
    """La vista principal para la gestión de agentes."""
    return rx.hstack(
        sidebar(),
        rx.vstack(
            rx.heading("Gestión de Agentes", color="white", size="8"),
            rx.text("Añadir un nuevo agente al sistema.", color="gray", margin_bottom="1em"),
            agent_form(),
            rx.divider(),
            rx.heading("Agentes Existentes", color="white", size="7"),
            rx.cond(
                AgentState.agents_data.length() > 0,
                rx.data_table(
                    data=AgentState.agents_data,
                    columns=["ID", "Nombre", "Apellido", "Cargo", "DNI", "Categoría"],
                    pagination=True,
                    search=True,
                    sort=True,
                    width="100%",
                ),
                rx.text("No hay agentes registrados.", color="gray")
            ),
            align_items="start",
            spacing="4",
            padding="20px",
            padding_left="290px", # Added padding to account for sidebar
            flex_grow=1, # Adjusted width
            min_height="100vh",
            bg="white", # Corrected typo
            overflow_y="auto",
            border_radius="10px"
        ),
        spacing="7",
        width="100%",
        height="100vh",
        background=rx.color("gray", 2),
    )
