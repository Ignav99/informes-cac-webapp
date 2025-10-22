#!/usr/bin/env python3
"""
Script para generar informes de análisis de equipos rivales de fútbol
Club Atlético Central - Versión 2.1 (con logo integrado)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as PlatypusImage, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, String
from reportlab.graphics import renderPDF
from PIL import Image as PILImage
import json
import sys
import os
import base64
import io
from datetime import datetime

# Colores corporativos
COLOR_NEGRO = colors.HexColor('#000000')
COLOR_GRIS = colors.HexColor('#6B7280')
COLOR_GRIS_FONDO = colors.HexColor('#F3F4F6')
COLOR_GRIS_CLARO = colors.HexColor('#E5E7EB')
COLOR_GRIS_OSCURO = colors.HexColor('#374151')
COLOR_VERDE = colors.HexColor('#10B981')
COLOR_AMARILLO = colors.HexColor('#FFC107')
COLOR_VERDE_CESPED = colors.HexColor('#2D7A3E')
COLOR_ROJO_PELIGRO = colors.HexColor('#EF4444')
COLOR_AZUL_NORMAL = colors.HexColor('#3B82F6')
COLOR_VERDE_DEBIL = colors.HexColor('#86EFAC')

# Logo del Club Atlético Central en base64 (integrado)
LOGO_BASE64 = """
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"""

def obtener_logo():
    """Retorna un objeto Image de ReportLab con el logo del club"""
    try:
        logo_bytes = base64.b64decode(LOGO_BASE64)
        logo_buffer = io.BytesIO(logo_bytes)
        return PlatypusImage(logo_buffer, width=1.8*cm, height=1.8*cm)
    except Exception as e:
        print(f"⚠ No se pudo cargar el logo: {e}")
        return None

def crear_campo_futbol_horizontal(jugadores, sistema_tactico, ancho=360, alto=240):
    """
    Crea un campo de fútbol HORIZONTAL con los jugadores posicionados
    Portero a la IZQUIERDA
    """
    drawing = Drawing(ancho, alto)
    
    # Fondo de césped
    drawing.add(Rect(0, 0, ancho, alto, fillColor=COLOR_VERDE_CESPED, strokeColor=colors.white, strokeWidth=2))
    
    # Línea central vertical
    drawing.add(Line(ancho/2, 0, ancho/2, alto, strokeColor=colors.white, strokeWidth=2))
    
    # Círculo central
    centro_x, centro_y = ancho/2, alto/2
    drawing.add(Circle(centro_x, centro_y, 35, fillColor=None, strokeColor=colors.white, strokeWidth=2))
    drawing.add(Circle(centro_x, centro_y, 2, fillColor=colors.white, strokeColor=colors.white))
    
    # Áreas - Lado IZQUIERDO (portero)
    drawing.add(Rect(0, alto*0.2, 60, alto*0.6, fillColor=None, strokeColor=colors.white, strokeWidth=2))
    drawing.add(Rect(0, alto*0.35, 25, alto*0.3, fillColor=None, strokeColor=colors.white, strokeWidth=2))
    
    # Áreas - Lado DERECHO
    drawing.add(Rect(ancho-60, alto*0.2, 60, alto*0.6, fillColor=None, strokeColor=colors.white, strokeWidth=2))
    drawing.add(Rect(ancho-25, alto*0.35, 25, alto*0.3, fillColor=None, strokeColor=colors.white, strokeWidth=2))
    
    # Puntos de penalti
    drawing.add(Circle(40, centro_y, 2, fillColor=colors.white, strokeColor=colors.white))
    drawing.add(Circle(ancho-40, centro_y, 2, fillColor=colors.white, strokeColor=colors.white))
    
    # Posicionar jugadores
    if jugadores:
        for jugador in jugadores:
            x = jugador.get('x', 0.5) * ancho
            y = jugador.get('y', 0.5) * alto
            nivel = jugador.get('nivel', 'normal')
            numero = jugador.get('numero', '')
            
            # Color según nivel
            if nivel == 'peligroso':
                color_jugador = COLOR_ROJO_PELIGRO
            elif nivel == 'debil':
                color_jugador = COLOR_VERDE_DEBIL
            else:
                color_jugador = COLOR_AZUL_NORMAL
            
            # Círculo del jugador
            drawing.add(Circle(x, y, 13, fillColor=color_jugador, strokeColor=colors.white, strokeWidth=2.5))
            
            # Número del jugador
            if numero:
                drawing.add(String(x, y-3.5, str(numero), fontSize=9, fillColor=colors.white, 
                                 textAnchor='middle', fontName='Helvetica-Bold'))
    
    return drawing

def generar_informe_pdf(datos, nombre_archivo):
    """
    Genera el PDF completo del informe EN UNA SOLA PÁGINA
    """
    doc = SimpleDocTemplate(nombre_archivo, pagesize=A4,
                           topMargin=0.8*cm, bottomMargin=0.8*cm,
                           leftMargin=1.2*cm, rightMargin=1.2*cm)
    
    story = []
    ancho_pagina = A4[0] - 2.4*cm
    
    # Estilos
    styles = getSampleStyleSheet()
    
    style_titulo_principal = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=COLOR_NEGRO,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    style_subtitulo_header = ParagraphStyle(
        'SubtituloHeader',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=COLOR_VERDE,
        spaceAfter=2,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    style_subtitulo = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=9,
        textColor=colors.white,
        spaceAfter=3,
        fontName='Helvetica-Bold',
        backColor=COLOR_VERDE,
        borderPadding=3,
        alignment=TA_LEFT,
        leftIndent=5
    )
    
    style_texto = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=7.5,
        textColor=COLOR_GRIS_OSCURO,
        alignment=TA_JUSTIFY,
        spaceAfter=3,
        leading=9
    )
    
    style_texto_small = ParagraphStyle(
        'CustomBodySmall',
        parent=styles['BodyText'],
        fontSize=7,
        textColor=COLOR_GRIS_OSCURO,
        alignment=TA_JUSTIFY,
        spaceAfter=2,
        leading=8
    )
    
    # ============================================
    # HEADER CON LOGO Y TÍTULO
    # ============================================
    
    logo = obtener_logo()
    
    if logo:
        header_data = [
            [logo, Paragraph('<b>CLUB ATLÉTICO CENTRAL</b><br/><font size=9>Análisis de Equipo Rival</font>', style_titulo_principal)]
        ]
        
        header_table = Table(header_data, colWidths=[2*cm, ancho_pagina-2*cm])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ]))
        story.append(header_table)
    else:
        story.append(Paragraph('<b>CLUB ATLÉTICO CENTRAL</b>', style_titulo_principal))
        story.append(Paragraph('Análisis de Equipo Rival', style_subtitulo_header))
    
    story.append(Spacer(1, 0.3*cm))
    
    # ============================================
    # FICHA DEL EQUIPO
    # ============================================
    
    ficha_data = [
        [Paragraph('<b>Equipo Rival:</b>', style_texto), 
         Paragraph(datos.get('nombre_rival', 'N/A'), style_texto),
         Paragraph('<b>Jornada:</b>', style_texto),
         Paragraph(datos.get('jornada', 'N/A'), style_texto)],
        [Paragraph('<b>Sistema:</b>', style_texto),
         Paragraph(datos.get('sistema', 'N/A'), style_texto),
         Paragraph('<b>Posición:</b>', style_texto),
         Paragraph(datos.get('posicion', 'N/A'), style_texto)],
        [Paragraph('<b>Racha:</b>', style_texto),
         Paragraph(datos.get('racha', 'N/A'), style_texto),
         '', '']
    ]
    
    ficha_table = Table(ficha_data, colWidths=[ancho_pagina*0.22, ancho_pagina*0.28, 
                                                ancho_pagina*0.22, ancho_pagina*0.28])
    ficha_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_GRIS_FONDO),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_GRIS_CLARO),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_GRIS_OSCURO),
    ]))
    
    story.append(ficha_table)
    story.append(Spacer(1, 0.25*cm))
    
    # ============================================
    # CAMPO + LEYENDA
    # ============================================
    
    jugadores = datos.get('jugadores', [])
    campo = crear_campo_futbol_horizontal(jugadores, datos.get('sistema', '4-4-2'))
    
    leyenda_data = [[
        Paragraph('<font color="#EF4444">●</font> Peligroso', style_texto_small),
        Paragraph('<font color="#3B82F6">●</font> Normal', style_texto_small),
        Paragraph('<font color="#86EFAC">●</font> Débil', style_texto_small)
    ]]
    
    leyenda_table = Table(leyenda_data, colWidths=[ancho_pagina*0.33]*3)
    leyenda_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    campo_leyenda_data = [
        [campo],
        [leyenda_table]
    ]
    
    campo_completo = Table(campo_leyenda_data, colWidths=[ancho_pagina])
    campo_completo.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(campo_completo)
    story.append(Spacer(1, 0.2*cm))
    
    # ============================================
    # BAJAS
    # ============================================
    
    if datos.get('bajas'):
        bajas_data = [[Paragraph('⚠ <b>BAJAS:</b> ' + datos['bajas'], style_texto_small)]]
        bajas_table = Table(bajas_data, colWidths=[ancho_pagina])
        bajas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_AMARILLO),
            ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_NEGRO),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(bajas_table)
        story.append(Spacer(1, 0.2*cm))
    
    # ============================================
    # ANÁLISIS TÁCTICO
    # ============================================
    
    analisis_data = [
        [Paragraph('<b>ATAQUE ORGANIZADO</b>', style_subtitulo), 
         Paragraph('<b>DEFENSA ORGANIZADA</b>', style_subtitulo)],
        [Paragraph(datos.get('ataque_organizado', 'N/A'), style_texto_small),
         Paragraph(datos.get('defensa_organizada', 'N/A'), style_texto_small)],
        [Paragraph('<b>TRANSICIÓN DEF→ATQ</b>', style_subtitulo),
         Paragraph('<b>TRANSICIÓN ATQ→DEF</b>', style_subtitulo)],
        [Paragraph(datos.get('transicion_def_atq', 'N/A'), style_texto_small),
         Paragraph(datos.get('transicion_atq_def', 'N/A'), style_texto_small)],
    ]
    
    analisis_table = Table(analisis_data, colWidths=[ancho_pagina*0.5]*2)
    analisis_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, 1), COLOR_GRIS_FONDO),
        ('BACKGROUND', (0, 3), (-1, 3), COLOR_GRIS_FONDO),
    ]))
    
    story.append(analisis_table)
    story.append(Spacer(1, 0.2*cm))
    
    # ============================================
    # ABP
    # ============================================
    
    story.append(Paragraph('<b>ACCIONES A BALÓN PARADO (ABP)</b>', style_subtitulo))
    abp_data = [[Paragraph(datos.get('abp', 'N/A'), style_texto_small)]]
    abp_table = Table(abp_data, colWidths=[ancho_pagina])
    abp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_GRIS_FONDO),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(abp_table)
    story.append(Spacer(1, 0.2*cm))
    
    # ============================================
    # ANÁLISIS INDIVIDUAL
    # ============================================
    
    story.append(Paragraph('<b>ANÁLISIS INDIVIDUAL DE JUGADORES</b>', style_subtitulo))
    jugadores_data = [[Paragraph(datos.get('analisis_jugadores', 'N/A'), style_texto_small)]]
    jugadores_table = Table(jugadores_data, colWidths=[ancho_pagina])
    jugadores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_GRIS_FONDO),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(jugadores_table)
    
    # Generar PDF
    doc.build(story)
    print(f"✅ Informe generado exitosamente: {nombre_archivo}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            datos = json.load(f)
        nombre_archivo = sys.argv[2] if len(sys.argv) > 2 else 'informe_rival.pdf'
        generar_informe_pdf(datos, nombre_archivo)
    else:
        print("Uso: python generar_informe.py <archivo_datos.json> [nombre_salida.pdf]")
