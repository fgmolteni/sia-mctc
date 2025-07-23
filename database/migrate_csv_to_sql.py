import pandas as pd
from components.db_connector import get_db_engine
import numpy as np

def migrate_data():
    """
    Lee los datos de los archivos CSV, los adapta a la nueva estructura de la base de datos
    y los inserta en las tablas de PostgreSQL.
    """
    engine = get_db_engine()
    if engine is None:
        print("No se pudo obtener el motor de la base de datos. Abortando migración.")
        return

    try:
        # --- Migración de Agentes ---
        print("Migrando datos de agentes...")
        try:
            agents_df = pd.read_csv("data/agents.csv")
            
            # Renombrar columnas para que coincidan con la BD
            agents_df.rename(columns={'clase': 'categoria'}, inplace=True)

            # Añadir columnas faltantes con valores por defecto
            agents_df['cargo'] = 'No especificado'
            # Generar DNI único para cada agente para cumplir con la restricción UNIQUE
            agents_df['dni'] = [f'0000{i}' for i in range(len(agents_df))]

            # Seleccionar y ordenar las columnas para la inserción
            agents_to_insert = agents_df[['nombre', 'apellido', 'cargo', 'dni', 'categoria']]
            
            agents_to_insert.to_sql('agentes', engine, if_exists='append', index=False)
            print(f"Se migraron {len(agents_to_insert)} registros a la tabla 'agentes'.")

        except FileNotFoundError:
            print("No se encontró el archivo data/agents.csv. Saltando migración de agentes.")
        except Exception as e:
            print(f"Error durante la migración de agentes: {e}")

        # --- Migración de Vehículos ---
        print("\nMigrando datos de vehículos...")
        try:
            cars_df = pd.read_csv("data/cars.csv")

            # Renombrar columnas
            cars_df.rename(columns={'brand': 'marca', 'model': 'modelo'}, inplace=True)

            # Añadir columnas faltantes con valores por defecto
            cars_df['patente'] = [f'AA{100+i}AA' for i in range(len(cars_df))] # Patente única de ejemplo
            cars_df['consumo'] = np.nan
            cars_df['combustible'] = 'No especificado'
            cars_df['condicion'] = 'Oficial'
            cars_df['activo'] = True

            # Seleccionar y ordenar las columnas para la inserción
            cars_to_insert = cars_df[['marca', 'modelo', 'patente', 'consumo', 'combustible', 'condicion', 'activo']]
            
            cars_to_insert.to_sql('vehiculos', engine, if_exists='append', index=False)
            print(f"Se migraron {len(cars_to_insert)} registros a la tabla 'vehiculos'.")

        except FileNotFoundError:
            print("No se encontró el archivo data/cars.csv. Saltando migración de vehículos.")
        except Exception as e:
            print(f"Error durante la migración de vehículos: {e}")

    finally:
        if engine:
            engine.dispose()

if __name__ == '__main__':
    print("--- Iniciando el script de migración de datos de CSV a SQL ---")
    migrate_data()
    print("--- Script de migración finalizado ---")