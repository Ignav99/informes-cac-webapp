#!/usr/bin/env python3
"""
Generador de Informes de Partido v2.0
Club Atlético Central

Genera PDFs visuales y compactos con análisis por fases del juego
Máximo 2 páginas, con mini-campos visuales y estructura de bullets
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from reportlab.graphics import renderPDF
from datetime import datetime
import os


class MiniCampo:
    """Clase para dibujar mini campos de fútbol visuales"""

    @staticmethod
    def crear_campo_horizontal(width=4*cm, height=2.5*cm):
        """Crea un mini campo horizontal simple"""
        d = Drawing(width, height)

        # Color de fondo (verde césped)
        d.add(Rect(0, 0, width, height,
                   fillColor=colors.HexColor('#4ADE80'),
                   strokeColor=colors.HexColor('#16A34A'),
                   strokeWidth=1))

        # Línea central
        d.add(Line(width/2, 0, width/2, height,
                   strokeColor=colors.white, strokeWidth=1))

        # Círculo central
        d.add(Circle(width/2, height/2, height/6,
                     strokeColor=colors.white, strokeWidth=1, fillColor=None))

        # Áreas (simplificadas)
        area_width = width * 0.15
        area_height = height * 0.6

        # Área izquierda
        d.add(Rect(0, (height - area_height)/2, area_width, area_height,
                   strokeColor=colors.white, strokeWidth=1, fillColor=None))

        # Área derecha
        d.add(Rect(width - area_width, (height - area_height)/2, area_width, area_height,
                   strokeColor=colors.white, strokeWidth=1, fillColor=None))

        return d


def generar_informe_v2_pdf(datos, output_path):
    """
    Genera un PDF visual y compacto con análisis por fases del juego

    Args:
        datos: Diccionario con todos los datos del formulario v2
        output_path: Ruta donde guardar el PDF
    """

    # Configuración del documento
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    story = []
    ancho_pagina = A4[0] - 4*cm

    # Estilos
    styles = getSampleStyleSheet()

    style_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    style_subtitulo = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.white,
        spaceAfter=4,
        spaceBefore=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    style_fase = ParagraphStyle(
        'FaseTitle',
        parent=styles['Heading3'],
        fontSize=9,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=3,
        fontName='Helvetica-Bold'
    )

    style_texto = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=8,
        textColor=colors.HexColor('#374151'),
        spaceAfter=2,
        leading=10
    )

    style_bullet = ParagraphStyle(
        'BulletStyle',
        parent=styles['BodyText'],
        fontSize=7.5,
        textColor=colors.HexColor('#374151'),
        leftIndent=10,
        spaceAfter=1,
        leading=9
    )

    # ============================================
    # PÁGINA 1: HEADER + ATAQUE + DEFENSA
    # ============================================

    # --- HEADER ---
    story.append(Paragraph('<b>INFORME DE PARTIDO</b>', style_titulo))
    story.append(Paragraph(f'Club Atlético Central · {datos.get("nombre_rival", "Rival").upper()}',
                          ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=10,
                                       textColor=colors.HexColor('#6B7280'), alignment=TA_CENTER)))
    story.append(Spacer(1, 0.3*cm))

    # Ficha técnica compacta
    sistema = datos.get('sistema', 'N/A')
    jornada = datos.get('jornada', 'N/A')
    posicion = datos.get('posicion', 'N/A')
    racha = datos.get('racha', 'N/A')
    gf = datos.get('goles_favor', '0')
    gc = datos.get('goles_contra', '0')

    ficha_data = [
        [Paragraph('<b>Jornada:</b>', style_texto), Paragraph(str(jornada), style_texto),
         Paragraph('<b>Sistema:</b>', style_texto), Paragraph(sistema, style_texto),
         Paragraph('<b>Posición:</b>', style_texto), Paragraph(str(posicion), style_texto)],
        [Paragraph('<b>Racha:</b>', style_texto), Paragraph(racha, style_texto),
         Paragraph('<b>Goles:</b>', style_texto), Paragraph(f'{gf} GF / {gc} GC', style_texto),
         '', '']
    ]

    ficha_table = Table(ficha_data, colWidths=[ancho_pagina*0.15, ancho_pagina*0.18,
                                                ancho_pagina*0.15, ancho_pagina*0.18,
                                                ancho_pagina*0.15, ancho_pagina*0.18])
    ficha_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(ficha_table)
    story.append(Spacer(1, 0.4*cm))

    # --- SECCIÓN ATAQUE ---
    story.append(Table([[Paragraph('⚔️ ATAQUE ORGANIZADO', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#DC2626')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.2*cm))

    # Crear tabla 3 columnas para las 3 fases del ataque
    ataque = datos.get('ataque', {})

    def crear_fase_ataque(fase_data, titulo):
        """Crea el contenido de una fase de ataque"""
        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_fase))

        # Mini campo
        campo = MiniCampo.crear_campo_horizontal(width=5*cm, height=2.2*cm)
        contenido.append(campo)
        contenido.append(Spacer(1, 0.1*cm))

        # Datos de la fase
        if fase_data:
            if fase_data.get('estructura'):
                contenido.append(Paragraph(f'<b>Estructura:</b> {fase_data["estructura"]}', style_bullet))
            if fase_data.get('triangulos'):
                contenido.append(Paragraph(f'<b>Triángulos:</b> {fase_data["triangulos"]}', style_bullet))
            if fase_data.get('jugadores_clave'):
                contenido.append(Paragraph(f'<b>Jugadores clave:</b> {fase_data["jugadores_clave"]}', style_bullet))
            if fase_data.get('zonas_activas'):
                contenido.append(Paragraph(f'<b>Zonas:</b> {fase_data["zonas_activas"]}', style_bullet))
            if fase_data.get('como_finalizan'):
                contenido.append(Paragraph(f'<b>Finalizan:</b> {fase_data["como_finalizan"]}', style_bullet))
            if fase_data.get('jugadores_area'):
                contenido.append(Paragraph(f'<b>En área:</b> {fase_data["jugadores_area"]}', style_bullet))

            # Patrones
            patrones = fase_data.get('patrones', [])
            if patrones:
                contenido.append(Paragraph('<b>Patrones:</b>', style_bullet))
                for patron in patrones[:2]:  # Max 2 patrones por espacio
                    contenido.append(Paragraph(f'• {patron}', style_bullet))

            # Debilidad
            if fase_data.get('debilidad'):
                contenido.append(Paragraph(f'<b>⚠️ Debilidad:</b> {fase_data["debilidad"]}', style_bullet))

        return contenido

    # Crear contenido de las 3 fases
    vs_alto = ataque.get('vs_bloque_alto', {})
    vs_medio = ataque.get('vs_bloque_medio', {})
    vs_bajo = ataque.get('vs_bloque_bajo', {})

    # Construir celdas (cada celda es una lista de flowables)
    ataque_data = [[
        crear_fase_ataque(vs_alto, 'VS BLOQUE ALTO'),
        crear_fase_ataque(vs_medio, 'VS BLOQUE MEDIO'),
        crear_fase_ataque(vs_bajo, 'VS BLOQUE BAJO')
    ]]

    # Para ReportLab, necesitamos convertir las listas de flowables en una tabla
    # Usaremos Paragraphs con formato especial en su lugar

    # Alternativa: Crear tabla de texto con mini-campos embebidos
    col_width = ancho_pagina / 3

    def fase_a_parrafo(fase_data, titulo):
        """Convierte una fase en un párrafo con bullets"""
        texto = f'<b>{titulo}</b><br/>'

        if fase_data:
            if fase_data.get('estructura'):
                texto += f'<b>Estructura:</b> {fase_data["estructura"]}<br/>'
            if fase_data.get('triangulos'):
                texto += f'<b>Triángulos:</b> {fase_data["triangulos"]}<br/>'
            if fase_data.get('jugadores_clave'):
                texto += f'<b>Jugadores:</b> {fase_data["jugadores_clave"]}<br/>'
            if fase_data.get('zonas_activas'):
                texto += f'<b>Zonas:</b> {fase_data["zonas_activas"]}<br/>'
            if fase_data.get('como_finalizan'):
                texto += f'<b>Finalizan:</b> {fase_data["como_finalizan"]}<br/>'
            if fase_data.get('jugadores_area'):
                texto += f'<b>En área:</b> {fase_data["jugadores_area"]}<br/>'

            patrones = fase_data.get('patrones', [])
            if patrones:
                texto += '<b>Patrones:</b><br/>'
                for patron in patrones[:2]:
                    texto += f'• {patron}<br/>'

            if fase_data.get('debilidad'):
                texto += f'<b>⚠️ Debilidad:</b> {fase_data["debilidad"]}<br/>'

        return Paragraph(texto, style_bullet)

    ataque_row = [
        fase_a_parrafo(vs_alto, 'VS BLOQUE ALTO'),
        fase_a_parrafo(vs_medio, 'VS BLOQUE MEDIO'),
        fase_a_parrafo(vs_bajo, 'VS BLOQUE BAJO')
    ]

    ataque_table = Table([ataque_row], colWidths=[col_width]*3)
    ataque_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEE2E2')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DC2626')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ataque_table)
    story.append(Spacer(1, 0.3*cm))

    # --- SECCIÓN DEFENSA ---
    story.append(Table([[Paragraph('🛡️ DEFENSA ORGANIZADA', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563EB')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.2*cm))

    # 3 fases de defensa
    defensa = datos.get('defensa', {})
    pressing = defensa.get('pressing_alto', {})
    bloque_medio = defensa.get('bloque_medio', {})
    bloque_bajo = defensa.get('bloque_bajo', {})

    def fase_defensa_a_parrafo(fase_data, titulo):
        """Convierte una fase defensiva en un párrafo"""
        texto = f'<b>{titulo}</b><br/>'

        if fase_data:
            if fase_data.get('estructura'):
                texto += f'<b>Estructura:</b> {fase_data["estructura"]}<br/>'
            if fase_data.get('gatillos'):
                texto += f'<b>Gatillos:</b> {fase_data["gatillos"]}<br/>'
            if fase_data.get('compactacion'):
                texto += f'<b>Compactación:</b> {fase_data["compactacion"]}<br/>'
            if fase_data.get('coberturas'):
                texto += f'<b>Coberturas:</b> {fase_data["coberturas"]}<br/>'
            if fase_data.get('organizacion'):
                texto += f'<b>Organización:</b> {fase_data["organizacion"]}<br/>'
            if fase_data.get('marcajes'):
                texto += f'<b>Marcajes:</b> {fase_data["marcajes"]}<br/>'

            patrones = fase_data.get('patrones', [])
            if patrones:
                texto += '<b>Patrones:</b><br/>'
                for patron in patrones[:2]:
                    texto += f'• {patron}<br/>'

            if fase_data.get('fortaleza'):
                texto += f'<b>💪 Fortaleza:</b> {fase_data["fortaleza"]}<br/>'
            if fase_data.get('debilidad'):
                texto += f'<b>⚠️ Debilidad:</b> {fase_data["debilidad"]}<br/>'

        return Paragraph(texto, style_bullet)

    defensa_row = [
        fase_defensa_a_parrafo(pressing, 'PRESSING ALTO'),
        fase_defensa_a_parrafo(bloque_medio, 'BLOQUE MEDIO'),
        fase_defensa_a_parrafo(bloque_bajo, 'BLOQUE BAJO')
    ]

    defensa_table = Table([defensa_row], colWidths=[col_width]*3)
    defensa_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#DBEAFE')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2563EB')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(defensa_table)

    # ============================================
    # PÁGINA 2: TRANSICIONES + ABP + JUGADORES
    # ============================================

    story.append(PageBreak())

    # --- TRANSICIONES ---
    story.append(Table([[Paragraph('⚡ TRANSICIONES', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.2*cm))

    transiciones = datos.get('transiciones', {})
    def_atq = transiciones.get('def_atq', {})
    atq_def = transiciones.get('atq_def', {})

    def transicion_a_parrafo(fase_data, titulo):
        """Convierte una transición en un párrafo"""
        texto = f'<b>{titulo}</b><br/>'

        if fase_data:
            if fase_data.get('velocidad'):
                texto += f'<b>Velocidad:</b> {fase_data["velocidad"]}<br/>'
            if fase_data.get('jugadores_clave'):
                texto += f'<b>Jugadores clave:</b> {fase_data["jugadores_clave"]}<br/>'
            if fase_data.get('equilibrios'):
                texto += f'<b>Equilibrios:</b> {fase_data["equilibrios"]}<br/>'
            if fase_data.get('repliegue'):
                texto += f'<b>Repliegue:</b> {fase_data["repliegue"]}<br/>'

            patrones = fase_data.get('patrones', [])
            if patrones:
                texto += '<b>Patrones:</b><br/>'
                for patron in patrones[:2]:
                    texto += f'• {patron}<br/>'

            if fase_data.get('como_cortar'):
                texto += f'<b>✂️ Cómo cortar:</b> {fase_data["como_cortar"]}<br/>'
            if fase_data.get('desbalance'):
                texto += f'<b>⚠️ Desbalance:</b> {fase_data["desbalance"]}<br/>'

        return Paragraph(texto, style_bullet)

    trans_row = [
        transicion_a_parrafo(def_atq, 'DEF → ATQ'),
        transicion_a_parrafo(atq_def, 'ATQ → DEF')
    ]

    trans_table = Table([trans_row], colWidths=[ancho_pagina/2]*2)
    trans_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF3C7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F59E0B')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(trans_table)
    story.append(Spacer(1, 0.3*cm))

    # --- ABP (ACCIONES BALÓN PARADO) ---
    story.append(Table([[Paragraph('🎯 ACCIONES BALÓN PARADO', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#8B5CF6')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.2*cm))

    abp = datos.get('abp', {})

    abp_texto = ''
    if abp.get('corners_favor'):
        abp_texto += f'<b>Corners a favor:</b> {abp["corners_favor"]}<br/>'
    if abp.get('faltas_favor'):
        abp_texto += f'<b>Faltas a favor:</b> {abp["faltas_favor"]}<br/>'
    if abp.get('corners_contra'):
        abp_texto += f'<b>Corners en contra:</b> {abp["corners_contra"]}<br/>'
    if abp.get('debilidad'):
        abp_texto += f'<b>⚠️ Debilidad ABP:</b> {abp["debilidad"]}<br/>'

    if abp_texto:
        abp_table = Table([[Paragraph(abp_texto, style_bullet)]], colWidths=[ancho_pagina])
        abp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EDE9FE')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#8B5CF6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(abp_table)
        story.append(Spacer(1, 0.3*cm))

    # --- JUGADORES CLAVE ---
    story.append(Table([[Paragraph('⭐ JUGADORES CLAVE', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#059669')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.2*cm))

    jugadores = datos.get('jugadores_clave', [])

    if jugadores:
        jugadores_rows = []

        # Header
        jugadores_rows.append([
            Paragraph('<b>N°</b>', style_fase),
            Paragraph('<b>Nombre</b>', style_fase),
            Paragraph('<b>Posición</b>', style_fase),
            Paragraph('<b>Nivel</b>', style_fase),
            Paragraph('<b>Características</b>', style_fase)
        ])

        # Jugadores (máximo 3)
        for jugador in jugadores[:3]:
            numero = jugador.get('numero', '-')
            nombre = jugador.get('nombre', '-')
            posicion = jugador.get('posicion', '-')
            nivel = jugador.get('nivel', 'normal')
            caracteristicas = jugador.get('caracteristicas', '-')

            # Color según nivel
            if nivel == 'peligroso':
                nivel_color = colors.HexColor('#DC2626')
                nivel_texto = '🔴 PELIGROSO'
            elif nivel == 'importante':
                nivel_color = colors.HexColor('#F59E0B')
                nivel_texto = '🟡 IMPORTANTE'
            else:
                nivel_color = colors.HexColor('#6B7280')
                nivel_texto = '⚪ NORMAL'

            jugadores_rows.append([
                Paragraph(f'<b>{numero}</b>', style_texto),
                Paragraph(nombre, style_texto),
                Paragraph(posicion, style_texto),
                Paragraph(nivel_texto, ParagraphStyle('nivel', parent=style_texto, textColor=nivel_color)),
                Paragraph(caracteristicas, style_bullet)
            ])

        jugadores_table = Table(jugadores_rows,
                               colWidths=[ancho_pagina*0.08, ancho_pagina*0.20,
                                         ancho_pagina*0.12, ancho_pagina*0.18,
                                         ancho_pagina*0.42])
        jugadores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D1FAE5')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECFDF5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#059669')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(jugadores_table)

    # --- FOOTER ---
    story.append(Spacer(1, 0.4*cm))
    footer_text = f'<i>Informe generado el {datetime.now().strftime("%d/%m/%Y %H:%M")} · Club Atlético Central</i>'
    story.append(Paragraph(footer_text,
                          ParagraphStyle('footer', parent=styles['Normal'],
                                       fontSize=7, textColor=colors.HexColor('#9CA3AF'),
                                       alignment=TA_CENTER)))

    # Generar PDF
    doc.build(story)
    print(f"✅ PDF v2.0 generado: {output_path}")


if __name__ == "__main__":
    # Test con datos de ejemplo
    datos_test = {
        'nombre_rival': 'FC Barcelona',
        'jornada': '15',
        'sistema': '4-3-3',
        'posicion': '2',
        'racha': 'VVVDE',
        'goles_favor': '35',
        'goles_contra': '12',
        'ataque': {
            'vs_bloque_alto': {
                'estructura': '4+1 (Portero + 4 defensas + pivote)',
                'triangulos': '1-4-6 (Portero-DC-Pivote)',
                'patrones': ['Pase corto entre centrales', 'Salida por bandas'],
                'debilidad': 'Poca velocidad en salida'
            },
            'vs_bloque_medio': {
                'jugadores_clave': '10 y 8 (centrocampistas)',
                'zonas_activas': 'Bandas con carrileros',
                'patrones': ['Cambios de orientación', 'Juego interior'],
                'debilidad': 'Dependen del 10'
            },
            'vs_bloque_bajo': {
                'como_finalizan': 'Centros laterales',
                'jugadores_area': '9 y 7',
                'patrones': ['Centros al primer palo', 'Remates de segunda jugada'],
                'debilidad': 'Poco juego aéreo'
            }
        },
        'defensa': {
            'pressing_alto': {
                'estructura': '4-4-2 en presión',
                'gatillos': 'Pase al central',
                'patrones': ['Presión en banda', 'Cierre de líneas de pase'],
                'fortaleza': 'Muy agresivos'
            },
            'bloque_medio': {
                'compactacion': '25-30 metros entre líneas',
                'coberturas': 'Coberturas laterales buenas',
                'patrones': ['Compactos en centro', 'Vigilancia de espacios'],
                'fortaleza': 'Bien organizados'
            },
            'bloque_bajo': {
                'organizacion': 'Dos líneas de 4',
                'marcajes': 'Zona pura',
                'patrones': ['Defensa en bloque', 'Salidas rápidas'],
                'debilidad': 'Dejan espacios entre líneas'
            }
        },
        'transiciones': {
            'def_atq': {
                'velocidad': 'Muy rápida',
                'jugadores_clave': '10 y extremos',
                'patrones': ['Pase largo a bandas', 'Verticalidad'],
                'como_cortar': 'Falta táctica rápida'
            },
            'atq_def': {
                'equilibrios': '2 centrales + pivote',
                'repliegue': 'Repliegue ordenado',
                'patrones': ['Presión al portador', 'Retrasar líneas'],
                'desbalance': 'Laterales adelantados'
            }
        },
        'abp': {
            'corners_favor': 'Estructura en zona, rematadores: 4, 5, 9',
            'faltas_favor': 'Ejecutor: 10, estrategias directas',
            'corners_contra': 'Defensa en zona mixta',
            'debilidad': 'Flojos en defensa de corners'
        },
        'jugadores_clave': [
            {
                'numero': '10',
                'nombre': 'Pedri',
                'posicion': 'MC',
                'nivel': 'peligroso',
                'caracteristicas': 'Organizador del juego, gran visión, difícil de presionar'
            },
            {
                'numero': '9',
                'nombre': 'Lewandowski',
                'posicion': 'DC',
                'nivel': 'peligroso',
                'caracteristicas': 'Goleador nato, movimientos en área, remate de cabeza'
            },
            {
                'numero': '8',
                'nombre': 'De Jong',
                'posicion': 'MC',
                'nivel': 'importante',
                'caracteristicas': 'Recuperador, buena conducción, apoya en construcción'
            }
        ]
    }

    generar_informe_v2_pdf(datos_test, 'test_informe_v2.pdf')
    print("✅ Test completado. Revisa test_informe_v2.pdf")
