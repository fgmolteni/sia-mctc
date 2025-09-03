#!/usr/bin/env python3
"""
Script de migración para agregar campo email a tabla usuarios.

Este script ejecuta la migración de forma segura, verificando primero
que la base de datos esté disponible y que la migración no haya sido
aplicada previamente.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.db_common import get_db_engine
from sqlalchemy import text
from components.logging import get_sia_logger

logger = get_sia_logger('migration')

def check_column_exists(engine, table_name: str, column_name: str) -> bool:
    """Verificar si una columna existe en una tabla."""
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table_name AND column_name = :column_name
            """)
            result = connection.execute(query, {
                "table_name": table_name,
                "column_name": column_name
            }).fetchone()
            return result is not None
    except Exception as e:
        logger.error(f"Error verificando columna {column_name}: {e}")
        return False

def run_migration():
    """Ejecutar la migración para agregar campo email."""
    logger.info("Iniciando migración: agregar campo email a tabla usuarios")
    
    engine = get_db_engine()
    if engine is None:
        logger.error("No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar si la columna ya existe
        if check_column_exists(engine, "usuarios", "email"):
            logger.info("La columna email ya existe. Migración no necesaria.")
            return True
        
        with engine.connect() as connection:
            with connection.begin():
                logger.info("Agregando columna email...")
                connection.execute(text("ALTER TABLE usuarios ADD COLUMN email VARCHAR(255)"))
                
                logger.info("Migrando datos existentes...")
                connection.execute(text("UPDATE usuarios SET email = nombre_usuario WHERE email IS NULL"))
                
                logger.info("Creando índice único para email...")
                connection.execute(text("CREATE UNIQUE INDEX idx_usuarios_email ON usuarios(email)"))
                
                logger.info("Estableciendo constraint NOT NULL...")
                connection.execute(text("ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL"))
        
        logger.info("Migración completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error durante la migración: {e}")
        return False
    finally:
        if engine:
            engine.dispose()

if __name__ == "__main__":
    print("=== Migración: Agregar campo email a usuarios ===")
    
    success = run_migration()
    
    if success:
        print("✅ Migración completada exitosamente")
        sys.exit(0)
    else:
        print("❌ Migración falló")
        sys.exit(1)