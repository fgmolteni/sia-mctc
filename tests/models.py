"""
Modelos Pydantic para datos de prueba siguiendo metodología TDD.

Estos modelos definen la estructura esperada de los datos que manejarán 
los componentes de usuario. Las pruebas fallarán inicialmente hasta que
la funcionalidad real implemente estas estructuras correctamente.
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator, EmailStr


class User(BaseModel):
    """
    Modelo Pydantic para datos de usuario.
    
    Este modelo define la estructura esperada que debe manejar UserState
    y los componentes de la tabla de usuarios.
    """
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: Literal["Administrador", "Manager", "Empleado"] = Field(..., description="Rol del usuario")
    area: str = Field(..., min_length=2, max_length=50, description="Área de trabajo")
    status: Literal["Activo", "Inactivo"] = Field(default="Activo", description="Estado del usuario")
    permissions: str = Field(..., pattern=r'^\d+\s+permisos?$', description="Número de permisos")
    attributes: str = Field(..., pattern=r'^\d+\s+atributos?$', description="Número de atributos")
    last_access: str = Field(..., description="Fecha de último acceso en formato dd/mm/yyyy")
    
    @validator('name')
    def validate_name_format(cls, v):
        """Valida que el nombre tenga formato 'Nombre Apellido'."""
        if not v or len(v.strip().split()) < 2:
            raise ValueError("El nombre debe incluir nombre y apellido")
        return v.strip()
    
    @validator('last_access')
    def validate_date_format(cls, v):
        """Valida el formato de fecha dd/mm/yyyy."""
        try:
            datetime.strptime(v, '%d/%m/%Y')
            return v
        except ValueError:
            raise ValueError("La fecha debe tener formato dd/mm/yyyy")
    
    class Config:
        """Configuración del modelo."""
        json_encoders = {
            datetime: lambda dt: dt.strftime('%d/%m/%Y')
        }
        schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "email": "juan.perez@empresa.com",
                "role": "Administrador",
                "area": "Administración",
                "status": "Activo",
                "permissions": "5 permisos",
                "attributes": "5 atributos",
                "last_access": "15/01/2024"
            }
        }


class Agent(BaseModel):
    """
    Modelo Pydantic para datos de agentes del sistema.
    
    Representa a los funcionarios que pueden realizar viáticos.
    """
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., min_length=2, max_length=100, description="Cargo del funcionario")
    department: str = Field(..., min_length=2, max_length=100, description="Departamento")
    identification: str = Field(..., regex=r'^\d{7,10}$', description="Número de identificación")
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, regex=r'^[\d\s\+\-\(\)]+$')
    is_active: bool = Field(default=True)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "María García López",
                "position": "Directora de Proyectos",
                "department": "Investigación",
                "identification": "12345678",
                "email": "maria.garcia@mct.gov.py",
                "phone": "+595 21 123456",
                "is_active": True
            }
        }


class Vehicle(BaseModel):
    """
    Modelo Pydantic para datos de vehículos del sistema.
    
    Representa los vehículos disponibles para viáticos.
    """
    id: Optional[int] = None
    plate: str = Field(..., regex=r'^[A-Z]{3}\s?\d{3,4}$', description="Placa del vehículo")
    brand: str = Field(..., min_length=2, max_length=50)
    model: str = Field(..., min_length=2, max_length=50)
    year: int = Field(..., ge=2000, le=2030, description="Año del vehículo")
    fuel_type: Literal["Gasolina", "Diesel", "Híbrido", "Eléctrico"] = Field(default="Gasolina")
    consumption_per_km: float = Field(..., gt=0, description="Consumo por kilómetro en litros")
    is_available: bool = Field(default=True)
    
    @validator('plate')
    def validate_plate_format(cls, v):
        """Valida el formato de placa paraguaya."""
        import re
        pattern = r'^[A-Z]{3}\s?\d{3,4}$'
        if not re.match(pattern, v.upper()):
            raise ValueError("Formato de placa inválido. Use ABC123 o ABC1234")
        return v.upper()
    
    class Config:
        schema_extra = {
            "example": {
                "plate": "ABC123",
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2022,
                "fuel_type": "Gasolina",
                "consumption_per_km": 0.08,
                "is_available": True
            }
        }


class UserStatistics(BaseModel):
    """
    Modelo para estadísticas de usuarios mostradas en stat_cards.
    """
    total_users: int = Field(..., ge=0, description="Total de usuarios")
    active_users: int = Field(..., ge=0, description="Usuarios activos")
    administrators: int = Field(..., ge=0, description="Número de administradores")
    managers: int = Field(..., ge=0, description="Número de managers")
    employees: int = Field(..., ge=0, description="Número de empleados")
    
    @validator('active_users', 'administrators', 'managers', 'employees')
    def validate_counts_dont_exceed_total(cls, v, values):
        """Valida que los conteos no excedan el total."""
        if 'total_users' in values and v > values['total_users']:
            raise ValueError("Los conteos individuales no pueden exceder el total")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "total_users": 4,
                "active_users": 3,
                "administrators": 1,
                "managers": 1,
                "employees": 2
            }
        }


class UserTableAction(BaseModel):
    """
    Modelo para acciones disponibles en la tabla de usuarios.
    """
    label: str = Field(..., min_length=1, description="Etiqueta de la acción")
    icon: str = Field(..., min_length=1, description="Nombre del ícono")
    href: Optional[str] = None
    text_color: Optional[str] = None
    color: Optional[str] = None
    separator_after: bool = Field(default=False, description="Si mostrar separador después")
    
    class Config:
        schema_extra = {
            "example": {
                "label": "Ver Perfil",
                "icon": "user",
                "href": "/users/profiles",
                "text_color": "#3b82f6",
                "color": "#6b7280"
            }
        }