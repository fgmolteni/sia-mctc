"""
Configuración global de pytest para el proyecto SIA-MCTC.

Este módulo contiene fixtures compartidas y configuración común para todas las pruebas.
Siguiendo metodología TDD, estas fixtures están diseñadas para fallar inicialmente
hasta que se implemente la funcionalidad correspondiente.
"""
import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_reflex_state():
    """
    Mock básico para el estado de Reflex.
    Esta fixture fallará inicialmente hasta implementar los estados reales.
    """
    mock_state = Mock()
    mock_state.users_data = []
    mock_state.load_users = Mock()
    mock_state.load_profiles = Mock()
    return mock_state


@pytest.fixture
def mock_reflex_component():
    """
    Mock para componentes de Reflex que simula el comportamiento básico.
    Fallará hasta que los componentes reales estén implementados.
    """
    def create_mock_component(*args, **kwargs):
        mock_comp = Mock()
        mock_comp.args = args
        mock_comp.kwargs = kwargs
        mock_comp.to_dict = Mock(return_value={"type": "mock_component", "props": kwargs})
        return mock_comp
    
    return create_mock_component


@pytest.fixture
def sample_database_connection():
    """
    Mock de conexión a base de datos para testing.
    Evita dependencias reales de PostgreSQL durante testing.
    """
    with patch('components.db_common.get_db_engine') as mock_engine:
        mock_conn = Mock()
        mock_engine.return_value = mock_conn
        yield mock_conn


@pytest.fixture(autouse=True)
def mock_reflex_imports():
    """
    Auto-fixture que mockea las importaciones de Reflex para evitar 
    errores de inicialización durante las pruebas.
    """
    with patch('reflex.Component') as mock_component, \
         patch('reflex.State') as mock_state, \
         patch('reflex.box') as mock_box, \
         patch('reflex.text') as mock_text, \
         patch('reflex.badge') as mock_badge, \
         patch('reflex.icon') as mock_icon, \
         patch('reflex.card') as mock_card:
        
        # Configurar comportamiento básico de los mocks
        for mock_element in [mock_component, mock_state, mock_box, 
                           mock_text, mock_badge, mock_icon, mock_card]:
            mock_element.return_value = Mock()
        
        yield {
            'component': mock_component,
            'state': mock_state,
            'box': mock_box,
            'text': mock_text,
            'badge': mock_badge,
            'icon': mock_icon,
            'card': mock_card
        }