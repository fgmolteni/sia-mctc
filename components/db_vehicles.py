from components.db_common import get_db_engine
import pandas as pd
from sqlalchemy import text

def get_vehiculos():
    """
    Consulta y devuelve todos los registros de la tabla 'vehiculos' como un DataFrame.
    Returns:
        pandas.DataFrame: Un DataFrame con los datos de los vehiculos.
                          Retorna un DataFrame vacío si ocurre un error.
    """
    engine = get_db_engine()
    if engine is None:
        return pd.DataFrame()

    try:
        query = "SELECT * FROM public.vehiculos;"
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as error:
        print("Error al consultar la tabla de vehiculos:", error)
        return pd.DataFrame()
    finally:
        if engine:
            engine.dispose()

def get_all_vehicles():
    """
    Consulta y devuelve todos los registros de la tabla 'vehiculos' como un DataFrame.
    Esta función es para uso general, por ejemplo, para mostrar en una tabla.
    Returns:
        pandas.DataFrame: Un DataFrame con los datos de los vehículos.
                          Retorna un DataFrame vacío si ocurre un error.
    """
    engine = get_db_engine()
    if engine is None:
        return pd.DataFrame()

    try:
        query = text("SELECT id, marca, modelo, patente, consumo, combustible, condicion, activo FROM public.vehiculos ORDER BY marca, modelo;")
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as error:
        print(f"Error al consultar todos los vehículos: {error}")
        return pd.DataFrame()
    finally:
        if engine:
            engine.dispose()

def add_vehicle(marca: str, modelo: str, patente: str, consumo: float | None, combustible: str, condicion: str, activo: bool) -> bool:
    """
    Añade un nuevo vehículo a la tabla 'vehiculos'.
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    engine = get_db_engine()
    if engine is None:
        return False

    try:
        with engine.connect() as connection:
            with connection.begin():
                query = text("""
                    INSERT INTO vehiculos (marca, modelo, patente, consumo, combustible, condicion, activo)
                    VALUES (:marca, :modelo, :patente, :consumo, :combustible, :condicion, :activo)
                """)
                connection.execute(query, {
                    "marca": marca,
                    "modelo": modelo,
                    "patente": patente,
                    "consumo": consumo,
                    "combustible": combustible,
                    "condicion": condicion,
                    "activo": activo
                })
            print(f"Vehículo {marca} {modelo} ({patente}) añadido exitosamente.")
            return True
    except Exception as error:
        print(f"Error al añadir vehículo: {error}")
        return False
    finally:
        if engine:
            engine.dispose()
