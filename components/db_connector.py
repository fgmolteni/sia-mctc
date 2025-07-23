import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_db_engine():
    """
    Establece y devuelve un motor de conexión SQLAlchemy a la base de datos PostgreSQL.
    Utiliza la URL de conexión definida en el archivo .env.
    Returns:
        sqlalchemy.engine.base.Engine: Objeto de motor de conexión a la base de datos.
                                     Retorna None si la conexión falla.
    """
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("Error: La variable de entorno DATABASE_URL no está definida.")
            return None
        
        engine = create_engine(db_url)
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
        query = "SELECT id, nombre, apellido, cargo, dni, categoria FROM public.agentes ORDER BY apellido, nombre;"
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as error:
        print("Error al consultar todos los agentes:", error)
        return pd.DataFrame()
    finally:
        if engine:
            engine.dispose()

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

from sqlalchemy import text

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

from sqlalchemy import text
from datetime import datetime

def get_fuel_price(fuel_type: str) -> float | None:
    """
    Obtiene el precio por litro de un tipo de combustible.
    Returns:
        float: El precio por litro, o None si no se encuentra.
    """
    engine = get_db_engine()
    if engine is None:
        return None

    try:
        with engine.connect() as connection:
            query = text("SELECT precio_por_litro FROM precios_combustibles WHERE tipo_combustible = :fuel_type;")
            result = connection.execute(query, {"fuel_type": fuel_type}).scalar_one_or_none()
            return float(result) if result is not None else None
    except Exception as error:
        print(f"Error al obtener precio de combustible para {fuel_type}: {error}")
        return None
    finally:
        if engine:
            engine.dispose()

def add_expediente(
    numero_expediente: str,
    vehiculo_id: int,
    origen: str,
    fecha_salida: datetime,
    fecha_regreso: datetime,
    objetivo_viaje: str,
    distancia_total_km: float,
    combustible_estimado_lts: float,
    monto_combustible_calculado: float,
    monto_viaticos_calculado: float,
    monto_total_expediente: float,
    estado: str,
    creado_por_usuario_id: int
) -> int | None:
    """
    Añade un nuevo expediente a la tabla 'expedientes'.
    Returns:
        int: El ID del expediente insertado, o None en caso de error.
    """
    engine = get_db_engine()
    if engine is None:
        return None

    try:
        with engine.connect() as connection:
            with connection.begin():
                query = text("""
                    INSERT INTO expedientes (
                        numero_expediente, vehiculo_id, origen, fecha_salida, fecha_regreso,
                        objetivo_viaje, distancia_total_km, combustible_estimado_lts,
                        monto_combustible_calculado, monto_viaticos_calculado, monto_total_expediente,
                        estado, creado_por_usuario_id
                    )
                    VALUES (
                        :numero_expediente, :vehiculo_id, :origen, :fecha_salida, :fecha_regreso,
                        :objetivo_viaje, :distancia_total_km, :combustible_estimado_lts,
                        :monto_combustible_calculado, :monto_viaticos_calculado, :monto_total_expediente,
                        :estado, :creado_por_usuario_id
                    ) RETURNING id;
                """)
                result = connection.execute(query, {
                    "numero_expediente": numero_expediente,
                    "vehiculo_id": vehiculo_id,
                    "origen": origen,
                    "fecha_salida": fecha_salida,
                    "fecha_regreso": fecha_regreso,
                    "objetivo_viaje": objetivo_viaje,
                    "distancia_total_km": distancia_total_km,
                    "combustible_estimado_lts": combustible_estimado_lts,
                    "monto_combustible_calculado": monto_combustible_calculado,
                    "monto_viaticos_calculado": monto_viaticos_calculado,
                    "monto_total_expediente": monto_total_expediente,
                    "estado": estado,
                    "creado_por_usuario_id": creado_por_usuario_id
                }).scalar_one()
            print(f"Expediente {numero_expediente} añadido exitosamente con ID: {result}")
            return result
    except Exception as error:
        print(f"Error al añadir expediente: {error}")
        return None
    finally:
        if engine:
            engine.dispose()

def add_expediente_agent(expediente_id: int, agente_id: int, dias_viatico_calculados: float, monto_viatico_calculado: float) -> bool:
    """
    Añade un agente a un expediente en la tabla 'expediente_agentes'.
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
                    INSERT INTO expediente_agentes (expediente_id, agente_id, dias_viatico_calculados, monto_viatico_calculado)
                    VALUES (:expediente_id, :agente_id, :dias_viatico_calculados, :monto_viatico_calculado);
                """)
                connection.execute(query, {
                    "expediente_id": expediente_id,
                    "agente_id": agente_id,
                    "dias_viatico_calculados": dias_viatico_calculados,
                    "monto_viatico_calculado": monto_viatico_calculado
                })
            print(f"Agente {agente_id} añadido al expediente {expediente_id} exitosamente.")
            return True
    except Exception as error:
        print(f"Error al añadir agente al expediente: {error}")
        return False
    finally:
        if engine:
            engine.dispose()

def add_expediente_destination(expediente_id: int, destino: str, orden: int) -> bool:
    """
    Añade un destino a un expediente en la tabla 'expediente_destinos'.
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
                    INSERT INTO expediente_destinos (expediente_id, destino, orden)
                    VALUES (:expediente_id, :destino, :orden);
                """)
                connection.execute(query, {
                    "expediente_id": expediente_id,
                    "destino": destino,
                    "orden": orden
                })
            print(f"Destino {destino} añadido al expediente {expediente_id} exitosamente.")
            return True
    except Exception as error:
        print(f"Error al añadir destino al expediente: {error}")
        return False
    finally:
        if engine:
            engine.dispose()

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

if __name__ == '__main__':
    # Pequeña prueba para verificar la conexión y la consulta
    engine = get_db_engine()
    if engine:
        print("¡Conexión a la base de datos exitosa!")
        
        print("\nProbando la función get_agentes():")
        agentes_df = get_agentes()
        if not agentes_df.empty:
            print("Se obtuvieron los siguientes datos de la tabla 'agentes':")
            print(agentes_df)
        else:
            print("No se pudieron obtener datos de la tabla 'agentes' o la tabla está vacía.")

        print("\nProbando la función get_vehiculos():")
        vehiculos_df = get_vehiculos()
        if not vehiculos_df.empty:
            print("Se obtuvieron los siguientes datos de la tabla 'vehiculos':")
            print(vehiculos_df)
        else:
            print("No se pudieron obtener datos de la tabla 'vehiculos' o la tabla está vacía.")
        
        engine.dispose()
    else:
        print("Fallo en la conexión a la base de datos.")