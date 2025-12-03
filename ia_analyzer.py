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
            "debilidad": "Debilidad específica a explotar"
        }},
        "vs_bloque_medio": {{
            "jugadores_clave": "Quiénes destacan en progresión",
            "zonas_activas": "Bandas/centro, carrileros, etc",
            "patrones": ["Patrón 1", "Patrón 2", "Patrón 3"],
            "debilidad": "Debilidad específica"
        }},
        "vs_bloque_bajo": {{
            "como_finalizan": "Centros, juego interior, etc",
            "jugadores_area": "Quiénes rematan",
            "patrones": ["Patrón 1", "Patrón 2"],
            "debilidad": "Debilidad específica"
        }}
    }},

    "defensa": {{
        "pressing_alto": {{
            "estructura": "Sistema defensivo (ej: 4-4-2, 4-1-3-2)",
            "gatillos": "Cuándo presionan (ej: pase al DC)",
            "patrones": ["Patrón 1", "Patrón 2"],
            "fortaleza": "Punto fuerte defensivo"
        }},
        "bloque_medio": {{
            "compactacion": "Distancia entre líneas, metros de bloque",
            "coberturas": "Cómo cubren espacios",
            "patrones": ["Patrón 1", "Patrón 2"],
            "fortaleza": "Punto fuerte"
        }},
        "bloque_bajo": {{
            "organizacion": "Cómo se organizan en área",
            "marcajes": "Zona/individual/mixto",
            "patrones": ["Patrón 1", "Patrón 2"],
            "debilidad": "Debilidad específica"
        }}
    }},

    "transiciones": {{
        "def_atq": {{
            "velocidad": "Rápida/lenta/media",
            "jugadores_clave": "Quiénes protagonizan",
            "patrones": ["Patrón 1", "Patrón 2"],
            "como_cortar": "Cómo podemos cortarla"
        }},
        "atq_def": {{
            "equilibrios": "Quiénes quedan en equilibrio al atacar",
            "repliegue": "Rápido/lento, pressing o repliegue",
            "patrones": ["Patrón 1", "Patrón 2"],
            "desbalance": "Dónde están expuestos"
        }}
    }},

    "abp": {{
        "corners_favor": "Estructura, ejecutor, zonas",
        "faltas_favor": "Ejecutores, estrategias",
        "corners_contra": "Organización defensiva",
        "debilidad": "Debilidad en ABP"
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


if __name__ == "__main__":
    # Test de conexión
    print("🧪 Testeando conexión con Groq...")
    resultado = test_conexion_ia('groq')
    print(resultado['message'])

    if resultado['success']:
        print("\n📊 Datos extraídos:")
        print(json.dumps(resultado['data'], indent=2, ensure_ascii=False))
