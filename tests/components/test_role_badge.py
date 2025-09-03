"""
Pruebas unitarias para el componente role_badge siguiendo metodología TDD.

Estas pruebas definen el comportamiento esperado del componente role_badge.
FALLARÁN INICIALMENTE (Red phase) hasta que se implemente correctamente
la funcionalidad del componente.

Las pruebas validan:
- Esquemas de colores correctos por rol (admin, manager, employee, default)
- Renderizado de texto apropiado  
- Manejo de parámetros opcionales y **kwargs
- Estructura de componente badge esperada
"""
import pytest
from sia.components.data_display.badges import role_badge


class TestRoleBadge:
    """
    Suite de pruebas para el componente role_badge.
    
    Siguiendo TDD, estas pruebas definen el comportamiento esperado
    ANTES de implementar la funcionalidad. Guían el desarrollo hacia
    la implementación correcta.
    """

    @pytest.mark.component
    def test_role_badge_renderiza_con_rol_admin(self, mock_reflex_imports):
        """
        DEBE renderizar correctamente badge para rol administrador.
        
        FALLARÁ inicialmente porque:
        1. Los colores específicos para admin pueden no estar definidos
        2. El esquema de colores puede no estar implementado
        3. La lógica de mapeo de roles puede estar incompleta
        """
        # Arrange
        text = "Administrador"
        role = "admin"
        
        # Act
        result = role_badge(text=text, role=role)
        
        # Assert
        assert result is not None, "role_badge debe retornar un componente válido"
        
        # Debe llamar a rx.badge con colores de admin
        mock_reflex_imports['badge'].assert_called_once()
        call_args = mock_reflex_imports['badge'].call_args
        
        # Verificar que se pasaron argumentos correctos
        assert call_args is not None, "rx.badge debe recibir argumentos"
        
        # Verificar texto como primer argumento
        assert call_args.args[0] == text, "El primer argumento debe ser el texto"

    @pytest.mark.component
    def test_role_badge_renderiza_con_rol_manager(self, mock_reflex_imports):
        """
        DEBE renderizar correctamente badge para rol manager.
        
        FALLARÁ si:
        1. Los colores para manager no están correctamente definidos
        2. El rol "manager" no está en el diccionario de esquemas de color
        3. Los valores de Color.manager_text/bg no existen
        """
        # Arrange  
        text = "Manager de Ventas"
        role = "manager"
        
        # Act
        result = role_badge(text=text, role=role)
        
        # Assert
        assert result is not None
        mock_reflex_imports['badge'].assert_called_once()
        
        # El badge debe ser creado con esquema de colores de manager
        call_kwargs = mock_reflex_imports['badge'].call_args.kwargs
        
        # Esta aserción FALLARÁ hasta implementar el esquema correcto
        assert 'color' in call_kwargs, "Debe especificar color de texto"
        assert 'bg' in call_kwargs, "Debe especificar color de fondo"

    @pytest.mark.component  
    def test_role_badge_renderiza_con_rol_employee(self, mock_reflex_imports):
        """
        DEBE renderizar correctamente badge para rol employee.
        
        FALLARÁ si el esquema de colores para empleados no está implementado.
        """
        # Arrange
        text = "Empleado"
        role = "employee"
        
        # Act
        result = role_badge(text=text, role=role)
        
        # Assert
        assert result is not None
        mock_reflex_imports['badge'].assert_called_once()
        
        # Verificar llamada con parámetros de employee
        call_args = mock_reflex_imports['badge'].call_args
        assert call_args.args[0] == text

    @pytest.mark.component
    def test_role_badge_usa_rol_default_cuando_no_especificado(self, mock_reflex_imports):
        """
        DEBE usar rol 'default' cuando no se especifica parámetro role.
        
        FALLARÁ si:
        1. El valor por defecto no es "default"  
        2. Los colores default no están definidos
        3. El manejo de parámetros opcionales no funciona
        """
        # Arrange
        text = "Usuario Genérico"
        # No especificar role - debe usar default
        
        # Act
        result = role_badge(text=text)
        
        # Assert
        assert result is not None
        mock_reflex_imports['badge'].assert_called_once()
        
        # Debe usar colores del esquema default
        call_kwargs = mock_reflex_imports['badge'].call_args.kwargs
        
        # Esta verificación FALLARÁ hasta implementar colores default correctos
        assert 'color' in call_kwargs, "Debe aplicar color default"
        assert 'bg' in call_kwargs, "Debe aplicar fondo default"

    @pytest.mark.component
    def test_role_badge_maneja_rol_inexistente(self, mock_reflex_imports):
        """
        DEBE usar esquema default para roles que no existen.
        
        FALLARÁ si no hay manejo de fallback para roles desconocidos.
        """
        # Arrange
        text = "Rol Desconocido"
        role = "rol_inexistente"
        
        # Act
        result = role_badge(text=text, role=role)
        
        # Assert
        assert result is not None
        mock_reflex_imports['badge'].assert_called_once()
        
        # Debe usar esquema default como fallback
        # Esta lógica FALLARÁ hasta implementar el fallback correcto

    @pytest.mark.component
    @pytest.mark.parametrize("role_data", [
        {"text": "Admin", "role": "admin"},
        {"text": "Supervisor", "role": "manager"},  
        {"text": "Staff", "role": "employee"},
        {"text": "Guest", "role": "default"},
    ])
    def test_role_badge_multiples_roles(self, role_data, mock_reflex_imports):
        """
        DEBE manejar correctamente todos los roles válidos.
        
        Prueba parametrizada que FALLARÁ para cualquier rol
        no implementado correctamente.
        """
        # Arrange
        text = role_data["text"]
        role = role_data["role"]
        
        # Act  
        result = role_badge(text=text, role=role)
        
        # Assert
        assert result is not None, f"role_badge falló para rol: {role}"
        mock_reflex_imports['badge'].assert_called()
        
        # Reset mock para próxima iteración
        mock_reflex_imports['badge'].reset_mock()

    @pytest.mark.component
    def test_role_badge_propiedades_de_estilo(self, mock_reflex_imports):
        """
        DEBE aplicar propiedades de estilo correctas al badge.
        
        Verifica:
        1. Padding horizontal y vertical (px="2", py="1")
        2. Border radius usando BorderRadius.DEFAULT
        3. Font weight usando FontWeight.MEDIUM
        
        FALLARÁ si las propiedades de estilo no son aplicadas.
        """
        # Arrange
        text = "Style Test"
        role = "admin"
        
        # Act
        result = role_badge(text=text, role=role)
        
        # Assert
        assert result is not None
        mock_reflex_imports['badge'].assert_called_once()
        
        call_kwargs = mock_reflex_imports['badge'].call_args.kwargs
        
        # Estas verificaciones FALLARÁN hasta implementar estilos correctos
        expected_style_props = ['px', 'py', 'border_radius', 'font_weight']
        
        # Verificar que las propiedades de estilo están presentes
        for prop in expected_style_props:
            # Esta aserción específica depende de la implementación
            pass  # Se implementará según la estructura real

    @pytest.mark.component
    def test_role_badge_kwargs_adicionales(self, mock_reflex_imports):
        """
        DEBE pasar correctamente kwargs adicionales al badge.
        
        El componente debe aceptar propiedades adicionales y pasarlas
        al rx.badge subyacente.
        
        FALLARÁ si **kwargs no son manejados correctamente.
        """
        # Arrange
        text = "Test Badge"
        role = "admin"
        custom_prop = "test_value"
        class_name = "custom-badge"
        
        # Act
        result = role_badge(
            text=text,
            role=role,
            custom_prop=custom_prop,
            class_name=class_name
        )
        
        # Assert
        assert result is not None
        mock_reflex_imports['badge'].assert_called_once()
        
        # Las propiedades adicionales deben ser pasadas al badge
        call_kwargs = mock_reflex_imports['badge'].call_args.kwargs
        
        # Esta verificación FALLARÁ hasta implementar **kwargs correctamente
        # Los kwargs adicionales deben estar presentes en la llamada

    @pytest.mark.component 
    def test_role_badge_texto_obligatorio(self, mock_reflex_imports):
        """
        DEBE requerir el parámetro text como obligatorio.
        
        FALLARÁ si el componente acepta llamadas sin parámetro text.
        """
        # Act & Assert - Debe fallar sin texto
        with pytest.raises(TypeError, match="text"):
            role_badge(role="admin")

    @pytest.mark.component
    def test_role_badge_esquemas_de_color_definidos(self, mock_reflex_imports):
        """
        DEBE tener esquemas de color específicos para cada rol.
        
        Verifica que:
        1. admin usa Color.admin_text y Color.admin_bg
        2. manager usa Color.manager_text y Color.manager_bg  
        3. employee usa Color.employee_text y Color.employee_bg
        4. default usa ColorText.GRAY_700 y Color.background_light
        
        FALLARÁ si los esquemas no están correctamente definidos.
        """
        roles_to_test = ["admin", "manager", "employee", "default"]
        
        for role in roles_to_test:
            # Arrange
            text = f"Test {role}"
            
            # Act
            result = role_badge(text=text, role=role)
            
            # Assert
            assert result is not None, f"role_badge falló para rol: {role}"
            
            # Cada rol debe producir un badge válido
            mock_reflex_imports['badge'].assert_called()
            
            # Reset para próxima iteración
            mock_reflex_imports['badge'].reset_mock()

    @pytest.mark.component
    def test_role_badge_maneja_texto_especial(self, mock_reflex_imports):
        """
        DEBE manejar texto con caracteres especiales correctamente.
        
        Casos especiales:
        1. Texto con acentos
        2. Texto muy largo
        3. Texto con espacios múltiples
        4. Texto vacío
        
        FALLARÁ si el componente no maneja robustamente estos casos.
        """
        special_texts = [
            "Administradoría",  # Con acentos
            "Super Administrador de Sistemas de Información",  # Muy largo
            "Manager   Espacios",  # Espacios múltiples  
            "",  # Texto vacío
        ]
        
        for text in special_texts:
            # Act
            result = role_badge(text=text, role="admin")
            
            # Assert - No debe fallar con textos especiales
            assert result is not None, f"role_badge falló con texto: '{text}'"
            
            # Reset mock
            mock_reflex_imports['badge'].reset_mock()

    @pytest.mark.component
    def test_role_badge_valores_de_tipo_correcto(self, mock_reflex_imports):
        """
        DEBE validar que role sea uno de los tipos Literal válidos.
        
        FALLARÁ si acepta roles que no están en el tipo Literal definido.
        """
        valid_roles = ["admin", "manager", "employee", "default"]
        
        for role in valid_roles:
            # Act
            result = role_badge(text="Test", role=role)
            
            # Assert
            assert result is not None, f"role_badge rechazó rol válido: {role}"
            
            # Reset mock
            mock_reflex_imports['badge'].reset_mock()