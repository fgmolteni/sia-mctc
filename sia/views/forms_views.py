import reflex as rx
from sia.components.form_components import form_input, form_button, form_reset_button, form_date_input, form_time_input, form_select
from datetime import datetime as dt, date, time
import pandas as pd
import asyncio
from components.distance_calculator import get_driving_distance_and_time as cddt
from components.date_calculator import calculate_travel_expenses as cte
from components.converter import number_to_text, number_to_currency
from components.pdf_generator import create_pdf
from components.formulario_generator import generar_anticipo_viatico as anticipo_viaticos
from components.db_connector import get_agentes, get_vehiculos, get_fuel_price, add_expediente, add_expediente_agent, add_expediente_destination


class FormState(rx.State):
    form_data: dict = {}

    # Variables de estado para todos los campos del formulario:
    number_file: str = ""
    selected_agent_last_name: str = ""
    travel_origin: str = ""
    travel_destination: str = ""
    date_start: str = str(dt.now().date())
    date_end: str = str(dt.now().date())
    time_start: str = str(dt.now().time())
    time_end: str = str(dt.now().time())
    selected_car_display_name: str = ""

    # Variables de estado para datos externos:
    agents_df: pd.DataFrame = pd.DataFrame()
    cars_df: pd.DataFrame = pd.DataFrame()
    agent_last_names: list[str] = []
    car_display_names: list[str] = []

    # Variables de estado para resultados y control de UI:
    calculation_done: bool = False
    report_data: dict = {}
    distance: float = 0.0
    duration: float = 0.0
    days_travel_expenses: float = 0.0
    amount_per_day: float = 0.0
    total_expenses: float = 0.0
    error_message: str = ""

    async def on_load(self):
        """Load agents and car data on page load."""
        # Load agents
        try:
            agents = get_agentes()
            if not agents.empty:
                self.agents_df = agents
                self.agent_last_names = agents["apellido"].tolist()
            else:
                self.error_message = "No se encontraron agentes en la base de datos."
        except Exception as e:
            self.error_message = f"Error al cargar agentes: {e}"

        # Load cars
        try:
            cars = get_vehiculos()
            cars['display_name'] = cars['marca'] + ' ' + cars['modelo']
            self.cars_df = cars
            self.car_display_names = cars['display_name'].tolist()
        except Exception as e:
            self.error_message = f"Error al cargar vehículos: {e}"

    @rx.var
    def get_selected_agent_data(self) -> pd.DataFrame:
        if not self.agents_df.empty and self.selected_agent_last_name:
            return self.agents_df[self.agents_df["apellido"] == self.selected_agent_last_name]
        return pd.DataFrame()

    @rx.var
    def get_selected_car_data(self) -> pd.DataFrame:
        if not self.cars_df.empty and self.selected_car_display_name:
            return self.cars_df[self.cars_df["display_name"] == self.selected_car_display_name]
        return pd.DataFrame()

    @rx.var
    def formatted_amount_per_day(self) -> str:
        return number_to_currency(self.amount_per_day)

    @rx.var
    def formatted_total_expenses(self) -> str:
        return number_to_currency(self.total_expenses)

    @rx.event
    async def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        self.error_message = "" # Clear previous errors

        # Extract data from form_data
        number_file = form_data.get("number_file", "")
        travel_origin = form_data.get("travel_origin", "")
        travel_destination = form_data.get("travel_destination", "")
        
        # Convert date and time strings to appropriate objects
        try:
            date_start_obj = dt.strptime(form_data.get("date_start"), "%Y-%m-%d").date()
            date_end_obj = dt.strptime(form_data.get("date_end"), "%Y-%m-%d").date()
            time_start_obj = dt.strptime(form_data.get("time_start"), "%H:%M").time()
            time_end_obj = dt.strptime(form_data.get("time_end"), "%H:%M").time()

            # Combine date and time for TIMESTAMP fields
            datetime_start_obj = datetime.combine(date_start_obj, time_start_obj)
            datetime_end_obj = datetime.combine(date_end_obj, time_end_obj)

        except (ValueError, TypeError) as e:
            self.error_message = f"Error en el formato de fecha/hora: {e}"
            self.calculation_done = False
            return

        # Get selected agent data
        selected_agent_data = self.get_selected_agent_data
        selected_car_data = self.get_selected_car_data
        
        if travel_origin and travel_destination and not selected_agent_data.empty and not selected_car_data.empty:
            data_travel = cddt(travel_origin, travel_destination)
            if data_travel:
                distance, duration = data_travel
                
                # Ensure distance is a number before passing to cte
                try:
                    distance_num = float(distance)
                except ValueError:
                    self.error_message = "La distancia no es un número válido."
                    self.calculation_done = False
                    return

                days_travel_expenses = cte(date_start_obj, date_end_obj, time_start_obj, time_end_obj, distance_num)

                # Get agent class and calculate expenses
                # agent_class = selected_agent_data['clase'].values[0] # 'clase' no existe en la nueva tabla agentes
                # Usaremos una cantidad fija por ahora, o podríamos buscarla por categoría si tuviéramos una tabla de montos
                amount_per_day = 100.0 # Placeholder for now

                self.total_expenses = days_travel_expenses * amount_per_day

                # Extract agent name safely
                agent_first_name = selected_agent_data['nombre'].values[0]
                agent_last_name = selected_agent_data['apellido'].values[0]
                full_name = f"{agent_last_name}, {agent_first_name}"

                # --- Cálculos para guardar en DB ---
                vehiculo_id = selected_car_data['id'].values[0]
                agente_id = selected_agent_data['id'].values[0]
                
                # Combustible
                fuel_type = selected_car_data['combustible'].values[0]
                fuel_consumption_l_per_100km = selected_car_data['consumo'].values[0]
                
                monto_combustible_calculado = 0.0
                combustible_estimado_lts = 0.0

                if pd.notna(fuel_consumption_l_per_100km) and fuel_consumption_l_per_100km > 0:
                    fuel_price = get_fuel_price(fuel_type)
                    if fuel_price is not None:
                        combustible_estimado_lts = (distance_num / 100) * fuel_consumption_l_per_100km
                        monto_combustible_calculado = combustible_estimado_lts * fuel_price
                    else:
                        self.error_message = f"Advertencia: No se encontró precio para el combustible {fuel_type}. El costo de combustible no se calculará."
                
                monto_viaticos_calculado = self.total_expenses
                monto_total_expediente = monto_viaticos_calculado + monto_combustible_calculado

                # --- Guardar en la Base de Datos ---
                # Usaremos un user_id de prueba por ahora
                creado_por_usuario_id = 1 # Asumimos un usuario con ID 1
                objetivo_viaje = "Comisión de servicio" # Placeholder, se podría añadir un campo al formulario
                estado_expediente = "Calculado" # Estado inicial

                expediente_id = add_expediente(
                    numero_expediente=number_file,
                    vehiculo_id=vehiculo_id,
                    origen=travel_origin,
                    fecha_salida=datetime_start_obj,
                    fecha_regreso=datetime_end_obj,
                    objetivo_viaje=objetivo_viaje,
                    distancia_total_km=distance_num,
                    combustible_estimado_lts=combustible_estimado_lts,
                    monto_combustible_calculado=monto_combustible_calculado,
                    monto_viaticos_calculado=monto_viaticos_calculado,
                    monto_total_expediente=monto_total_expediente,
                    estado=estado_expediente,
                    creado_por_usuario_id=creado_por_usuario_id
                )

                if expediente_id:
                    # Guardar agente del expediente
                    add_expediente_agent(
                        expediente_id=expediente_id,
                        agente_id=agente_id,
                        dias_viatico_calculados=days_travel_expenses,
                        monto_viatico_calculado=monto_viaticos_calculado # Monto de viático para este agente
                    )

                    # Guardar destinos del expediente (origen y destino como destinos)
                    add_expediente_destination(expediente_id=expediente_id, destino=travel_origin, orden=1)
                    add_expediente_destination(expediente_id=expediente_id, destino=travel_destination, orden=2)

                    self.error_message = "Cálculo y guardado en DB realizado con éxito."
                    self.calculation_done = True
                    self.report_data = {
                        "number_file": number_file,
                        "name_agent": full_name,
                        "travel_origin": travel_origin,
                        "travel_destination": travel_destination,
                        "date_start": date_start_obj,
                        "time_start": time_start_obj,
                        "date_end": date_end_obj,
                        "time_end": time_end_obj,
                        "distance": distance,
                        "duration": duration,
                        "days_travel_expenses": days_travel_expenses,
                        "agent_first_name": agent_first_name,
                        "agent_last_name": agent_last_name,
                        "total_expenses": self.total_expenses
                    }
                    self.distance = distance
                    self.duration = duration
                    self.days_travel_expenses = days_travel_expenses
                    self.amount_per_day = amount_per_day
                    self.total_expenses = monto_total_expediente # Actualizar para mostrar el total real

                else:
                    self.error_message = "Error al guardar el expediente en la base de datos."
                    self.calculation_done = False

            else:
                self.error_message = "No se pudo calcular la distancia. Verifique las direcciones ingresadas."
                self.calculation_done = False
        else:
            self.error_message = "Por favor, ingrese origen, destino, seleccione un agente y un vehículo."
            self.calculation_done = False

    @rx.var
    def form_data_str(self) -> str:
        return str(self.form_data)

    async def generate_report_pdf(self):
        if not self.calculation_done:
            self.error_message = "Realice el cálculo primero para generar el reporte."
            return

        report_data = self.report_data
        report_content = [
            f"Reporte de Viáticos - Expediente: {report_data['number_file']}",
            "--------------------------------------------------",
            f"Agente: {report_data['name_agent']}",
            f"Origen: {report_data['travel_origin']}",
            f"Destino: {report_data['travel_destination']}",
            f"Fecha de Salida: {report_data['date_start']} a las {report_data['time_start']}",
            f"Fecha de Regreso: {report_data['date_end']} a las {report_data['time_end']}",
            f"Distancia Total (ida y vuelta): {report_data['distance']:.2f} km",
            f"Días para viáticos: {report_data['days_travel_expenses']}",
            f"Total de viáticos: {number_to_currency(report_data['total_expenses'])}",
        ]

        pdf_file_path = f"assets/report/reporte_{report_data['number_file']}.pdf"

        if create_pdf(pdf_file_path, report_content):
            self.error_message = f"Reporte generado: {pdf_file_path}"
            with open(pdf_file_path, "rb") as f:
                return rx.download(data=f.read(), filename=f"reporte_{report_data['number_file']}.pdf")
        else:
            self.error_message = "No se pudo generar el reporte en PDF."

    async def generate_anticipo_pdf(self):
        if not self.calculation_done:
            self.error_message = "Realice el cálculo primero para generar el anticipo."
            return

        report_data = self.report_data
        monto_anticipo_float = report_data['total_expenses']

        report_content = {
            "director": "",
            "fecha_anticipo": "01/07/2025", # Hardcoded for now
            "unidad_organizacion": "DIRECCIÓN GENERAL DE ADMINISTRACIÓN",
            "unidad_operativa": "DEPARTAMENTO DE TESORERÍA",
            "apellido": report_data['agent_last_name'],
            "nombre": report_data['agent_first_name'],
            "nombre_completo": report_data['name_agent'],
            "cargo": "MINISTRO",
            "sueldo_basico": "",
            "fecha_iniciacion": report_data['date_start'],
            "destino": "ITUZAINGO - VIRASORO - SANTO TOME", # Hardcoded for now
            "medio_transporte": "Vehículo Oficial AH096KX", # Hardcoded for now
            "objetivo": "COMISIONES OFICIALES", # Hardcoded for now
            "anticipo_monto": number_to_currency(monto_anticipo_float),
            "total_monto": number_to_currency(monto_anticipo_float),
            "rendicion_gasto": number_to_currency(monto_anticipo_float),
            "fecha_autorizacion": "02/07/2025", # Hardcoded for now
            "monto_en_letras": number_to_text(monto_anticipo_float),
            "mi_nro": "12.345.678" # Hardcoded for now
        }

        pdf_file_path = f"assets/report/anticipo_{report_data['number_file']}.pdf"

        if anticipo_viaticos(pdf_file_path, report_content):
            self.error_message = f"Anticipo generado: {pdf_file_path}"
            with open(pdf_file_path, "rb") as f:
                return rx.download(data=f.read(), filename=f"anticipo_{report_data['number_file']}.pdf")
        else:
            self.error_message = "No se pudo generar el anticipo en PDF."


def forms_views() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                # Numero de Expediente
                form_input("Numero de Expediente", "Ingrese el número de expediente", "text", "number_file"),

                # Seleccion de agente
                form_select(
                    "Seleccione el agente.",
                    "selected_agent_last_name",
                    FormState.agent_last_names,
                    on_change=FormState.set_selected_agent_last_name,
                    value=FormState.selected_agent_last_name
                ),
                # Muestra informacion de agente
                rx.cond(
                    ~FormState.get_selected_agent_data.empty,
                    rx.data_table(
                        data=FormState.get_selected_agent_data,
                        pagination=False,
                        search=False,
                        # Add styling as needed
                    )
                ),

                # Ubicacion de partida y destino
                rx.hstack(
                    form_input("Ingrese la ubicacion de partida", "Origen", "text", "travel_origin"),
                    form_input("Ingrese la ubicacion de destino", "Destino", "text", "travel_destination"),
                ),

                # Seleccion de fechas y horas
                rx.hstack(
                    rx.vstack(
                        form_date_input("Ingresa fecha de inicio", "date_start", default_value=FormState.date_start),
                        form_date_input("Ingresa fecha de fin", "date_end", default_value=FormState.date_end),
                    ),
                    rx.vstack(
                        form_time_input("Ingresa hora de inicio", "time_start", default_value=FormState.time_start),
                        form_time_input("Ingresa hora de fin", "time_end", default_value=FormState.time_end),
                    ),
                ),

                # Seleccion de vehiculo
                form_select(
                    "Seleccione el vehiculo.",
                    "selected_car_display_name",
                    FormState.car_display_names,
                    on_change=FormState.set_selected_car_display_name,
                    value=FormState.selected_car_display_name
                ),
                # Muestra informacion de vehiculo
                rx.cond(
                    ~FormState.get_selected_car_data.empty,
                    rx.data_table(
                        data=FormState.get_selected_car_data,
                        pagination=False,
                        search=False,
                        # Add styling as needed
                    )
                ),

                # Botones
                rx.hstack(
                    form_button("Confirmar"),
                    form_reset_button("Limpiar"),
                    spacing="4",
                ),
                spacing="4",
            ),
            on_submit=FormState.handle_submit,
        ),
        rx.divider(),
        rx.heading("results"),
        rx.text(FormState.form_data_str),
        rx.text(f"Agente Seleccionado: {FormState.selected_agent_last_name}"),
        rx.text(f"Vehículo Seleccionado: {FormState.selected_car_display_name}"),
        rx.cond(
            FormState.calculation_done,
            rx.vstack(
                rx.text(f"Distancia y duración: {(FormState.distance / 2):.2f} km, {FormState.duration:.2f} horas"),
                rx.text(f"Días calculados para viáticos: {FormState.days_travel_expenses}"),
                rx.text(f"Monto por día: {FormState.formatted_amount_per_day}"),
                rx.text(f"Total de viáticos: {FormState.formatted_total_expenses}"),
            )
        ),
        rx.cond(
            FormState.error_message != "",
            rx.text(FormState.error_message, color="red")
        ),
        rx.cond(
            FormState.calculation_done,
            rx.hstack(
                rx.button("Generar Reporte en PDF", on_click=FormState.generate_report_pdf),
                rx.button("Generar Anticipo en PDF", on_click=FormState.generate_anticipo_pdf),
                spacing="4",
            )
        ),
        rx.heading("Agentes Cargados:"),
        rx.text(str(FormState.agent_last_names)),
        rx.heading("Vehículos Cargados:"),
        rx.text(str(FormState.car_display_names))

    )
