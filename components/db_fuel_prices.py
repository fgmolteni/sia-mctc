from components.db_common import get_db_engine
from sqlalchemy import text

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
