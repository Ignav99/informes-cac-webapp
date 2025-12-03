#!/usr/bin/env python3
"""
Analizador de IA para Notas de Partido
Club Atlético Central
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
    print(f"✓ Groq importado correctamente", file=sys.stderr)
except ImportError as e:
    print(f"✗ Error importando Groq: {e}", file=sys.stderr)
    raise


class IAAnalyzer:
    """
    Clase para analizar notas informales de partidos usando IA
    """

    def __init__(self, provider='groq'):
        """
        Inicializar analizador

        Args:
            provider: 'groq', 'claude', 'ollama'
        """
        self.provider = provider
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')

        # Log para debugging
        print(f"[IA] Provider: {provider}", file=sys.stderr)
        if provider == 'groq':
            if self.groq_key:
                print(f"[IA] API Key encontrada: {self.groq_key[:20]}...", file=sys.stderr)
            else:
                print(f"[IA] ✗ GROQ_API_KEY no encontrada", file=sys.stderr)

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


    def generar_dibujo_tactico(self, fase, tipo, texto_tactico):
        """
        Genera instrucciones de dibujo para un campo táctico basándose en el texto

        Args:
            fase: 'ataque', 'defensa', 'transicion', 'abp'
            tipo: subtipo de la fase (ej: 'vs_bloque_alto', 'pressing_alto', 'def_atq')
            texto_tactico: dict con los datos tácticos escritos por el usuario

        Returns:
            dict con instrucciones de dibujo (jugadores, flechas, zonas)
        """
        prompt = self._construir_prompt_dibujo(fase, tipo, texto_tactico)

        try:
            if self.provider == 'groq':
                resultado = self._analizar_groq_dibujo(prompt)
            else:
                resultado = self._analizar_groq_dibujo(prompt)  # Default a Groq

            return {
                'success': True,
                'data': resultado
            }
        except Exception as e:
            print(f"[IA] Error generando dibujo: {e}", file=sys.stderr)
            # Devolver dibujo por defecto
            return {
                'success': False,
                'data': self._dibujo_por_defecto(fase, tipo),
                'error': str(e)
            }

    def _construir_prompt_dibujo(self, fase, tipo, texto_tactico):
        """Construye prompt para generar instrucciones de dibujo táctico"""

        # Contexto según la fase
        contextos = {
            'ataque': {
                'vs_bloque_alto': 'Representa cómo sale el equipo rival desde atrás contra pressing. Muestra portero, defensas, pivote y triángulos de pase.',
                'vs_bloque_medio': 'Representa cómo progresa el rival en zona media. Muestra centrocampistas creativos y zonas de peligro.',
                'vs_bloque_bajo': 'Representa cómo finaliza el rival. Muestra jugadores en área, centros laterales, rematadores.'
            },
            'defensa': {
                'pressing_alto': 'Representa la línea de pressing alto del rival. Muestra altura de presión y gatillos.',
                'bloque_medio': 'Representa el bloque medio defensivo. Muestra compactación entre líneas.',
                'bloque_bajo': 'Representa el bloque bajo. Muestra organización defensiva en área.'
            },
            'transicion': {
                'def_atq': 'Representa el contraataque rival. Muestra recuperación y carreras hacia portería.',
                'atq_def': 'Representa la transición defensiva rival. Muestra repliegue y zonas de desbalance.'
            },
            'abp': {
                'corners': 'Representa estrategia de corners. Muestra posiciones de rematadores y ejecutor.',
                'faltas': 'Representa estrategia de faltas. Muestra ejecutor y movimientos.'
            }
        }

        contexto = contextos.get(fase, {}).get(tipo, 'Representa la situación táctica descrita.')

        return f"""Eres un analista táctico visual de fútbol. Genera instrucciones de dibujo para un campo de fútbol.

CONTEXTO: {contexto}

INFORMACIÓN TÁCTICA DEL USUARIO:
{json.dumps(texto_tactico, indent=2, ensure_ascii=False)}

El campo tiene coordenadas de 0 a 100 en X (izquierda a derecha) y 0 a 100 en Y (abajo a arriba).
- Portería RIVAL está en X=95-100 (derecha)
- Portería PROPIA está en X=0-5 (izquierda)
- Centro del campo: X=50

Genera un JSON con instrucciones de dibujo:
- jugadores: Lista de jugadores a dibujar (máx 6-8)
- flechas: Lista de flechas de movimiento/pase (máx 4-5)
- zonas: Lista de zonas destacadas (máx 2)

DEVUELVE ÚNICAMENTE este JSON:
{{
    "jugadores": [
        {{"x": 85, "y": 50, "numero": "1", "color": "amarillo", "destacado": true}},
        {{"x": 75, "y": 35, "numero": "4", "color": "rojo", "destacado": false}},
        {{"x": 75, "y": 65, "numero": "5", "color": "rojo", "destacado": false}}
    ],
    "flechas": [
        {{"x1": 85, "y1": 50, "x2": 75, "y2": 40, "color": "blanco", "tipo": "pase"}},
        {{"x1": 70, "y1": 50, "x2": 50, "y2": 50, "color": "amarillo", "tipo": "movimiento"}}
    ],
    "zonas": [
        {{"x": 65, "y": 25, "ancho": 20, "alto": 50, "color": "verde", "nombre": "Zona salida"}}
    ],
    "linea_tactica": {{
        "activa": true,
        "x": 70,
        "color": "rojo",
        "etiqueta": "Línea pressing"
    }}
}}

COLORES PERMITIDOS: rojo, azul, amarillo, verde, naranja, blanco, morado
TIPOS DE FLECHA: pase, movimiento, carrera, pressing

Sé creativo y representa visualmente lo que describe el texto táctico. Los jugadores destacados (destacado=true) se dibujan más grandes y en amarillo."""

    def _analizar_groq_dibujo(self, prompt):
        """Analiza usando Groq para generar dibujos - versión optimizada"""
        if not self.groq_key:
            raise ValueError("API Key de Groq no configurada")

        try:
            client = Groq(api_key=self.groq_key)

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un generador de instrucciones de dibujo táctico de fútbol. Respondes SIEMPRE en JSON válido con coordenadas precisas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,  # Un poco más creativo para los dibujos
                max_tokens=1500
            )

            contenido = completion.choices[0].message.content.strip()

            # Limpiar markdown
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
        """
        Genera todas las instrucciones de dibujo para un informe completo

        Args:
            datos_completos: dict con todos los datos del formulario

        Returns:
            dict con instrucciones de dibujo para cada sección
        """
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


if __name__ == "__main__":
    # Test de conexión
    print("🧪 Testeando conexión con Groq...")
    resultado = test_conexion_ia('groq')
    print(resultado['message'])

    if resultado['success']:
        print("\n📊 Datos extraídos:")
        print(json.dumps(resultado['data'], indent=2, ensure_ascii=False))
