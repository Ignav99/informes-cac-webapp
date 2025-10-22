# 🚀 Web App - Generador de Informes de Equipos Rivales
## Club Atlético Central

---

## ✨ Características

- ✅ Formulario paso a paso intuitivo
- ✅ Generación de PDFs profesionales
- ✅ Acceso protegido con contraseña
- ✅ Sin base de datos (todo en memoria temporal)
- ✅ Logo integrado automáticamente
- ✅ Diseño responsive y profesional

---

## 📋 Requisitos Previos

- Cuenta en **Railway** o **Render** (GRATIS)
- Cuenta de GitHub (opcional pero recomendado)

---

## 🚀 OPCIÓN 1: Desplegar en Railway (Recomendado)

Railway es muy fácil y tiene plan gratuito generoso.

### Paso 1: Crear cuenta en Railway
1. Ve a https://railway.app
2. Regístrate con GitHub o email
3. Verificar cuenta (plan gratuito: $5 de crédito/mes)

### Paso 2: Subir el código

#### Opción A: Desde GitHub (Recomendado)
1. Sube la carpeta `webapp-informes` a un repositorio de GitHub
2. En Railway: "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repositorio
4. Railway detectará automáticamente que es una app Flask

#### Opción B: Desde CLI de Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# En la carpeta webapp-informes:
cd webapp-informes
railway init
railway up
```

### Paso 3: Configurar
1. Railway desplegará automáticamente la app
2. Te dará una URL: `https://tu-app.up.railway.app`
3. ¡Listo! Ya funciona

### Paso 4: Cambiar la contraseña
1. Abre el archivo `app.py` en Railway
2. Busca la línea: `ACCESS_PASSWORD = "CAC2025"`
3. Cámbiala por tu contraseña deseada
4. Railway redesplegará automáticamente

---

## 🚀 OPCIÓN 2: Desplegar en Render

Render también es gratis y muy fácil.

### Paso 1: Crear cuenta en Render
1. Ve a https://render.com
2. Regístrate con GitHub o email

### Paso 2: Nuevo Web Service
1. Sube tu código a GitHub
2. En Render: "New" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name**: informes-cac
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

### Paso 3: Deploy
1. Click "Create Web Service"
2. Render desplegará tu app
3. Te dará una URL: `https://informes-cac.onrender.com`

---

## 🔐 Cambiar la Contraseña

Edita el archivo `app.py`:

```python
# Línea 20 aproximadamente
ACCESS_PASSWORD = "TU_CONTRASEÑA_AQUI"
```

**Contraseña por defecto**: `CAC2025`

**⚠️ IMPORTANTE**: Cambia esta contraseña antes de usar en producción.

---

## 🎯 Uso de la Web App

### 1. Acceder
- Ve a tu URL: `https://tu-app.railway.app` o `https://tu-app.onrender.com`
- Introduce la contraseña

### 2. Crear Informe
**Paso 1: Datos Básicos**
- Nombre del rival
- Jornada
- Sistema táctico
- Posición en tabla
- Racha de resultados
- Bajas (opcional)

**Paso 2: Jugadores**
- Se generan automáticamente 11 jugadores según el sistema
- Asigna dorsales
- Marca niveles (Peligroso/Normal/Débil)

**Paso 3: Análisis Táctico**
- Ataque organizado
- Defensa organizada
- Transiciones
- ABP
- Análisis individual

**Paso 4: Generar**
- Revisa el resumen
- Click "Generar Informe PDF"
- Se descarga automáticamente

### 3. Descargar PDF
- El PDF se descarga automáticamente
- Nombre: `Informe_[Equipo]_[Fecha].pdf`

### 4. Crear Otro Informe
- Refresca la página (todos los datos se borran)
- O click "Sí" cuando pregunte si quieres crear otro

---

## 🔒 Seguridad

✅ Acceso protegido por contraseña
✅ Sin base de datos (nada se guarda)
✅ Datos solo en memoria temporal
✅ Al recargar página → todo se borra
✅ Sesión expira al cerrar navegador

---

## 💡 Consejos

1. **Guarda la URL**: Anótala para acceso rápido
2. **Comparte solo con tu equipo**: La contraseña da acceso completo
3. **Cambia la contraseña periódicamente**: Para mayor seguridad
4. **Usa navegador moderno**: Chrome, Firefox, Safari, Edge

---

## 🆓 Costos

### Railway
- **Plan gratuito**: $5 de crédito/mes
- **Uso estimado**: ~$3-4/mes (muy bajo tráfico)
- **Después del crédito**: $0.000231/GB-hora

### Render
- **Plan gratuito**: 750 horas/mes
- **Suficiente para**: Uso del equipo sin problemas
- **Limitación**: Duerme después de 15 min sin uso (despierta en 30 seg)

**Recomendación**: Railway para mejor rendimiento, Render si quieres 100% gratis

---

## 📁 Estructura de Archivos

```
webapp-informes/
├── app.py                    # Backend Flask
├── generar_informe.py        # Script generador de PDFs (con logo)
├── requirements.txt          # Dependencias Python
├── Procfile                  # Configuración de despliegue
├── runtime.txt               # Versión de Python
├── templates/
│   ├── login.html           # Página de login
│   └── index.html           # Aplicación principal
└── README_DEPLOY.md         # Este archivo
```

---

## 🔧 Personalización

### Cambiar Colores
Edita `templates/index.html` y `templates/login.html`:
- Verde: `#10B981` → Tu color
- Amarillo: `#FFC107` → Tu color

### Añadir Campos
Edita `templates/index.html`:
1. Añade campos HTML en la sección correspondiente
2. Añade la lógica en el script JavaScript
3. Actualiza `generar_informe.py` para usar los nuevos campos

---

## ❓ Solución de Problemas

### Error: "No module named 'reportlab'"
- Verifica que `requirements.txt` esté correcto
- Redespliega la aplicación

### Error: "No se puede conectar"
- Verifica que la app esté "Running" en Railway/Render
- Espera 1-2 minutos después del despliegue

### PDF no se descarga
- Verifica que el navegador permita descargas
- Prueba en otro navegador
- Revisa la consola del navegador (F12)

### Contraseña no funciona
- Verifica que no haya espacios extras
- Contraseña por defecto: `CAC2025` (case-sensitive)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway/Render
2. Verifica que todos los archivos estén subidos
3. Comprueba que `requirements.txt` esté completo

---

## 🎉 ¡Listo!

Ya tienes tu generador de informes en la nube, accesible desde cualquier lugar:
- 🌐 Acceso web desde cualquier dispositivo
- 🔒 Protegido con contraseña
- 📊 PDFs profesionales al instante
- 💰 Gratis (o casi gratis)

**URL de ejemplo**: `https://informes-cac.railway.app`

---

**Club Atlético Central** 🟢⚽  
**Versión 2.1 - Web App**  
**Octubre 2025**
