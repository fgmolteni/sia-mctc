from ast import Name
from altair.vegalite.v5 import data
import streamlit as st
from datetime import datetime as dt, date, time
import pandas as pd
from components.distance_calculator import get_driving_distance_and_time as cddt
from components.date_calculator import calculate_travel_expenses as cte
from components.pdf_generator import create_pdf
from components.formulario_generator import generar_anticipo_viatico as anticipo_viaticos
from components.converter import number_to_text, number_to_currency
from components.db_connector import get_agentes, get_db_engine

# Initialize session state
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False

# titulo
st.title("Sistema Interno de Administración")

# Load data and set index for easy lookup
engine = get_db_engine()
if engine:
    df_class_amount = pd.read_sql_query("SELECT class, amounts FROM public.montos_viaticos;", engine).set_index('class')
    engine.dispose()
else:
    st.error("No se pudo conectar a la base de datos para cargar los montos de viáticos.")
    df_class_amount = pd.DataFrame() # Asegura que df_class_amount sea un DataFrame vacío en caso de error

# numero de expediente
number_file = st.text_input("Numero de Expediente")

# seleccion de agente
option_agent = get_agentes()

if not option_agent.empty:
    option_agent_last_name = option_agent["apellido"]

    # Nombre de Agente
    last_name_agent = st.selectbox(
        "Seleccione el agente.",
        option_agent_last_name
    )
    data_agent = option_agent[option_agent["apellido"] == last_name_agent]
else:
    st.warning("No se encontraron agentes en la base de datos.")
    option_agent_last_name = []
    last_name_agent = None
    data_agent = pd.DataFrame()

#muesta informacion de agente
st.table(data_agent)

# seleccion de fechas
col1, col2, col3 = st.columns(3)
with col1:
    travel_origen = st.text_input("Ingrese la ubicacion de partida")
    travel_detiny = st.text_input("Ingrese la ubicacion de destino")
with col2:
    date_start = st.date_input("Ingresa fecha de inicio", date.today(), key="date_start")
    date_end = st.date_input("Ingresa fecha de fin", date.today(), key="date_end")
with col3:
    time_start = st.time_input("Ingresa hora de inicio", time(8, 0), key="time_start")
    time_end = st.time_input("Ingresa hora de fin", time(12, 0), key="time_end")

# seleccion de vehiculo
option_cars = pd.read_csv(r"data/cars.csv")
# Crear un nombre de visualización para la selección
option_cars['display_name'] = option_cars['brand'] + ' ' + option_cars['model']
# Nombre de Agente
name_cars = st.selectbox(
    "Seleccione el vehiculo.",
    option_cars['display_name']
)
st.table(option_cars[option_cars['display_name'] == name_cars])

# botom confirmar
if st.button("Confirmar", icon="🆗", use_container_width=True, type="primary"):
    # Calculo de distancia y tiempo de viaje
    if travel_origen and travel_detiny and not data_agent.empty:
        data_travel = cddt(travel_origen, travel_detiny)
        if data_travel:
            distance, duration = data_travel
            days_travel_expenses = cte(date_start, date_end, time_start, time_end, distance)

            # Get agent class and calculate expenses
            agent_class = data_agent['clase'].values[0]
            amount_per_day = df_class_amount.loc[agent_class, 'amounts']
            total_expenses = days_travel_expenses * amount_per_day

            # Extraer el nombre y apellido de forma segura
            agent_first_name = data_agent['nombre'].values[0]
            agent_last_name = data_agent['apellido'].values[0]
            full_name = f"{agent_last_name}, {agent_first_name}"

            # Guardar los resultados en el estado de la sesión
            st.session_state.calculation_done = True
            st.session_state.report_data = {
                "number_file": number_file,
                "name_agent": full_name,
                "travel_origen": travel_origen,
                "travel_detiny": travel_detiny,
                "date_start": date_start,
                "time_start": time_start,
                "date_end": date_end,
                "time_end": time_end,
                "distance": distance,
                "duration": duration,
                "days_travel_expenses": days_travel_expenses,
                "agent_first_name": agent_first_name,
                "agent_last_name": agent_last_name,
                "total_expenses": total_expenses
            }

            st.write(f"Distancia y duración: {(distance / 2):.2f} km, {duration:.2f} horas")
            st.write(f"Fecha de inicio: {date_start}, Hora: {time_start}")
            st.write(f"Fecha de fin: {date_end}, Hora: {time_end}")
            st.write(f"Días calculados para viáticos: {days_travel_expenses}")
            st.write(f"Monto por día: {number_to_currency(amount_per_day)}")
            st.write(f"Total de viáticos: {number_to_currency(total_expenses)}")
            st.success("Cálculo realizado con éxito.")
        else:
            st.error("No se pudo calcular la distancia. Verifique las direcciones ingresadas.")
            st.session_state.calculation_done = False
    else:
        st.warning("Por favor, ingrese origen, destino y seleccione un agente.")
        st.session_state.calculation_done = False

# Botón para generar el PDF (aparece después de un cálculo exitoso)
if st.session_state.calculation_done:
    if st.button("Generar Reporte en PDF"):
        report_data = st.session_state.report_data
        
        # Contenido para el PDF
        report_content = [
            f"Reporte de Viáticos - Expediente: {report_data['number_file']}",
            "--------------------------------------------------",
            f"Agente: {report_data['name_agent']}",
            f"Origen: {report_data['travel_origen']}",
            f"Destino: {report_data['travel_detiny']}",
            f"Fecha de Salida: {report_data['date_start']} a las {report_data['time_start']}",
            f"Fecha de Regreso: {report_data['date_end']} a las {report_data['time_end']}",
            f"Distancia Total (ida y vuelta): {report_data['distance']:.2f} km",
            f"Días para viáticos: {report_data['days_travel_expenses']}",
            f"Total de viáticos: {number_to_currency(report_data['total_expenses'])}",
        ]
        
        pdf_file_path = r"report/" + f"reporte_{report_data['number_file']}.pdf"

        if create_pdf(pdf_file_path, report_content):
            st.success(f"Reporte generado: {pdf_file_path}")
            with open(pdf_file_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF",
                    data=f,
                    file_name=pdf_file_path,
                    mime="application/pdf"
                )
        else:
            st.error("No se pudo generar el reporte en PDF.")
    
# Botón para generar Anticipo (aparece después de un cálculo exitoso)
if st.session_state.calculation_done:
    if st.button("Generar Anticipo en PDF"):
        report_data = st.session_state.report_data
        
        # Use the calculated expense amount
        monto_anticipo_float = report_data['total_expenses']

        # Contenido para el PDF
        report_content = {
            "director": "",
            "fecha_anticipo": "01/07/2025",
            "unidad_organizacion": "DIRECCIÓN GENERAL DE ADMINISTRACIÓN",
            "unidad_operativa": "DEPARTAMENTO DE TESORERÍA",
            "apellido": report_data['agent_last_name'],
            "nombre": report_data['agent_first_name'],
            "nombre_completo": report_data['name_agent'],
            "cargo": "MINISTRO",
            "sueldo_basico": "",
            "fecha_iniciacion": report_data['date_start'],
            "destino": "ITUZAINGO - VIRASORO - SANTO TOME",
            "medio_transporte": "Vehículo Oficial AH096KX",
            "objetivo": "COMISIONES OFICIALES",
            "anticipo_monto": number_to_currency(monto_anticipo_float),
            "total_monto": number_to_currency(monto_anticipo_float),
            "rendicion_gasto": number_to_currency(monto_anticipo_float),
            "fecha_autorizacion": "02/07/2025",
            "monto_en_letras": number_to_text(monto_anticipo_float),
            "mi_nro": "12.345.678"
        }
        
        pdf_file_path = r"report/" + f"anticipo_{report_data['number_file']}.pdf"

        if anticipo_viaticos(pdf_file_path, report_content):
            st.success(f"Reporte generado: {pdf_file_path}")
            with open(pdf_file_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF",
                    data=f,
                    file_name=pdf_file_path,
                    mime="application/pdf"
                )
        else:
            st.error("No se pudo generar el reporte en PDF.")
