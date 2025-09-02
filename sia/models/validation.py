"""
Modelos Pydantic para validación de datos del SIA-MCTC.

Este módulo define los modelos de datos que corresponden a las tablas
de la base de datos PostgreSQL, incluyendo validaciones específicas
para el dominio del sistema (DNI argentino, patentes, emails, etc.).
"""

import re
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator, ConfigDict


class BaseValidationModel(BaseModel):
    """
    Modelo base para todos los modelos de validación del SIA.
    
    Configurado para trabajar con SQLAlchemy y proporcionar
    funcionalidades comunes de validación.
    """
    
    model_config = ConfigDict(
        # Permite usar el modelo con objetos SQLAlchemy
        from_attributes=True,
        # Validar asignaciones de campos
        validate_assignment=True,
        # Usar enum por valor
        use_enum_values=True,
        # Configuración de JSON
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class User(BaseValidationModel):
    """
    Modelo de validación para la tabla 'usuarios'.
    
    Valida los datos de usuarios del sistema incluyendo roles,
    credenciales y información personal.
    
    Campos correspondientes a la tabla SQL:
    - id: SERIAL PRIMARY KEY
    - nombre: VARCHAR(100) NOT NULL
    - apellido: VARCHAR(100) NOT NULL  
    - nombre_usuario: VARCHAR(50) UNIQUE NOT NULL
    - hash_contrasena: VARCHAR(255) NOT NULL
    - rol: VARCHAR(50) DEFAULT 'usuario' NOT NULL
    - fecha_creacion: TIMESTAMPTZ DEFAULT now()
    """
    
    id: Optional[int] = Field(None, description="ID único del usuario")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del usuario")
    nombre_usuario: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Nombre de usuario único en el sistema"
    )
    hash_contrasena: str = Field(..., max_length=255, description="Hash de la contraseña")
    rol: Literal["admin", "usuario", "supervisor"] = Field(
        "usuario", 
        description="Rol del usuario en el sistema"
    )
    fecha_creacion: Optional[datetime] = Field(None, description="Fecha de creación del usuario")
    
    @validator('nombre', 'apellido')
    def validate_names(cls, v):
        """Valida que nombres y apellidos no estén vacíos y tengan formato correcto."""
        if not v or not v.strip():
            raise ValueError('El nombre y apellido no pueden estar vacíos')
        
        # Solo letras, espacios, acentos y caracteres especiales del español
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        
        return v.strip().title()
    
    @validator('nombre_usuario')
    def validate_username(cls, v):
        """Valida el formato del nombre de usuario."""
        if not v or not v.strip():
            raise ValueError('El nombre de usuario no puede estar vacío')
        
        # Permitir letras, números, guiones, guiones bajos, puntos y arrobas (para emails)
        if not re.match(r'^[a-zA-Z0-9_.-@]+$', v.strip()):
            raise ValueError('El nombre de usuario solo puede contener letras, números, guiones, puntos y @')
        
        return v.strip().lower()


class Agent(BaseValidationModel):
    """
    Modelo de validación para la tabla 'agentes'.
    
    Valida los datos de agentes/empleados del ministerio,
    incluyendo validación específica de DNI argentino.
    
    Campos correspondientes a la tabla SQL:
    - id: SERIAL PRIMARY KEY
    - nombre: VARCHAR(100) NOT NULL
    - apellido: VARCHAR(100) NOT NULL
    - cargo: VARCHAR(100)
    - dni: VARCHAR(20) UNIQUE NOT NULL
    - categoria: VARCHAR(50)
    """
    
    id: Optional[int] = Field(None, description="ID único del agente")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del agente")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del agente")
    cargo: Optional[str] = Field(None, max_length=100, description="Cargo del agente")
    dni: str = Field(..., min_length=7, max_length=20, description="DNI del agente")
    categoria: Optional[str] = Field(None, max_length=50, description="Categoría del agente")
    
    @validator('nombre', 'apellido')
    def validate_names(cls, v):
        """Valida que nombres y apellidos tengan formato correcto."""
        if not v or not v.strip():
            raise ValueError('El nombre y apellido no pueden estar vacíos')
        
        # Solo letras, espacios, acentos y caracteres especiales del español
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        
        return v.strip().title()
    
    @validator('dni')
    def validate_dni(cls, v):
        """Valida el formato del DNI argentino."""
        if not v or not v.strip():
            raise ValueError('El DNI no puede estar vacío')
        
        # Remover puntos y espacios si los hay
        dni_clean = re.sub(r'[.\s-]', '', v.strip())
        
        # El DNI debe tener entre 7 y 8 dígitos
        if not re.match(r'^\d{7,8}$', dni_clean):
            raise ValueError('El DNI debe contener entre 7 y 8 dígitos numéricos')
        
        # Verificar que no sea un DNI obviamente inválido
        dni_num = int(dni_clean)
        if dni_num < 1000000 or dni_num > 99999999:
            raise ValueError('El DNI debe estar en el rango válido (1.000.000 - 99.999.999)')
        
        return dni_clean
    
    @validator('cargo', 'categoria')
    def validate_optional_strings(cls, v):
        """Valida campos de texto opcionales."""
        if v is not None:
            v = v.strip()
            if not v:  # Si está vacío después de strip, convertir a None
                return None
            return v.title()
        return v


class Vehicle(BaseValidationModel):
    """
    Modelo de validación para la tabla 'vehiculos'.
    
    Valida los datos de vehículos incluyendo patente argentina,
    consumo, tipo de combustible y condición.
    
    Campos correspondientes a la tabla SQL:
    - id: SERIAL PRIMARY KEY
    - marca: VARCHAR(100) NOT NULL
    - modelo: VARCHAR(100) NOT NULL
    - patente: VARCHAR(20) UNIQUE NOT NULL
    - consumo: NUMERIC(5, 2) -- L/100km
    - combustible: VARCHAR(50) -- Tipo de combustible
    - condicion: VARCHAR(50) -- 'Oficial', 'Afectado'
    - activo: BOOLEAN DEFAULT true
    """
    
    id: Optional[int] = Field(None, description="ID único del vehículo")
    marca: str = Field(..., min_length=1, max_length=100, description="Marca del vehículo")
    modelo: str = Field(..., min_length=1, max_length=100, description="Modelo del vehículo")
    patente: str = Field(..., min_length=6, max_length=20, description="Patente del vehículo")
    consumo: Optional[float] = Field(
        None, 
        gt=0, 
        le=999.99,
        description="Consumo en litros por 100km"
    )
    combustible: Optional[Literal["Nafta", "Diesel", "GNC", "Eléctrico"]] = Field(
        None, 
        description="Tipo de combustible"
    )
    condicion: Optional[Literal["Oficial", "Afectado"]] = Field(
        None,
        description="Condición del vehículo"
    )
    activo: bool = Field(True, description="Estado del vehículo (activo/inactivo)")
    
    @validator('marca', 'modelo')
    def validate_vehicle_info(cls, v):
        """Valida información básica del vehículo."""
        if not v or not v.strip():
            raise ValueError('La marca y modelo no pueden estar vacíos')
        
        # Permitir letras, números, espacios y algunos caracteres especiales
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$', v.strip()):
            raise ValueError('La marca/modelo contiene caracteres no válidos')
        
        return v.strip().title()
    
    @validator('patente')
    def validate_patente(cls, v):
        """Valida el formato de patente argentina."""
        if not v or not v.strip():
            raise ValueError('La patente no puede estar vacía')
        
        # Remover espacios y convertir a mayúsculas
        patente_clean = v.strip().upper().replace(' ', '')
        
        # Patente antigua: 3 letras + 3 números (ej: ABC123)
        old_format = re.match(r'^[A-Z]{3}\d{3}$', patente_clean)
        
        # Patente nueva: 2 letras + 3 números + 2 letras (ej: AB123CD)
        new_format = re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', patente_clean)
        
        # Patente de motos: 3 números + 3 letras (ej: 123ABC)
        moto_format = re.match(r'^\d{3}[A-Z]{3}$', patente_clean)
        
        if not (old_format or new_format or moto_format):
            raise ValueError(
                'Formato de patente inválido. '
                'Formatos válidos: ABC123 (antigua), AB123CD (nueva), 123ABC (moto)'
            )
        
        return patente_clean
    
    @validator('consumo')
    def validate_consumo(cls, v):
        """Valida que el consumo sea razonable."""
        if v is not None:
            if v <= 0:
                raise ValueError('El consumo debe ser mayor que 0')
            if v > 50:  # Consumo muy alto, probablemente error
                raise ValueError('El consumo parece excesivamente alto (>50L/100km)')
        return v


class Expedient(BaseValidationModel):
    """
    Modelo de validación para la tabla 'expedientes'.
    
    Valida los datos de expedientes de viaje incluyendo fechas,
    montos y estados válidos.
    
    Campos correspondientes a la tabla SQL:
    - id: SERIAL PRIMARY KEY
    - numero_expediente: VARCHAR(100) UNIQUE NOT NULL
    - vehiculo_id: INTEGER REFERENCES vehiculos(id)
    - origen: VARCHAR(255) NOT NULL
    - fecha_salida: TIMESTAMP NOT NULL
    - fecha_regreso: TIMESTAMP NOT NULL
    - objetivo_viaje: TEXT
    - distancia_total_km: NUMERIC(10, 2)
    - combustible_estimado_lts: NUMERIC(10, 2)
    - monto_combustible_calculado: NUMERIC(12, 2)
    - monto_viaticos_calculado: NUMERIC(12, 2)
    - monto_total_expediente: NUMERIC(12, 2)
    - estado: VARCHAR(50) -- 'Anticipo', 'Recomposicion', 'Cerrado'
    - creado_por_usuario_id: INTEGER NOT NULL REFERENCES usuarios(id)
    - fecha_creacion: TIMESTAMPTZ DEFAULT now()
    """
    
    id: Optional[int] = Field(None, description="ID único del expediente")
    numero_expediente: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Número único del expediente"
    )
    vehiculo_id: Optional[int] = Field(None, description="ID del vehículo asignado")
    origen: str = Field(..., min_length=1, max_length=255, description="Lugar de origen")
    fecha_salida: datetime = Field(..., description="Fecha y hora de salida")
    fecha_regreso: datetime = Field(..., description="Fecha y hora de regreso")
    objetivo_viaje: Optional[str] = Field(None, description="Objetivo del viaje")
    distancia_total_km: Optional[float] = Field(
        None, 
        ge=0,
        description="Distancia total en kilómetros"
    )
    combustible_estimado_lts: Optional[float] = Field(
        None,
        ge=0,
        description="Combustible estimado en litros"
    )
    monto_combustible_calculado: Optional[float] = Field(
        None,
        ge=0,
        description="Monto calculado para combustible"
    )
    monto_viaticos_calculado: Optional[float] = Field(
        None,
        ge=0,
        description="Monto calculado para viáticos"
    )
    monto_total_expediente: Optional[float] = Field(
        None,
        ge=0,
        description="Monto total del expediente"
    )
    estado: Literal["Anticipo", "Recomposicion", "Cerrado"] = Field(
        "Anticipo",
        description="Estado del expediente"
    )
    creado_por_usuario_id: int = Field(..., description="ID del usuario que creó el expediente")
    fecha_creacion: Optional[datetime] = Field(None, description="Fecha de creación")
    
    @validator('numero_expediente')
    def validate_numero_expediente(cls, v):
        """Valida el formato del número de expediente."""
        if not v or not v.strip():
            raise ValueError('El número de expediente no puede estar vacío')
        
        # Formato típico: letras, números, guiones, barras
        if not re.match(r'^[A-Za-z0-9\-/]+$', v.strip()):
            raise ValueError(
                'El número de expediente solo puede contener letras, números, guiones y barras'
            )
        
        return v.strip().upper()
    
    @validator('fecha_regreso')
    def validate_fecha_regreso(cls, v, values):
        """Valida que la fecha de regreso sea posterior a la de salida."""
        if 'fecha_salida' in values and v <= values['fecha_salida']:
            raise ValueError('La fecha de regreso debe ser posterior a la fecha de salida')
        return v
    
    @validator('origen')
    def validate_origen(cls, v):
        """Valida el origen del viaje."""
        if not v or not v.strip():
            raise ValueError('El origen no puede estar vacío')
        
        return v.strip().title()
    
    @validator('objetivo_viaje')
    def validate_objetivo_viaje(cls, v):
        """Valida el objetivo del viaje."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
            if len(v) < 10:
                raise ValueError('El objetivo del viaje debe tener al menos 10 caracteres')
        return v
    
    @validator('distancia_total_km')
    def validate_distancia(cls, v):
        """Valida que la distancia sea razonable."""
        if v is not None and v > 10000:  # Más de 10,000 km parece excesivo
            raise ValueError('La distancia total parece excesivamente alta')
        return v


# Modelos para operaciones específicas (Create, Update)
class UserCreate(BaseValidationModel):
    """Modelo para crear nuevos usuarios."""
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    nombre_usuario: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=6, description="Contraseña en texto plano")
    rol: Literal["admin", "usuario", "supervisor"] = "usuario"
    
    @validator('contrasena')
    def validate_password(cls, v):
        """Valida la fortaleza de la contraseña."""
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra')
        
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        
        return v


class UserUpdate(BaseValidationModel):
    """Modelo para actualizar usuarios existentes."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    nombre_usuario: Optional[str] = Field(None, min_length=3, max_length=50)
    rol: Optional[Literal["admin", "usuario", "supervisor"]] = None
    activo: Optional[bool] = None


class AgentCreate(BaseValidationModel):
    """Modelo para crear nuevos agentes."""
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    cargo: Optional[str] = Field(None, max_length=100)
    dni: str = Field(..., min_length=7, max_length=20)
    categoria: Optional[str] = Field(None, max_length=50)


class VehicleCreate(BaseValidationModel):
    """Modelo para crear nuevos vehículos."""
    marca: str = Field(..., min_length=1, max_length=100)
    modelo: str = Field(..., min_length=1, max_length=100)
    patente: str = Field(..., min_length=6, max_length=20)
    consumo: Optional[float] = Field(None, gt=0, le=999.99)
    combustible: Optional[Literal["Nafta", "Diesel", "GNC", "Eléctrico"]] = None
    condicion: Optional[Literal["Oficial", "Afectado"]] = None