import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

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
