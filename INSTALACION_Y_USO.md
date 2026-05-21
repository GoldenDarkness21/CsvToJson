# Guía Rápida de Instalación y Uso - Versión Simplificada

## 📋 Resumen del Proyecto

Herramienta ETL que transforma archivos CSV jerárquicos en estructuras JSON anidadas, con una interfaz web interactiva desarrollada en Streamlit. **La plantilla JSON base ahora está integrada directamente en el código**, simplificando la experiencia de usuario.

## 🎯 Características Principales

✅ **Interfaz simplificada** - Solo un cargador de archivos (CSV)  
✅ **Plantilla JSON integrada** en el código  
✅ **Procesamiento automático** con un solo clic  
✅ **Mapeo inteligente** usando expresiones regulares  
✅ **Estructura anidada** de capítulos, insights y tendencias  
✅ **Descarga directa** del JSON generado  
✅ **Soporte UTF-8** completo para caracteres en español  
✅ **Robusto y flexible** - funciona con cualquier CSV del mismo tipo  

## 📁 Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Aplicación principal con plantilla JSON integrada |
| `Biotech_ESTRUCTURA_CAPITULOS_COMPLETO.csv` | CSV de ejemplo para probar |
| `info_consolidada_biotech.json` | Referencia de la plantilla (solo consulta) |
| `requirements.txt` | Dependencias (streamlit) |
| `test_transformacion.py` | Script de prueba sin Streamlit |
| `README.md` | Documentación completa |

## 🚀 Instalación Rápida

### Paso 1: Instalar Streamlit
```bash
pip install streamlit
```

### Paso 2: Ejecutar la Aplicación
```bash
streamlit run app.py
```

### Paso 3: Acceder
El navegador se abrirá automáticamente en `http://localhost:8501`

## 🎮 Uso de la Aplicación

### Flujo Simplificado (3 pasos)

1. **Cargar CSV** → Arrastra o selecciona tu archivo CSV
2. **Procesar** → Clic en "🚀 Procesar y Generar"
3. **Descargar** → Clic en "📥 Descargar JSON"

¡Listo! El archivo `info_consolidada_ACTUALIZADO.json` se descargará automáticamente.

## 🧪 Probar sin Streamlit

Si solo quieres verificar que la lógica funciona:

```bash
python test_transformacion.py
```

Este script:
- Carga los archivos de ejemplo
- Ejecuta la transformación
- Muestra estadísticas
- Genera el archivo de salida
- Verifica que todo funcione

## 📊 ¿Qué Hace la Herramienta?

### Entrada: CSV Jerárquico
```
Capítulo 1 | Título | Introducción al tema
Capítulo 1 | Insight 1 | Contenido del insight
Capítulo 1 | Tendencia 1 | Nombre de tendencia
...
```

### Salida: JSON Anidado
```json
{
  "metadata": { ... },
  "autores": [ ... ],
  "aprendizajes": [
    {
      "capitulo": 1,
      "titulo": "Introducción al tema",
      "insights": [
        {
          "numero": 1,
          "contenido": "Contenido del insight",
          "quote": { ... }
        }
      ],
      "tendencias": [
        {
          "numero": 1,
          "nombre": "Nombre de tendencia"
        }
      ]
    }
  ],
  "estadisticas": { ... }
}
```

## 🔧 Lógica de Mapeo Inteligente

La herramienta detecta automáticamente:

- **Capítulos**: Por el campo "Capítulo" y extrae el número
- **Títulos/Subtítulos**: Por las subsecciones correspondientes
- **Insights**: Por la palabra "insight" + número
- **Tendencias**: Por la palabra "tendencia" + número
- **Quotes/Autores**: Por las subsecciones específicas
- **Scan Cards**: Separa por comas automáticamente

### Ejemplos de Detección:
| Subsección en CSV | Mapeo a JSON |
|-------------------|--------------|
| `"Título"` | → `aprendizajes[].titulo` |
| `"Título Insight 1"` | → `aprendizajes[].insights[0].titulo` |
| `"Quote Insight 1"` | → `aprendizajes[].insights[0].quote.texto` |
| `"Autor Insight 1"` | → `aprendizajes[].insights[0].quote.autor/afiliacion` |
| `"Nombre Tendencia 1"` | → `aprendizajes[].tendencias[0].nombre` |

## 📝 Formato CSV Requerido

Columnas obligatorias:
- `Capitulo` - Nombre del capítulo (ej: "Capítulo 1")
- `subsección` - Tipo de contenido (ej: "Título", "Insight 1", "Tendencia 1")
- `Contenido_Generado` - El texto o dato a insertar

## 🌐 Despliegue en la Nube

### Streamlit Cloud (Gratis)
1. Subir a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar repositorio
4. ¡Listo!

### Heroku / Otros
Ver instrucciones completas en `README.md`

## 🛠️ Requisitos Técnicos

- **Python**: 3.8 o superior
- **Streamlit**: 1.28.0 o superior
- **Navegador**: Cualquier navegador moderno
- **Encoding**: UTF-8 con detección de BOM

## 📝 Consideraciones Importantes

### Para el CSV:
- Debe tener encoding UTF-8
- Columnas requeridas: `Capitulo`, `subsección`, `Contenido_Generado`
- Delimitado por comas (formato estándar CSV)

### Para la Plantilla Integrada:
- Está definida en `app.py` como `PLANTILLA_BASE_JSON`
- Contiene metadata, configuración, autores y tags
- Solo se modifica la propiedad `"aprendizajes"`
- Las estadísticas se actualizan automáticamente

### Para la Ejecución:
- No requiere configuración especial
- Funciona en Windows, Mac, Linux
- Puede ejecutarse localmente o en la nube

## 🐛 Solución de Problemas Comunes

### "Streamlit no está instalado"
```bash
pip install streamlit
```

### "Error al cargar CSV"
- Verificar que sea CSV real (no Excel)
- Guardar con encoding UTF-8
- Verificar nombres de columnas

### "Caracteres raros en el output"
- El archivo usa UTF-8 por defecto
- Abrir con editor que soporte UTF-8 (VS Code, Notepad++, etc.)

### "El botón está deshabilitado"
- Asegurarse de que el CSV esté cargado
- Verificar que el archivo no esté vacío

## 📞 Soporte

- **Documentación completa**: Ver `README.md`
- **Streamlit docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Issues**: Reportar en el repositorio de GitHub

## ✨ Próximos Pasos

1. **Probar la aplicación**:
   ```bash
   streamlit run app.py
   ```

2. **Cargar tu CSV**:
   - Arrastra tu archivo CSV con los datos

3. **Procesar y descargar**:
   - Clic en "Procesar y Generar"
   - Clic en "Descargar JSON"

4. **Personalizar** (opcional):
   - Modificar `PLANTILLA_BASE_JSON` en `app.py` para cambiar la estructura base
   - Ajustar la lógica de mapeo según necesidades

## 🎉 ¡Listo para Usar!

La herramienta está **completamente funcional** y lista para producción. Solo necesitas:

1. Tener Python instalado
2. Instalar Streamlit
3. Ejecutar `streamlit run app.py`
4. Cargar tu CSV y ¡comenzar a transformar!

---

**Creado con ❤️ - Herramienta ETL CSV → JSON (Versión Simplificada)**