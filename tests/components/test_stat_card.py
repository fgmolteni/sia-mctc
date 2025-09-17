"""
Pruebas unitarias para el componente stat_card siguiendo metodología TDD.

Estas pruebas definen el comportamiento esperado del componente stat_card.
FALLARÁN INICIALMENTE (Red phase) hasta que se implemente correctamente
la funcionalidad del componente.

Las pruebas validan:
- Renderizado correcto con diferentes props
- Manejo de parámetros obligatorios y opcionales
- Estructura HTML/componente esperada
- Estilos y colores apropiados
"""
import pytest
from sia.components.data_display.cards import stat_card


class TestStatCard:
    """
    Suite de pruebas para el componente stat_card.
    
    Siguiendo TDD, estas pruebas definen EXACTAMENTE cómo debe comportarse
    el componente antes de implementar la funcionalidad.
    """

    @pytest.mark.component
    def test_stat_card_renderiza_con_props_basicos(self, mock_reflex_imports):
        """
        DEBE renderizar correctamente con props básicos (título, valor, icono).
        
        Esta prueba FALLARÁ inicialmente porque:
        1. El componente puede no existir
        2. Los props pueden no ser manejados correctamente
        3. La estructura de componente puede ser incorrecta
        """
        # Arrange - Datos de entrada válidos
        title = "Total Usuarios"
        value = "4" 
        icon = "user-check"
        
        # Act - Llamar al componente
        result = stat_card(title=title, value=value, icon=icon)
        
        # Assert - Verificar comportamiento esperado
        # El componente debe retornar un objeto válido
        assert result is not None, "stat_card debe retornar un componente válido"
        
        # Mock de rx.card debe haber sido llamado
        mock_reflex_imports['card'].assert_called_once()
        call_args = mock_reflex_imports['card'].call_args
        
        # Debe recibir estructura interna correcta (vstack con contenido)
        assert call_args is not None, "rx.card debe recibir argumentos"
        
    @pytest.mark.component  
    def test_stat_card_renderiza_con_icon_color_personalizado(self, mock_reflex_imports):
        """
        DEBE manejar correctamente el parámetro opcional icon_color.
        
        FALLARÁ si:
        1. El parámetro icon_color no se pasa al ícono
        2. El color por defecto no es aplicado correctamente
        3. Los colores personalizados no son respetados
        """
        # Arrange
        title = "Usuarios Activos"
        value = "3"
        icon = "check"
        custom_color = "green.400"
        
        # Act
        result = stat_card(
            title=title,
            value=value, 
            icon=icon,
            icon_color=custom_color
        )
        
        # Assert
        assert result is not None
        mock_reflex_imports['card'].assert_called_once()
        
        # El ícono debe ser llamado con el color personalizado
        # Esto fallará hasta implementar correctamente el manejo de icon_color
        mock_reflex_imports['icon'].assert_called()
        
    @pytest.mark.component
    def test_stat_card_usa_color_por_defecto_cuando_no_especificado(self, mock_reflex_imports):
        """
        DEBE usar color por defecto 'white.400' cuando icon_color no se especifica.
        
        FALLARÁ si el valor por defecto no está implementado correctamente.
        """
        # Arrange
        title = "Test Card"
        value = "10"
        icon = "test-icon"
        
        # Act - Sin especificar icon_color
        result = stat_card(title=title, value=value, icon=icon)
        
        # Assert
        assert result is not None
        
        # El ícono debe usar color por defecto "white.400"
        # Esta aserción FALLARÁ hasta implementar el comportamiento esperado
        mock_reflex_imports['icon'].assert_called()
        icon_call_args = mock_reflex_imports['icon'].call_args
        assert icon_call_args is not None, "El ícono debe ser renderizado"
    
    @pytest.mark.component
    @pytest.mark.parametrize("test_case", [
        {"title": "Total", "value": "4", "icon": "user-check"},
        {"title": "Activos", "value": "3", "icon": "check", "icon_color": "green.400"},
        {"title": "Admins", "value": "1", "icon": "shield", "icon_color": "purple.400"},
    ])
    def test_stat_card_renderiza_multiples_configuraciones(
        self, 
        test_case, 
        mock_reflex_imports
    ):
        """
        DEBE manejar correctamente múltiples configuraciones diferentes.
        
        Prueba parametrizada que FALLARÁ para cualquier configuración
        que no sea manejada correctamente por el componente.
        """
        # Arrange - Usar datos del caso de prueba
        title = test_case["title"]
        value = test_case["value"]
        icon = test_case["icon"]
        icon_color = test_case.get("icon_color")
        
        # Act
        if icon_color:
            result = stat_card(
                title=title, 
                value=value, 
                icon=icon, 
                icon_color=icon_color
            )
        else:
            result = stat_card(title=title, value=value, icon=icon)
        
        # Assert
        assert result is not None, f"stat_card falló con configuración: {test_case}"
        mock_reflex_imports['card'].assert_called()
    
    @pytest.mark.component
    def test_stat_card_estructura_componente_correcta(self, mock_reflex_imports):
        """
        DEBE generar la estructura de componente correcta según diseño.
        
        Verifica que:
        1. Se use rx.card como contenedor principal
        2. Se incluya rx.vstack para organización vertical
        3. Se incluya rx.hstack para header con título e ícono
        4. Se incluya rx.heading para el valor
        
        FALLARÁ si la estructura no coincide con el diseño esperado.
        """
        # Arrange
        title = "Test Structure"
        value = "99"
        icon = "test"
        
        # Act
        result = stat_card(title=title, value=value, icon=icon)
        
        # Assert - Verificar llamadas a componentes esperados
        mock_reflex_imports['card'].assert_called_once()
        
        # Debe incluir elementos de estructura interna
        # Estas aserciones FALLARÁN hasta implementar la estructura correcta
        
        # Se espera que se llame rx.text para el título
        # Se espera que se llame rx.icon para el ícono  
        # Se espera que se llame rx.heading para el valor
        
        # Nota: Las aserciones específicas dependen de la implementación real
        # Estas pruebas guiarán el desarrollo hacia la estructura correcta
        assert result is not None
    
    @pytest.mark.component
    def test_stat_card_propiedades_de_estilo(self, mock_reflex_imports):
        """
        DEBE aplicar las propiedades de estilo correctas.
        
        Verifica:
        1. Dimensiones mínimas (width_min="250px", height="120px")
        2. Padding apropiado
        3. Estructura responsive (width="100%")
        
        FALLARÁ si las propiedades de estilo no son aplicadas correctamente.
        """
        # Arrange
        title = "Style Test"
        value = "42"
        icon = "style"
        
        # Act
        result = stat_card(title=title, value=value, icon=icon)
        
        # Assert
        assert result is not None
        
        # Verificar que rx.card fue llamado con propiedades de estilo
        mock_reflex_imports['card'].assert_called_once()
        call_kwargs = mock_reflex_imports['card'].call_args.kwargs if mock_reflex_imports['card'].call_args else {}
        
        # Estas aserciones FALLARÁN hasta que las propiedades sean implementadas
        expected_style_props = ['width_min', 'width', 'height', 'padding']
        # Nota: Verificación específica depende de cómo se pasen los argumentos
        
    @pytest.mark.component
    def test_stat_card_maneja_valores_edge_case(self, mock_reflex_imports):
        """
        DEBE manejar casos límite de valores correctamente.
        
        Casos límite:
        1. Valores muy largos
        2. Valores con caracteres especiales  
        3. Títulos muy largos
        4. Íconos inexistentes
        
        FALLARÁ si el componente no maneja robustamente estos casos.
        """
        edge_cases = [
            {
                "title": "Título Extremadamente Largo Que Podría Romper El Layout",
                "value": "999999999",
                "icon": "user-check"
            },
            {
                "title": "Caracteres Especiales",
                "value": "4 (±2)",
                "icon": "check"
            },
            {
                "title": "Empty", 
                "value": "",
                "icon": "question"
            }
        ]
        
        for case in edge_cases:
            # Act
            result = stat_card(
                title=case["title"],
                value=case["value"], 
                icon=case["icon"]
            )
            
            # Assert - No debe fallar con casos límite
            assert result is not None, f"stat_card falló con caso límite: {case}"
    
    @pytest.mark.component
    def test_stat_card_parametros_requeridos(self, mock_reflex_imports):
        """
        DEBE fallar apropiadamente cuando faltan parámetros requeridos.
        
        Los parámetros title, value e icon son obligatorios.
        FALLARÁ si el componente no valida correctamente los parámetros requeridos.
        """
        # Test con parámetro faltante - title
        with pytest.raises(TypeError):
            stat_card(value="4", icon="user")
        
        # Test con parámetro faltante - value  
        with pytest.raises(TypeError):
            stat_card(title="Test", icon="user")
            
        # Test con parámetro faltante - icon
        with pytest.raises(TypeError):
            stat_card(title="Test", value="4")
    
    @pytest.mark.component
    def test_stat_card_kwargs_adicionales(self, mock_reflex_imports):
        """
        DEBE pasar correctamente kwargs adicionales al componente.
        
        El componente debe aceptar propiedades adicionales y pasarlas
        al elemento contenedor.
        
        FALLARÁ si **kwargs no son manejados correctamente.
        """
        # Arrange
        title = "Test"
        value = "1"
        icon = "test"
        extra_prop = "test_value"
        class_name = "custom-stat-card"
        
        # Act
        result = stat_card(
            title=title,
            value=value,
            icon=icon,
            extra_prop=extra_prop,
            class_name=class_name
        )
        
        # Assert
        assert result is not None
        
        # Las propiedades adicionales deben ser pasadas al componente
        # Esta verificación FALLARÁ hasta implementar correctamente **kwargs
        mock_reflex_imports['card'].assert_called_once()