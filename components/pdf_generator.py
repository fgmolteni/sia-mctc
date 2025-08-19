from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from components.logging import get_sia_logger

# Logger para este módulo
logger = get_sia_logger('pdf')

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
        logger.info(f"PDF creado exitosamente", extra={
            'action': 'pdf_created', 'file_path': file_path, 'content_lines': len(content)
        })
        return True
    except Exception as e:
        logger.error(f"Error al crear PDF: {str(e)}", extra={
            'action': 'pdf_creation_failed', 'file_path': file_path, 'content_lines': len(content) if content else 0
        })
        return False
