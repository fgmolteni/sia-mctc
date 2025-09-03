from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from components.logging import get_sia_logger

# Logger para este módulo
logger = get_sia_logger('pdf')

def generar_anticipo_viatico(file_path: str, data: dict):
    """
    Crea un archivo PDF de solicitud de viático completo basado en la imagen proporcionada.

    Args:
        file_path: La ruta donde se guardará el archivo PDF.
        data: Un diccionario con los datos del formulario.
    """
    try:
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleN.fontName = 'Helvetica'
        styleN.fontSize = 7
        styleN.leading = 10

        # === Coordenadas y Márgenes ===
        margin = 1.2 * cm
        left_margin = margin
        right_margin = width - margin
        
        # === Fuentes ===
        font_large_bold = "Helvetica-Bold"
        font_normal_bold = "Helvetica-Bold"
        font_normal = "Helvetica"
        font_small = "Helvetica"
        
        font_size_large = 10
        font_size_normal = 8
        font_size_small = 7
        font_size_extra_small = 5
        
        # --- Bloque 1: Anticipo y Datos del Agente ---
        y_pos = height - margin - 0.5*cm
        box1_height = 6 * cm
        c.rect(left_margin, y_pos - box1_height, right_margin - left_margin, box1_height)
        
        # Líneas divisorias del Bloque 1
        center_x_b1 = left_margin + (right_margin - left_margin) / 2
        c.line(center_x_b1, y_pos - box1_height, center_x_b1, y_pos)
        
        # Contenido Izquierda Bloque 1
        x_text = left_margin + 0.5 * cm
        y_text = y_pos + 0.2 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "(Anticipo)")
        y_text -= 1 * cm
        c.setFont(font_normal, font_size_normal)
        c.drawString(x_text, y_text, f"Señor Director: {data.get('director', '...................................')}")
        y_text -= 0.7 * cm
        p = Paragraph("Conforme a instrucciones recibidas el suscripto solicita anticipo de fondos el que se detalla en el presente formulario.", styleN)
        p.wrapOn(c, center_x_b1 - left_margin - 1*cm, 2*cm)
        p.drawOn(c, x_text, y_text - p.height)
        
        y_firma = y_pos - box1_height + 0.2*cm
        c.drawString(x_text, y_firma, f"Fecha: {data.get('fecha_anticipo', '..../..../........')}")
        c.setDash([2, 2])
        c.line(center_x_b1 - 4*cm, y_firma + 0.8*cm, center_x_b1 - 1*cm, y_firma + 0.8*cm)
        c.setDash([])
        c.drawCentredString(center_x_b1 - 2.5*cm, y_firma + 0.2*cm, "Firma")

        # Contenido Derecha Bloque 1
        x_text = center_x_b1 + 0.5 * cm
        y_text = y_pos - 0.3 * cm
        c.setFont(font_normal_bold, font_size_extra_small)
        c.drawString(x_text, y_text, f"UNIDAD DE ORGANIZACION: {data.get('unidad_organizacion', '')}")
        y_text -= 0.2 * cm
        c.drawString(x_text, y_text, f"UNIDAD OPERATIVA: {data.get('unidad_operativa', '')}")
        y_text -= 0.2 * cm
        c.line(x_text, y_text, right_margin - 0.5*cm, y_text)
        y_text -= 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "DEL AGENTE")
        c.setFont(font_normal, font_size_small)
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Apellido: {data.get('apellido', '')}")
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Nombre: {data.get('nombre', '')}")
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Cargo: {data.get('cargo', '')}")
        c.drawRightString(right_margin - 0.5*cm, y_text, f"Sueldo Básico $ {data.get('sueldo_basico', '0.00')}")
        y_text -= 0.3 * cm
        c.line(x_text, y_text, right_margin - 0.5*cm, y_text)
        y_text -= 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "De la Comisión:")
        c.setFont(font_normal, font_size_small)
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Fecha de Iniciación: {data.get('fecha_iniciacion', '')}")
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Destino: {data.get('destino', '')}")
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Medio de Transporte: {data.get('medio_transporte', '')}")
        y_text -= 0.5 * cm
        c.drawString(x_text, y_text, f"Obj: {data.get('objetivo', '')}")

        # --- Bloque 2: Solicitud y Autorización ---
        y_pos = y_pos - box1_height
        box2_height = 3.5 * cm
        c.rect(left_margin, y_pos - box2_height, right_margin - left_margin, box2_height)
        
        # Líneas divisorias del Bloque 2
        c.line(center_x_b1, y_pos - box2_height, center_x_b1, y_pos)
        
        # Contenido Izquierda Bloque 2
        x_text = left_margin + 0.5 * cm
        y_text = y_pos - 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "SEÑOR")
        y_text -= 0.5 * cm
        c.setFont(font_normal, font_size_normal)
        c.drawString(x_text, y_text, "Presente:")
        y_text -= 0.2 * cm
        p = Paragraph("De conformidad a los términos legales correspondientes, solicitando se sirva autorizar la presente comisión oficial.", styleN)
        p.wrapOn(c, center_x_b1 - left_margin - 1*cm, 2*cm)
        p.drawOn(c, x_text, y_text - p.height)
        
        y_firma = y_pos - box2_height + 0.5*cm
        c.drawString(x_text, y_firma + 0.2*cm, f"Fecha: {data.get('fecha_autorizacion', '..../..../........')}")
        c.setDash([2, 2])
        c.line(center_x_b1 - 4*cm, y_firma + 0.5*cm, center_x_b1 - 1*cm, y_firma + 0.5*cm)
        c.setDash([])
        c.drawCentredString(center_x_b1 - 2.5*cm, y_firma + 0.2*cm, "Firma")

        # Contenido Derecha Bloque 2
        x_text = center_x_b1 + 0.5 * cm
        y_text = y_pos - 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "SOLICITUD DE FONDO")
        c.setFont(font_normal, font_size_normal)
        y_text -= 0.7 * cm
        c.drawString(x_text, y_text, "Anticipo")
        c.drawRightString(right_margin - 0.5*cm, y_text, f"$ {data.get('anticipo_monto', '0.00')}")
        y_text -= 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "TOTAL")
        c.drawRightString(right_margin - 0.5*cm, y_text, f"$ {data.get('total_monto', '0.00')}")
        y_text -= 0.5 * cm
        c.line(x_text, y_text, right_margin - 0.5*cm, y_text)
        y_text -= 0.7 * cm
        c.setFont(font_normal, font_size_normal)
        c.drawString(x_text, y_text, "Rendición del Gasto:")
        c.drawRightString(right_margin - 0.5*cm, y_text, f"$ {data.get('rendicion_gasto', '0.00')}")

        # --- Bloque 3: Rendición de Cuentas ---
        y_pos = y_pos - box2_height - 0.5*cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(left_margin, y_pos, "RENDICIÓN DE CUENTAS:")
        c.setFont(font_normal, font_size_normal)
        p_text = "INFORMA que el agente comisionado si no adeuda suma alguna en concepto de viático y movilidad y que el importe del básico es correcto."
        p = Paragraph(p_text, styleN)
        p.wrapOn(c, right_margin - left_margin, 2*cm)
        y_pos -= 0.2*cm
        p.drawOn(c, left_margin, y_pos - p.height)
        y_pos -= (p.height + 0.5*cm)
        c.drawString(left_margin, y_pos, "Corrientes,")
        c.setDash([2, 2])
        c.line(right_margin - 5*cm, y_pos - 0.2*cm, right_margin, y_pos - 0.2*cm)
        c.setDash([])
        c.drawCentredString(right_margin - 2.5*cm, y_pos - 0.5*cm, "Firma Autorizada")

        # --- Bloque 4: Administración y Tesorería ---
        y_pos -= 1*cm
        box4_height = 2.5 * cm
        c.rect(left_margin, y_pos - box4_height, right_margin - left_margin, box4_height)
        c.line(center_x_b1, y_pos - box4_height, center_x_b1, y_pos)
        
        # Contenido Izquierda Bloque 4
        x_text = left_margin + 0.5 * cm
        y_text = y_pos - 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "DIRECCION DE ADMINISTRACION:")
        c.setFont(font_normal, font_size_small)
        y_text -= 0.5 * cm
        p = Paragraph("Por autorizada la comisión solicitada para la liquidación y pago del anticipo correspondiente.", styleN)
        p.wrapOn(c, center_x_b1 - left_margin - 1*cm, 2*cm)
        p.drawOn(c, x_text, y_text - p.height)
        
        # Contenido Derecha Bloque 4
        x_text = center_x_b1 + 0.5 * cm
        y_text = y_pos - 0.5 * cm
        c.setFont(font_normal_bold, font_size_normal)
        c.drawString(x_text, y_text, "A TESORERIA:")
        c.setFont(font_normal, font_size_small)
        y_text -= 0.5 * cm
        p = Paragraph("Con Libramiento de Entrega .................... donde se cumplimenta la liquidación para su pago.", styleN)
        p.wrapOn(c, right_margin - center_x_b1 - 1*cm, 2*cm)
        p.drawOn(c, x_text, y_text - p.height)

        # Firmas Bloque 4
        y_firma = y_pos - box4_height - 0.8*cm
        c.setDash([2, 2])
        c.line(left_margin + 2*cm, y_firma + 0.3*cm, center_x_b1 - 2*cm, y_firma + 0.3*cm)
        c.line(center_x_b1 + 2*cm, y_firma + 0.3*cm, right_margin - 2*cm, y_firma + 0.3*cm)
        c.setDash([])
        c.drawCentredString(left_margin + (center_x_b1-left_margin)/2, y_firma - 0.3*cm, "Subsecretario o Ministro")
        c.drawCentredString(center_x_b1 + (right_margin-center_x_b1)/2, y_firma - 0.3*cm, "Jefe Departamento Contable")

        # --- Bloque 5: Recibí ---
        y_pos = y_pos - box4_height - 1.5*cm
        c.setFont(font_normal_bold, font_size_normal)
        recibi_text = f"""
        RECIBÍ de la Tesorería de la Dirección de Administración del Ministerio de Ciencia y Tecnología.
        Por transferencia la suma de Pesos {data.get('monto_en_letras', '...................')} ({data.get('total_monto', '$0.00')}) en
        concepto de anticipo de Viáticos, cuya rendición de cuentas me comprometo a realizar dentro de los
        6 (seis) días de finalizada la comisión o en menos tiempo en caso de recibir instrucciones de
        realizar una nueva comisión, en caso contrario me sujeto a las sanciones establecidas en la ley de
        CONTABILIDAD.
        """
        p = Paragraph(recibi_text, styleN)
        p.wrapOn(c, right_margin - left_margin, 5*cm)
        p.drawOn(c, left_margin, y_pos - p.height)
        y_pos -= (p.height + 0.5*cm)
        
        c.setDash([2, 2])
        c.line(right_margin - 5*cm, y_pos + 0.3*cm, right_margin, y_pos + 0.3*cm)
        c.setDash([])
        c.drawCentredString(right_margin - 2.5*cm, y_pos - 0.3*cm, "Firma")
        c.drawString(right_margin - 4.5*cm, y_pos - 0.8*cm, f"M. I. Nº: {data.get('mi_nro', '..................')}")

        # --- Bloque 6: Certificación ---
        y_pos -= 1.5*cm
        c.setFont(font_large_bold, font_size_large)
        c.drawCentredString(width/2, y_pos, "LA DIRECCIÓN DE ADMINISTRACIÓN CERTIFICA QUE EL DÍA ... de ... del 202...")
        y_pos -= 0.8*cm
        cert_text = f"""
        El Señor {data.get('nombre_completo', '........................................')}, ha presentado la rendición de cuentas correspondiente al anticipo por
        libramiento Nº .................... de fecha ....................
        Se extiende la presente a los efectos pertinentes.
        """
        p = Paragraph(cert_text, styleN)
        p.wrapOn(c, right_margin - left_margin, 5*cm)
        p.drawOn(c, left_margin, y_pos - p.height)
        y_pos -= (p.height + 1*cm)
        
        c.setDash([2, 2])
        c.line(right_margin - 5*cm, y_pos + 0.3*cm, right_margin, y_pos + 0.3*cm)
        c.setDash([])
        c.drawCentredString(right_margin - 2.5*cm, y_pos - 0.3*cm, "Firma Autorizada")

        c.save()
        logger.info("Formulario de viático creado exitosamente", extra={
            'action': 'form_pdf_created', 'file_path': file_path, 'form_type': 'anticipo_viatico'
        })
        return True
    except Exception as e:
        logger.error(f"Error al crear formulario PDF: {str(e)}", extra={
            'action': 'form_pdf_creation_failed', 'file_path': file_path, 'form_type': 'anticipo_viatico'
        })
        return False

if __name__ == '__main__':
    # Datos de ejemplo para probar la generación del PDF
    datos_ejemplo = {
        "director": "Dr. Juan Perez",
        "fecha_anticipo": "01/07/2025",
        "unidad_organizacion": "DIRECCIÓN GENERAL DE ADMINISTRACIÓN",
        "unidad_operativa": "DEPARTAMENTO DE TESORERÍA",
        "apellido": "GOMEZ",
        "nombre": "JORGE ANTONIO",
        "nombre_completo": "GOMEZ, JORGE ANTONIO",
        "cargo": "MINISTRO",
        "sueldo_basico": "150000.00",
        "fecha_iniciacion": "02/04/2025",
        "destino": "ITUZAINGO - VIRASORO - SANTO TOME",
        "medio_transporte": "Vehículo Oficial AH096KX",
        "objetivo": "COMISIONES OFICIALES",
        "anticipo_monto": "192,000.00",
        "total_monto": "192,000.00",
        "rendicion_gasto": "192,000.00",
        "fecha_autorizacion": "02/07/2025",
        "monto_en_letras": "Ciento Noventa y Dos Mil con 00/100",
        "mi_nro": "12.345.678"
    }
    
    # Generar el PDF en la carpeta 'report'
    generar_anticipo_viatico('/home/gabi/projects/SIA/report/formulario_viatico_completo.pdf', datos_ejemplo)