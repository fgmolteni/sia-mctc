"""
Fixtures de datos para pruebas siguiendo metodología TDD.

Este módulo contiene fixtures que proporcionan datos de prueba validados
con modelos Pydantic. Las pruebas fallarán inicialmente hasta que los
componentes implementen correctamente el manejo de estos datos.
"""
import pytest
from typing import List, Dict, Any
from tests.models import User, UserStatistics, UserTableAction


@pytest.fixture
def valid_user_data() -> Dict[str, Any]:
    """
    Datos válidos de usuario para pruebas exitosas.
    
    Esta fixture fallará si los componentes no manejan correctamente
    los datos estructurados de usuario.
    """
    return {
        "name": "Juan Pérez",
        "email": "juan.perez@empresa.com",
        "role": "Administrador",
        "area": "Administración",
        "status": "Activo",
        "permissions": "5 permisos",
        "attributes": "5 atributos",
        "last_access": "15/01/2024"
    }


@pytest.fixture
def invalid_user_data() -> List[Dict[str, Any]]:
    """
    Lista de datos inválidos de usuario para probar validaciones.
    
    Las pruebas con estos datos deben fallar y manejar errores apropiadamente.
    """
    return [
        # Email inválido
        {
            "name": "Juan Pérez",
            "email": "email-invalido",
            "role": "Administrador",
            "area": "Administración",
            "status": "Activo",
            "permissions": "5 permisos",
            "attributes": "5 atributos",
            "last_access": "15/01/2024"
        },
        # Nombre muy corto
        {
            "name": "J",
            "email": "j@empresa.com",
            "role": "Administrador",
            "area": "Administración",
            "status": "Activo",
            "permissions": "5 permisos",
            "attributes": "5 atributos",
            "last_access": "15/01/2024"
        },
        # Rol inválido
        {
            "name": "María García",
            "email": "maria@empresa.com",
            "role": "RolInexistente",
            "area": "Administración",
            "status": "Activo",
            "permissions": "5 permisos",
            "attributes": "5 atributos",
            "last_access": "15/01/2024"
        },
        # Formato de fecha incorrecto
        {
            "name": "Carlos López",
            "email": "carlos@empresa.com",
            "role": "Empleado",
            "area": "Marketing",
            "status": "Activo",
            "permissions": "5 permisos",
            "attributes": "5 atributos",
            "last_access": "2024-01-15"  # Formato incorrecto
        }
    ]


@pytest.fixture
def sample_users_list() -> List[Dict[str, Any]]:
    """
    Lista de usuarios de muestra para pruebas de tabla y estado.
    
    Simula los datos que UserState.load_users() debería cargar y validar.
    """
    return [
        {
            "name": "Juan Pérez",
            "email": "juan.perez@empresa.com",
            "role": "Administrador",
            "area": "Administración",
            "status": "Activo",
            "permissions": "5 permisos",
            "attributes": "5 atributos",
            "last_access": "15/01/2024"
        },
        {
            "name": "María García",
            "email": "maria.garcia@empresa.com",
            "role": "Manager",
            "area": "Ventas",
            "status": "Activo",
            "permissions": "4 permisos",
            "attributes": "3 atributos",
            "last_access": "14/01/2024"
        },
        {
            "name": "Carlos López",
            "email": "carlos.lopez@empresa.com",
            "role": "Empleado",
            "area": "Marketing",
            "status": "Activo",
            "permissions": "4 permisos",
            "attributes": "3 atributos",
            "last_access": "13/01/2024"
        },
        {
            "name": "Ana Martínez",
            "email": "ana.martinez@empresa.com",
            "role": "Empleado",
            "area": "RRHH",
            "status": "Inactivo",
            "permissions": "3 permisos",
            "attributes": "3 atributos",
            "last_access": "10/01/2024"
        }
    ]


@pytest.fixture
def validated_users(sample_users_list) -> List[User]:
    """
    Lista de usuarios validados con Pydantic.
    
    Esta fixture fallará si los modelos Pydantic no validan correctamente
    o si los datos no cumplen con las restricciones definidas.
    """
    return [User(**user_data) for user_data in sample_users_list]


@pytest.fixture
def user_statistics_data() -> Dict[str, Any]:
    """
    Datos de estadísticas de usuarios para stat_cards.
    
    Los componentes stat_card deberán mostrar estos datos correctamente.
    """
    return {
        "total_users": 4,
        "active_users": 3,
        "administrators": 1,
        "managers": 1,
        "employees": 2
    }


@pytest.fixture
def validated_statistics(user_statistics_data) -> UserStatistics:
    """
    Estadísticas validadas con Pydantic.
    
    Fallará si el modelo UserStatistics no valida los datos correctamente.
    """
    return UserStatistics(**user_statistics_data)


@pytest.fixture
def stat_card_test_cases() -> List[Dict[str, Any]]:
    """
    Casos de prueba para el componente stat_card.
    
    Cada caso define props diferentes que stat_card debe manejar correctamente.
    """
    return [
        {
            "title": "Total Usuarios",
            "value": "4",
            "icon": "user-check",
            "icon_color": "white.400"  # Color por defecto
        },
        {
            "title": "Activos",
            "value": "3",
            "icon": "check",
            "icon_color": "green.400"
        },
        {
            "title": "Administradores",
            "value": "1",
            "icon": "shield",
            "icon_color": "purple.400"
        },
        {
            "title": "Managers",
            "value": "1",
            "icon": "briefcase",
            "icon_color": "orange.400"
        }
    ]


@pytest.fixture
def role_badge_test_cases() -> List[Dict[str, Any]]:
    """
    Casos de prueba para el componente role_badge.
    
    Cada caso prueba un rol diferente con su esquema de colores esperado.
    """
    return [
        {
            "text": "Administrador",
            "role": "admin",
            "expected_colors": {
                "color": "admin_text",  # Se deben mapear a colores reales
                "bg": "admin_bg"
            }
        },
        {
            "text": "Manager",
            "role": "manager", 
            "expected_colors": {
                "color": "manager_text",
                "bg": "manager_bg"
            }
        },
        {
            "text": "Empleado",
            "role": "employee",
            "expected_colors": {
                "color": "employee_text",
                "bg": "employee_bg"
            }
        },
        {
            "text": "Usuario",
            "role": "default",
            "expected_colors": {
                "color": "gray_700",
                "bg": "background_light"
            }
        }
    ]


@pytest.fixture
def status_badge_test_cases() -> List[Dict[str, Any]]:
    """
    Casos de prueba para el componente status_badge.
    
    Prueba diferentes estados con y sin dots indicadores.
    """
    return [
        {
            "text": "Activo",
            "status": "active",
            "show_dot": True,
            "expected_dot_color": "status_active"
        },
        {
            "text": "Inactivo",
            "status": "inactive",
            "show_dot": True,
            "expected_dot_color": "icon_inactive"
        },
        {
            "text": "Pendiente",
            "status": "pending",
            "show_dot": False,
            "expected_dot_color": None
        },
        {
            "text": "Error",
            "status": "error",
            "show_dot": True,
            "expected_dot_color": "error"
        }
    ]


@pytest.fixture
def table_headers() -> List[str]:
    """
    Headers esperados para la tabla de usuarios.
    
    Los componentes de tabla deben renderizar estos headers correctamente.
    """
    return ["Usuario", "Email", "Área", "Estado", "Permisos", "Acciones"]


@pytest.fixture
def table_render_functions() -> Dict[str, str]:
    """
    Mapeo de funciones de renderizado para columnas de tabla.
    
    Define qué funciones personalizadas debe usar cada columna.
    """
    return {
        "name": "render_user_column",
        "role": "render_role_column", 
        "status": "render_status_column",
        "permissions": "render_permissions_column",
        "attributes": "render_attributes_column"
    }


@pytest.fixture
def table_actions() -> List[UserTableAction]:
    """
    Acciones disponibles en la tabla de usuarios validadas con Pydantic.
    
    Fallará si UserTableAction no valida correctamente las acciones.
    """
    actions_data = [
        {
            "label": "Ver Perfil",
            "icon": "user",
            "href": "/users/profiles",
            "text_color": "#3b82f6",
            "color": "#6b7280"
        },
        {
            "label": "Modificar",
            "icon": "pencil",
            "color": "#6b7280"
        },
        {
            "label": "Eliminar",
            "icon": "trash-2",
            "color": "#ef4444",
            "text_color": "#ef4444",
            "separator_after": True
        }
    ]
    return [UserTableAction(**action) for action in actions_data]


@pytest.fixture
def search_filters_options() -> Dict[str, List[str]]:
    """
    Opciones disponibles en los filtros de búsqueda.
    
    Los componentes de filtro deben mostrar estas opciones correctamente.
    """
    return {
        "roles": ["Todos los roles", "Administrador", "Manager", "Empleado"],
        "statuses": ["Todos los estados", "Activo", "Inactivo"]
    }


@pytest.fixture
def empty_users_data() -> List[Dict[str, Any]]:
    """
    Datos vacíos para probar estados sin usuarios.
    
    Los componentes deben manejar correctamente el estado vacío.
    """
    return []


@pytest.fixture
def single_user_data() -> List[Dict[str, Any]]:
    """
    Un solo usuario para probar casos límite.
    
    Útil para probar renderizado con datos mínimos.
    """
    return [{
        "name": "Usuario Test",
        "email": "test@empresa.com",
        "role": "Empleado",
        "area": "Testing",
        "status": "Activo",
        "permissions": "1 permiso",
        "attributes": "1 atributo",
        "last_access": "01/01/2024"
    }]


@pytest.fixture
def user_modal_test_cases() -> List[Dict[str, Any]]:
    """
    Casos de prueba para el modal de usuario (crear/editar).
    
    Define diferentes escenarios que el modal debe manejar correctamente.
    FALLARÁ hasta que el componente user_modal esté implementado.
    """
    return [
        # Caso: Modal cerrado
        {
            "show_user_modal": False,
            "form_is_editing": False,
            "expected_render": False,
            "description": "Modal no debe renderizarse cuando está cerrado"
        },
        # Caso: Crear usuario nuevo  
        {
            "show_user_modal": True,
            "form_is_editing": False,
            "expected_title": "Crear Usuario",
            "expected_button_text": "Crear Usuario", 
            "expected_password_field": True,
            "expected_action": "create_user_submit",
            "description": "Modal en modo crear debe mostrar todos los campos"
        },
        # Caso: Editar usuario existente
        {
            "show_user_modal": True,
            "form_is_editing": True,
            "expected_title": "Editar Usuario",
            "expected_button_text": "Actualizar Usuario",
            "expected_password_field": False,
            "expected_action": "update_user_submit", 
            "description": "Modal en modo editar no debe mostrar campo contraseña"
        }
    ]


@pytest.fixture
def user_form_fields_data() -> Dict[str, Any]:
    """
    Datos de prueba para los campos del formulario de usuario.
    
    Proporciona valores válidos para probar el binding de estado.
    """
    return {
        "form_nombre": "Juan Carlos",
        "form_apellido": "González Pérez",
        "form_nombre_usuario": "juan.gonzalez@ministerio.gob.py",
        "form_contrasena": "ContraseñaSegura123!",
        "form_rol": "admin"
    }


@pytest.fixture  
def user_form_validation_cases() -> List[Dict[str, Any]]:
    """
    Casos de validación para el formulario de usuario.
    
    Define casos válidos e inválidos para probar validaciones.
    FALLARÁ hasta que la validación esté implementada.
    """
    return [
        # Caso válido completo
        {
            "form_nombre": "María",
            "form_apellido": "García", 
            "form_nombre_usuario": "maria.garcia",
            "form_contrasena": "Pass123!",
            "form_rol": "usuario",
            "is_valid": True,
            "description": "Datos válidos completos"
        },
        # Caso: nombre vacío (inválido)
        {
            "form_nombre": "",
            "form_apellido": "López",
            "form_nombre_usuario": "lopez",
            "form_contrasena": "Pass123!",
            "form_rol": "usuario",
            "is_valid": False,
            "expected_error": "Nombre es requerido",
            "description": "Nombre vacío debe ser inválido"
        },
        # Caso: apellido vacío (inválido) 
        {
            "form_nombre": "Carlos",
            "form_apellido": "",
            "form_nombre_usuario": "carlos",
            "form_contrasena": "Pass123!",
            "form_rol": "usuario",
            "is_valid": False,
            "expected_error": "Apellido es requerido",
            "description": "Apellido vacío debe ser inválido"
        },
        # Caso: nombre de usuario vacío (inválido)
        {
            "form_nombre": "Ana",
            "form_apellido": "Martínez",
            "form_nombre_usuario": "",
            "form_contrasena": "Pass123!",
            "form_rol": "usuario", 
            "is_valid": False,
            "expected_error": "Nombre de usuario es requerido",
            "description": "Nombre de usuario vacío debe ser inválido"
        },
        # Caso: contraseña vacía en modo crear (inválido)
        {
            "form_nombre": "Luis",
            "form_apellido": "Rodríguez",
            "form_nombre_usuario": "luis.rodriguez",
            "form_contrasena": "",
            "form_rol": "usuario",
            "is_valid": False,
            "expected_error": "Contraseña es requerida",
            "description": "Contraseña vacía en crear debe ser inválido",
            "context": {"form_is_editing": False}
        }
    ]


@pytest.fixture
def user_modal_role_options() -> List[Dict[str, str]]:
    """
    Opciones disponibles para el select de rol en el modal.
    
    Define las opciones exactas que debe mostrar el select.
    """
    return [
        {"value": "usuario", "label": "Usuario"},
        {"value": "supervisor", "label": "Supervisor"},
        {"value": "admin", "label": "Administrador"}
    ]


@pytest.fixture
def user_modal_state_methods() -> List[str]:
    """
    Lista de métodos que UserState debe implementar para el modal.
    
    Estos métodos deben existir para que el modal funcione correctamente.
    FALLARÁ hasta que se implementen en UserState.
    """
    return [
        "set_form_nombre",
        "set_form_apellido", 
        "set_form_nombre_usuario",
        "set_form_contrasena",
        "set_form_rol",
        "show_create_user_modal",
        "show_edit_user_modal", 
        "close_user_modal",
        "create_user_submit",
        "update_user_submit"
    ]


@pytest.fixture
def user_modal_responsive_breakpoints() -> Dict[str, str]:
    """
    Breakpoints responsivos para el modal de usuario.
    
    Define cómo debe adaptarse el modal en diferentes pantallas.
    """
    return {
        "mobile": "90vw",     # Pantallas pequeñas
        "tablet": "600px",    # Tablets
        "desktop": "500px",   # Escritorio
        "max_width": "600px"  # Ancho máximo
    }