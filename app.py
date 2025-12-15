from flask import Flask, render_template, request, send_file, jsonify, session, redirect
from flask_cors import CORS
import os
import json
import tempfile
import secrets
import io
from datetime import datetime
import sys
import base64

# Importar los generadores y analizador IA
sys.path.append(os.path.dirname(__file__))
from generar_informe import generar_informe_pdf
from generar_informe_v2 import generar_informe_v2_pdf
from generar_plan_partido import generar_plan_partido_pdf
from ia_analyzer import IAAnalyzer

app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(32)
CORS(app)

# Crear directorio static si no existe
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

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


@app.route('/generar_dibujos_ia', methods=['POST'])
def generar_dibujos_ia():
    """Generar instrucciones de dibujo táctico con IA"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json
        provider = datos.get('provider', 'groq')

        # Analizar con IA para generar dibujos
        analyzer = IAAnalyzer(provider=provider)
        dibujos = analyzer.generar_todos_los_dibujos(datos)

        return jsonify({
            'success': True,
            'dibujos': dibujos
        })

    except Exception as e:
        print(f"Error generando dibujos IA: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/previsualizar_v2', methods=['POST'])
def previsualizar_v2():
    """Generar previsualización del PDF v2.0 y devolver como base64"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json
        dibujos_ia = datos.get('dibujos_ia', None)

        # Crear archivo temporal para el PDF
        pdf_path = tempfile.mktemp(suffix='.pdf')

        # Generar PDF v2.0 con dibujos de IA
        generar_informe_v2_pdf(datos, pdf_path, dibujos_ia=dibujos_ia)

        # Leer el PDF y convertir a base64
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        # Limpiar archivo temporal
        try:
            os.unlink(pdf_path)
        except:
            pass

        return jsonify({
            'success': True,
            'pdf_base64': pdf_base64,
            'nombre_archivo': f"Informe_v2_{datos.get('nombre_rival', 'Rival').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        })

    except Exception as e:
        print(f"Error en previsualización: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/generar_v2', methods=['POST'])
def generar_v2():
    """Generar el PDF v2.0 con análisis por fases y dibujos de IA"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        datos = request.json
        dibujos_ia = datos.get('dibujos_ia', None)

        # Crear archivo temporal para el PDF
        pdf_path = tempfile.mktemp(suffix='.pdf')

        # Generar PDF v2.0 con dibujos de IA
        generar_informe_v2_pdf(datos, pdf_path, dibujos_ia=dibujos_ia)

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


@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    """Subir logo del club"""
    if not session.get('authenticated'):
        return jsonify({'error': 'No autorizado'}), 401

    try:
        if 'logo' not in request.files:
            return jsonify({'success': False, 'error': 'No se envió ningún archivo'}), 400

        file = request.files['logo']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó ningún archivo'}), 400

        # Verificar extensión
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Formato no válido. Use PNG, JPG o GIF'}), 400

        # Guardar como logo.png en static
        logo_path = os.path.join(static_dir, 'logo.png')
        file.save(logo_path)

        return jsonify({
            'success': True,
            'message': 'Logo subido correctamente'
        })

    except Exception as e:
        print(f"Error subiendo logo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/check_logo', methods=['GET'])
def check_logo():
    """Verificar si existe el logo del club"""
    logo_path = os.path.join(static_dir, 'logo.png')
    exists = os.path.exists(logo_path)
    return jsonify({
        'exists': exists,
        'path': '/static/logo.png' if exists else None
    })


@app.route('/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
