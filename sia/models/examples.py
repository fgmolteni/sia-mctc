"""
Ejemplos de uso de los modelos de validación del SIA-MCTC.

Este archivo contiene ejemplos prácticos de cómo usar los modelos Pydantic
para validación de datos en el frontend y backend del sistema.
"""

from datetime import datetime
from .validation import User, Agent, Vehicle, Expedient, UserCreate, AgentCreate


def example_user_validation():
    """Ejemplo de validación de usuario."""
    
    # Datos válidos
    user_data = {
        "nombre": "juan carlos",
        "apellido": "pérez garcía",
        "nombre_usuario": "jperez",
        "hash_contrasena": "hash_de_la_contraseña_aquí",
        "rol": "usuario"
    }
    
    try:
        user = User(**user_data)
        print(f"Usuario válido: {user.nombre} {user.apellido}")
        print(f"Username: {user.nombre_usuario}")
        print(f"Rol: {user.rol}")
        return user
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None


def example_agent_validation():
    """Ejemplo de validación de agente."""
    
    # Datos válidos
    agent_data = {
        "nombre": "maría josé",
        "apellido": "lópez martínez",
        "cargo": "técnico especialista",
        "dni": "12345678",
        "categoria": "planta permanente"
    }
    
    try:
        agent = Agent(**agent_data)
        print(f"Agente válido: {agent.nombre} {agent.apellido}")
        print(f"DNI: {agent.dni}")
        print(f"Cargo: {agent.cargo}")
        return agent
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None


def example_vehicle_validation():
    """Ejemplo de validación de vehículo."""
    
    # Datos válidos - patente formato nuevo
    vehicle_data = {
        "marca": "toyota",
        "modelo": "hilux 4x4",
        "patente": "AB123CD",
        "consumo": 12.5,
        "combustible": "Diesel",
        "condicion": "Oficial",
        "activo": True
    }
    
    try:
        vehicle = Vehicle(**vehicle_data)
        print(f"Vehículo válido: {vehicle.marca} {vehicle.modelo}")
        print(f"Patente: {vehicle.patente}")
        print(f"Consumo: {vehicle.consumo} L/100km")
        return vehicle
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None


def example_expedient_validation():
    """Ejemplo de validación de expediente."""
    
    # Datos válidos
    expedient_data = {
        "numero_expediente": "EXP-2024-001",
        "vehiculo_id": 1,
        "origen": "Ciudad de Buenos Aires",
        "fecha_salida": datetime(2024, 3, 15, 8, 0),
        "fecha_regreso": datetime(2024, 3, 17, 18, 0),
        "objetivo_viaje": "Capacitación técnica en nuevas tecnologías de información",
        "distancia_total_km": 450.5,
        "combustible_estimado_lts": 56.3,
        "estado": "Anticipo",
        "creado_por_usuario_id": 1
    }
    
    try:
        expedient = Expedient(**expedient_data)
        print(f"Expediente válido: {expedient.numero_expediente}")
        print(f"Destino desde: {expedient.origen}")
        print(f"Estado: {expedient.estado}")
        return expedient
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None


def example_creation_models():
    """Ejemplo de uso de modelos de creación."""
    
    # Crear usuario
    user_create_data = {
        "nombre": "Ana",
        "apellido": "González",
        "nombre_usuario": "agonzalez",
        "contrasena": "MiPassword123",
        "rol": "supervisor"
    }
    
    try:
        new_user = UserCreate(**user_create_data)
        print(f"Usuario para crear: {new_user.nombre} {new_user.apellido}")
        print(f"Contraseña válida: {'Sí' if new_user.contrasena else 'No'}")
    except ValueError as e:
        print(f"Error en creación de usuario: {e}")
    
    # Crear agente
    agent_create_data = {
        "nombre": "Roberto",
        "apellido": "Fernández",
        "dni": "87654321",
        "cargo": "Director de Área"
    }
    
    try:
        new_agent = AgentCreate(**agent_create_data)
        print(f"Agente para crear: {new_agent.nombre} {new_agent.apellido}")
        print(f"DNI: {new_agent.dni}")
    except ValueError as e:
        print(f"Error en creación de agente: {e}")


def example_validation_errors():
    """Ejemplos de errores de validación comunes."""
    
    print("=== Ejemplos de errores de validación ===")
    
    # DNI inválido
    try:
        Agent(nombre="Test", apellido="User", dni="123", cargo="Test")
    except ValueError as e:
        print(f"Error DNI inválido: {e}")
    
    # Patente inválida
    try:
        Vehicle(marca="Ford", modelo="Focus", patente="INVALID123")
    except ValueError as e:
        print(f"Error patente inválida: {e}")
    
    # Consumo negativo
    try:
        Vehicle(marca="Ford", modelo="Focus", patente="ABC123", consumo=-5.0)
    except ValueError as e:
        print(f"Error consumo negativo: {e}")
    
    # Fecha de regreso anterior a salida
    try:
        Expedient(
            numero_expediente="TEST-001",
            origen="Buenos Aires",
            fecha_salida=datetime(2024, 3, 17, 8, 0),
            fecha_regreso=datetime(2024, 3, 15, 18, 0),  # Anterior a salida
            creado_por_usuario_id=1
        )
    except ValueError as e:
        print(f"Error fechas inconsistentes: {e}")
    
    # Contraseña débil
    try:
        UserCreate(
            nombre="Test",
            apellido="User", 
            nombre_usuario="testuser",
            contrasena="123"  # Muy corta
        )
    except ValueError as e:
        print(f"Error contraseña débil: {e}")


if __name__ == "__main__":
    """Ejecutar ejemplos si el archivo se ejecuta directamente."""
    
    print("=== Ejemplos de Validación SIA-MCTC ===\n")
    
    print("1. Validación de Usuario:")
    example_user_validation()
    
    print("\n2. Validación de Agente:")
    example_agent_validation()
    
    print("\n3. Validación de Vehículo:")
    example_vehicle_validation()
    
    print("\n4. Validación de Expediente:")
    example_expedient_validation()
    
    print("\n5. Modelos de Creación:")
    example_creation_models()
    
    print("\n6. Errores de Validación:")
    example_validation_errors()