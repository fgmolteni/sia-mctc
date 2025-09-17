from PIL import Image

def open_image(image_path: str):
    """
    Abre una imagen usando la librería Pillow (PIL).

    Args:
        image_path: La ruta absoluta al archivo de imagen.

    Returns:
        Un objeto Image de Pillow si la imagen se abre correctamente,
        o None si ocurre un error.
    """
    try:
        img = Image.open(image_path)
        print(f"Imagen '{image_path}' abierta exitosamente. Formato: {img.format}, Tamaño: {img.size}")
        return img
    except FileNotFoundError:
        print(f"Error: El archivo '{image_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al abrir la imagen: {e}")
        return None