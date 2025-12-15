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
        """Construye prompt para generar instrucciones de dibujo táctico - VERSIÓN MEJORADA"""

        # Zonas específicas del campo según la fase
        zonas_campo = {
            'ataque': {
                'vs_bloque_alto': {
                    'descripcion': 'SALIDA DE BALÓN del rival (su campo, cerca de su portería)',
                    'zona_x': '70-95',  # Lado derecho = su portería
                    'explicacion': 'El RIVAL sale desde ATRÁS. Portero en X=92, defensas en X=75-82, pivote en X=65-70.'
                },
                'vs_bloque_medio': {
                    'descripcion': 'PROGRESIÓN del rival (zona media del campo)',
                    'zona_x': '40-70',
                    'explicacion': 'El RIVAL progresa por CENTRO. Centrocampistas en X=45-60, extremos en X=35-50.'
                },
                'vs_bloque_bajo': {
                    'descripcion': 'FINALIZACIÓN del rival (cerca de nuestra portería)',
                    'zona_x': '5-35',  # Lado izquierdo = nuestra portería
                    'explicacion': 'El RIVAL ataca NUESTRA ÁREA. Delanteros en X=10-25, centros desde X=5-15.'
                }
            },
            'defensa': {
                'pressing_alto': {
                    'descripcion': 'PRESSING ALTO del rival (en nuestro campo)',
                    'zona_x': '60-90',
                    'explicacion': 'El RIVAL presiona ALTO. Sus delanteros presionan en X=70-85, línea de pressing en X=65-75.'
                },
                'bloque_medio': {
                    'descripcion': 'BLOQUE MEDIO del rival (centro del campo)',
                    'zona_x': '40-65',
                    'explicacion': 'El RIVAL se compacta en MEDIO. Sus líneas entre X=45-60, bloque de 25-30m.'
                },
                'bloque_bajo': {
                    'descripcion': 'BLOQUE BAJO del rival (en su área)',
                    'zona_x': '70-95',
                    'explicacion': 'El RIVAL defiende en su ÁREA. Defensas en X=78-88, líneas muy juntas.'
                }
            },
            'transicion': {
                'def_atq': {
                    'descripcion': 'CONTRAATAQUE del rival (de su área hacia la nuestra)',
                    'zona_x': '30-70',
                    'explicacion': 'Transición OFENSIVA. Recuperación en X=50-65, carreras hacia X=10-30.'
                },
                'atq_def': {
                    'descripcion': 'REPLIEGUE del rival (volviendo a defender)',
                    'zona_x': '40-80',
                    'explicacion': 'Transición DEFENSIVA. Equilibrios en X=60-75, zonas de desbalance a explotar.'
                }
            },
            'abp': {
                'corners': {
                    'descripcion': 'CORNER del rival (atacando nuestra portería)',
                    'zona_x': '5-25',
                    'explicacion': 'Corner OFENSIVO rival. Ejecutor en X=2-5, rematadores en X=8-18.'
                },
                'faltas': {
                    'descripcion': 'FALTA del rival',
                    'zona_x': '15-40',
                    'explicacion': 'Falta OFENSIVA rival. Ejecutor y barrera/movimientos.'
                }
            }
        }

        info_zona = zonas_campo.get(fase, {}).get(tipo, {
            'descripcion': 'Situación táctica',
            'zona_x': '20-80',
            'explicacion': 'Dibuja según el texto.'
        })

        return f"""Eres un analista táctico de fútbol. Genera SOLO los elementos que se mencionan en el texto.

══════════════════════════════════════════════════════════════
SITUACIÓN: {info_zona['descripcion']}
ZONA DEL CAMPO: X = {info_zona['zona_x']}
{info_zona['explicacion']}
══════════════════════════════════════════════════════════════

COORDENADAS DEL CAMPO (MUY IMPORTANTE):
┌─────────────────────────────────────────────────────────────┐
│  X=0-5: Nuestra portería (izquierda)                        │
│  X=5-30: Nuestro campo defensivo                            │
│  X=30-50: Nuestro mediocampo                                │
│  X=50: Línea central                                        │
│  X=50-70: Mediocampo rival                                  │
│  X=70-95: Campo defensivo rival                             │
│  X=95-100: Portería rival (derecha)                         │
│  Y=0-100: De banda a banda (0=abajo, 50=centro, 100=arriba) │
└─────────────────────────────────────────────────────────────┘

TEXTO TÁCTICO A REPRESENTAR:
{json.dumps(texto_tactico, indent=2, ensure_ascii=False)}

══════════════════════════════════════════════════════════════
REGLAS ESTRICTAS:
══════════════════════════════════════════════════════════════
1. SOLO dibuja lo que SE MENCIONA en el texto. NO inventes.
2. Si dice "estructura 4+1" → dibuja 4 defensas + 1 pivote
3. Si menciona triángulos específicos (ej: "1-4-6") → conecta esos números con flechas
4. Si menciona jugadores por NÚMERO (ej: "el 10", "el 9") → ponlos con ese número
5. Si menciona ZONAS (ej: "bandas", "centro") → dibuja zona en esa área
6. Las FLECHAS solo para pases/movimientos MENCIONADOS
7. Posiciona a los jugadores en la ZONA CORRECTA del campo según la fase

FORMACIONES TÍPICAS (Y en banda):
- Portero: Y=50
- Defensas (4): Y=20, Y=40, Y=60, Y=80
- Centrocampistas (3): Y=25, Y=50, Y=75
- Delanteros: Y=30, Y=50, Y=70

══════════════════════════════════════════════════════════════

DEVUELVE SOLO ESTE JSON (sin explicaciones):
{{
    "jugadores": [
        {{"x": 85, "y": 50, "numero": "1", "color": "amarillo", "destacado": false}}
    ],
    "flechas": [
        {{"x1": 85, "y1": 50, "x2": 75, "y2": 40, "color": "blanco", "tipo": "pase"}}
    ],
    "zonas": [
        {{"x": 65, "y": 25, "ancho": 15, "alto": 50, "color": "verde", "nombre": "Zona"}}
    ],
    "linea_tactica": {{
        "activa": false,
        "x": 50,
        "color": "rojo",
        "etiqueta": ""
    }}
}}

COLORES: rojo, azul, amarillo, verde, naranja, blanco, morado
- Jugadores DESTACADOS o clave: amarillo con destacado=true
- Jugadores normales: rojo con destacado=false
- Flechas de pase: blanco
- Flechas de movimiento/carrera: amarillo o verde"""

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
                        {'x': 88, 'y': 50, 'numero': '1', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 20, 'numero': '2', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 40, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 60, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 80, 'numero': '3', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [
                        {'x1': 55, 'y1': 50, 'x2': 68, 'y2': 50, 'color': 'amarillo', 'tipo': 'pressing'},
                        {'x1': 50, 'y1': 25, 'x2': 65, 'y2': 25, 'color': 'amarillo', 'tipo': 'pressing'},
                        {'x1': 50, 'y1': 75, 'x2': 65, 'y2': 75, 'color': 'amarillo', 'tipo': 'pressing'},
                    ],
                    'zonas': [],
                    'linea_tactica': {'activa': True, 'x': 70, 'color': 'rojo', 'etiqueta': 'Pressing'}
                },
                'bloque_medio': {
                    'jugadores': [
                        {'x': 88, 'y': 50, 'numero': '1', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 20, 'numero': '2', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 40, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 60, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 75, 'y': 80, 'numero': '3', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [],
                    'zonas': [
                        {'x': 45, 'y': 15, 'ancho': 15, 'alto': 70, 'color': 'naranja', 'nombre': 'Bloque'}
                    ],
                    'linea_tactica': {'activa': True, 'x': 50, 'color': 'naranja', 'etiqueta': 'Línea media'}
                },
                'bloque_bajo': {
                    'jugadores': [
                        {'x': 92, 'y': 50, 'numero': '1', 'color': 'rojo', 'destacado': False},
                        {'x': 82, 'y': 20, 'numero': '2', 'color': 'rojo', 'destacado': False},
                        {'x': 82, 'y': 40, 'numero': '4', 'color': 'rojo', 'destacado': False},
                        {'x': 82, 'y': 60, 'numero': '5', 'color': 'rojo', 'destacado': False},
                        {'x': 82, 'y': 80, 'numero': '3', 'color': 'rojo', 'destacado': False},
                    ],
                    'flechas': [],
                    'zonas': [],
                    'linea_tactica': {'activa': True, 'x': 30, 'color': 'azul', 'etiqueta': 'Bloque bajo'}
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
