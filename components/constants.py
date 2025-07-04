from enum import Enum

class LimitesViaje(Enum):
    """Enum para los límites y valores fijos relacionados con los viajes."""
    DISTANCIA_MINIMA_VIATICOS = 60  # Límite de distancia en Km
    PORCENTAJE_MAXIMO_TAXI = 0.2    # Límite de taxi como porcentaje del total de viáticos
    DIAS_PARA_RENDICION = 3

class PorcentajesAjuste(Enum):
    """Enum para los porcentajes de ajuste de viáticos según las provisiones."""
    CON_ALOJAMIENTO_Y_COMIDA = 0.25  # Se provee alojamiento y comida
    CON_ALOJAMIENTO = 0.50           # Se provee solo alojamiento
    CON_COMIDA = 0.75                # Se provee solo comida

# Las categorías son una lista de strings, por lo que mantenerlas como una constante es adecuado.
class CasesPorCargo(Enum):
    MINISTRO = "I"
    SUBSECRETARIO = "II"
    DIRECTOR = "II"
    AGENTE = "IV"
