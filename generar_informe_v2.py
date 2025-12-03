#!/usr/bin/env python3
"""
Generador de Informes de Partido v2.0 PROFESIONAL
Club Atlético Central

PDF ultra-visual con:
- Escudo vectorial del club
- Campos tácticos con jugadores, flechas y zonas
- Diseño profesional compacto
- Mapas de juego para cada fase
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon, Wedge
from reportlab.graphics import renderPDF
from reportlab.graphics.widgets.markers import makeMarker
from datetime import datetime
import os
import math


# =============================================================================
# COLORES CORPORATIVOS
# =============================================================================
COLORES = {
    'verde_principal': colors.HexColor('#10B981'),
    'verde_oscuro': colors.HexColor('#059669'),
    'verde_claro': colors.HexColor('#D1FAE5'),
    'rojo': colors.HexColor('#DC2626'),
    'rojo_claro': colors.HexColor('#FEE2E2'),
    'azul': colors.HexColor('#2563EB'),
    'azul_claro': colors.HexColor('#DBEAFE'),
    'naranja': colors.HexColor('#F59E0B'),
    'naranja_claro': colors.HexColor('#FEF3C7'),
    'morado': colors.HexColor('#8B5CF6'),
    'morado_claro': colors.HexColor('#EDE9FE'),
    'gris_oscuro': colors.HexColor('#1F2937'),
    'gris': colors.HexColor('#6B7280'),
    'gris_claro': colors.HexColor('#F3F4F6'),
    'blanco': colors.white,
    'campo_verde': colors.HexColor('#22C55E'),
    'campo_verde_oscuro': colors.HexColor('#16A34A'),
    'campo_linea': colors.HexColor('#FFFFFF'),
}


# =============================================================================
# ESCUDO CAC VECTORIAL
# =============================================================================
class EscudoCAC:
    """Dibuja el escudo del Club Atlético Central"""

    @staticmethod
    def crear_escudo(width=60, height=70):
        """Crea el escudo vectorial del club"""
        d = Drawing(width, height)

        # Fondo del escudo (forma de escudo clásico)
        # Base más ancha arriba, punta abajo
        cx = width / 2

        # Forma de escudo usando polígono
        puntos_escudo = [
            5, height - 5,           # Esquina superior izquierda
            width - 5, height - 5,   # Esquina superior derecha
            width - 5, height * 0.4, # Lado derecho
            cx, 5,                   # Punta inferior
            5, height * 0.4,         # Lado izquierdo
        ]

        # Fondo verde del escudo
        d.add(Polygon(puntos_escudo,
                     fillColor=COLORES['verde_principal'],
                     strokeColor=COLORES['verde_oscuro'],
                     strokeWidth=2))

        # Banda diagonal blanca
        d.add(Polygon([
            10, height - 10,
            25, height - 10,
            width - 10, height * 0.35,
            width - 25, height * 0.35,
        ], fillColor=colors.white, strokeColor=None))

        # Texto "CAC" en el centro
        d.add(String(cx, height * 0.55, 'C',
                    fontSize=16, fontName='Helvetica-Bold',
                    fillColor=colors.white, textAnchor='middle'))
        d.add(String(cx, height * 0.38, 'A',
                    fontSize=12, fontName='Helvetica-Bold',
                    fillColor=colors.white, textAnchor='middle'))
        d.add(String(cx, height * 0.23, 'C',
                    fontSize=10, fontName='Helvetica-Bold',
                    fillColor=colors.white, textAnchor='middle'))

        # Estrellas decorativas
        d.add(String(15, height - 20, '★',
                    fontSize=8, fillColor=colors.HexColor('#FFD700'),
                    textAnchor='middle'))
        d.add(String(width - 15, height - 20, '★',
                    fontSize=8, fillColor=colors.HexColor('#FFD700'),
                    textAnchor='middle'))

        return d


# =============================================================================
# CAMPO TÁCTICO VISUAL
# =============================================================================
class CampoTactico:
    """Dibuja campos de fútbol profesionales con jugadores, flechas y zonas"""

    @staticmethod
    def crear_campo_base(width, height, orientacion='horizontal'):
        """Crea un campo de fútbol base"""
        d = Drawing(width, height)

        # Césped con gradiente simulado (franjas)
        num_franjas = 8
        franja_width = width / num_franjas if orientacion == 'horizontal' else height / num_franjas

        for i in range(num_franjas):
            color = COLORES['campo_verde'] if i % 2 == 0 else COLORES['campo_verde_oscuro']
            if orientacion == 'horizontal':
                d.add(Rect(i * franja_width, 0, franja_width, height,
                          fillColor=color, strokeColor=None))
            else:
                d.add(Rect(0, i * franja_width, width, franja_width,
                          fillColor=color, strokeColor=None))

        # Borde del campo
        d.add(Rect(2, 2, width - 4, height - 4,
                  fillColor=None, strokeColor=colors.white, strokeWidth=2))

        if orientacion == 'horizontal':
            # Línea central vertical
            d.add(Line(width/2, 2, width/2, height - 2,
                      strokeColor=colors.white, strokeWidth=1.5))

            # Círculo central
            d.add(Circle(width/2, height/2, height/5,
                        strokeColor=colors.white, strokeWidth=1.5, fillColor=None))
            d.add(Circle(width/2, height/2, 3,
                        fillColor=colors.white, strokeColor=None))

            # Área izquierda (portería local)
            area_w = width * 0.16
            area_h = height * 0.6
            d.add(Rect(2, (height - area_h)/2, area_w, area_h,
                      fillColor=None, strokeColor=colors.white, strokeWidth=1.5))
            # Área pequeña
            area_p_w = width * 0.06
            area_p_h = height * 0.3
            d.add(Rect(2, (height - area_p_h)/2, area_p_w, area_p_h,
                      fillColor=None, strokeColor=colors.white, strokeWidth=1.5))

            # Área derecha (portería rival)
            d.add(Rect(width - 2 - area_w, (height - area_h)/2, area_w, area_h,
                      fillColor=None, strokeColor=colors.white, strokeWidth=1.5))
            d.add(Rect(width - 2 - area_p_w, (height - area_p_h)/2, area_p_w, area_p_h,
                      fillColor=None, strokeColor=colors.white, strokeWidth=1.5))

            # Puntos de penalti
            d.add(Circle(width * 0.12, height/2, 2,
                        fillColor=colors.white, strokeColor=None))
            d.add(Circle(width * 0.88, height/2, 2,
                        fillColor=colors.white, strokeColor=None))
        else:
            # Orientación vertical
            # Línea central horizontal
            d.add(Line(2, height/2, width - 2, height/2,
                      strokeColor=colors.white, strokeWidth=1.5))

            # Círculo central
            d.add(Circle(width/2, height/2, width/5,
                        strokeColor=colors.white, strokeWidth=1.5, fillColor=None))
            d.add(Circle(width/2, height/2, 3,
                        fillColor=colors.white, strokeColor=None))

            # Áreas
            area_h = height * 0.16
            area_w = width * 0.6
            d.add(Rect((width - area_w)/2, 2, area_w, area_h,
                      fillColor=None, strokeColor=colors.white, strokeWidth=1.5))
            d.add(Rect((width - area_w)/2, height - 2 - area_h, area_w, area_h,
                      fillColor=None, strokeColor=colors.white, strokeWidth=1.5))

        return d

    @staticmethod
    def agregar_jugador(d, x, y, numero='', color=colors.red, tamano=12, es_rival=True):
        """Agrega un jugador al campo"""
        # Círculo del jugador
        fill = color if es_rival else colors.HexColor('#3B82F6')
        d.add(Circle(x, y, tamano/2,
                    fillColor=fill,
                    strokeColor=colors.white,
                    strokeWidth=1.5))

        # Número del jugador
        if numero:
            d.add(String(x, y - 3, str(numero),
                        fontSize=7, fontName='Helvetica-Bold',
                        fillColor=colors.white, textAnchor='middle'))

    @staticmethod
    def agregar_flecha(d, x1, y1, x2, y2, color=colors.yellow, grosor=2, punta=True):
        """Agrega una flecha de movimiento"""
        d.add(Line(x1, y1, x2, y2,
                  strokeColor=color, strokeWidth=grosor))

        if punta:
            # Calcular ángulo para la punta de flecha
            angulo = math.atan2(y2 - y1, x2 - x1)
            tam_punta = 6

            # Puntos de la punta
            px1 = x2 - tam_punta * math.cos(angulo - 0.5)
            py1 = y2 - tam_punta * math.sin(angulo - 0.5)
            px2 = x2 - tam_punta * math.cos(angulo + 0.5)
            py2 = y2 - tam_punta * math.sin(angulo + 0.5)

            d.add(Polygon([x2, y2, px1, py1, px2, py2],
                         fillColor=color, strokeColor=None))

    @staticmethod
    def agregar_zona(d, x, y, ancho, alto, color, alpha=0.3):
        """Agrega una zona destacada"""
        zona_color = colors.Color(color.red, color.green, color.blue, alpha=alpha)
        d.add(Rect(x, y, ancho, alto,
                  fillColor=zona_color,
                  strokeColor=color,
                  strokeWidth=1,
                  strokeDashArray=[3, 2]))

    @staticmethod
    def crear_formacion_4_3_3(width, height, numeros=None):
        """Crea un campo con formación 4-3-3 del rival"""
        d = CampoTactico.crear_campo_base(width, height, 'horizontal')

        # Posiciones para 4-3-3 (lado derecho = rival atacando hacia nuestra portería)
        posiciones = [
            (width * 0.92, height * 0.5),    # Portero
            (width * 0.78, height * 0.15),   # LD
            (width * 0.78, height * 0.38),   # DFC
            (width * 0.78, height * 0.62),   # DFC
            (width * 0.78, height * 0.85),   # LI
            (width * 0.58, height * 0.25),   # MC
            (width * 0.58, height * 0.5),    # MC (pivote)
            (width * 0.58, height * 0.75),   # MC
            (width * 0.35, height * 0.15),   # ED
            (width * 0.30, height * 0.5),    # DC
            (width * 0.35, height * 0.85),   # EI
        ]

        nums = numeros or ['1', '2', '4', '5', '3', '8', '6', '10', '7', '9', '11']

        for i, (x, y) in enumerate(posiciones):
            CampoTactico.agregar_jugador(d, x, y, nums[i] if i < len(nums) else '',
                                         colors.red, tamano=14, es_rival=True)

        return d

    @staticmethod
    def crear_campo_pressing(width, height, tipo='alto'):
        """Crea campo mostrando línea de pressing"""
        d = CampoTactico.crear_campo_base(width, height, 'horizontal')

        # Línea de pressing según tipo
        if tipo == 'alto':
            linea_x = width * 0.70
            zona_color = colors.HexColor('#DC2626')
        elif tipo == 'medio':
            linea_x = width * 0.50
            zona_color = colors.HexColor('#F59E0B')
        else:
            linea_x = width * 0.30
            zona_color = colors.HexColor('#3B82F6')

        # Zona de presión
        CampoTactico.agregar_zona(d, linea_x - 20, 5, 30, height - 10, zona_color, 0.3)

        # Línea de presión
        d.add(Line(linea_x, 5, linea_x, height - 5,
                  strokeColor=zona_color, strokeWidth=3, strokeDashArray=[8, 4]))

        # Posiciones defensivas del rival (simplificadas)
        jugadores_def = [
            (width * 0.88, height * 0.5, '1'),   # GK
            (width * 0.75, height * 0.2, '2'),   # LD
            (width * 0.75, height * 0.4, '4'),   # DFC
            (width * 0.75, height * 0.6, '5'),   # DFC
            (width * 0.75, height * 0.8, '3'),   # LI
        ]

        for x, y, num in jugadores_def:
            CampoTactico.agregar_jugador(d, x, y, num, colors.red, 12, True)

        # Flechas de pressing (nuestros jugadores presionando)
        if tipo == 'alto':
            CampoTactico.agregar_flecha(d, width * 0.55, height * 0.5,
                                        width * 0.68, height * 0.5, colors.yellow, 2)
            CampoTactico.agregar_flecha(d, width * 0.50, height * 0.25,
                                        width * 0.65, height * 0.25, colors.yellow, 2)
            CampoTactico.agregar_flecha(d, width * 0.50, height * 0.75,
                                        width * 0.65, height * 0.75, colors.yellow, 2)

        return d

    @staticmethod
    def crear_campo_transicion(width, height, tipo='def_atq'):
        """Crea campo mostrando transición"""
        d = CampoTactico.crear_campo_base(width, height, 'horizontal')

        if tipo == 'def_atq':
            # Transición defensa-ataque (contraataque)
            color_flecha = colors.HexColor('#22C55E')

            # Recuperación en zona media
            CampoTactico.agregar_zona(d, width * 0.35, height * 0.3,
                                      width * 0.15, height * 0.4,
                                      colors.HexColor('#22C55E'), 0.3)

            # Flechas de contraataque
            CampoTactico.agregar_flecha(d, width * 0.45, height * 0.5,
                                        width * 0.25, height * 0.5, color_flecha, 3)
            CampoTactico.agregar_flecha(d, width * 0.40, height * 0.3,
                                        width * 0.20, height * 0.15, color_flecha, 2)
            CampoTactico.agregar_flecha(d, width * 0.40, height * 0.7,
                                        width * 0.20, height * 0.85, color_flecha, 2)

            # Jugadores clave en transición
            CampoTactico.agregar_jugador(d, width * 0.45, height * 0.5, '10',
                                         colors.HexColor('#FBBF24'), 14, True)
            CampoTactico.agregar_jugador(d, width * 0.30, height * 0.2, '7',
                                         colors.red, 12, True)
            CampoTactico.agregar_jugador(d, width * 0.30, height * 0.8, '11',
                                         colors.red, 12, True)
        else:
            # Transición ataque-defensa (repliegue)
            color_flecha = colors.HexColor('#EF4444')

            # Zona de desorden
            CampoTactico.agregar_zona(d, width * 0.55, height * 0.2,
                                      width * 0.25, height * 0.6,
                                      colors.HexColor('#EF4444'), 0.25)

            # Flechas de repliegue
            CampoTactico.agregar_flecha(d, width * 0.30, height * 0.5,
                                        width * 0.55, height * 0.5, color_flecha, 2)
            CampoTactico.agregar_flecha(d, width * 0.25, height * 0.2,
                                        width * 0.50, height * 0.3, color_flecha, 2)
            CampoTactico.agregar_flecha(d, width * 0.25, height * 0.8,
                                        width * 0.50, height * 0.7, color_flecha, 2)

        return d

    @staticmethod
    def crear_campo_ataque(width, height, fase='alto'):
        """Crea campo mostrando fase de ataque del rival"""
        d = CampoTactico.crear_campo_base(width, height, 'horizontal')

        if fase == 'alto':
            # VS bloque alto - Salida de balón
            # Zona de salida
            CampoTactico.agregar_zona(d, width * 0.70, height * 0.25,
                                      width * 0.20, height * 0.5,
                                      COLORES['verde_principal'], 0.3)

            # Triángulos de pase
            CampoTactico.agregar_jugador(d, width * 0.88, height * 0.5, '1',
                                         colors.HexColor('#FBBF24'), 14, True)
            CampoTactico.agregar_jugador(d, width * 0.75, height * 0.35, '4',
                                         colors.red, 12, True)
            CampoTactico.agregar_jugador(d, width * 0.75, height * 0.65, '5',
                                         colors.red, 12, True)
            CampoTactico.agregar_jugador(d, width * 0.60, height * 0.5, '6',
                                         colors.HexColor('#FBBF24'), 14, True)

            # Flechas de pase
            CampoTactico.agregar_flecha(d, width * 0.85, height * 0.5,
                                        width * 0.77, height * 0.38, colors.white, 1.5)
            CampoTactico.agregar_flecha(d, width * 0.73, height * 0.37,
                                        width * 0.63, height * 0.48, colors.white, 1.5)
            CampoTactico.agregar_flecha(d, width * 0.73, height * 0.63,
                                        width * 0.63, height * 0.52, colors.white, 1.5)

        elif fase == 'medio':
            # VS bloque medio - Progresión
            CampoTactico.agregar_zona(d, width * 0.40, height * 0.15,
                                      width * 0.25, height * 0.70,
                                      COLORES['naranja'], 0.25)

            # Jugadores en zona de creación
            CampoTactico.agregar_jugador(d, width * 0.55, height * 0.5, '8',
                                         colors.HexColor('#FBBF24'), 14, True)
            CampoTactico.agregar_jugador(d, width * 0.50, height * 0.25, '10',
                                         colors.HexColor('#FBBF24'), 14, True)
            CampoTactico.agregar_jugador(d, width * 0.40, height * 0.15, '7',
                                         colors.red, 12, True)
            CampoTactico.agregar_jugador(d, width * 0.40, height * 0.85, '11',
                                         colors.red, 12, True)

            # Flechas de progresión
            CampoTactico.agregar_flecha(d, width * 0.52, height * 0.5,
                                        width * 0.35, height * 0.5, colors.yellow, 2)
            CampoTactico.agregar_flecha(d, width * 0.48, height * 0.27,
                                        width * 0.38, height * 0.20, colors.yellow, 2)

        else:
            # VS bloque bajo - Finalización
            CampoTactico.agregar_zona(d, width * 0.08, height * 0.20,
                                      width * 0.22, height * 0.60,
                                      COLORES['rojo'], 0.3)

            # Jugadores en área
            CampoTactico.agregar_jugador(d, width * 0.22, height * 0.5, '9',
                                         colors.HexColor('#EF4444'), 16, True)
            CampoTactico.agregar_jugador(d, width * 0.25, height * 0.30, '7',
                                         colors.red, 12, True)
            CampoTactico.agregar_jugador(d, width * 0.25, height * 0.70, '11',
                                         colors.red, 12, True)

            # Centro lateral
            CampoTactico.agregar_flecha(d, width * 0.35, height * 0.10,
                                        width * 0.22, height * 0.40, colors.yellow, 2)
            CampoTactico.agregar_flecha(d, width * 0.35, height * 0.90,
                                        width * 0.22, height * 0.60, colors.yellow, 2)

        return d


# =============================================================================
# ICONOS Y ELEMENTOS VISUALES
# =============================================================================
class Iconos:
    """Iconos visuales para el PDF"""

    @staticmethod
    def crear_icono_nivel(nivel, size=20):
        """Crea un icono visual del nivel del jugador"""
        d = Drawing(size, size)

        if nivel == 'peligroso':
            # Triángulo de peligro rojo
            d.add(Polygon([size/2, size-2, 2, 2, size-2, 2],
                         fillColor=colors.HexColor('#DC2626'),
                         strokeColor=colors.white, strokeWidth=1))
            d.add(String(size/2, 6, '!',
                        fontSize=10, fontName='Helvetica-Bold',
                        fillColor=colors.white, textAnchor='middle'))
        elif nivel == 'importante':
            # Estrella amarilla
            d.add(Circle(size/2, size/2, size/2-1,
                        fillColor=colors.HexColor('#F59E0B'),
                        strokeColor=colors.white, strokeWidth=1))
            d.add(String(size/2, size/2-4, '★',
                        fontSize=12, fillColor=colors.white, textAnchor='middle'))
        else:
            # Círculo gris
            d.add(Circle(size/2, size/2, size/2-1,
                        fillColor=colors.HexColor('#9CA3AF'),
                        strokeColor=colors.white, strokeWidth=1))

        return d


# =============================================================================
# GENERADOR PDF PRINCIPAL
# =============================================================================
def generar_informe_v2_pdf(datos, output_path):
    """
    Genera un PDF profesional ultra-visual con análisis táctico

    Args:
        datos: Diccionario con todos los datos del formulario v2
        output_path: Ruta donde guardar el PDF
    """

    # Configuración del documento
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=1*cm,
        bottomMargin=1*cm,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm
    )

    story = []
    ancho_pagina = A4[0] - 3*cm

    # Estilos
    styles = getSampleStyleSheet()

    style_titulo = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=COLORES['gris_oscuro'],
        spaceAfter=2,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    style_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.white,
        spaceAfter=4,
        spaceBefore=4,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    style_seccion = ParagraphStyle(
        'SeccionTitulo',
        parent=styles['Heading3'],
        fontSize=9,
        textColor=COLORES['gris_oscuro'],
        spaceAfter=2,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    )

    style_texto = ParagraphStyle(
        'TextoNormal',
        parent=styles['BodyText'],
        fontSize=7.5,
        textColor=COLORES['gris'],
        spaceAfter=1,
        leading=9,
        alignment=TA_LEFT
    )

    style_dato = ParagraphStyle(
        'Dato',
        parent=styles['BodyText'],
        fontSize=8,
        textColor=COLORES['gris_oscuro'],
        spaceAfter=1,
        leading=10
    )

    style_fortaleza = ParagraphStyle(
        'Fortaleza',
        parent=style_texto,
        fontSize=7,
        textColor=colors.HexColor('#059669'),
        leftIndent=0
    )

    style_debilidad = ParagraphStyle(
        'Debilidad',
        parent=style_texto,
        fontSize=7,
        textColor=colors.HexColor('#DC2626'),
        leftIndent=0
    )

    # ==================================================================
    # HEADER CON ESCUDO
    # ==================================================================
    escudo = EscudoCAC.crear_escudo(50, 60)

    rival = datos.get('nombre_rival', 'RIVAL').upper()
    jornada = datos.get('jornada', '-')
    fecha = datetime.now().strftime('%d/%m/%Y')

    header_data = [[
        escudo,
        [Paragraph(f'<b>INFORME TÁCTICO</b>', style_titulo),
         Paragraph(f'vs {rival}', ParagraphStyle('rival', fontSize=14,
                   textColor=COLORES['verde_principal'], alignment=TA_CENTER,
                   fontName='Helvetica-Bold')),
         Paragraph(f'Jornada {jornada} · {fecha}',
                  ParagraphStyle('fecha', fontSize=9, textColor=COLORES['gris'],
                                alignment=TA_CENTER))],
        escudo
    ]]

    header_table = Table(header_data, colWidths=[60, ancho_pagina - 120, 60])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.3*cm))

    # ==================================================================
    # FICHA TÉCNICA COMPACTA
    # ==================================================================
    sistema = datos.get('sistema', 'N/A')
    posicion = datos.get('posicion', '-')
    racha = datos.get('racha', '-')
    gf = datos.get('goles_favor', '0')
    gc = datos.get('goles_contra', '0')

    ficha_data = [[
        Paragraph(f'<b>Sistema:</b> {sistema}', style_dato),
        Paragraph(f'<b>Posición:</b> {posicion}°', style_dato),
        Paragraph(f'<b>Racha:</b> {racha}', style_dato),
        Paragraph(f'<b>Goles:</b> {gf}↑ {gc}↓', style_dato),
    ]]

    ficha_table = Table(ficha_data, colWidths=[ancho_pagina/4]*4)
    ficha_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['gris_claro']),
        ('GRID', (0, 0), (-1, -1), 1, COLORES['verde_principal']),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ficha_table)
    story.append(Spacer(1, 0.4*cm))

    # ==================================================================
    # SECCIÓN ATAQUE ORGANIZADO
    # ==================================================================
    story.append(Table([[Paragraph('⚔️  ATAQUE ORGANIZADO', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['rojo']),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 0.2*cm))

    ataque = datos.get('ataque', {})
    col_width = ancho_pagina / 3 - 2
    campo_size = (col_width - 10, 4.5*cm)

    def crear_celda_ataque(fase_data, titulo, campo):
        """Crea celda visual para fase de ataque"""
        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_seccion))
        contenido.append(Spacer(1, 2))
        contenido.append(campo)
        contenido.append(Spacer(1, 3))

        if fase_data:
            # Datos principales (compactos)
            if fase_data.get('estructura'):
                contenido.append(Paragraph(f'<b>→</b> {fase_data["estructura"][:60]}', style_texto))
            if fase_data.get('triangulos'):
                contenido.append(Paragraph(f'<b>△</b> {fase_data["triangulos"][:50]}', style_texto))
            if fase_data.get('jugadores_clave'):
                contenido.append(Paragraph(f'<b>★</b> {fase_data["jugadores_clave"][:50]}', style_texto))
            if fase_data.get('zonas_activas'):
                contenido.append(Paragraph(f'<b>◉</b> {fase_data["zonas_activas"][:50]}', style_texto))
            if fase_data.get('como_finalizan'):
                contenido.append(Paragraph(f'<b>⚽</b> {fase_data["como_finalizan"][:50]}', style_texto))

            # Patrones (máximo 2)
            patrones = fase_data.get('patrones', [])
            if patrones:
                for p in patrones[:2]:
                    if p:
                        contenido.append(Paragraph(f'• {p[:45]}', style_texto))

            # Fortaleza/Debilidad
            if fase_data.get('fortaleza'):
                contenido.append(Paragraph(f'<b>💪</b> {fase_data["fortaleza"][:40]}', style_fortaleza))
            if fase_data.get('debilidad'):
                contenido.append(Paragraph(f'<b>⚠️</b> {fase_data["debilidad"][:40]}', style_debilidad))

        return contenido

    # Crear campos tácticos para cada fase
    campo_alto = CampoTactico.crear_campo_ataque(campo_size[0], campo_size[1], 'alto')
    campo_medio = CampoTactico.crear_campo_ataque(campo_size[0], campo_size[1], 'medio')
    campo_bajo = CampoTactico.crear_campo_ataque(campo_size[0], campo_size[1], 'bajo')

    vs_alto = ataque.get('vs_bloque_alto', {})
    vs_medio = ataque.get('vs_bloque_medio', {})
    vs_bajo = ataque.get('vs_bloque_bajo', {})

    ataque_row = [
        crear_celda_ataque(vs_alto, 'VS BLOQUE ALTO', campo_alto),
        crear_celda_ataque(vs_medio, 'VS BLOQUE MEDIO', campo_medio),
        crear_celda_ataque(vs_bajo, 'VS BLOQUE BAJO', campo_bajo)
    ]

    ataque_table = Table([ataque_row], colWidths=[col_width + 1]*3)
    ataque_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['rojo_claro']),
        ('GRID', (0, 0), (-1, -1), 1, COLORES['rojo']),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ataque_table)
    story.append(Spacer(1, 0.3*cm))

    # ==================================================================
    # SECCIÓN DEFENSA ORGANIZADA
    # ==================================================================
    story.append(Table([[Paragraph('🛡️  DEFENSA ORGANIZADA', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['azul']),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 0.2*cm))

    defensa = datos.get('defensa', {})

    def crear_celda_defensa(fase_data, titulo, tipo_pressing):
        """Crea celda visual para fase defensiva"""
        campo = CampoTactico.crear_campo_pressing(campo_size[0], campo_size[1], tipo_pressing)

        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_seccion))
        contenido.append(Spacer(1, 2))
        contenido.append(campo)
        contenido.append(Spacer(1, 3))

        if fase_data:
            if fase_data.get('estructura'):
                contenido.append(Paragraph(f'<b>→</b> {fase_data["estructura"][:50]}', style_texto))
            if fase_data.get('gatillos'):
                contenido.append(Paragraph(f'<b>⚡</b> {fase_data["gatillos"][:50]}', style_texto))
            if fase_data.get('compactacion'):
                contenido.append(Paragraph(f'<b>◁▷</b> {fase_data["compactacion"][:50]}', style_texto))
            if fase_data.get('coberturas'):
                contenido.append(Paragraph(f'<b>↔</b> {fase_data["coberturas"][:50]}', style_texto))
            if fase_data.get('organizacion'):
                contenido.append(Paragraph(f'<b>▣</b> {fase_data["organizacion"][:50]}', style_texto))
            if fase_data.get('marcajes'):
                contenido.append(Paragraph(f'<b>⊗</b> {fase_data["marcajes"][:50]}', style_texto))

            patrones = fase_data.get('patrones', [])
            for p in patrones[:2]:
                if p:
                    contenido.append(Paragraph(f'• {p[:45]}', style_texto))

            if fase_data.get('fortaleza'):
                contenido.append(Paragraph(f'<b>💪</b> {fase_data["fortaleza"][:40]}', style_fortaleza))
            if fase_data.get('debilidad'):
                contenido.append(Paragraph(f'<b>⚠️</b> {fase_data["debilidad"][:40]}', style_debilidad))

        return contenido

    pressing = defensa.get('pressing_alto', {})
    bloque_medio = defensa.get('bloque_medio', {})
    bloque_bajo = defensa.get('bloque_bajo', {})

    defensa_row = [
        crear_celda_defensa(pressing, 'PRESSING ALTO', 'alto'),
        crear_celda_defensa(bloque_medio, 'BLOQUE MEDIO', 'medio'),
        crear_celda_defensa(bloque_bajo, 'BLOQUE BAJO', 'bajo')
    ]

    defensa_table = Table([defensa_row], colWidths=[col_width + 1]*3)
    defensa_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['azul_claro']),
        ('GRID', (0, 0), (-1, -1), 1, COLORES['azul']),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(defensa_table)

    # ==================================================================
    # PÁGINA 2: TRANSICIONES + ABP + JUGADORES
    # ==================================================================
    story.append(PageBreak())

    # --- TRANSICIONES ---
    story.append(Table([[Paragraph('⚡  TRANSICIONES', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['naranja']),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 0.2*cm))

    transiciones = datos.get('transiciones', {})
    campo_trans_w = ancho_pagina / 2 - 10
    campo_trans_h = 5*cm

    def crear_celda_transicion(fase_data, titulo, tipo):
        """Crea celda visual para transición"""
        campo = CampoTactico.crear_campo_transicion(campo_trans_w - 10, campo_trans_h, tipo)

        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_seccion))
        contenido.append(Spacer(1, 3))
        contenido.append(campo)
        contenido.append(Spacer(1, 4))

        if fase_data:
            if tipo == 'def_atq':
                if fase_data.get('velocidad'):
                    contenido.append(Paragraph(f'<b>⏱</b> Velocidad: {fase_data["velocidad"]}', style_texto))
                if fase_data.get('jugadores_clave'):
                    contenido.append(Paragraph(f'<b>★</b> Claves: {fase_data["jugadores_clave"]}', style_texto))
                if fase_data.get('como_cortar'):
                    contenido.append(Paragraph(f'<b>✂️</b> Cortar: {fase_data["como_cortar"]}', style_debilidad))
            else:
                if fase_data.get('equilibrios'):
                    contenido.append(Paragraph(f'<b>⚖</b> Equilibrios: {fase_data["equilibrios"]}', style_texto))
                if fase_data.get('repliegue'):
                    contenido.append(Paragraph(f'<b>↩</b> Repliegue: {fase_data["repliegue"]}', style_texto))
                if fase_data.get('desbalance'):
                    contenido.append(Paragraph(f'<b>⚠️</b> Desbalance: {fase_data["desbalance"]}', style_debilidad))

            patrones = fase_data.get('patrones', [])
            for p in patrones[:2]:
                if p:
                    contenido.append(Paragraph(f'• {p[:50]}', style_texto))

            if fase_data.get('fortaleza'):
                contenido.append(Paragraph(f'<b>💪</b> {fase_data["fortaleza"]}', style_fortaleza))

        return contenido

    def_atq = transiciones.get('def_atq', {})
    atq_def = transiciones.get('atq_def', {})

    trans_row = [
        crear_celda_transicion(def_atq, 'DEFENSA → ATAQUE', 'def_atq'),
        crear_celda_transicion(atq_def, 'ATAQUE → DEFENSA', 'atq_def')
    ]

    trans_table = Table([trans_row], colWidths=[campo_trans_w]*2)
    trans_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['naranja_claro']),
        ('GRID', (0, 0), (-1, -1), 1, COLORES['naranja']),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(trans_table)
    story.append(Spacer(1, 0.4*cm))

    # --- ABP (ACCIONES BALÓN PARADO) ---
    story.append(Table([[Paragraph('🎯  BALÓN PARADO', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['morado']),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 0.2*cm))

    abp = datos.get('abp', {})

    # Crear campo ABP visual
    campo_abp = CampoTactico.crear_campo_base(ancho_pagina * 0.4, 4*cm, 'horizontal')
    # Agregar zona de corner
    CampoTactico.agregar_zona(campo_abp, 5, 5, ancho_pagina * 0.08, 3.5*cm,
                              COLORES['morado'], 0.4)
    # Jugadores en área
    CampoTactico.agregar_jugador(campo_abp, ancho_pagina * 0.12, 2.5*cm, '9', colors.red, 12, True)
    CampoTactico.agregar_jugador(campo_abp, ancho_pagina * 0.10, 1.5*cm, '4', colors.red, 10, True)
    CampoTactico.agregar_jugador(campo_abp, ancho_pagina * 0.14, 3.2*cm, '5', colors.red, 10, True)
    # Flecha de corner
    CampoTactico.agregar_flecha(campo_abp, ancho_pagina * 0.02, 3.8*cm,
                                ancho_pagina * 0.10, 2.8*cm, colors.yellow, 2)

    abp_info = []
    if abp.get('corners_favor'):
        abp_info.append(Paragraph(f'<b>⚽ Corners A Favor:</b> {abp["corners_favor"]}', style_dato))
    if abp.get('faltas_favor'):
        abp_info.append(Paragraph(f'<b>⚽ Faltas A Favor:</b> {abp["faltas_favor"]}', style_dato))
    if abp.get('corners_contra'):
        abp_info.append(Paragraph(f'<b>🛡 Corners En Contra:</b> {abp["corners_contra"]}', style_dato))
    if abp.get('debilidad'):
        abp_info.append(Paragraph(f'<b>⚠️ Debilidad:</b> {abp["debilidad"]}', style_debilidad))
    if abp.get('fortaleza'):
        abp_info.append(Paragraph(f'<b>💪 Fortaleza:</b> {abp["fortaleza"]}', style_fortaleza))

    if abp_info:
        abp_row = [[campo_abp, abp_info]]
        abp_table = Table(abp_row, colWidths=[ancho_pagina * 0.45, ancho_pagina * 0.55])
        abp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLORES['morado_claro']),
            ('GRID', (0, 0), (-1, -1), 1, COLORES['morado']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(abp_table)

    story.append(Spacer(1, 0.4*cm))

    # --- JUGADORES CLAVE ---
    story.append(Table([[Paragraph('⭐  JUGADORES CLAVE', style_subtitulo)]],
                       colWidths=[ancho_pagina]))
    story[-1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLORES['verde_oscuro']),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 0.2*cm))

    jugadores = datos.get('jugadores_clave', [])

    if jugadores:
        # Crear cards visuales para cada jugador
        jugador_cards = []
        card_width = ancho_pagina / 3 - 5

        for jugador in jugadores[:3]:
            numero = jugador.get('numero', '-')
            nombre = jugador.get('nombre', '-')
            posicion = jugador.get('posicion', '-')
            nivel = jugador.get('nivel', 'normal')
            caracteristicas = jugador.get('caracteristicas', '-')

            # Icono de nivel
            icono = Iconos.crear_icono_nivel(nivel, 18)

            # Color de fondo según nivel
            if nivel == 'peligroso':
                bg_color = colors.HexColor('#FEE2E2')
                border_color = colors.HexColor('#DC2626')
                nivel_text = 'PELIGROSO'
            elif nivel == 'importante':
                bg_color = colors.HexColor('#FEF3C7')
                border_color = colors.HexColor('#F59E0B')
                nivel_text = 'IMPORTANTE'
            else:
                bg_color = colors.HexColor('#F3F4F6')
                border_color = colors.HexColor('#9CA3AF')
                nivel_text = 'NORMAL'

            # Crear mini campo con jugador
            mini_campo = Drawing(card_width - 20, 2.5*cm)
            mini_campo.add(Rect(0, 0, card_width - 20, 2.5*cm,
                               fillColor=COLORES['campo_verde'],
                               strokeColor=COLORES['campo_verde_oscuro'],
                               strokeWidth=1))
            # Línea central
            mini_campo.add(Line((card_width-20)/2, 0, (card_width-20)/2, 2.5*cm,
                               strokeColor=colors.white, strokeWidth=1))
            # Jugador destacado
            CampoTactico.agregar_jugador(mini_campo, (card_width-20)/2, 1.25*cm,
                                         numero, border_color, 20, True)

            card_content = [
                Paragraph(f'<b>#{numero} {nombre}</b>',
                         ParagraphStyle('nombre', fontSize=10,
                                       textColor=COLORES['gris_oscuro'],
                                       alignment=TA_CENTER,
                                       fontName='Helvetica-Bold')),
                Spacer(1, 3),
                mini_campo,
                Spacer(1, 3),
                Paragraph(f'<b>{posicion}</b> · {nivel_text}',
                         ParagraphStyle('pos', fontSize=8,
                                       textColor=border_color,
                                       alignment=TA_CENTER,
                                       fontName='Helvetica-Bold')),
                Spacer(1, 2),
                Paragraph(caracteristicas[:80] if len(caracteristicas) > 80 else caracteristicas,
                         ParagraphStyle('caract', fontSize=7,
                                       textColor=COLORES['gris'],
                                       alignment=TA_CENTER,
                                       leading=9)),
            ]

            jugador_cards.append(card_content)

        # Rellenar si hay menos de 3 jugadores
        while len(jugador_cards) < 3:
            jugador_cards.append([Paragraph('', style_texto)])

        jug_table = Table([jugador_cards], colWidths=[card_width + 2]*3)
        jug_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#FEE2E2') if jugadores and jugadores[0].get('nivel') == 'peligroso' else COLORES['verde_claro']),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#FEF3C7') if len(jugadores) > 1 and jugadores[1].get('nivel') == 'importante' else COLORES['verde_claro']),
            ('BACKGROUND', (2, 0), (2, 0), COLORES['verde_claro']),
            ('GRID', (0, 0), (-1, -1), 1, COLORES['verde_oscuro']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(jug_table)

    # ==================================================================
    # FOOTER
    # ==================================================================
    story.append(Spacer(1, 0.5*cm))

    footer_escudo = EscudoCAC.crear_escudo(30, 35)
    footer_text = Paragraph(
        f'<i>Club Atlético Central · Informe generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}</i>',
        ParagraphStyle('footer', fontSize=8, textColor=COLORES['gris'],
                      alignment=TA_CENTER)
    )

    footer_row = [[footer_escudo, footer_text, footer_escudo]]
    footer_table = Table(footer_row, colWidths=[40, ancho_pagina - 80, 40])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LINEABOVE', (0, 0), (-1, 0), 1, COLORES['verde_principal']),
    ]))
    story.append(footer_table)

    # Generar PDF
    doc.build(story)
    print(f"✅ PDF v2.0 PROFESIONAL generado: {output_path}")


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
                'debilidad': 'Poca velocidad en salida',
                'fortaleza': 'Buena técnica individual'
            },
            'vs_bloque_medio': {
                'jugadores_clave': '10 y 8 (centrocampistas)',
                'zonas_activas': 'Bandas con carrileros',
                'patrones': ['Cambios de orientación', 'Juego interior'],
                'debilidad': 'Dependen del 10',
                'fortaleza': 'Circulación rápida'
            },
            'vs_bloque_bajo': {
                'como_finalizan': 'Centros laterales al área',
                'jugadores_area': '9 y 7 atacan primer palo',
                'patrones': ['Centros al primer palo', 'Remates de segunda jugada'],
                'debilidad': 'Poco juego aéreo',
                'fortaleza': 'Buenos tiradores desde fuera'
            }
        },
        'defensa': {
            'pressing_alto': {
                'estructura': '4-4-2 en presión',
                'gatillos': 'Pase al central',
                'patrones': ['Presión en banda', 'Cierre de líneas de pase'],
                'fortaleza': 'Muy agresivos en recuperación',
                'debilidad': 'Espacios a la espalda'
            },
            'bloque_medio': {
                'compactacion': '25-30 metros entre líneas',
                'coberturas': 'Coberturas laterales buenas',
                'patrones': ['Compactos en centro', 'Vigilancia de espacios'],
                'fortaleza': 'Bien organizados',
                'debilidad': 'Lentos en basculaciones'
            },
            'bloque_bajo': {
                'organizacion': 'Dos líneas de 4 muy juntas',
                'marcajes': 'Zona pura en área',
                'patrones': ['Defensa en bloque', 'Salidas rápidas'],
                'debilidad': 'Dejan espacios entre líneas',
                'fortaleza': 'Buenos en duelos aéreos'
            }
        },
        'transiciones': {
            'def_atq': {
                'velocidad': 'Muy rápida - Contraataques letales',
                'jugadores_clave': '10 y extremos (7, 11)',
                'patrones': ['Pase largo a bandas', 'Verticalidad inmediata'],
                'como_cortar': 'Falta táctica rápida al inicio',
                'fortaleza': 'Velocidad de los extremos'
            },
            'atq_def': {
                'equilibrios': '2 centrales + pivote quedan atrás',
                'repliegue': 'Repliegue ordenado pero lento',
                'patrones': ['Presión al portador', 'Retrasar líneas'],
                'desbalance': 'Laterales muy adelantados',
                'fortaleza': 'Pivote cubre bien'
            }
        },
        'abp': {
            'corners_favor': 'Zona con 4 rematadores. Buscan primer palo.',
            'faltas_favor': 'Ejecutor: 10. Directas peligrosas.',
            'corners_contra': 'Defensa mixta, vulnerable segundo palo.',
            'debilidad': 'Flojos en defensa de corners',
            'fortaleza': 'Peligrosos en estrategia ofensiva'
        },
        'jugadores_clave': [
            {
                'numero': '10',
                'nombre': 'Pedri',
                'posicion': 'MC',
                'nivel': 'peligroso',
                'caracteristicas': 'Organizador del juego, gran visión de pase, difícil de presionar, clave en transiciones'
            },
            {
                'numero': '9',
                'nombre': 'Lewandowski',
                'posicion': 'DC',
                'nivel': 'peligroso',
                'caracteristicas': 'Goleador nato, movimientos en área, potente remate de cabeza, finalización letal'
            },
            {
                'numero': '8',
                'nombre': 'De Jong',
                'posicion': 'MC',
                'nivel': 'importante',
                'caracteristicas': 'Recuperador, buena conducción, apoya en construcción desde atrás'
            }
        ]
    }

    generar_informe_v2_pdf(datos_test, 'test_informe_v2_profesional.pdf')
    print("✅ Test completado. Revisa test_informe_v2_profesional.pdf")
