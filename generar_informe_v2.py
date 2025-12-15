#!/usr/bin/env python3
"""
Generador de Informes de Partido v2.0 PROFESIONAL
Club Atlético Central

PDF ultra-visual con:
- Logo del club desde imagen externa
- Campos tácticos DINÁMICOS generados por IA según el texto
- Diseño profesional compacto
- Mapas de juego personalizados
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon
from reportlab.graphics import renderPDF
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
    'amarillo': colors.HexColor('#FBBF24'),
}

# Mapeo de nombres de colores a objetos Color
COLOR_MAP = {
    'rojo': colors.HexColor('#DC2626'),
    'azul': colors.HexColor('#2563EB'),
    'amarillo': colors.HexColor('#FBBF24'),
    'verde': colors.HexColor('#22C55E'),
    'naranja': colors.HexColor('#F59E0B'),
    'blanco': colors.white,
    'morado': colors.HexColor('#8B5CF6'),
}


# =============================================================================
# CAMPO TÁCTICO DINÁMICO
# =============================================================================
class CampoDinamico:
    """Dibuja campos de fútbol con instrucciones dinámicas de la IA"""

    @staticmethod
    def crear_campo_base(width, height):
        """Crea un campo de fútbol base con césped realista"""
        d = Drawing(width, height)

        # Césped con franjas
        num_franjas = 8
        franja_width = width / num_franjas

        for i in range(num_franjas):
            color = COLORES['campo_verde'] if i % 2 == 0 else COLORES['campo_verde_oscuro']
            d.add(Rect(i * franja_width, 0, franja_width, height,
                      fillColor=color, strokeColor=None))

        # Borde del campo
        d.add(Rect(2, 2, width - 4, height - 4,
                  fillColor=None, strokeColor=colors.white, strokeWidth=2))

        # Línea central vertical
        d.add(Line(width/2, 2, width/2, height - 2,
                  strokeColor=colors.white, strokeWidth=1.5))

        # Círculo central
        d.add(Circle(width/2, height/2, height/5,
                    strokeColor=colors.white, strokeWidth=1.5, fillColor=None))
        d.add(Circle(width/2, height/2, 3,
                    fillColor=colors.white, strokeColor=None))

        # Área izquierda (portería propia)
        area_w = width * 0.16
        area_h = height * 0.6
        d.add(Rect(2, (height - area_h)/2, area_w, area_h,
                  fillColor=None, strokeColor=colors.white, strokeWidth=1.5))
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

        return d

    @staticmethod
    def aplicar_instrucciones(d, instrucciones, width, height):
        """Aplica instrucciones de dibujo de la IA al campo"""
        if not instrucciones:
            return d

        # Dibujar zonas primero (debajo de todo)
        for zona in instrucciones.get('zonas', []):
            x = zona.get('x', 50) / 100 * width
            y = zona.get('y', 50) / 100 * height
            ancho = zona.get('ancho', 20) / 100 * width
            alto = zona.get('alto', 30) / 100 * height
            color = COLOR_MAP.get(zona.get('color', 'verde'), COLORES['verde_principal'])

            # Color semitransparente
            zona_color = colors.Color(color.red, color.green, color.blue, alpha=0.3)
            d.add(Rect(x, y, ancho, alto,
                      fillColor=zona_color,
                      strokeColor=color,
                      strokeWidth=1,
                      strokeDashArray=[3, 2]))

        # Dibujar línea táctica si está activa
        linea = instrucciones.get('linea_tactica', {})
        if linea.get('activa', False):
            linea_x = linea.get('x', 50) / 100 * width
            color = COLOR_MAP.get(linea.get('color', 'rojo'), COLORES['rojo'])
            d.add(Line(linea_x, 5, linea_x, height - 5,
                      strokeColor=color, strokeWidth=3, strokeDashArray=[8, 4]))

        # Dibujar flechas
        for flecha in instrucciones.get('flechas', []):
            x1 = flecha.get('x1', 50) / 100 * width
            y1 = flecha.get('y1', 50) / 100 * height
            x2 = flecha.get('x2', 60) / 100 * width
            y2 = flecha.get('y2', 50) / 100 * height
            color = COLOR_MAP.get(flecha.get('color', 'amarillo'), COLORES['amarillo'])

            # Línea
            d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=2))

            # Punta de flecha
            angulo = math.atan2(y2 - y1, x2 - x1)
            tam_punta = 6
            px1 = x2 - tam_punta * math.cos(angulo - 0.5)
            py1 = y2 - tam_punta * math.sin(angulo - 0.5)
            px2 = x2 - tam_punta * math.cos(angulo + 0.5)
            py2 = y2 - tam_punta * math.sin(angulo + 0.5)
            d.add(Polygon([x2, y2, px1, py1, px2, py2],
                         fillColor=color, strokeColor=None))

        # Dibujar jugadores (encima de todo)
        for jugador in instrucciones.get('jugadores', []):
            x = jugador.get('x', 50) / 100 * width
            y = jugador.get('y', 50) / 100 * height
            numero = jugador.get('numero', '')
            destacado = jugador.get('destacado', False)
            color_nombre = jugador.get('color', 'rojo')

            # Tamaño según si está destacado
            tamano = 16 if destacado else 12
            color = COLOR_MAP.get(color_nombre, COLORES['rojo'])

            # Círculo del jugador
            d.add(Circle(x, y, tamano/2,
                        fillColor=color,
                        strokeColor=colors.white,
                        strokeWidth=1.5))

            # Número
            if numero:
                d.add(String(x, y - 3, str(numero),
                            fontSize=7 if not destacado else 8,
                            fontName='Helvetica-Bold',
                            fillColor=colors.white,
                            textAnchor='middle'))

        return d

    @staticmethod
    def crear_campo_con_instrucciones(width, height, instrucciones):
        """Crea un campo completo con instrucciones de la IA"""
        d = CampoDinamico.crear_campo_base(width, height)
        d = CampoDinamico.aplicar_instrucciones(d, instrucciones, width, height)
        return d


# =============================================================================
# CAMPO DE FORMACIÓN CON 11 JUGADORES
# =============================================================================
class CampoFormacion:
    """Dibuja un campo con el 11 completo, destacando jugadores clave"""

    # Posiciones estándar en el campo (X%, Y%) - campo horizontal
    # X: 0=portería propia, 100=portería rival
    # Y: 0=banda inferior, 100=banda superior
    POSICIONES = {
        # Portero
        'PT': (8, 50), 'POR': (8, 50), 'GK': (8, 50),
        # Defensas
        'DFC': (22, 50), 'CB': (22, 50),  # Central único
        'DFCd': (22, 35), 'DFCi': (22, 65),  # Centrales en pareja
        'LD': (22, 15), 'RB': (22, 15), 'LTD': (22, 15),  # Lateral derecho
        'LI': (22, 85), 'LB': (22, 85), 'LTI': (22, 85),  # Lateral izquierdo
        'CAD': (28, 20), 'RWB': (28, 20),  # Carrilero derecho
        'CAI': (28, 80), 'LWB': (28, 80),  # Carrilero izquierdo
        # Centrocampistas
        'MCD': (40, 50), 'CDM': (40, 50), 'PIV': (40, 50),  # Pivote
        'MC': (50, 50), 'CM': (50, 50),  # Centrocampista
        'MCd': (50, 35), 'MCi': (50, 65),  # MC derecho/izquierdo
        'MCO': (55, 50), 'CAM': (55, 50), 'MP': (55, 50),  # Mediapunta
        'MD': (45, 25), 'RM': (45, 25),  # Mediocentro derecho
        'MI': (45, 75), 'LM': (45, 75),  # Mediocentro izquierdo
        'INT': (50, 40),  # Interior
        # Extremos
        'ED': (65, 15), 'RW': (65, 15), 'EXD': (65, 15),  # Extremo derecho
        'EI': (65, 85), 'LW': (65, 85), 'EXI': (65, 85),  # Extremo izquierdo
        # Delanteros
        'DC': (75, 50), 'ST': (75, 50), 'CF': (75, 50),  # Delantero centro
        'DCd': (72, 35), 'DCi': (72, 65),  # Delanteros en pareja
        'SD': (68, 40), 'SS': (68, 40),  # Segundo delantero/media punta alta
    }

    @staticmethod
    def obtener_posicion(posicion_texto):
        """Obtiene coordenadas para una posición dada"""
        pos = posicion_texto.upper().strip()
        return CampoFormacion.POSICIONES.get(pos, (50, 50))

    @staticmethod
    def crear_campo_formacion(width, height, jugadores_destacados, sistema='4-3-3'):
        """
        Crea un campo con el 11 completo

        Args:
            width, height: Dimensiones del dibujo
            jugadores_destacados: Lista de dicts con {numero, posicion, nombre, nivel}
            sistema: Sistema táctico para posicionar el resto del 11

        Returns:
            Drawing con el campo y jugadores
        """
        d = Drawing(width, height)

        # Césped con franjas
        num_franjas = 10
        franja_width = width / num_franjas
        for i in range(num_franjas):
            color = COLORES['campo_verde'] if i % 2 == 0 else COLORES['campo_verde_oscuro']
            d.add(Rect(i * franja_width, 0, franja_width, height,
                      fillColor=color, strokeColor=None))

        # Borde
        d.add(Rect(2, 2, width - 4, height - 4,
                  fillColor=None, strokeColor=colors.white, strokeWidth=1.5))

        # Línea central
        d.add(Line(width/2, 2, width/2, height - 2,
                  strokeColor=colors.white, strokeWidth=1))

        # Círculo central
        d.add(Circle(width/2, height/2, height/6,
                    strokeColor=colors.white, strokeWidth=1, fillColor=None))

        # Áreas
        area_w = width * 0.14
        area_h = height * 0.55
        # Área izquierda
        d.add(Rect(2, (height - area_h)/2, area_w, area_h,
                  fillColor=None, strokeColor=colors.white, strokeWidth=1))
        # Área derecha
        d.add(Rect(width - area_w - 2, (height - area_h)/2, area_w, area_h,
                  fillColor=None, strokeColor=colors.white, strokeWidth=1))

        # Formación base del 11 (posiciones estándar en gris)
        formacion_base = [
            ('1', 8, 50),    # Portero
            ('2', 22, 15),   # LD
            ('4', 22, 38),   # DFCd
            ('5', 22, 62),   # DFCi
            ('3', 22, 85),   # LI
            ('6', 40, 50),   # Pivote
            ('8', 50, 30),   # MC derecho
            ('10', 55, 50),  # Mediapunta
            ('7', 65, 15),   # Extremo derecho
            ('9', 75, 50),   # Delantero centro
            ('11', 65, 85),  # Extremo izquierdo
        ]

        # Crear set de números destacados
        numeros_destacados = {}
        for jug in jugadores_destacados:
            num = str(jug.get('numero', ''))
            pos = jug.get('posicion', '')
            nivel = jug.get('nivel', 'normal')
            if num:
                numeros_destacados[num] = {'posicion': pos, 'nivel': nivel}

        # Dibujar el 11
        for numero, x_pct, y_pct in formacion_base:
            x = (x_pct / 100) * width
            y = (y_pct / 100) * height

            # Verificar si es un jugador destacado
            if numero in numeros_destacados:
                info = numeros_destacados[numero]
                # Reposicionar según la posición real si la tiene
                if info['posicion']:
                    new_x, new_y = CampoFormacion.obtener_posicion(info['posicion'])
                    x = (new_x / 100) * width
                    y = (new_y / 100) * height

                # Color según nivel
                if info['nivel'] == 'peligroso':
                    fill_color = COLORES['rojo']
                    tamano = 14
                elif info['nivel'] == 'importante':
                    fill_color = COLORES['naranja']
                    tamano = 12
                else:
                    fill_color = COLORES['amarillo']
                    tamano = 12
                stroke_width = 2
            else:
                # Jugador normal - gris
                fill_color = colors.HexColor('#6B7280')
                tamano = 9
                stroke_width = 1

            # Círculo del jugador
            d.add(Circle(x, y, tamano/2,
                        fillColor=fill_color,
                        strokeColor=colors.white,
                        strokeWidth=stroke_width))

            # Número
            font_size = 7 if numero in numeros_destacados else 5
            d.add(String(x, y - 2, numero,
                        fontSize=font_size,
                        fontName='Helvetica-Bold',
                        fillColor=colors.white,
                        textAnchor='middle'))

        return d


# =============================================================================
# UTILIDADES
# =============================================================================
def obtener_logo_path():
    """Obtiene la ruta del logo del club"""
    # Buscar en varios lugares posibles
    posibles_rutas = [
        os.path.join(os.path.dirname(__file__), 'static', 'logo.png'),
        os.path.join(os.path.dirname(__file__), 'logo.png'),
        os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png'),
        '/home/user/informes-cac-webapp/static/logo.png',
        '/home/user/informes-cac-webapp/logo.png',
    ]

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta

    return None


def crear_logo_placeholder(width=50, height=60):
    """Crea un placeholder si no hay logo"""
    d = Drawing(width, height)

    # Forma de escudo
    cx = width / 2
    puntos_escudo = [
        5, height - 5,
        width - 5, height - 5,
        width - 5, height * 0.4,
        cx, 5,
        5, height * 0.4,
    ]

    d.add(Polygon(puntos_escudo,
                 fillColor=COLORES['verde_principal'],
                 strokeColor=COLORES['verde_oscuro'],
                 strokeWidth=2))

    # Texto "CAC"
    d.add(String(cx, height * 0.5, 'CAC',
                fontSize=12, fontName='Helvetica-Bold',
                fillColor=colors.white, textAnchor='middle'))

    return d


# =============================================================================
# GENERADOR PDF PRINCIPAL
# =============================================================================
def generar_informe_v2_pdf(datos, output_path, dibujos_ia=None):
    """
    Genera un PDF profesional ultra-visual con análisis táctico

    Args:
        datos: Diccionario con todos los datos del formulario v2
        output_path: Ruta donde guardar el PDF
        dibujos_ia: Diccionario con instrucciones de dibujo generadas por IA (opcional)
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
    # HEADER CON LOGO
    # ==================================================================
    logo_path = obtener_logo_path()

    # Crear elemento de logo (imagen real o placeholder)
    if logo_path:
        try:
            logo_img = RLImage(logo_path, width=50, height=60)
            logo_img_right = RLImage(logo_path, width=50, height=60)
        except:
            logo_img = crear_logo_placeholder(50, 60)
            logo_img_right = crear_logo_placeholder(50, 60)
    else:
        logo_img = crear_logo_placeholder(50, 60)
        logo_img_right = crear_logo_placeholder(50, 60)

    rival = datos.get('nombre_rival', 'RIVAL').upper()
    jornada = datos.get('jornada', '-')
    fecha = datetime.now().strftime('%d/%m/%Y')

    header_data = [[
        logo_img,
        [Paragraph(f'<b>INFORME TÁCTICO</b>', style_titulo),
         Paragraph(f'vs {rival}', ParagraphStyle('rival', fontSize=14,
                   textColor=COLORES['verde_principal'], alignment=TA_CENTER,
                   fontName='Helvetica-Bold')),
         Paragraph(f'Jornada {jornada} · {fecha}',
                  ParagraphStyle('fecha', fontSize=9, textColor=COLORES['gris'],
                                alignment=TA_CENTER))],
        logo_img_right
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

    # Obtener instrucciones de dibujo de la IA
    dibujos_ataque = {}
    if dibujos_ia:
        dibujos_ataque = dibujos_ia.get('ataque', {})

    def crear_celda_ataque(fase_data, titulo, tipo_fase):
        """Crea celda visual para fase de ataque con campo dinámico"""
        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_seccion))
        contenido.append(Spacer(1, 2))

        # Campo con instrucciones de IA
        instrucciones = dibujos_ataque.get(tipo_fase, {})
        campo = CampoDinamico.crear_campo_con_instrucciones(
            campo_size[0], campo_size[1], instrucciones
        )
        contenido.append(campo)
        contenido.append(Spacer(1, 3))

        if fase_data:
            if fase_data.get('estructura'):
                contenido.append(Paragraph(f'<b>Estructura:</b> {fase_data["estructura"][:55]}', style_texto))
            if fase_data.get('triangulos'):
                contenido.append(Paragraph(f'<b>Triángulos:</b> {fase_data["triangulos"][:45]}', style_texto))
            if fase_data.get('jugadores_clave'):
                contenido.append(Paragraph(f'<b>Jugadores clave:</b> {fase_data["jugadores_clave"][:40]}', style_texto))
            if fase_data.get('zonas_activas'):
                contenido.append(Paragraph(f'<b>Zonas activas:</b> {fase_data["zonas_activas"][:40]}', style_texto))
            if fase_data.get('como_finalizan'):
                contenido.append(Paragraph(f'<b>Finalización:</b> {fase_data["como_finalizan"][:45]}', style_texto))

            patrones = fase_data.get('patrones', [])
            if patrones:
                contenido.append(Paragraph('<b>Patrones:</b>', style_texto))
                for p in patrones[:2]:
                    if p:
                        contenido.append(Paragraph(f'  • {p[:42]}', style_texto))

            if fase_data.get('fortaleza'):
                contenido.append(Paragraph(f'<b>Fortaleza:</b> {fase_data["fortaleza"][:38]}', style_fortaleza))
            if fase_data.get('debilidad'):
                contenido.append(Paragraph(f'<b>Debilidad:</b> {fase_data["debilidad"][:38]}', style_debilidad))

        return contenido

    vs_alto = ataque.get('vs_bloque_alto', {})
    vs_medio = ataque.get('vs_bloque_medio', {})
    vs_bajo = ataque.get('vs_bloque_bajo', {})

    ataque_row = [
        crear_celda_ataque(vs_alto, 'VS BLOQUE ALTO', 'vs_bloque_alto'),
        crear_celda_ataque(vs_medio, 'VS BLOQUE MEDIO', 'vs_bloque_medio'),
        crear_celda_ataque(vs_bajo, 'VS BLOQUE BAJO', 'vs_bloque_bajo')
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
    dibujos_defensa = {}
    if dibujos_ia:
        dibujos_defensa = dibujos_ia.get('defensa', {})

    def crear_celda_defensa(fase_data, titulo, tipo_fase):
        """Crea celda visual para fase defensiva con campo dinámico"""
        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_seccion))
        contenido.append(Spacer(1, 2))

        instrucciones = dibujos_defensa.get(tipo_fase, {})
        campo = CampoDinamico.crear_campo_con_instrucciones(
            campo_size[0], campo_size[1], instrucciones
        )
        contenido.append(campo)
        contenido.append(Spacer(1, 3))

        if fase_data:
            if fase_data.get('estructura'):
                contenido.append(Paragraph(f'<b>Estructura:</b> {fase_data["estructura"][:45]}', style_texto))
            if fase_data.get('gatillos'):
                contenido.append(Paragraph(f'<b>Gatillos:</b> {fase_data["gatillos"][:45]}', style_texto))
            if fase_data.get('compactacion'):
                contenido.append(Paragraph(f'<b>Compactación:</b> {fase_data["compactacion"][:40]}', style_texto))
            if fase_data.get('coberturas'):
                contenido.append(Paragraph(f'<b>Coberturas:</b> {fase_data["coberturas"][:42]}', style_texto))
            if fase_data.get('organizacion'):
                contenido.append(Paragraph(f'<b>Organización:</b> {fase_data["organizacion"][:42]}', style_texto))
            if fase_data.get('marcajes'):
                contenido.append(Paragraph(f'<b>Marcajes:</b> {fase_data["marcajes"][:45]}', style_texto))

            patrones = fase_data.get('patrones', [])
            if patrones:
                contenido.append(Paragraph('<b>Patrones:</b>', style_texto))
                for p in patrones[:2]:
                    if p:
                        contenido.append(Paragraph(f'  • {p[:42]}', style_texto))

            if fase_data.get('fortaleza'):
                contenido.append(Paragraph(f'<b>Fortaleza:</b> {fase_data["fortaleza"][:38]}', style_fortaleza))
            if fase_data.get('debilidad'):
                contenido.append(Paragraph(f'<b>Debilidad:</b> {fase_data["debilidad"][:38]}', style_debilidad))

        return contenido

    pressing = defensa.get('pressing_alto', {})
    bloque_medio = defensa.get('bloque_medio', {})
    bloque_bajo = defensa.get('bloque_bajo', {})

    defensa_row = [
        crear_celda_defensa(pressing, 'PRESSING ALTO', 'pressing_alto'),
        crear_celda_defensa(bloque_medio, 'BLOQUE MEDIO', 'bloque_medio'),
        crear_celda_defensa(bloque_bajo, 'BLOQUE BAJO', 'bloque_bajo')
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
    dibujos_trans = {}
    if dibujos_ia:
        dibujos_trans = dibujos_ia.get('transiciones', {})

    campo_trans_w = ancho_pagina / 2 - 10
    campo_trans_h = 5*cm

    def crear_celda_transicion(fase_data, titulo, tipo):
        """Crea celda visual para transición con campo dinámico"""
        contenido = []
        contenido.append(Paragraph(f'<b>{titulo}</b>', style_seccion))
        contenido.append(Spacer(1, 3))

        instrucciones = dibujos_trans.get(tipo, {})
        campo = CampoDinamico.crear_campo_con_instrucciones(
            campo_trans_w - 10, campo_trans_h, instrucciones
        )
        contenido.append(campo)
        contenido.append(Spacer(1, 4))

        if fase_data:
            if tipo == 'def_atq':
                if fase_data.get('velocidad'):
                    contenido.append(Paragraph(f'<b>Velocidad:</b> {fase_data["velocidad"]}', style_texto))
                if fase_data.get('jugadores_clave'):
                    contenido.append(Paragraph(f'<b>Jugadores clave:</b> {fase_data["jugadores_clave"]}', style_texto))
                if fase_data.get('como_cortar'):
                    contenido.append(Paragraph(f'<b>Cómo cortarla:</b> {fase_data["como_cortar"]}', style_debilidad))
            else:
                if fase_data.get('equilibrios'):
                    contenido.append(Paragraph(f'<b>Equilibrios:</b> {fase_data["equilibrios"]}', style_texto))
                if fase_data.get('repliegue'):
                    contenido.append(Paragraph(f'<b>Repliegue:</b> {fase_data["repliegue"]}', style_texto))
                if fase_data.get('desbalance'):
                    contenido.append(Paragraph(f'<b>Desbalance:</b> {fase_data["desbalance"]}', style_debilidad))

            patrones = fase_data.get('patrones', [])
            if patrones:
                contenido.append(Paragraph('<b>Patrones:</b>', style_texto))
                for p in patrones[:2]:
                    if p:
                        contenido.append(Paragraph(f'  • {p[:48]}', style_texto))

            if fase_data.get('fortaleza'):
                contenido.append(Paragraph(f'<b>Fortaleza:</b> {fase_data["fortaleza"]}', style_fortaleza))

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
    dibujos_abp = {}
    if dibujos_ia:
        dibujos_abp = dibujos_ia.get('abp', {})

    # Campo ABP con instrucciones de IA
    instrucciones_abp = dibujos_abp.get('corners', {})
    campo_abp = CampoDinamico.crear_campo_con_instrucciones(
        ancho_pagina * 0.4, 4*cm, instrucciones_abp
    )

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

    if abp_info or instrucciones_abp:
        abp_row = [[campo_abp, abp_info if abp_info else [Paragraph('', style_texto)]]]
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
        # Campo con el 11 completo - jugadores destacados resaltados
        campo_formacion = CampoFormacion.crear_campo_formacion(
            ancho_pagina,
            4.5*cm,
            jugadores[:3]
        )
        story.append(campo_formacion)
        story.append(Spacer(1, 0.3*cm))

        # Leyenda del campo
        leyenda_items = []
        for jug in jugadores[:3]:
            nivel = jug.get('nivel', 'normal')
            if nivel == 'peligroso':
                color_dot = COLORES['rojo']
            elif nivel == 'importante':
                color_dot = COLORES['naranja']
            else:
                color_dot = COLORES['amarillo']

            leyenda_items.append(
                Paragraph(f'<font color="{color_dot.hexval()}">●</font> #{jug.get("numero", "-")} {jug.get("nombre", "-")} ({jug.get("posicion", "-")})',
                         ParagraphStyle('leyenda', fontSize=8, textColor=COLORES['gris_oscuro']))
            )

        leyenda_gris = Paragraph('<font color="#6B7280">●</font> Resto del 11',
                                ParagraphStyle('leyenda', fontSize=8, textColor=COLORES['gris']))

        leyenda_table = Table([[leyenda_items[0] if len(leyenda_items) > 0 else '',
                               leyenda_items[1] if len(leyenda_items) > 1 else '',
                               leyenda_items[2] if len(leyenda_items) > 2 else '',
                               leyenda_gris]],
                             colWidths=[ancho_pagina/4]*4)
        leyenda_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(leyenda_table)
        story.append(Spacer(1, 0.3*cm))

        # Tarjetas de info de cada jugador
        jugador_cards = []
        card_width = ancho_pagina / 3 - 5

        for jugador in jugadores[:3]:
            numero = jugador.get('numero', '-')
            nombre = jugador.get('nombre', '-')
            posicion = jugador.get('posicion', '-')
            nivel = jugador.get('nivel', 'normal')
            caracteristicas = jugador.get('caracteristicas', '-')

            if nivel == 'peligroso':
                border_color = colors.HexColor('#DC2626')
                nivel_text = '🔴 PELIGROSO'
                bg_color = colors.HexColor('#FEE2E2')
            elif nivel == 'importante':
                border_color = colors.HexColor('#F59E0B')
                nivel_text = '🟠 IMPORTANTE'
                bg_color = colors.HexColor('#FEF3C7')
            else:
                border_color = colors.HexColor('#9CA3AF')
                nivel_text = '⚪ NORMAL'
                bg_color = COLORES['gris_claro']

            card_content = [
                Paragraph(f'<b>#{numero}</b>',
                         ParagraphStyle('num', fontSize=16,
                                       textColor=border_color,
                                       alignment=TA_CENTER,
                                       fontName='Helvetica-Bold')),
                Paragraph(f'<b>{nombre}</b>',
                         ParagraphStyle('nombre', fontSize=9,
                                       textColor=COLORES['gris_oscuro'],
                                       alignment=TA_CENTER,
                                       fontName='Helvetica-Bold')),
                Spacer(1, 3),
                Paragraph(f'{posicion} · {nivel_text}',
                         ParagraphStyle('pos', fontSize=8,
                                       textColor=border_color,
                                       alignment=TA_CENTER)),
                Spacer(1, 4),
                Paragraph(caracteristicas[:90] if len(caracteristicas) > 90 else caracteristicas,
                         ParagraphStyle('caract', fontSize=7,
                                       textColor=COLORES['gris'],
                                       alignment=TA_CENTER,
                                       leading=9)),
            ]

            jugador_cards.append(card_content)

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

    # Logo en footer
    if logo_path:
        try:
            footer_logo = RLImage(logo_path, width=30, height=35)
            footer_logo_right = RLImage(logo_path, width=30, height=35)
        except:
            footer_logo = crear_logo_placeholder(30, 35)
            footer_logo_right = crear_logo_placeholder(30, 35)
    else:
        footer_logo = crear_logo_placeholder(30, 35)
        footer_logo_right = crear_logo_placeholder(30, 35)

    footer_text = Paragraph(
        f'<i>Club Atlético Central · Informe generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}</i>',
        ParagraphStyle('footer', fontSize=8, textColor=COLORES['gris'],
                      alignment=TA_CENTER)
    )

    footer_row = [[footer_logo, footer_text, footer_logo_right]]
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
                'caracteristicas': 'Organizador del juego, gran visión de pase'
            },
            {
                'numero': '9',
                'nombre': 'Lewandowski',
                'posicion': 'DC',
                'nivel': 'peligroso',
                'caracteristicas': 'Goleador nato, remate de cabeza'
            },
            {
                'numero': '8',
                'nombre': 'De Jong',
                'posicion': 'MC',
                'nivel': 'importante',
                'caracteristicas': 'Recuperador, buena conducción'
            }
        ]
    }

    generar_informe_v2_pdf(datos_test, 'test_informe_v2_profesional.pdf')
    print("✅ Test completado. Revisa test_informe_v2_profesional.pdf")
