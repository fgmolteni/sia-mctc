from components.db_common import get_db_engine
from sqlalchemy import text
from datetime import datetime

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
