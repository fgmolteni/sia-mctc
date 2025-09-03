import reflex as rx
from sia.components.forms.inputs import form_input
from sia.components.forms.buttons import form_button
from sia.components.forms.selects import form_select
from components.db_vehicles import add_vehicle, get_all_vehicles

class VehicleState(rx.State):
    """Estado para manejar el formulario de añadir vehículo."""
    # Campos del formulario
    marca: str = ""
    modelo: str = ""
    patente: str = ""
    consumo: str = "" # Se maneja como string para el input, se convierte a float al guardar
    combustible: str = "Nafta"
    condicion: str = "Oficial"
    activo: bool = True

    # Opciones para selectores
    combustible_options: list[str] = ["Nafta", "Diesel", "GNC", "Eléctrico"]
    condicion_options: list[str] = ["Oficial", "Afectado"]

    # Datos de la tabla de vehículos
    vehicles_data: list[list[str]] = []

    # Mensaje de feedback para el usuario
    feedback_message: str = ""
    feedback_success: bool = False

    async def on_load(self):
        """Carga los vehículos existentes al cargar la página."""
        self.vehicles_data = self.get_vehicles_list()

    def get_vehicles_list(self) -> list[list[str]]:
        df = get_all_vehicles()
        if not df.empty:
            # Convertir DataFrame a lista de listas para rx.data_table
            # Asegurarse de que el ID también se incluya si es necesario para la tabla
            return df.values.tolist()
        return []

    def handle_submit(self):
        """Gestiona el envío del formulario para crear un nuevo vehículo."""
        # Validar campos obligatorios
        if not self.marca.strip() or not self.modelo.strip() or not self.patente.strip():
            self.feedback_message = "Los campos Marca, Modelo y Patente son obligatorios."
            self.feedback_success = False
            return

        # Validar consumo si se proporciona
        consumo_float = None
        if self.consumo.strip():
            try:
                consumo_float = float(self.consumo)
            except ValueError:
                self.feedback_message = "El consumo debe ser un número válido."
                self.feedback_success = False
                return

        success = add_vehicle(
            marca=self.marca,
            modelo=self.modelo,
            patente=self.patente,
            consumo=consumo_float,
            combustible=self.combustible,
            condicion=self.condicion,
            activo=self.activo
        )

        if success:
            self.feedback_message = f"¡Vehículo {self.marca} {self.modelo} ({self.patente}) añadido con éxito!"
            self.feedback_success = True
            # Limpiar formulario
            self.marca = ""
            self.modelo = ""
            self.patente = ""
            self.consumo = ""
            self.combustible = "Nafta"
            self.condicion = "Oficial"
            self.activo = True
            # Recargar la lista de vehículos
            self.vehicles_data = self.get_vehicles_list()
        else:
            self.feedback_message = "Error al añadir el vehículo. Verifique que la Patente no esté duplicada."
            self.feedback_success = False

def vehicle_form() -> rx.Component:
    """Renderiza el formulario para añadir un nuevo vehículo."""
    return rx.box(
        rx.form.root(
            rx.vstack(
                form_input("Marca", "", "text", "marca", on_change=VehicleState.set_marca, value=VehicleState.marca),
                form_input("Modelo", "", "text", "modelo", on_change=VehicleState.set_modelo, value=VehicleState.modelo),
                form_input("Patente", "", "text", "patente", on_change=VehicleState.set_patente, value=VehicleState.patente),
                form_input("Consumo (L/100km)", "", "text", "consumo", on_change=VehicleState.set_consumo, value=VehicleState.consumo),
                form_select(
                    "Combustible",
                    "combustible",
                    VehicleState.combustible_options,
                    on_change=VehicleState.set_combustible,
                    value=VehicleState.combustible
                ),
                form_select(
                    "Condición",
                    "condicion",
                    VehicleState.condicion_options,
                    on_change=VehicleState.set_condicion,
                    value=VehicleState.condicion
                ),
                rx.checkbox("Activo", is_checked=VehicleState.activo, on_change=VehicleState.set_activo),
                form_button("Añadir Vehículo", on_click=VehicleState.handle_submit),
                spacing="4",
            ),
        ),
        # Mensaje de feedback
        rx.cond(
            VehicleState.feedback_message != "",
            rx.text(
                VehicleState.feedback_message,
                color=rx.cond(VehicleState.feedback_success, "green", "red"),
                margin_top="1em"
            )
        ),
        width="100%",
        padding="20px",
        border="1px solid #444",
        border_radius="10px",
    )

def vehicle_view() -> rx.Component:
    """La vista principal para la gestión de vehículos."""
    return rx.vstack(
        rx.heading("Gestión de Vehículos", color="white", size="8"),
        rx.text("Añadir un nuevo vehículo al sistema.", color="gray", margin_bottom="1em"),
        vehicle_form(),
        rx.divider(),
        rx.heading("Vehículos Existentes", color="white", size="7"),
        rx.cond(
            VehicleState.vehicles_data.length() > 0,
            rx.data_table(
                data=VehicleState.vehicles_data,
                columns=["ID", "Marca", "Modelo", "Patente", "Consumo", "Combustible", "Condición", "Activo"],
                pagination=True,
                search=True,
                sort=True,
                width="100%",
            ),
            rx.text("No hay vehículos registrados.", color="gray")
        ),
        align_items="start",
        spacing="4",
        padding="20px",
        width="calc(100vw - 280px - 30px)",
        min_height="100vh",
        margin_left="280px",
        margin_right="30px",
        bg="#1a1a1a",
        overflow_y="auto",
        border_radius="10px"
    )
