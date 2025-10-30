"""
Opciones Tácticas Predefinidas para Plan de Partido
Club Atlético Central

Basado en conocimiento táctico de entrenadores como:
- Pep Guardiola (posesión y pressing)
- Diego Simeone (bloque bajo organizado)
- Jürgen Klopp (gegenpressing)
- José Mourinho (transiciones)
"""

# ============================================================================
# OPCIONES DEFENSIVAS
# ============================================================================

DEFENSIVA_OPCIONES = {
    "bloque_alto": {
        "nombre": "Bloque Alto (Pressing)",
        "descripcion": "Presionar al rival en su campo. Línea defensiva adelantada (40-45m).",
        "ventajas": [
            "Recuperar balón cerca de la portería rival",
            "Dificultar la construcción del rival",
            "Generar ocasiones en transición rápida",
            "Dominar territorialmente el partido"
        ],
        "desventajas": [
            "Vulnerable a balones largos y espacios a la espalda",
            "Requiere alta condición física",
            "Riesgo ante delanteros rápidos"
        ],
        "cuando_usar": "Contra rivales con salida desde atrás débil o portero con mal juego de pies. Equipos técnicamente inferiores.",
        "conceptos_clave": [
            "Pressing coordinado por zonas",
            "Línea defensiva entre 40-45m",
            "Portero como líbero",
            "Basculaciones rápidas",
            "Coberturas permanentes"
        ],
        "referencias": "Guardiola (Man City), Klopp (Liverpool), Bielsa"
    },

    "bloque_medio": {
        "nombre": "Bloque Medio (Equilibrado)",
        "descripcion": "Replegar entre medio campo y 3/4 del campo. Línea defensiva en 30-35m.",
        "ventajas": [
            "Equilibrio defensivo-ofensivo",
            "Facilita transiciones",
            "Compactar líneas (15-20m entre ellas)",
            "Menor desgaste físico que bloque alto"
        ],
        "desventajas": [
            "Permite iniciación al rival",
            "Requiere disciplina táctica",
            "Cede dominio territorial"
        ],
        "cuando_usar": "Contra rivales de nivel similar. Cuando se busca equilibrio. Equipos físicamente potentes.",
        "conceptos_clave": [
            "Presión tras pase (gatillo de presión)",
            "Línea defensiva en 30-35m",
            "Distancia entre líneas: 15-20m",
            "Pressing selectivo en zonas",
            "Coberturas interiores"
        ],
        "referencias": "Ancelotti, Luis Enrique, Nagelsmann"
    },

    "bloque_bajo": {
        "nombre": "Bloque Bajo (Repliegue)",
        "descripcion": "Defender cerca del área propia. Línea defensiva por debajo de 30m.",
        "ventajas": [
            "Mayor protección del área",
            "Reducir espacios entre líneas",
            "Aprovechamiento de transiciones",
            "Efectivo ante rivales superiores"
        ],
        "desventajas": [
            "Ceder iniciativa y posesión",
            "Presión constante del rival",
            "Desgaste mental del equipo",
            "Pocas ocasiones de gol"
        ],
        "cuando_usar": "Contra rivales superiores técnica o físicamente. Proteger resultados. Equipos con delanteros rápidos en contraataque.",
        "conceptos_clave": [
            "Línea defensiva < 30m",
            "Bloque ultra-compacto (10-15m entre líneas)",
            "Defensa del área en zona",
            "Salidas rápidas en contraataque",
            "Sacrificio colectivo"
        ],
        "referencias": "Simeone (Atlético), Mourinho (Inter 2010), Allegri"
    }
}


# ============================================================================
# OPCIONES OFENSIVAS (SALIDA DE BALÓN)
# ============================================================================

OFENSIVA_SALIDA = {
    "vs_bloque_alto": {
        "nombre": "Salida vs Bloque Alto (Pressing Rival)",
        "descripcion": "El rival presiona arriba. Aprovechamos espacios a su espalda.",
        "estrategias": [
            {
                "nombre": "Salida larga (balones a la espalda)",
                "descripcion": "Portero o centrales juegan directo a delanteros o espacios",
                "ventajas": ["Evitar pressing", "Aprovechar velocidad", "Desgastar rival"],
                "jugadores_clave": ["Portero con buen pie", "Delantero de referencia", "Extremos rápidos"]
            },
            {
                "nombre": "Salida corta con superioridad",
                "descripcion": "Portero se incorpora como +1. Crear superioridad numérica atrás (3v2 o 4v3)",
                "ventajas": ["Progresión controlada", "Atraer presión y liberar mediocampistas", "Juego posicional"],
                "jugadores_clave": ["Portero líbero", "Centrales buenos con balón", "Pivote que baja a recibir"]
            },
            {
                "nombre": "Tercer hombre",
                "descripcion": "Pase a jugador presionado que devuelve de primera a un tercero libre",
                "ventajas": ["Romper líneas de presión", "Velocidad de circulación", "Generar desmarques"],
                "jugadores_clave": ["Mediocampistas con visión", "Laterales en amplitud"]
            }
        ],
        "conceptos_clave": [
            "Portero como +1 en construcción",
            "Amplitud para estirar pressing",
            "Pivote entre centrales o bajo presión",
            "Velocidad en pase (< 3 toques)",
            "Paciencia: esperar momento para romper presión"
        ],
        "referencias": "Guardiola, De Zerbi, Arteta"
    },

    "vs_bloque_medio": {
        "nombre": "Salida vs Bloque Medio",
        "descripcion": "El rival nos deja iniciar pero cierra medio campo.",
        "estrategias": [
            {
                "nombre": "Progresión por bandas",
                "descripcion": "Laterales suben, extremos al interior. Aprovechar amplitud.",
                "ventajas": ["Estirar bloque rival", "Centros al área", "1v1 en bandas"],
                "jugadores_clave": ["Laterales ofensivos", "Extremos en perfil cambiado", "Mediapunta"]
            },
            {
                "nombre": "Juego interior",
                "descripcion": "Circular balón por dentro buscando líneas de pase entre líneas",
                "ventajas": ["Atraer rival y liberar bandas", "Control del partido", "Cambios de orientación"],
                "jugadores_clave": ["Mediocampistas creativos", "Mediapunta/enganche", "Pivotes con visión"]
            },
            {
                "nombre": "Cambios de orientación",
                "descripcion": "Mover balón de banda a banda rápidamente para encontrar espacios",
                "ventajas": ["Desorganizar defensa rival", "Encontrar 1v1", "Generar superioridades"],
                "jugadores_clave": ["Jugadores con pase largo", "Laterales bien posicionados"]
            }
        ],
        "conceptos_clave": [
            "Paciencia en circulación",
            "Amplitud máxima (uso de bandas)",
            "Movimientos entre líneas",
            "Cambios de ritmo",
            "Aprovechar mediapunta como enlace"
        ],
        "referencias": "Ancelotti, Emery, Xavi"
    },

    "vs_bloque_bajo": {
        "nombre": "Salida vs Bloque Bajo (Rival Replegado)",
        "descripcion": "El rival defiende muy atrás. Necesitamos creatividad y paciencia.",
        "estrategias": [
            {
                "nombre": "Ataque posicional",
                "descripcion": "Circular balón hasta encontrar espacios. Paciencia extrema.",
                "ventajas": ["Control total", "Desgastar rival", "Pocas pérdidas peligrosas"],
                "jugadores_clave": ["Mediocampistas creativos", "Laterales con centro", "Delantero de referencia"]
            },
            {
                "nombre": "Amplitud + centro",
                "descripcion": "Llevar balón a banda, centrar al área. Juego directo.",
                "ventajas": ["Aprovechar físico", "Segundas jugadas", "Córners"],
                "jugadores_clave": ["Laterales", "Extremos", "Delanteros con juego aéreo"]
            },
            {
                "nombre": "Jugadores entre líneas",
                "descripcion": "Mediapunta o falso 9 entre defensa y medio rival. Recibir entre líneas.",
                "ventajas": ["Generar dudas en defensa", "Pases filtrados", "Remates desde fuera del área"],
                "jugadores_clave": ["Mediapunta", "Mediocampistas llegadores", "Rematadores de larga distancia"]
            }
        ],
        "conceptos_clave": [
            "Paciencia máxima (mantener posesión)",
            "Amplitud para estirar defensa",
            "Movimientos sin balón",
            "Remates de fuera del área",
            "Aprovechar balones parados (córners, faltas)"
        ],
        "referencias": "Guardiola vs buses, Xavi, Ancelotti"
    }
}


# ============================================================================
# TRANSICIONES
# ============================================================================

TRANSICIONES = {
    "def_ataque": {
        "nombre": "Transición Defensa → Ataque (Contraataque)",
        "descripcion": "Recuperamos balón y atacamos con velocidad",
        "opciones": [
            "Contraataque directo: máximo 3 pases al área rival",
            "Contraataque elaborado: progresión rápida pero con apoyo",
            "Contra-pressing: presión inmediata tras pérdida para recuperar rápido"
        ],
        "conceptos_clave": [
            "Velocidad en toma de decisiones",
            "Verticalidad en el pase",
            "Apoyo de jugadores desde atrás",
            "Aprovechar desorden rival"
        ]
    },
    "ataque_def": {
        "nombre": "Transición Ataque → Defensa (Repliegue)",
        "descripcion": "Perdemos balón, necesitamos reorganizarnos",
        "opciones": [
            "Pressing inmediato: presionar 5 segundos tras pérdida (gegenpressing)",
            "Repliegue intensivo: correr hacia atrás para organizarse",
            "Repliegue selectivo: algunos presionan, otros repliegan"
        ],
        "conceptos_clave": [
            "Presión inmediata (5-6 segundos)",
            "Basculaciones defensivas",
            "Cerrar líneas de pase centrales",
            "Evitar contragolpes peligrosos"
        ]
    }
}


# ============================================================================
# BALÓN PARADO
# ============================================================================

BALON_PARADO = {
    "ofensivo": {
        "corners": [
            "Córner corto: combinación para centro posterior",
            "Córner al primer palo: bloqueador + rematador",
            "Córner al segundo palo: zona de mayor efectividad",
            "Córner ensayado: jugada preparada"
        ],
        "faltas": [
            "Falta directa: jugador especialista",
            "Falta con barrera: combinación de 2-3 jugadores",
            "Falta al área: centro al área como córner"
        ],
        "saques_banda": [
            "Saque largo al área: como centro",
            "Saque corto: mantener posesión",
            "Saque rápido: sorprender al rival"
        ]
    },
    "defensivo": {
        "corners_contra": [
            "Defensa en zona: cada jugador defiende una zona del área",
            "Defensa mixta: zona + marcaje a jugadores peligrosos",
            "Defensa individual: cada jugador marca a un rival"
        ],
        "faltas_contra": [
            "Barrera de X jugadores según distancia",
            "Jugador en poste para proteger ángulo",
            "Contragolpe preparado tras despeje"
        ]
    }
}


# ============================================================================
# INSTRUCCIONES ESPECÍFICAS POR PUESTO
# ============================================================================

INSTRUCCIONES_PUESTOS = {
    "portero": [
        "Jugar como líbero (salir del área para despejar)",
        "Salida corta siempre que sea posible",
        "Balones largos a bandas cuando hay presión",
        "Comunicación constante con defensa"
    ],
    "defensas": [
        "Mantener línea (atención fuera de juego)",
        "Coberturas permanentes entre centrales",
        "Laterales: equilibrio entre defensa y ataque",
        "Basculaciones según posición del balón"
    ],
    "mediocampistas": [
        "Pivote: no subir en transiciones (equilibrio)",
        "Interiores: llegada al área en ataque",
        "Mediocentros: control del ritmo y circulación",
        "Presión coordinada según gatillo"
    ],
    "delanteros": [
        "Presión a centrales rivales (si bloque alto)",
        "Desmarques entre centrales rivales",
        "Movimientos a banda para arrastrar defensa",
        "Sacrificio defensivo en transición"
    ]
}


# ============================================================================
# FUNCIÓN PARA OBTENER OPCIONES
# ============================================================================

def obtener_todas_opciones():
    """Devuelve todas las opciones tácticas organizadas"""
    return {
        "defensiva": DEFENSIVA_OPCIONES,
        "ofensiva_salida": OFENSIVA_SALIDA,
        "transiciones": TRANSICIONES,
        "balon_parado": BALON_PARADO,
        "instrucciones_puestos": INSTRUCCIONES_PUESTOS
    }


def obtener_resumen_opcion(tipo, clave):
    """Devuelve un resumen breve de una opción específica"""
    opciones_map = {
        "defensiva": DEFENSIVA_OPCIONES,
        "ofensiva": OFENSIVA_SALIDA,
    }

    if tipo in opciones_map and clave in opciones_map[tipo]:
        opcion = opciones_map[tipo][clave]
        return {
            "nombre": opcion["nombre"],
            "descripcion": opcion["descripcion"],
            "cuando_usar": opcion.get("cuando_usar", "")
        }

    return None
