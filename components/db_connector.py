import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_db_engine():
    """
    Establece y devuelve un motor de conexión SQLAlchemy a la base de datos PostgreSQL.

    Utiliza las credenciales definidas en el archivo .env.

    Returns:
        sqlalchemy.engine.base.Engine: Objeto de motor de conexión a la base de datos.
                                     Retorna None si la conexión falla.
    """
    try:
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_name = os.getenv("POSTGRES_DB")
        db_host = "localhost"  # Conexión local a la base de datos Dockerizada
        db_port = "5432"

        # Cadena de conexión para SQLAlchemy
        db_connection_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_connection_str)
        return engine
    except Exception as e:
        print(f"Error al crear el motor de la base de datos: {e}")
        return None

def get_agentes():
    """
    Consulta y devuelve todos los registros de la tabla 'agentes' como un DataFrame.

    Returns:
        pandas.DataFrame: Un DataFrame con los datos de los agentes.
                          Retorna un DataFrame vacío si ocurre un error.
    """
    engine = get_db_engine()
    if engine is None:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay conexión

    try:
        query = "SELECT * FROM public.agentes;"
        # pd.read_sql_query puede usar directamente el motor de SQLAlchemy
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as error:
        print("Error al consultar la tabla de agentes:", error)
        return pd.DataFrame() # Devuelve un DataFrame vacío en caso de error
    finally:
        if engine:
            engine.dispose() # Cierra la conexión del motor

if __name__ == '__main__':
    # Pequeña prueba para verificar la conexión y la consulta
    engine = get_db_engine()
    if engine:
        print("¡Conexión a la base de datos exitosa!")
        engine.dispose()

        print("\nProbando la función get_agentes():")
        agentes_df = get_agentes()
        if not agentes_df.empty:
            print("Se obtuvieron los siguientes datos de la tabla 'agentes':")
            print(agentes_df)
        else:
            print("No se pudieron obtener datos de la tabla 'agentes' o la tabla está vacía.")

    else:
        print("Fallo en la conexión a la base de datos.")