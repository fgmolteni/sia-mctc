from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(file_path: str, content: list[str]):
    """
    Crea un archivo PDF con el contenido proporcionado.

    Args:
        file_path: La ruta donde se guardará el archivo PDF.
        content: Una lista de strings, donde cada string es una línea de texto.
    """
    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter  # Ancho y alto de la página

        # Posición inicial del texto (desde la parte superior izquierda)
        x = 72
        y = height - 72

        # Espacio entre líneas
        line_height = 14

        for line in content:
            c.drawString(x, y, line)
            y -= line_height  # Mover a la siguiente línea

        c.save()
        print(f"PDF creado exitosamente en: {file_path}")
        return True
    except Exception as e:
        print(f"Error al crear el PDF: {e}")
        return False
