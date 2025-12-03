# Versión 1.0 - Backup

Esta carpeta contiene el backup de la versión original del sistema de informes.

## Archivos incluidos:

- `templates/index.html` - Formulario original con 5 pasos
- `generar_informe.py` - Generador PDF original
- `generar_plan_partido.py` - Generador de plan de partido original

## Características v1.0:

- Formulario de 5 pasos con análisis de texto
- PDF con campo de jugadores posicionados
- Análisis táctico por párrafos
- Integración con IA (Groq)
- Plan de partido táctico

## Fecha de backup:

Diciembre 2025 - Previo a actualización v2.0 (análisis por fases del juego)

## Para restaurar:

Si necesitas volver a esta versión:
```bash
cp v1_backup/templates/index.html templates/
cp v1_backup/generar_informe.py .
cp v1_backup/generar_plan_partido.py .
```
