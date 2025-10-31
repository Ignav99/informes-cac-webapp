#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Groq
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno
load_dotenv()

def test_groq():
    """Prueba la API de Groq"""

    api_key = os.getenv('GROQ_API_KEY')

    if not api_key:
        print("❌ ERROR: No se encontró GROQ_API_KEY en el archivo .env")
        print("\nAsegúrate de tener un archivo .env con:")
        print("GROQ_API_KEY=tu_api_key_aqui")
        return False

    print(f"✓ API Key encontrada: {api_key[:20]}...")
    print("\n🔄 Probando conexión con Groq...")

    try:
        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Responde solo: OK"
                }
            ],
            temperature=0.3,
            max_tokens=10
        )

        respuesta = completion.choices[0].message.content

        print(f"✅ ÉXITO! Groq respondió: {respuesta}")
        print("\n✅ Tu API key funciona correctamente")
        print("✅ El sistema de IA está listo para usar")
        return True

    except Exception as e:
        print(f"\n❌ ERROR al conectar con Groq:")
        print(f"   {str(e)}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que tu API key sea válida")
        print("   2. Genera una nueva en: https://console.groq.com/keys")
        print("   3. Actualiza el archivo .env con la nueva key")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE CONEXIÓN - CLUB ATLÉTICO CENTRAL")
    print("=" * 60)
    print()

    success = test_groq()

    print()
    print("=" * 60)

    if success:
        print("🎉 TODO LISTO! Puedes ejecutar: python app.py")
    else:
        print("⚠️  Corrige los errores antes de continuar")

    print("=" * 60)
