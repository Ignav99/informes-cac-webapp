#!/usr/bin/env python3
"""
Analizador de IA para Notas de Partido
Club Atlético Central - Integración con Groq, Claude y Ollama
"""

import os
import json
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


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
        """Construye el prompt para analizar al rival"""
        return f"""Eres un analista táctico de fútbol profesional con experiencia en equipos profesionales.
Analiza estas notas informales que un entrenador tomó durante la observación de un equipo rival.

IMPORTANTE:
- Transforma las notas en un análisis profesional y estructurado
- Usa lenguaje técnico pero claro
- Identifica patrones tácticos
- Señala puntos fuertes y débiles
- Sé específico y concreto

NOTAS DEL ENTRENADOR:
{notas}

Devuelve ÚNICAMENTE un JSON válido (sin texto adicional) con esta estructura:

{{
    "sistema_tactico": "sistema detectado (ej: 4-3-3, 4-4-2, etc)",
    "ataque_organizado": "Párrafo profesional describiendo cómo ataca el rival en fase organizada. Incluye: esquema posicional, jugadores clave, patrones de juego, amplitud/profundidad, circulación de balón.",
    "defensa_organizada": "Párrafo profesional describiendo cómo defiende el rival. Incluye: altura del bloque, presión, coberturas, líneas defensivas, compactación.",
    "transicion_def_atq": "Párrafo sobre cómo transiciona de defensa a ataque. Incluye: velocidad, verticalidad, jugadores implicados, patrones de contraataque.",
    "transicion_atq_def": "Párrafo sobre cómo transiciona de ataque a defensa. Incluye: repliegue, pressing inmediato, reorganización.",
    "abp": "Análisis de acciones a balón parado (córners, faltas, saques). Incluye: esquemas ofensivos y defensivos, efectividad.",
    "jugadores_clave": [
        {{"numero": "X", "descripcion": "Descripción del jugador: posición, características, nivel"}},
        {{"numero": "Y", "descripcion": "..."}}
    ],
    "debilidades_rival": [
        "Debilidad 1 específica que podemos explotar",
        "Debilidad 2 específica que podemos explotar"
    ],
    "fortalezas_rival": [
        "Fortaleza 1 del rival que debemos neutralizar",
        "Fortaleza 2 del rival que debemos neutralizar"
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
        """Analiza usando Groq API (GRATIS)"""
        if not self.groq_key:
            raise ValueError("GROQ_API_KEY no configurada en .env")

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-70b-versatile",  # Modelo potente y gratis
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un analista táctico de fútbol profesional. Respondes SIEMPRE en formato JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # Más determinista para análisis
            "max_tokens": 2000
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        resultado = response.json()
        contenido = resultado['choices'][0]['message']['content']

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
        return json.loads(contenido)

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
