from components.db_common import get_db_engine
import pandas as pd
from sqlalchemy import text

def get_agentes():
    """
    Consulta y devuelve todos los registros de la tabla 'agentes' como un DataFrame.
    Returns:
        pandas.DataFrame: Un DataFrame con los datos de los agentes.
                          Retorna un DataFrame vacío si ocurre un error.
    """
    engine = get_db_engine()
    if engine is None:
        return pd.DataFrame()

    try:
        query = "SELECT * FROM public.agentes;"
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as error:
        print("Error al consultar la tabla de agentes:", error)
        return pd.DataFrame()
    finally:
        if engine:
            engine.dispose()

def get_all_agents():
    """
    Consulta y devuelve todos los registros de la tabla 'agentes' como un DataFrame.
    Esta función es para uso general, por ejemplo, para mostrar en una tabla.
    Returns:
        pandas.DataFrame: Un DataFrame con los datos de los agentes.
                          Retorna un DataFrame vacío si ocurre un error.
    """
    engine = get_db_engine()
    if engine is None:
        return pd.DataFrame()

    try:
        query = text("SELECT id, nombre, apellido, cargo, dni, categoria FROM public.agentes ORDER BY apellido, nombre;")
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as error:
        print("Error al consultar todos los agentes:", error)
        return pd.DataFrame()
    finally:
        if engine:
            engine.dispose()

def add_agent(nombre: str, apellido: str, cargo: str, dni: str, categoria: str) -> bool:
    """
    Añade un nuevo agente a la tabla 'agentes'.
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    engine = get_db_engine()
    if engine is None:
        return False

    try:
        with engine.connect() as connection:
            # Usamos una transacción para asegurar la integridad de los datos
            with connection.begin() as transaction:
                query = text("""
                    INSERT INTO agentes (nombre, apellido, cargo, dni, categoria)
                    VALUES (:nombre, :apellido, :cargo, :dni, :categoria)
                """)
                connection.execute(query, {
                    "nombre": nombre,
                    "apellido": apellido,
                    "cargo": cargo,
                    "dni": dni,
                    "categoria": categoria
                })
            print(f"Agente {nombre} {apellido} añadido exitosamente.")
            return True
    except Exception as error:
        print(f"Error al añadir agente: {error}")
        return False
    finally:
        if engine:
            engine.dispose()
