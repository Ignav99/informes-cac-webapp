#!/usr/bin/env python3
"""
Generador de PDF para Plan de Partido
Club Atlético Central
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import json
from datetime import datetime
from tactical_options import DEFENSIVA_OPCIONES, OFENSIVA_SALIDA

# Colores corporativos
COLOR_NEGRO = colors.HexColor('#000000')
COLOR_VERDE = colors.HexColor('#10B981')
COLOR_GRIS = colors.HexColor('#6B7280')
COLOR_GRIS_FONDO = colors.HexColor('#F3F4F6')
COLOR_AZUL = colors.HexColor('#3B82F6')


def generar_plan_partido_pdf(datos, nombre_archivo):
    """
    Genera el PDF del Plan de Partido
    """
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Estilos
    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLOR_VERDE,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    style_heading = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLOR_NEGRO,
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )

    style_subheading = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=COLOR_AZUL,
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_NEGRO,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    style_bullet = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_GRIS,
        spaceAfter=6,
        leftIndent=20,
        fontName='Helvetica'
    )

    # Contenido del PDF
    story = []

    # TÍTULO PRINCIPAL
    story.append(Paragraph(f"⚽ PLAN DE PARTIDO", style_title))
    story.append(Paragraph(f"vs {datos.get('nombre_rival', 'Rival')}", style_title))
    story.append(Spacer(1, 0.5*cm))

    # DATOS BÁSICOS
    datos_basicos = [
        ['Jornada:', datos.get('jornada', '-')],
        ['Sistema Rival:', datos.get('sistema_rival', '-')],
        ['Nuestro Sistema:', datos.get('plan_sistema_propio', '-')],
        ['Fecha:', datetime.now().strftime('%d/%m/%Y')]
    ]

    table = Table(datos_basicos, colWidths=[5*cm, 10*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_GRIS_FONDO),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_NEGRO),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.7*cm))

    # 1. ORGANIZACIÓN DEFENSIVA
    story.append(Paragraph("🛡️ 1. ORGANIZACIÓN DEFENSIVA", style_heading))

    opcion_defensiva = datos.get('plan_defensiva', '')
    if opcion_defensiva and opcion_defensiva in DEFENSIVA_OPCIONES:
        info_def = DEFENSIVA_OPCIONES[opcion_defensiva]

        story.append(Paragraph(f"<b>{info_def['nombre']}</b>", style_subheading))
        story.append(Paragraph(info_def['descripcion'], style_normal))

        # Conceptos clave
        story.append(Paragraph("<b>Conceptos clave:</b>", style_normal))
        for concepto in info_def['conceptos_clave']:
            story.append(Paragraph(f"• {concepto}", style_bullet))

        # Cuándo usar
        story.append(Paragraph(f"<b>Cuándo usar:</b> {info_def['cuando_usar']}", style_normal))

    story.append(Spacer(1, 0.5*cm))

    # 2. SALIDA DE BALÓN / ATAQUE
    story.append(Paragraph("⚡ 2. SALIDA DE BALÓN / ATAQUE", style_heading))

    opcion_ofensiva = datos.get('plan_ofensiva', '')
    if opcion_ofensiva and opcion_ofensiva in OFENSIVA_SALIDA:
        info_of = OFENSIVA_SALIDA[opcion_ofensiva]

        story.append(Paragraph(f"<b>{info_of['nombre']}</b>", style_subheading))
        story.append(Paragraph(info_of['descripcion'], style_normal))

        # Estrategias
        if 'estrategias' in info_of:
            story.append(Paragraph("<b>Estrategias disponibles:</b>", style_normal))
            for estrategia in info_of['estrategias']:
                story.append(Paragraph(f"<b>• {estrategia['nombre']}</b>", style_bullet))
                story.append(Paragraph(f"  {estrategia['descripcion']}", style_bullet))

        # Conceptos clave
        story.append(Paragraph("<b>Conceptos clave:</b>", style_normal))
        for concepto in info_of['conceptos_clave']:
            story.append(Paragraph(f"• {concepto}", style_bullet))

    story.append(Spacer(1, 0.5*cm))

    # 3. TRANSICIONES
    story.append(Paragraph("🔄 3. TRANSICIONES", style_heading))

    trans_def_atq = datos.get('plan_transicion_def_atq', '')
    if trans_def_atq:
        nombres_trans_def_atq = {
            'directo': 'Contraataque directo (máximo 3 pases)',
            'elaborado': 'Contraataque elaborado (progresión rápida con apoyo)',
            'contra_pressing': 'Contra-pressing (presión inmediata tras pérdida)'
        }
        story.append(Paragraph(f"<b>Defensa → Ataque:</b> {nombres_trans_def_atq.get(trans_def_atq, trans_def_atq)}", style_normal))

    trans_atq_def = datos.get('plan_transicion_atq_def', '')
    if trans_atq_def:
        nombres_trans_atq_def = {
            'pressing_inmediato': 'Pressing inmediato (5 segundos tras pérdida - gegenpressing)',
            'repliegue_intensivo': 'Repliegue intensivo (correr hacia atrás para organizarse)',
            'repliegue_selectivo': 'Repliegue selectivo (algunos presionan, otros repliegan)'
        }
        story.append(Paragraph(f"<b>Ataque → Defensa:</b> {nombres_trans_atq_def.get(trans_atq_def, trans_atq_def)}", style_normal))

    story.append(Spacer(1, 0.5*cm))

    # 4. BALÓN PARADO
    story.append(Paragraph("🎯 4. BALÓN PARADO", style_heading))

    corners_favor = datos.get('plan_corners_favor', '')
    if corners_favor:
        nombres_corners = {
            'corto': 'Córner corto: combinación para centro posterior',
            'primer_palo': 'Córner al primer palo: bloqueador + rematador',
            'segundo_palo': 'Córner al segundo palo: zona de mayor efectividad',
            'ensayado': 'Córner ensayado: jugada preparada'
        }
        story.append(Paragraph(f"<b>Córners a favor:</b> {nombres_corners.get(corners_favor, corners_favor)}", style_normal))

    corners_contra = datos.get('plan_corners_contra', '')
    if corners_contra:
        nombres_corners_contra = {
            'zona': 'Defensa en zona: cada jugador defiende una zona del área',
            'mixta': 'Defensa mixta: zona + marcaje a jugadores peligrosos',
            'individual': 'Defensa individual: cada jugador marca a un rival'
        }
        story.append(Paragraph(f"<b>Córners en contra:</b> {nombres_corners_contra.get(corners_contra, corners_contra)}", style_normal))

    story.append(Spacer(1, 0.5*cm))

    # 5. NUESTRO EQUIPO
    story.append(Paragraph("👕 5. NUESTRO EQUIPO", style_heading))

    jugadores_clave = datos.get('plan_jugadores_clave', '')
    if jugadores_clave:
        story.append(Paragraph("<b>Jugadores Clave:</b>", style_subheading))
        story.append(Paragraph(jugadores_clave, style_normal))

    bajas = datos.get('plan_bajas', '')
    if bajas:
        story.append(Paragraph("<b>Bajas / Lesionados:</b>", style_subheading))
        story.append(Paragraph(bajas, style_normal))

    instrucciones = datos.get('plan_instrucciones', '')
    if instrucciones:
        story.append(Paragraph("<b>Instrucciones Específicas por Puesto:</b>", style_subheading))
        story.append(Paragraph(instrucciones, style_normal))

    story.append(Spacer(1, 0.5*cm))

    # 6. OBSERVACIONES DEL ENTRENADOR
    story.append(Paragraph("📝 6. OBSERVACIONES DEL ENTRENADOR", style_heading))

    notas = datos.get('plan_notas', '')
    if notas:
        story.append(Paragraph("<b>Notas Tácticas:</b>", style_subheading))
        story.append(Paragraph(notas, style_normal))

    cambios = datos.get('plan_cambios', '')
    if cambios:
        story.append(Paragraph("<b>Cambios Previstos:</b>", style_subheading))
        story.append(Paragraph(cambios, style_normal))

    # FOOTER
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("─" * 80, style_normal))
    story.append(Paragraph(
        f"Plan de Partido generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')} | Club Atlético Central",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=COLOR_GRIS, alignment=TA_CENTER)
    ))

    # Construir PDF
    doc.build(story)
    print(f"✅ Plan de Partido generado: {nombre_archivo}")


if __name__ == "__main__":
    # Test
    datos_test = {
        'nombre_rival': 'FC Barcelona',
        'jornada': 'Jornada 15',
        'sistema_rival': '4-3-3',
        'plan_sistema_propio': '4-4-2',
        'plan_defensiva': 'bloque_medio',
        'plan_ofensiva': 'vs_bloque_alto',
        'plan_transicion_def_atq': 'directo',
        'plan_transicion_atq_def': 'pressing_inmediato',
        'plan_corners_favor': 'segundo_palo',
        'plan_corners_contra': 'mixta',
        'plan_jugadores_clave': '#10 Pérez (mediapunta), #9 García (delantero)',
        'plan_bajas': '#5 López (lesión)',
        'plan_instrucciones': 'Portero: salir como líbero. Laterales: equilibrio.',
        'plan_notas': 'Importante mantener la concentración todo el partido.',
        'plan_cambios': 'Si vamos perdiendo, meter un delantero más en el minuto 60.'
    }

    generar_plan_partido_pdf(datos_test, 'test_plan_partido.pdf')
