#!/usr/bin/env python3
"""
Analizador de IA para Notas de Partido
Club Atlético Central

Soporta:
- Groq (LLaMA) - Para análisis de texto rápido
- Google Gemini - Para dibujos tácticos precisos
"""

import os
import json
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar Groq con manejo de errores
try:
    from groq import Groq
    GROQ_DISPONIBLE = True
    print(f"✓ Groq importado correctamente", file=sys.stderr)
except ImportError as e:
    GROQ_DISPONIBLE = False
    print(f"⚠ Groq no disponible: {e}", file=sys.stderr)

# Importar Google Gemini con manejo de errores
try:
    import google.generativeai as genai
    GEMINI_DISPONIBLE = True
    print(f"✓ Google Gemini importado correctamente", file=sys.stderr)
except ImportError as e:
    GEMINI_DISPONIBLE = False
    print(f"⚠ Google Gemini no disponible: {e}", file=sys.stderr)


class IAAnalyzer:
    """
    Clase para analizar notas informales de partidos usando IA
    """

    def __init__(self, provider='groq'):
        """
        Inicializar analizador

        Args:
            provider: 'groq', 'claude', 'ollama', 'gemini'
        """
        self.provider = provider
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_key = os.getenv('GOOGLE_API_KEY')

        # Configurar Gemini si está disponible
        if GEMINI_DISPONIBLE and self.google_key:
            genai.configure(api_key=self.google_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            print(f"[IA] ✓ Gemini configurado correctamente", file=sys.stderr)
        else:
            self.gemini_model = None

        # Log para debugging
        print(f"[IA] Provider principal: {provider}", file=sys.stderr)
        if self.groq_key:
            print(f"[IA] ✓ GROQ_API_KEY encontrada", file=sys.stderr)
        if self.google_key:
            print(f"[IA] ✓ GOOGLE_API_KEY encontrada", file=sys.stderr)
        else:
            print(f"[IA] ⚠ GOOGLE_API_KEY no encontrada (Gemini no disponible)", file=sys.stderr)

    def analizar_notas_rival(self, notas_texto):
        """
        Analiza notas informales sobre el rival y devuelve datos estructurados

        Args:
            notas_texto: String con las notas del entrenador

        Returns:
            dict con datos estructurados del rival
        """
        prompt = self._construir_prompt_rival(notas_texto)

        try:
            if self.provider == 'groq':
                resultado = self._analizar_groq(prompt)
            elif self.provider == 'claude':
                resultado = self._analizar_claude(prompt)
            elif self.provider == 'ollama':
                resultado = self._analizar_ollama(prompt)
            else:
                raise ValueError(f"Provider '{self.provider}' no soportado")

            return {
                'success': True,
                'data': resultado
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generar_plan_tactico(self, datos_rival, notas_entrenador=''):
        """
        Genera sugerencias tácticas para combatir al rival

        Args:
            datos_rival: dict con datos del rival
            notas_entrenador: notas adicionales del entrenador

        Returns:
            dict con sugerencias tácticas
        """
        prompt = self._construir_prompt_plan(datos_rival, notas_entrenador)

        try:
            if self.provider == 'groq':
                resultado = self._analizar_groq(prompt)
            elif self.provider == 'claude':
                resultado = self._analizar_claude(prompt)
            elif self.provider == 'ollama':
                resultado = self._analizar_ollama(prompt)
            else:
                raise ValueError(f"Provider '{self.provider}' no soportado")

            return {
                'success': True,
                'data': resultado
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _construir_prompt_rival(self, notas):
        """Construye el prompt para analizar al rival por fases del juego"""
        return f"""Eres un analista táctico de fútbol profesional. Analiza estas notas de observación de un rival.

NOTAS DEL ENTRENADOR:
{notas}

Analiza el equipo rival por FASES DEL JUEGO. Sé específico, concreto y visual. Máximo 3-4 puntos por fase.

Devuelve ÚNICAMENTE un JSON válido con esta estructura:

{{
    "sistema_tactico": "4-3-3",

    "ataque": {{
        "vs_bloque_alto": {{
            "estructura": "Estructura de salida (ej: 4+1, portero+4 defensas+1 pivote)",
            "triangulos": "Triángulos clave de pase (ej: 1-4-6, Portero-DC-Pivote)",
            "patrones": ["Patrón 1", "Patrón 2", "Patrón 3"],
            "debilidad": "Debilidad específica a explotar",
            "fortaleza": "Principal fortaleza en salida de balón"
        }},
        "vs_bloque_medio": {{
            "jugadores_clave": "Quiénes destacan en progresión",
            "zonas_activas": "Bandas/centro, carrileros, etc",
            "patrones": ["Patrón 1", "Patrón 2", "Patrón 3"],
            "debilidad": "Debilidad específica",
            "fortaleza": "Principal fortaleza en progresión"
        }},
        "vs_bloque_bajo": {{
            "como_finalizan": "Centros, juego interior, etc",
            "jugadores_area": "Quiénes rematan",
            "patrones": ["Patrón 1", "Patrón 2"],
            "debilidad": "Debilidad específica",
            "fortaleza": "Principal fortaleza en finalización"
        }}
    }},

    "defensa": {{
        "pressing_alto": {{
            "estructura": "Sistema defensivo (ej: 4-4-2, 4-1-3-2)",
            "gatillos": "Cuándo presionan (ej: pase al DC)",
            "patrones": ["Patrón 1", "Patrón 2"],
            "debilidad": "Debilidad específica a explotar",
            "fortaleza": "Punto fuerte defensivo"
        }},
        "bloque_medio": {{
            "compactacion": "Distancia entre líneas, metros de bloque",
            "coberturas": "Cómo cubren espacios",
            "patrones": ["Patrón 1", "Patrón 2"],
            "debilidad": "Debilidad específica",
            "fortaleza": "Punto fuerte"
        }},
        "bloque_bajo": {{
            "organizacion": "Cómo se organizan en área",
            "marcajes": "Zona/individual/mixto",
            "patrones": ["Patrón 1", "Patrón 2"],
            "debilidad": "Debilidad específica",
            "fortaleza": "Principal fortaleza defensiva en bloque bajo"
        }}
    }},

    "transiciones": {{
        "def_atq": {{
            "velocidad": "Rápida/lenta/media",
            "jugadores_clave": "Quiénes protagonizan",
            "patrones": ["Patrón 1", "Patrón 2"],
            "como_cortar": "Cómo podemos cortarla",
            "fortaleza": "Principal fortaleza en transición ofensiva"
        }},
        "atq_def": {{
            "equilibrios": "Quiénes quedan en equilibrio al atacar",
            "repliegue": "Rápido/lento, pressing o repliegue",
            "patrones": ["Patrón 1", "Patrón 2"],
            "desbalance": "Dónde están expuestos",
            "fortaleza": "Principal fortaleza en transición defensiva"
        }}
    }},

    "abp": {{
        "corners_favor": "Estructura, ejecutor, zonas",
        "faltas_favor": "Ejecutores, estrategias",
        "corners_contra": "Organización defensiva",
        "debilidad": "Debilidad en ABP",
        "fortaleza": "Principal fortaleza en ABP"
    }},

    "jugadores_clave": [
        {{
            "numero": "10",
            "nombre": "Apellido",
            "posicion": "MC",
            "nivel": "peligroso",
            "caracteristicas": "Breve descripción"
        }}
    ]
}}"""

    def _construir_prompt_plan(self, datos_rival, notas_adicionales):
        """Construye el prompt para generar plan táctico"""
        return f"""Eres un entrenador táctico profesional de fútbol.
Basándote en el análisis del rival, sugiere las mejores opciones tácticas para combatirlo.

DATOS DEL RIVAL:
Sistema: {datos_rival.get('sistema_tactico', 'No especificado')}
Ataque: {datos_rival.get('ataque_organizado', '')}
Defensa: {datos_rival.get('defensa_organizada', '')}

{f"NOTAS ADICIONALES DEL ENTRENADOR: {notas_adicionales}" if notas_adicionales else ""}

Devuelve ÚNICAMENTE un JSON válido con sugerencias tácticas:

{{
    "bloque_defensivo_sugerido": "bloque_alto|bloque_medio|bloque_bajo",
    "justificacion_defensiva": "Por qué recomiendas ese bloque defensivo contra este rival",
    "salida_ofensiva_sugerida": "vs_bloque_alto|vs_bloque_medio|vs_bloque_bajo",
    "justificacion_ofensiva": "Por qué recomiendas esa salida ofensiva",
    "transicion_def_atq_sugerida": "directo|elaborado|contra_pressing",
    "transicion_atq_def_sugerida": "pressing_inmediato|repliegue_intensivo|repliegue_selectivo",
    "puntos_clave": [
        "Punto clave 1 a trabajar",
        "Punto clave 2 a trabajar"
    ]
}}"""

    def _analizar_groq(self, prompt):
        """Analiza usando Groq API"""
        if not self.groq_key:
            print("[IA] Error: API Key no configurada", file=sys.stderr)
            raise ValueError("API Key de Groq no configurada en variables de entorno")

        try:
            print("[IA] Inicializando cliente Groq...", file=sys.stderr)

            # Inicializar cliente - compatible con versiones antiguas y nuevas
            try:
                # Versión nueva (>0.10.0)
                client = Groq(api_key=self.groq_key)
            except TypeError as te:
                print(f"[IA] Error con versión nueva, intentando versión antigua: {te}", file=sys.stderr)
                # Versión antigua (0.4.x)
                import groq as groq_module
                client = groq_module.Client(api_key=self.groq_key)

            print("[IA] Cliente Groq inicializado, haciendo petición...", file=sys.stderr)

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un analista táctico de fútbol profesional. Respondes SIEMPRE en formato JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )

            print("[IA] Respuesta recibida, procesando...", file=sys.stderr)
            contenido = completion.choices[0].message.content

            # Limpiar markdown si existe
            contenido = contenido.strip()
            if contenido.startswith('```json'):
                contenido = contenido[7:]
            if contenido.startswith('```'):
                contenido = contenido[3:]
            if contenido.endswith('```'):
                contenido = contenido[:-3]
            contenido = contenido.strip()

            # Parsear JSON
            resultado = json.loads(contenido)
            print("[IA] ✓ Análisis completado exitosamente", file=sys.stderr)
            return resultado

        except Exception as e:
            print(f"[IA] ✗ Error en _analizar_groq: {type(e).__name__}: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise ValueError(f"Error al conectar con Groq: {type(e).__name__} - {str(e)}")

    def _analizar_claude(self, prompt):
        """Analiza usando Claude API"""
        if not self.claude_key:
            raise ValueError("ANTHROPIC_API_KEY no configurada en .env")

        try:
            import anthropic
        except ImportError:
            raise ImportError("Instala: pip install anthropic")

        client = anthropic.Anthropic(api_key=self.claude_key)

        message = client.messages.create(
            model="claude-3-haiku-20240307",  # Modelo barato
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        contenido = message.content[0].text

        # Limpiar y parsear
        contenido = contenido.strip()
        if contenido.startswith('```json'):
            contenido = contenido[7:]
        if contenido.startswith('```'):
            contenido = contenido[3:]
        if contenido.endswith('```'):
            contenido = contenido[:-3]
        contenido = contenido.strip()

        return json.loads(contenido)

    def _analizar_ollama(self, prompt):
        """Analiza usando Ollama (local)"""
        url = "http://localhost:11434/api/generate"

        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        response = requests.post(url, json=data, timeout=60)
        response.raise_for_status()

        resultado = response.json()
        contenido = resultado['response']

        return json.loads(contenido)

    def generar_dibujo_tactico(self, fase, tipo, texto_tactico):
        """
        Genera instrucciones de dibujo para un campo táctico basándose en el texto

        PRIORIDAD: Gemini (mejor razonamiento espacial) > Groq (fallback)

        Args:
            fase: 'ataque', 'defensa', 'transicion', 'abp'
            tipo: subtipo de la fase (ej: 'vs_bloque_alto', 'pressing_alto', 'def_atq')
            texto_tactico: dict con los datos tácticos escritos por el usuario

        Returns:
            dict con instrucciones de dibujo (jugadores, flechas, zonas)
        """
        prompt = self._construir_prompt_dibujo(fase, tipo, texto_tactico)

        # Intentar con Gemini primero (mejor para dibujos)
        if self.gemini_model:
            try:
                print(f"[IA] Usando Gemini para dibujo {fase}/{tipo}", file=sys.stderr)
                resultado = self._analizar_gemini_dibujo(prompt)
                return {
                    'success': True,
                    'data': resultado,
                    'provider': 'gemini'
                }
            except Exception as e:
                print(f"[IA] Error Gemini, intentando Groq: {e}", file=sys.stderr)

        # Fallback a Groq
        try:
            print(f"[IA] Usando Groq para dibujo {fase}/{tipo}", file=sys.stderr)
            resultado = self._analizar_groq_dibujo(prompt)
            return {
                'success': True,
                'data': resultado,
                'provider': 'groq'
            }
        except Exception as e:
            print(f"[IA] Error generando dibujo: {e}", file=sys.stderr)
            return {
                'success': False,
                'data': self._dibujo_por_defecto(fase, tipo),
                'error': str(e)
            }

    def _construir_prompt_dibujo(self, fase, tipo, texto_tactico):
        """
        Construye prompt PROFESIONAL para generar instrucciones de dibujo táctico.
        Cada fase tiene instrucciones ultra-específicas.
        """

        # Prompts específicos por fase y tipo
        prompts_especificos = {
            'ataque': {
                'vs_bloque_alto': self._prompt_ataque_bloque_alto(texto_tactico),
                'vs_bloque_medio': self._prompt_ataque_bloque_medio(texto_tactico),
                'vs_bloque_bajo': self._prompt_ataque_bloque_bajo(texto_tactico),
            },
            'defensa': {
                'pressing_alto': self._prompt_defensa_pressing(texto_tactico),
                'bloque_medio': self._prompt_defensa_bloque_medio(texto_tactico),
                'bloque_bajo': self._prompt_defensa_bloque_bajo(texto_tactico),
            },
            'transicion': {
                'def_atq': self._prompt_transicion_contra(texto_tactico),
                'atq_def': self._prompt_transicion_repliegue(texto_tactico),
            },
            'abp': {
                'corners': self._prompt_abp_corners(texto_tactico),
                'faltas': self._prompt_abp_corners(texto_tactico),
            }
        }

        return prompts_especificos.get(fase, {}).get(tipo, self._prompt_generico(texto_tactico))

    def _prompt_ataque_bloque_alto(self, texto):
        """Prompt para SALIDA DE BALÓN del rival (fase de creación)"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - SALIDA DE BALÓN RIVAL

═══════════════════════════════════════════════════════════════
FASE: CREACIÓN - Cómo sale el RIVAL jugando desde atrás
ZONA DEL CAMPO: X = 65-95 (campo del rival, cerca de su portería)
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO SOBRE ESTA FASE:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO:

1. ESTRUCTURA DE SALIDA:
   - Si menciona "4+1" o "5 jugadores": Portero (X=92, Y=50) + 4 defensas + pivote
   - Si menciona "3+2": 3 centrales + 2 pivotes
   - Posiciona según el ESQUEMA mencionado

2. TRIÁNGULOS DE PASE:
   - Si menciona triángulos (ej: "1-4-6"): Dibuja flechas BLANCAS conectando esos dorsales
   - Representa las líneas de pase con flechas tipo "pase"

3. JUGADORES CLAVE:
   - Jugadores MENCIONADOS por número → color AMARILLO, destacado=true
   - Resto de la estructura → color ROJO, destacado=false

4. ZONAS:
   - Si menciona "salida por bandas" → zona VERDE en X=70-85, Y=10-30 o Y=70-90
   - Si menciona "salida por centro" → zona VERDE en X=70-85, Y=35-65

POSICIONES ESTÁNDAR SALIDA (si menciona estructura):
- Portero: X=92, Y=50
- Central derecho: X=80, Y=35
- Central izquierdo: X=80, Y=65
- Lateral derecho: X=78, Y=15
- Lateral izquierdo: X=78, Y=85
- Pivote: X=68, Y=50

COORDENADAS: X=0 nuestra portería, X=100 portería rival. Y=0 banda inferior, Y=100 banda superior.

DEVUELVE ÚNICAMENTE ESTE JSON:
{{
    "jugadores": [{{"x": 92, "y": 50, "numero": "1", "color": "amarillo", "destacado": true}}],
    "flechas": [{{"x1": 92, "y1": 50, "x2": 80, "y2": 40, "color": "blanco", "tipo": "pase"}}],
    "zonas": [{{"x": 70, "y": 25, "ancho": 18, "alto": 50, "color": "verde", "nombre": "Salida"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _prompt_ataque_bloque_medio(self, texto):
        """Prompt para PROGRESIÓN del rival (fase de creación/progresión)"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - PROGRESIÓN RIVAL

═══════════════════════════════════════════════════════════════
FASE: PROGRESIÓN - Cómo el RIVAL avanza por zona media
ZONA DEL CAMPO: X = 35-65 (centro del campo)
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO:

1. JUGADORES CREATIVOS:
   - Si menciona números (ej: "10 y 8") → dibújalos en AMARILLO destacado
   - Posición: centrocampistas en X=45-55, Y según posición (interior/banda)

2. ZONAS ACTIVAS:
   - "Bandas" → zonas NARANJAS en Y=5-25 y/o Y=75-95
   - "Centro" → zona NARANJA en Y=35-65
   - "Entre líneas" → zona VERDE en X=40-55

3. MOVIMIENTOS/PATRONES:
   - "Cambios de orientación" → flecha AMARILLA de banda a banda
   - "Juego interior" → flechas hacia el centro
   - "Desmarques de ruptura" → flechas VERDES hacia portería (hacia X bajo)

4. ESTRUCTURA EN PROGRESIÓN:
   - Centrocampista creativo: X=50, Y=50 (si es mediapunta)
   - Interiores: X=48, Y=30 y Y=70
   - Extremos progresando: X=40, Y=15 y Y=85

DEVUELVE ÚNICAMENTE ESTE JSON:
{{
    "jugadores": [{{"x": 50, "y": 50, "numero": "10", "color": "amarillo", "destacado": true}}],
    "flechas": [{{"x1": 50, "y1": 50, "x2": 35, "y2": 50, "color": "amarillo", "tipo": "movimiento"}}],
    "zonas": [{{"x": 38, "y": 20, "ancho": 20, "alto": 60, "color": "naranja", "nombre": "Creación"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _prompt_ataque_bloque_bajo(self, texto):
        """Prompt para FINALIZACIÓN del rival"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - FINALIZACIÓN RIVAL

═══════════════════════════════════════════════════════════════
FASE: FINALIZACIÓN - Cómo el RIVAL ataca nuestra área
ZONA DEL CAMPO: X = 5-30 (nuestro campo, cerca de nuestra portería)
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO:

1. REMATADORES:
   - Si menciona "9" o delantero centro → X=15, Y=50 en AMARILLO
   - Si menciona "primer palo" → jugador en Y=35-45
   - Si menciona "segundo palo" → jugador en Y=55-65
   - Extremos rematando: X=18, Y=20 y Y=80

2. CENTROS LATERALES:
   - Si menciona "centros" → flechas desde X=8-12, Y=10 o Y=90 hacia el área
   - Color AMARILLO, tipo "pase"

3. ZONA DE REMATE:
   - Dibuja zona ROJA en X=5-20, Y=25-75 (área de peligro)

4. MOVIMIENTOS DE ATAQUE:
   - "Atacan primer palo" → flecha hacia Y=40
   - "Atacan segundo palo" → flecha hacia Y=60
   - "Segunda jugada" → jugador en X=25 esperando rechace

POSICIONES FINALIZACIÓN:
- Delantero centro: X=15, Y=50
- Extremo derecho rematando: X=18, Y=25
- Extremo izquierdo rematando: X=18, Y=75
- Mediapunta llegando: X=22, Y=50

DEVUELVE ÚNICAMENTE ESTE JSON:
{{
    "jugadores": [{{"x": 15, "y": 50, "numero": "9", "color": "amarillo", "destacado": true}}],
    "flechas": [{{"x1": 8, "y1": 90, "x2": 15, "y2": 55, "color": "amarillo", "tipo": "pase"}}],
    "zonas": [{{"x": 5, "y": 25, "ancho": 18, "alto": 50, "color": "rojo", "nombre": "Peligro"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _prompt_defensa_pressing(self, texto):
        """Prompt para PRESSING ALTO del rival"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - PRESSING ALTO RIVAL

═══════════════════════════════════════════════════════════════
FASE: PRESSING ALTO - Cómo el RIVAL nos presiona en salida
ZONA DEL CAMPO: X = 55-90 (presionan en nuestro campo)
IMPORTANTE: DIBUJAR LOS 11 JUGADORES COMPLETOS
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO - OBLIGATORIO DIBUJAR LOS 11:

1. PORTERO (1 jugador):
   - Portero: X=95, Y=50, numero="1", color="rojo"

2. LÍNEA DEFENSIVA (4 jugadores):
   - Lateral derecho: X=75, Y=15, numero="2", color="rojo"
   - Central derecho: X=75, Y=38, numero="4", color="rojo"
   - Central izquierdo: X=75, Y=62, numero="5", color="rojo"
   - Lateral izquierdo: X=75, Y=85, numero="3", color="rojo"

3. LÍNEA DE MEDIOS (4 jugadores):
   - Medio derecho: X=65, Y=18, numero="7", color="rojo"
   - Medio centro-derecho: X=65, Y=40, numero="8", color="rojo"
   - Medio centro-izquierdo: X=65, Y=60, numero="6", color="rojo"
   - Medio izquierdo: X=65, Y=82, numero="11", color="rojo"

4. LÍNEA DE ATAQUE/PRESSING (2 jugadores - los que presionan):
   - Delantero derecho: X=55, Y=40, numero="10", color="amarillo", destacado=true
   - Delantero izquierdo: X=55, Y=60, numero="9", color="amarillo", destacado=true

5. LÍNEA DE PRESSING:
   - SIEMPRE linea_tactica activa=true
   - X=58, color ROJO, etiqueta "Pressing"

6. FLECHAS DE PRESSING:
   - Flechas ROJAS desde los 2 delanteros hacia donde presionan (hacia X=45-50)

7. ZONA DE ESPACIO (si menciona debilidad):
   - Zona VERDE detrás de la línea defensiva (X=78-90)

DEVUELVE ÚNICAMENTE ESTE JSON CON LOS 11 JUGADORES:
{{
    "jugadores": [
        {{"x": 95, "y": 50, "numero": "1", "color": "rojo", "destacado": false}},
        {{"x": 75, "y": 15, "numero": "2", "color": "rojo", "destacado": false}},
        {{"x": 75, "y": 38, "numero": "4", "color": "rojo", "destacado": false}},
        {{"x": 75, "y": 62, "numero": "5", "color": "rojo", "destacado": false}},
        {{"x": 75, "y": 85, "numero": "3", "color": "rojo", "destacado": false}},
        {{"x": 65, "y": 18, "numero": "7", "color": "rojo", "destacado": false}},
        {{"x": 65, "y": 40, "numero": "8", "color": "rojo", "destacado": false}},
        {{"x": 65, "y": 60, "numero": "6", "color": "rojo", "destacado": false}},
        {{"x": 65, "y": 82, "numero": "11", "color": "rojo", "destacado": false}},
        {{"x": 55, "y": 40, "numero": "10", "color": "amarillo", "destacado": true}},
        {{"x": 55, "y": 60, "numero": "9", "color": "amarillo", "destacado": true}}
    ],
    "flechas": [
        {{"x1": 55, "y1": 40, "x2": 45, "y2": 38, "color": "rojo", "tipo": "pressing"}},
        {{"x1": 55, "y1": 60, "x2": 45, "y2": 62, "color": "rojo", "tipo": "pressing"}}
    ],
    "zonas": [{{"x": 78, "y": 20, "ancho": 15, "alto": 60, "color": "verde", "nombre": "Espacio"}}],
    "linea_tactica": {{"activa": true, "x": 58, "color": "rojo", "etiqueta": "Pressing"}}
}}"""

    def _prompt_defensa_bloque_medio(self, texto):
        """Prompt para BLOQUE MEDIO del rival"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - BLOQUE MEDIO RIVAL

═══════════════════════════════════════════════════════════════
FASE: BLOQUE MEDIO - Cómo el RIVAL defiende en zona media
ZONA DEL CAMPO: X = 40-70 (centro del campo)
IMPORTANTE: DIBUJAR LOS 11 JUGADORES COMPLETOS
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO - OBLIGATORIO DIBUJAR LOS 11:

1. PORTERO (1 jugador):
   - Portero: X=95, Y=50, numero="1", color="rojo"

2. LÍNEA DEFENSIVA (4 jugadores) - COMPACTA:
   - Lateral derecho: X=62, Y=15, numero="2", color="rojo"
   - Central derecho: X=62, Y=38, numero="4", color="rojo"
   - Central izquierdo: X=62, Y=62, numero="5", color="rojo"
   - Lateral izquierdo: X=62, Y=85, numero="3", color="rojo"

3. LÍNEA DE MEDIOS (4 jugadores) - COMPACTA cerca de defensa:
   - Medio derecho: X=52, Y=18, numero="7", color="rojo"
   - Medio centro-derecho: X=52, Y=40, numero="8", color="rojo"
   - Medio centro-izquierdo: X=52, Y=60, numero="6", color="rojo"
   - Medio izquierdo: X=52, Y=82, numero="11", color="rojo"

4. LÍNEA DE ATAQUE (2 jugadores) - Esperando contraataque:
   - Delantero derecho: X=40, Y=40, numero="10", color="amarillo", destacado=true
   - Delantero izquierdo: X=40, Y=60, numero="9", color="amarillo", destacado=true

5. LÍNEA TÁCTICA:
   - linea_tactica activa=true
   - X=57, color NARANJA, etiqueta "Bloque medio"
   - Representa la zona compacta del bloque

6. COBERTURAS (si menciona):
   - Flechas BLANCAS cortas entre defensas y medios (basculaciones)

7. ZONA ENTRE LÍNEAS (para explotar):
   - Zona VERDE entre defensa y medios: X=55-60, Y=25-75

DEVUELVE ÚNICAMENTE ESTE JSON CON LOS 11 JUGADORES:
{{
    "jugadores": [
        {{"x": 95, "y": 50, "numero": "1", "color": "rojo", "destacado": false}},
        {{"x": 62, "y": 15, "numero": "2", "color": "rojo", "destacado": false}},
        {{"x": 62, "y": 38, "numero": "4", "color": "rojo", "destacado": false}},
        {{"x": 62, "y": 62, "numero": "5", "color": "rojo", "destacado": false}},
        {{"x": 62, "y": 85, "numero": "3", "color": "rojo", "destacado": false}},
        {{"x": 52, "y": 18, "numero": "7", "color": "rojo", "destacado": false}},
        {{"x": 52, "y": 40, "numero": "8", "color": "rojo", "destacado": false}},
        {{"x": 52, "y": 60, "numero": "6", "color": "rojo", "destacado": false}},
        {{"x": 52, "y": 82, "numero": "11", "color": "rojo", "destacado": false}},
        {{"x": 40, "y": 40, "numero": "10", "color": "amarillo", "destacado": true}},
        {{"x": 40, "y": 60, "numero": "9", "color": "amarillo", "destacado": true}}
    ],
    "flechas": [
        {{"x1": 52, "y1": 40, "x2": 52, "y2": 60, "color": "blanco", "tipo": "cobertura"}},
        {{"x1": 62, "y1": 38, "x2": 62, "y2": 62, "color": "blanco", "tipo": "cobertura"}}
    ],
    "zonas": [{{"x": 55, "y": 25, "ancho": 8, "alto": 50, "color": "verde", "nombre": "Entre líneas"}}],
    "linea_tactica": {{"activa": true, "x": 57, "color": "naranja", "etiqueta": "Bloque medio"}}
}}"""

    def _prompt_defensa_bloque_bajo(self, texto):
        """Prompt para BLOQUE BAJO del rival"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - BLOQUE BAJO RIVAL

═══════════════════════════════════════════════════════════════
FASE: BLOQUE BAJO - Cómo el RIVAL defiende en su área
ZONA DEL CAMPO: X = 65-95 (campo del rival, su área)
IMPORTANTE: DIBUJAR LOS 11 JUGADORES COMPLETOS
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO - OBLIGATORIO DIBUJAR LOS 11:

1. PORTERO (1 jugador):
   - Portero: X=95, Y=50, numero="1", color="rojo"

2. LÍNEA DEFENSIVA (4 jugadores) - MUY ATRÁS cerca de área:
   - Lateral derecho: X=85, Y=20, numero="2", color="rojo"
   - Central derecho: X=87, Y=40, numero="4", color="rojo"
   - Central izquierdo: X=87, Y=60, numero="5", color="rojo"
   - Lateral izquierdo: X=85, Y=80, numero="3", color="rojo"

3. LÍNEA DE MEDIOS (4 jugadores) - MUY CERCA de la defensa (7-10 unidades):
   - Medio derecho: X=78, Y=22, numero="7", color="rojo"
   - Medio centro-derecho: X=78, Y=40, numero="8", color="rojo"
   - Medio centro-izquierdo: X=78, Y=60, numero="6", color="rojo"
   - Medio izquierdo: X=78, Y=78, numero="11", color="rojo"

4. LÍNEA DE ATAQUE (2 jugadores) - Referencias para contraataque:
   - Delantero derecho: X=65, Y=40, numero="10", color="amarillo", destacado=true
   - Delantero izquierdo: X=65, Y=60, numero="9", color="amarillo", destacado=true

5. LÍNEA TÁCTICA:
   - linea_tactica activa=true
   - X=82, color AZUL, etiqueta "Bloque bajo"
   - Representa el bloque compacto muy atrás

6. ZONA ENTRE CENTRALES (si menciona debilidad):
   - Zona VERDE en X=85-92, Y=42-58

7. SEGUNDOS PALOS (si menciona debilidad):
   - Zona VERDE en Y=75-90 o Y=10-25

DEVUELVE ÚNICAMENTE ESTE JSON CON LOS 11 JUGADORES:
{{
    "jugadores": [
        {{"x": 95, "y": 50, "numero": "1", "color": "rojo", "destacado": false}},
        {{"x": 85, "y": 20, "numero": "2", "color": "rojo", "destacado": false}},
        {{"x": 87, "y": 40, "numero": "4", "color": "rojo", "destacado": false}},
        {{"x": 87, "y": 60, "numero": "5", "color": "rojo", "destacado": false}},
        {{"x": 85, "y": 80, "numero": "3", "color": "rojo", "destacado": false}},
        {{"x": 78, "y": 22, "numero": "7", "color": "rojo", "destacado": false}},
        {{"x": 78, "y": 40, "numero": "8", "color": "rojo", "destacado": false}},
        {{"x": 78, "y": 60, "numero": "6", "color": "rojo", "destacado": false}},
        {{"x": 78, "y": 78, "numero": "11", "color": "rojo", "destacado": false}},
        {{"x": 65, "y": 40, "numero": "10", "color": "amarillo", "destacado": true}},
        {{"x": 65, "y": 60, "numero": "9", "color": "amarillo", "destacado": true}}
    ],
    "flechas": [],
    "zonas": [{{"x": 85, "y": 42, "ancho": 8, "alto": 16, "color": "verde", "nombre": "Entre centrales"}}],
    "linea_tactica": {{"activa": true, "x": 82, "color": "azul", "etiqueta": "Bloque bajo"}}
}}"""

    def _prompt_transicion_contra(self, texto):
        """Prompt para CONTRAATAQUE del rival (DEF → ATQ)"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - CONTRAATAQUE RIVAL

═══════════════════════════════════════════════════════════════
FASE: TRANSICIÓN OFENSIVA - Contraataque del RIVAL
ZONA DEL CAMPO: X = 30-70 (todo el campo en transición)
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO:

1. VELOCIDAD DE TRANSICIÓN:
   - Si "muy rápida" → flechas VERDES largas y directas hacia nuestra portería
   - Si "progresiva" → flechas más cortas, escalonadas

2. JUGADORES EN TRANSICIÓN:
   - Si menciona números → dibújalos en AMARILLO
   - "Extremos corren" → jugadores en Y=15 y Y=85 con flechas hacia X=10
   - "10 organiza" → jugador en X=50, Y=50 con flechas de pase

3. CARRERAS:
   - Flechas VERDES tipo "carrera" desde zona de recuperación (X=55-65) hacia nuestra área (X=15-25)
   - Carreras diagonales por bandas

4. ZONA DE RECUPERACIÓN:
   - Dibuja zona VERDE en X=50-65 donde recuperan

5. CÓMO CORTAR:
   - Si menciona "falta táctica" → zona ROJA donde hacer falta

POSICIONES CONTRAATAQUE:
- Jugador que recupera: X=55, Y=50
- Extremo derecho corriendo: X=40→20, Y=20
- Extremo izquierdo corriendo: X=40→20, Y=80
- Delantero esperando: X=25, Y=50

DEVUELVE ÚNICAMENTE ESTE JSON:
{{
    "jugadores": [{{"x": 55, "y": 50, "numero": "10", "color": "amarillo", "destacado": true}}],
    "flechas": [{{"x1": 55, "y1": 50, "x2": 25, "y2": 50, "color": "verde", "tipo": "carrera"}}],
    "zonas": [{{"x": 50, "y": 30, "ancho": 18, "alto": 40, "color": "verde", "nombre": "Recuperación"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _prompt_transicion_repliegue(self, texto):
        """Prompt para REPLIEGUE del rival (ATQ → DEF)"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - REPLIEGUE RIVAL

═══════════════════════════════════════════════════════════════
FASE: TRANSICIÓN DEFENSIVA - Repliegue del RIVAL
ZONA DEL CAMPO: X = 40-80 (volviendo a defender)
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO:

1. EQUILIBRIOS:
   - Si menciona "centrales + pivote" → 3 jugadores en X=70-75 quedándose
   - Dibújalos en ROJO (son los que equilibran)

2. REPLIEGUE:
   - Si "ordenado" → flechas paralelas volviendo
   - Si "lento" → marca zona de DESBALANCE

3. ZONAS DE DESBALANCE (A EXPLOTAR):
   - Si menciona "laterales adelantados" → zona VERDE en X=50-65, Y=10-30 o Y=70-90
   - Son los espacios que podemos atacar cuando pierden balón

4. FLECHAS DE REPLIEGUE:
   - Flechas ROJAS tipo "movimiento" volviendo hacia su portería (hacia X alto)

POSICIONES REPLIEGUE:
- Pivote equilibrando: X=70, Y=50
- Centrales: X=75, Y=40 y Y=60
- Laterales volviendo: X=55→70, Y=20 y Y=80 (flechas)
- Zona de desbalance: donde están los laterales fuera de posición

DEVUELVE ÚNICAMENTE ESTE JSON:
{{
    "jugadores": [{{"x": 70, "y": 50, "numero": "6", "color": "rojo", "destacado": false}}],
    "flechas": [{{"x1": 55, "y1": 20, "x2": 70, "y2": 25, "color": "rojo", "tipo": "movimiento"}}],
    "zonas": [{{"x": 50, "y": 10, "ancho": 20, "alto": 25, "color": "verde", "nombre": "Desbalance"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _prompt_abp_corners(self, texto):
        """Prompt para ABP - Corners y Faltas"""
        return f"""ANALISTA TÁCTICO PROFESIONAL - ACCIONES A BALÓN PARADO

═══════════════════════════════════════════════════════════════
FASE: ABP - Corners y Faltas del RIVAL
ZONA DEL CAMPO: X = 5-25 (nuestra área, donde atacan)
═══════════════════════════════════════════════════════════════

DATOS DEL USUARIO:
{json.dumps(texto, indent=2, ensure_ascii=False)}

INSTRUCCIONES DE DIBUJO:

1. EJECUTOR:
   - Corner: X=3, Y=95 (esquina superior) o Y=5 (esquina inferior)
   - Falta: posición según distancia mencionada
   - Color AMARILLO, destacado=true

2. REMATADORES:
   - Si menciona "primer palo" → jugador en X=12, Y=40
   - Si menciona "segundo palo" → jugador en X=12, Y=65
   - Si menciona dorsales → usa esos números

3. TRAYECTORIA:
   - Flecha AMARILLA desde ejecutor hacia zona de remate
   - Tipo "pase"

4. ZONA DE REMATE:
   - Zona MORADA en X=8-18, Y=30-70

5. DEFENSA DE CORNERS:
   - Si menciona "defensa mixta" → algunos marcando, otros en zona
   - Si menciona "vulnerable segundo palo" → zona VERDE ahí

DEVUELVE ÚNICAMENTE ESTE JSON:
{{
    "jugadores": [{{"x": 3, "y": 95, "numero": "10", "color": "amarillo", "destacado": true}}],
    "flechas": [{{"x1": 3, "y1": 95, "x2": 12, "y2": 55, "color": "amarillo", "tipo": "pase"}}],
    "zonas": [{{"x": 8, "y": 30, "ancho": 12, "alto": 40, "color": "morado", "nombre": "Remate"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _prompt_generico(self, texto):
        """Prompt genérico de fallback"""
        return f"""ANALISTA TÁCTICO - Genera dibujo según el texto

DATOS:
{json.dumps(texto, indent=2, ensure_ascii=False)}

COORDENADAS: X=0-100 (0=nuestra portería, 100=rival), Y=0-100 (bandas)

DEVUELVE SOLO JSON:
{{
    "jugadores": [{{"x": 50, "y": 50, "numero": "10", "color": "amarillo", "destacado": true}}],
    "flechas": [{{"x1": 50, "y1": 50, "x2": 30, "y2": 50, "color": "blanco", "tipo": "pase"}}],
    "zonas": [{{"x": 40, "y": 30, "ancho": 20, "alto": 40, "color": "verde", "nombre": "Zona"}}],
    "linea_tactica": {{"activa": false, "x": 50, "color": "rojo", "etiqueta": ""}}
}}"""

    def _analizar_groq_dibujo(self, prompt):
        """Analiza usando Groq para generar dibujos - VERSIÓN PRECISA"""
        if not self.groq_key:
            raise ValueError("API Key de Groq no configurada")

        try:
            client = Groq(api_key=self.groq_key)

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un analista táctico de fútbol que genera dibujos PRECISOS.

REGLAS CRÍTICAS:
1. SOLO dibuja elementos MENCIONADOS en el texto del usuario
2. NO inventes jugadores, flechas o zonas que no estén en el texto
3. Respeta SIEMPRE las coordenadas X indicadas para cada fase
4. Devuelve ÚNICAMENTE JSON válido, sin explicaciones
5. Si el texto menciona números de jugadores específicos (ej: "el 10"), usa ESE número
6. Si menciona una estructura (ej: "4+1"), dibuja EXACTAMENTE esos jugadores"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,  # Más bajo = más preciso, menos inventivo
                max_tokens=1500
            )

            contenido = completion.choices[0].message.content.strip()

            if contenido.startswith('```json'):
                contenido = contenido[7:]
            if contenido.startswith('```'):
                contenido = contenido[3:]
            if contenido.endswith('```'):
                contenido = contenido[:-3]
            contenido = contenido.strip()

            return json.loads(contenido)

        except Exception as e:
            print(f"[IA] Error en dibujo Groq: {e}", file=sys.stderr)
            raise

    def _analizar_gemini_dibujo(self, prompt):
        """
        Analiza usando Google Gemini para generar dibujos tácticos

        Gemini tiene mejor razonamiento espacial que LLaMA, ideal para
        posicionar jugadores y flechas en coordenadas precisas.
        """
        if not self.gemini_model:
            raise ValueError("Gemini no configurado")

        try:
            # Prompt de sistema integrado para Gemini
            full_prompt = f"""Eres un analista táctico de fútbol profesional especializado en visualización.

INSTRUCCIONES CRÍTICAS:
1. SOLO dibuja elementos EXPLÍCITAMENTE mencionados en el texto
2. NO inventes ni añadas elementos que no estén descritos
3. Respeta EXACTAMENTE las coordenadas X indicadas para cada zona del campo
4. Si menciona números de jugadores (ej: "el 10", "el 9"), usa ESOS números
5. Si menciona una estructura (ej: "4+1", "4-4-2"), dibuja EXACTAMENTE esos jugadores
6. Las flechas SOLO para movimientos/pases que se describan
7. Devuelve ÚNICAMENTE el JSON, sin explicaciones ni comentarios

{prompt}"""

            # Configuración para respuestas precisas
            generation_config = genai.types.GenerationConfig(
                temperature=0.1,  # Muy bajo para máxima precisión
                max_output_tokens=2000,
            )

            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=generation_config
            )

            contenido = response.text.strip()

            # Limpiar markdown si existe
            if contenido.startswith('```json'):
                contenido = contenido[7:]
            if contenido.startswith('```'):
                contenido = contenido[3:]
            if contenido.endswith('```'):
                contenido = contenido[:-3]
            contenido = contenido.strip()

            resultado = json.loads(contenido)
            print(f"[IA] Gemini generó dibujo con {len(resultado.get('jugadores', []))} jugadores", file=sys.stderr)
            return resultado

        except Exception as e:
            print(f"[IA] Error en dibujo Gemini: {e}", file=sys.stderr)
            raise

    def _dibujo_por_defecto(self, fase, tipo):
        """Devuelve un dibujo por defecto si la IA falla"""
        defaults = {
            'ataque': {
                'vs_bloque_alto': {
                    'jugadores': [
                        {'x': 92, 'y': 50, 'numero': '1', 'color': 'amarillo', 'destacado': True},
                        {'x': 78, 'y': 30, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 78, 'y': 70, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 65, 'y': 50, 'numero': '6', 'color': 'amarillo', 'destacado': True},
                    ],
                    'flechas': [
                        {'x1': 88, 'y1': 50, 'x2': 80, 'y2': 35, 'color': 'blanco', 'tipo': 'pase'},
                        {'x1': 76, 'y1': 32, 'x2': 68, 'y2': 48, 'color': 'blanco', 'tipo': 'pase'},
                    ],
                    'zonas': [
                        {'x': 70, 'y': 25, 'ancho': 22, 'alto': 50, 'color': 'verde', 'nombre': 'Salida'}
                    ],
                    'linea_tactica': {'activa': False}
                },
                'vs_bloque_medio': {
                    'jugadores': [
                        {'x': 55, 'y': 50, 'numero': '8', 'color': 'amarillo', 'destacado': True},
                        {'x': 50, 'y': 25, 'numero': '10', 'color': 'amarillo', 'destacado': True},
                        {'x': 40, 'y': 15, 'numero': '7', 'color': 'rojo', 'destacado': False},
                        {'x': 40, 'y': 85, 'numero': '11', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [
                        {'x1': 52, 'y1': 50, 'x2': 35, 'y2': 50, 'color': 'amarillo', 'tipo': 'movimiento'},
                        {'x1': 48, 'y1': 27, 'x2': 38, 'y2': 20, 'color': 'amarillo', 'tipo': 'pase'},
                    ],
                    'zonas': [
                        {'x': 40, 'y': 15, 'ancho': 25, 'alto': 70, 'color': 'naranja', 'nombre': 'Creación'}
                    ],
                    'linea_tactica': {'activa': False}
                },
                'vs_bloque_bajo': {
                    'jugadores': [
                        {'x': 22, 'y': 50, 'numero': '9', 'color': 'rojo', 'destacado': True},
                        {'x': 25, 'y': 30, 'numero': '7', 'color': 'rojo', 'destacado': False},
                        {'x': 25, 'y': 70, 'numero': '11', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [
                        {'x1': 35, 'y1': 10, 'x2': 22, 'y2': 40, 'color': 'amarillo', 'tipo': 'pase'},
                        {'x1': 35, 'y1': 90, 'x2': 22, 'y2': 60, 'color': 'amarillo', 'tipo': 'pase'},
                    ],
                    'zonas': [
                        {'x': 8, 'y': 20, 'ancho': 22, 'alto': 60, 'color': 'rojo', 'nombre': 'Área'}
                    ],
                    'linea_tactica': {'activa': False}
                }
            },
            'defensa': {
                'pressing_alto': {
                    'jugadores': [
                        # 11 jugadores completos - pressing alto
                        {'x': 95, 'y': 50, 'numero': '1', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 15, 'numero': '2', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 38, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 62, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 85, 'numero': '3', 'color': 'rojo', 'destacado': False},
                        {'x': 65, 'y': 18, 'numero': '7', 'color': 'rojo', 'destacado': False},
                        {'x': 65, 'y': 40, 'numero': '8', 'color': 'rojo', 'destacado': False},
                        {'x': 65, 'y': 60, 'numero': '6', 'color': 'rojo', 'destacado': False},
                        {'x': 65, 'y': 82, 'numero': '11', 'color': 'rojo', 'destacado': False},
                        {'x': 55, 'y': 40, 'numero': '10', 'color': 'amarillo', 'destacado': True},
                        {'x': 55, 'y': 60, 'numero': '9', 'color': 'amarillo', 'destacado': True},
                    ],
                    'flechas': [
                        {'x1': 55, 'y1': 40, 'x2': 45, 'y2': 38, 'color': 'rojo', 'tipo': 'pressing'},
                        {'x1': 55, 'y1': 60, 'x2': 45, 'y2': 62, 'color': 'rojo', 'tipo': 'pressing'},
                    ],
                    'zonas': [
                        {'x': 78, 'y': 20, 'ancho': 15, 'alto': 60, 'color': 'verde', 'nombre': 'Espacio'}
                    ],
                    'linea_tactica': {'activa': True, 'x': 58, 'color': 'rojo', 'etiqueta': 'Pressing'}
                },
                'bloque_medio': {
                    'jugadores': [
                        # 11 jugadores completos - bloque medio compacto
                        {'x': 95, 'y': 50, 'numero': '1', 'color': 'rojo', 'destacado': False},
                        {'x': 62, 'y': 15, 'numero': '2', 'color': 'rojo', 'destacado': False},
                        {'x': 62, 'y': 38, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 62, 'y': 62, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 62, 'y': 85, 'numero': '3', 'color': 'rojo', 'destacado': False},
                        {'x': 52, 'y': 18, 'numero': '7', 'color': 'rojo', 'destacado': False},
                        {'x': 52, 'y': 40, 'numero': '8', 'color': 'rojo', 'destacado': False},
                        {'x': 52, 'y': 60, 'numero': '6', 'color': 'rojo', 'destacado': False},
                        {'x': 52, 'y': 82, 'numero': '11', 'color': 'rojo', 'destacado': False},
                        {'x': 40, 'y': 40, 'numero': '10', 'color': 'amarillo', 'destacado': True},
                        {'x': 40, 'y': 60, 'numero': '9', 'color': 'amarillo', 'destacado': True},
                    ],
                    'flechas': [
                        {'x1': 52, 'y1': 40, 'x2': 52, 'y2': 60, 'color': 'blanco', 'tipo': 'cobertura'},
                        {'x1': 62, 'y1': 38, 'x2': 62, 'y2': 62, 'color': 'blanco', 'tipo': 'cobertura'},
                    ],
                    'zonas': [
                        {'x': 55, 'y': 25, 'ancho': 8, 'alto': 50, 'color': 'verde', 'nombre': 'Entre líneas'}
                    ],
                    'linea_tactica': {'activa': True, 'x': 57, 'color': 'naranja', 'etiqueta': 'Bloque medio'}
                },
                'bloque_bajo': {
                    'jugadores': [
                        # 11 jugadores completos - bloque bajo muy junto
                        {'x': 95, 'y': 50, 'numero': '1', 'color': 'rojo', 'destacado': False},
                        {'x': 85, 'y': 20, 'numero': '2', 'color': 'rojo', 'destacado': False},
                        {'x': 87, 'y': 40, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 87, 'y': 60, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 85, 'y': 80, 'numero': '3', 'color': 'rojo', 'destacado': False},
                        {'x': 78, 'y': 22, 'numero': '7', 'color': 'rojo', 'destacado': False},
                        {'x': 78, 'y': 40, 'numero': '8', 'color': 'rojo', 'destacado': False},
                        {'x': 78, 'y': 60, 'numero': '6', 'color': 'rojo', 'destacado': False},
                        {'x': 78, 'y': 78, 'numero': '11', 'color': 'rojo', 'destacado': False},
                        {'x': 65, 'y': 40, 'numero': '10', 'color': 'amarillo', 'destacado': True},
                        {'x': 65, 'y': 60, 'numero': '9', 'color': 'amarillo', 'destacado': True},
                    ],
                    'flechas': [],
                    'zonas': [
                        {'x': 85, 'y': 42, 'ancho': 8, 'alto': 16, 'color': 'verde', 'nombre': 'Entre centrales'}
                    ],
                    'linea_tactica': {'activa': True, 'x': 82, 'color': 'azul', 'etiqueta': 'Bloque bajo'}
                }
            },
            'transicion': {
                'def_atq': {
                    'jugadores': [
                        {'x': 45, 'y': 50, 'numero': '10', 'color': 'amarillo', 'destacado': True},
                        {'x': 30, 'y': 20, 'numero': '7', 'color': 'rojo', 'destacado': False},
                        {'x': 30, 'y': 80, 'numero': '11', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [
                        {'x1': 45, 'y1': 50, 'x2': 25, 'y2': 50, 'color': 'verde', 'tipo': 'movimiento'},
                        {'x1': 40, 'y1': 30, 'x2': 20, 'y2': 15, 'color': 'verde', 'tipo': 'carrera'},
                        {'x1': 40, 'y1': 70, 'x2': 20, 'y2': 85, 'color': 'verde', 'tipo': 'carrera'},
                    ],
                    'zonas': [
                        {'x': 35, 'y': 30, 'ancho': 15, 'alto': 40, 'color': 'verde', 'nombre': 'Recuperación'}
                    ],
                    'linea_tactica': {'activa': False}
                },
                'atq_def': {
                    'jugadores': [
                        {'x': 75, 'y': 40, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 60, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 60, 'y': 50, 'numero': '6', 'color': 'amarillo', 'destacado': True},
                    ],
                    'flechas': [
                        {'x1': 30, 'y1': 50, 'x2': 55, 'y2': 50, 'color': 'rojo', 'tipo': 'movimiento'},
                        {'x1': 25, 'y1': 20, 'x2': 50, 'y2': 30, 'color': 'rojo', 'tipo': 'movimiento'},
                        {'x1': 25, 'y1': 80, 'x2': 50, 'y2': 70, 'color': 'rojo', 'tipo': 'movimiento'},
                    ],
                    'zonas': [
                        {'x': 55, 'y': 20, 'ancho': 25, 'alto': 60, 'color': 'rojo', 'nombre': 'Desbalance'}
                    ],
                    'linea_tactica': {'activa': False}
                }
            },
            'abp': {
                'corners': {
                    'jugadores': [
                        {'x': 12, 'y': 50, 'numero': '9', 'color': 'rojo', 'destacado': True},
                        {'x': 10, 'y': 35, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 14, 'y': 65, 'numero': '5', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [
                        {'x1': 2, 'y1': 95, 'x2': 10, 'y2': 55, 'color': 'amarillo', 'tipo': 'pase'},
                    ],
                    'zonas': [
                        {'x': 5, 'y': 25, 'ancho': 15, 'alto': 50, 'color': 'morado', 'nombre': 'Zona remate'}
                    ],
                    'linea_tactica': {'activa': False}
                },
                'faltas': {
                    'jugadores': [
                        {'x': 25, 'y': 50, 'numero': '10', 'color': 'amarillo', 'destacado': True},
                        {'x': 15, 'y': 45, 'numero': '9', 'color': 'rojo', 'destacado': False},
                        {'x': 15, 'y': 55, 'numero': '7', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [
                        {'x1': 25, 'y1': 50, 'x2': 8, 'y2': 50, 'color': 'amarillo', 'tipo': 'pase'},
                    ],
                    'zonas': [],
                    'linea_tactica': {'activa': False}
                }
            }
        }

        return defaults.get(fase, {}).get(tipo, {
            'jugadores': [],
            'flechas': [],
            'zonas': [],
            'linea_tactica': {'activa': False}
        })

    def generar_todos_los_dibujos(self, datos_completos):
        """Genera todas las instrucciones de dibujo para un informe completo"""
        dibujos = {
            'ataque': {},
            'defensa': {},
            'transiciones': {},
            'abp': {}
        }

        # Ataque
        ataque = datos_completos.get('ataque', {})
        for tipo in ['vs_bloque_alto', 'vs_bloque_medio', 'vs_bloque_bajo']:
            fase_data = ataque.get(tipo, {})
            if fase_data:
                resultado = self.generar_dibujo_tactico('ataque', tipo, fase_data)
                dibujos['ataque'][tipo] = resultado['data']
            else:
                dibujos['ataque'][tipo] = self._dibujo_por_defecto('ataque', tipo)

        # Defensa
        defensa = datos_completos.get('defensa', {})
        for tipo in ['pressing_alto', 'bloque_medio', 'bloque_bajo']:
            fase_data = defensa.get(tipo, {})
            if fase_data:
                resultado = self.generar_dibujo_tactico('defensa', tipo, fase_data)
                dibujos['defensa'][tipo] = resultado['data']
            else:
                dibujos['defensa'][tipo] = self._dibujo_por_defecto('defensa', tipo)

        # Transiciones
        transiciones = datos_completos.get('transiciones', {})
        for tipo in ['def_atq', 'atq_def']:
            fase_data = transiciones.get(tipo, {})
            if fase_data:
                resultado = self.generar_dibujo_tactico('transicion', tipo, fase_data)
                dibujos['transiciones'][tipo] = resultado['data']
            else:
                dibujos['transiciones'][tipo] = self._dibujo_por_defecto('transicion', tipo)

        # ABP
        abp = datos_completos.get('abp', {})
        if abp:
            resultado = self.generar_dibujo_tactico('abp', 'corners', abp)
            dibujos['abp']['corners'] = resultado['data']
        else:
            dibujos['abp']['corners'] = self._dibujo_por_defecto('abp', 'corners')

        return dibujos


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def test_conexion_ia(provider='groq'):
    """
    Prueba la conexión con el proveedor de IA

    Returns:
        dict con resultado del test
    """
    analyzer = IAAnalyzer(provider=provider)

    notas_test = """
    El rival juega en 4-3-3. El 10 es muy bueno, organiza todo el juego.
    El 9 es rápido pero flojo de cabeza.
    Salen bien desde atrás, el portero tiene buen pie.
    En defensa presionan alto pero dejan espacios a la espalda.
    Los laterales suben mucho y dejan huecos.
    """

    try:
        resultado = analyzer.analizar_notas_rival(notas_test)
        if resultado['success']:
            return {
                'success': True,
                'message': f'✅ Conexión exitosa con {provider.upper()}',
                'data': resultado['data']
            }
        else:
            return {
                'success': False,
                'message': f'❌ Error: {resultado["error"]}'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'❌ Error de conexión: {str(e)}'
        }


if __name__ == "__main__":
    # Test de conexión
    print("🧪 Testeando conexión con Groq...")
    resultado = test_conexion_ia('groq')
    print(resultado['message'])

    if resultado['success']:
        print("\n📊 Datos extraídos:")
        print(json.dumps(resultado['data'], indent=2, ensure_ascii=False))
