from flask import Flask, render_template, request, send_file, jsonify, session, redirect
from flask_cors import CORS
import os
import json
import tempfile
import secrets
import io
from datetime import datetime
import sys

# Importar los generadores y analizador IA
sys.path.append(os.path.dirname(__file__))
from generar_informe import generar_informe_pdf
from generar_informe_v2 import generar_informe_v2_pdf
from generar_plan_partido import generar_plan_partido_pdf
from ia_analyzer import IAAnalyzer

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Contraseña de acceso - CAMBIAR ESTO
ACCESS_PASSWORD = "CAC2025"

@app.route('/')
def index():
    """Página de login"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Verificar contraseña"""
    data = request.json
    password = data.get('password', '')
    
    if password == ACCESS_PASSWORD:
        session['authenticated'] = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Contraseña incorrecta'}), 401

@app.route('/app')
def app_page():
    """Página principal de la aplicación - v2.0"""
    if not session.get('authenticated'):
        return redirect('/')
    return render_template('index_v2.html')

@app.route('/generar', methods=['POST'])
def generar():
    """Generar el PDF con los datos recibidos"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        datos = request.json
        
        # Crear archivo temporal para el JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as json_file:
            json.dump(datos, json_file, ensure_ascii=False, indent=2)
            json_path = json_file.name
        
        # Crear archivo temporal para el PDF
        pdf_path = tempfile.mktemp(suffix='.pdf')
        
        # Generar el PDF
        generar_informe_pdf(datos, pdf_path)
        
        # Leer el PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
        
        # Limpiar archivos temporales
        try:
            os.unlink(json_path)
            os.unlink(pdf_path)
        except:
            pass
        
        # Nombre del archivo
        nombre_archivo = f"Informe_{datos.get('nombre_rival', 'Rival').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Enviar el PDF
        return send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analizar_notas', methods=['POST'])
def analizar_notas():
    """Analizar notas del partido con IA y devolver datos estructurados"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json
        notas_texto = datos.get('notas', '')
        provider = datos.get('provider', 'groq')

        if not notas_texto or len(notas_texto.strip()) < 50:
            return jsonify({
                'success': False,
                'error': 'Las notas deben tener al menos 50 caracteres para un análisis adecuado'
            }), 400

        # Analizar con IA
        analyzer = IAAnalyzer(provider=provider)
        resultado = analyzer.analizar_notas_rival(notas_texto)

        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500

    except Exception as e:
        print(f"Error en análisis IA: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al analizar: {str(e)}'
        }), 500


@app.route('/generar_sugerencias_plan', methods=['POST'])
def generar_sugerencias_plan():
    """Generar sugerencias tácticas para el plan de partido"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json
        datos_rival = datos.get('datos_rival', {})
        notas_adicionales = datos.get('notas_adicionales', '')
        provider = datos.get('provider', 'groq')

        # Analizar con IA
        analyzer = IAAnalyzer(provider=provider)
        resultado = analyzer.generar_plan_tactico(datos_rival, notas_adicionales)

        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500

    except Exception as e:
        print(f"Error en generación de plan: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al generar sugerencias: {str(e)}'
        }), 500


@app.route('/generar_plan', methods=['POST'])
def generar_plan():
    """Generar el PDF del Plan de Partido"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json

        # Crear archivo temporal para el PDF
        pdf_path = tempfile.mktemp(suffix='.pdf')

        # Generar el PDF
        generar_plan_partido_pdf(datos, pdf_path)

        # Leer el PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        # Limpiar archivo temporal
        try:
            os.unlink(pdf_path)
        except:
            pass

        # Nombre del archivo
        nombre_archivo = f"Plan_Partido_vs_{datos.get('nombre_rival', 'Rival').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

        # Enviar el PDF
        return send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/generar_v2', methods=['POST'])
def generar_v2():
    """Generar el PDF v2.0 con análisis por fases"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json

        # Crear archivo temporal para el PDF
        pdf_path = tempfile.mktemp(suffix='.pdf')

        # Generar PDF v2.0 con análisis por fases
        generar_informe_v2_pdf(datos, pdf_path)

        # Leer el PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        # Limpiar archivo temporal
        try:
            os.unlink(pdf_path)
        except:
            pass

        # Nombre del archivo
        nombre_archivo = f"Informe_v2_{datos.get('nombre_rival', 'Rival').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

        # Enviar el PDF
        return send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
