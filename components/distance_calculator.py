

import requests
from geopy.geocoders import Nominatim

def get_driving_distance_and_time(address1: str, address2: str) -> tuple[float, float] | None:
    """
    Calcula la distancia y el tiempo de viaje en auto entre dos direcciones.

    Utiliza Nominatim para la geocodificación y el API público de OSRM para
    obtener la ruta por carretera.

    Args:
        address1: La dirección de origen.
        address2: La dirección de destino.

    Returns:
        Una tupla con (distancia_en_km, duracion_en_minutos), o None si
        ocurre un error o no se encuentra la ruta.
    """
    geolocator = Nominatim(user_agent="route_calculator_app")

    try:
        # 1. Geocodificar las direcciones
        location1 = geolocator.geocode(address1)
        location2 = geolocator.geocode(address2)

        if not location1 or not location2:
            print("Error: Una o ambas direcciones no pudieron ser geocodificadas.")
            return None

        coords1 = f"{location1.longitude},{location1.latitude}"
        coords2 = f"{location2.longitude},{location2.latitude}"

        # 2. Consultar al API de enrutamiento de OSRM
        url = f"http://router.project-osrm.org/route/v1/driving/{coords1};{coords2}?overview=false"
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la petición HTTP falla

        data = response.json()

        # 3. Procesar la respuesta
        if data['code'] == 'Ok' and data['routes']:
            route = data['routes'][0]
            distance_meters = route['distance']  # Distancia en metros
            duration_seconds = route['duration'] # Duración en segundos

            distance_km = distance_meters / 1000
            duration_hours = duration_seconds / 3600

            return (distance_km, duration_hours)
        else:
            print(f"Error de OSRM: {data.get('message', 'No se encontró ruta')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error de red al contactar OSRM: {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None


