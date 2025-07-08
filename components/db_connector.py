import os
import psycopg2
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos PostgreSQL.

    Utiliza las credenciales definidas en el archivo .env.

    Returns:
        psycopg2.connection: Objeto de conexión a la base de datos.
                             Retorna None si la conexión falla.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",  # El servicio 'db' de Docker se expone en localhost
            port="5432"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

if __name__ == '__main__':
    # Pequeña prueba para verificar la conexión
    connection = get_db_connection()
    if connection:
        print("¡Conexión a la base de datos exitosa!")
        connection.close()
    else:
        print("Fallo en la conexión a la base de datos.")
