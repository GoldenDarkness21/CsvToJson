# Herramienta de Transformación de Datos (ETL) - CSV a JSON

## Descripción

Esta aplicación Streamlit permite convertir archivos CSV jerárquicos en estructuras JSON anidadas, utilizando una **plantilla JSON base integrada directamente en el código**. La herramienta está diseñada para procesar datos de capítulos, insights, tendencias y otros contenidos de manera dinámica y robusta.

## Características Principales

- ✅ **Interfaz simplificada**: Solo requiere cargar el archivo CSV
- ✅ **Plantilla JSON integrada**: Metadatos, configuración y estructura estática ya vienen en el código
- ✅ **Procesamiento en tiempo real** con botón de transformación
- ✅ **Mapeo dinámico** basado en expresiones regulares
- ✅ **Estructura anidada** de aprendizajes (capítulos, insights, tendencias)
- ✅ **Descarga automática** del archivo generado
- ✅ **Soporte UTF-8** con detección de BOM para compatibilidad con Excel
- ✅ **Interfaz intuitiva** con Streamlit

## Requisitos Técnicos

- Python 3.8 o superior
- Streamlit 1.28.0 o superior
- Navegador web moderno

## Instalación

1. **Clonar o descargar el repositorio:**
   ```bash
   git clone https://github.com/GoldenDarkness21/Raoccked-main.git
   cd CsvToJson
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

4. **Acceder a la aplicación:**
   - El navegador se abrirá automáticamente en `http://localhost:8501`
   - O accede manualmente a esa URL

## Uso de la Aplicación

### Paso 1: Cargar CSV

- Sube el archivo CSV con la información a transformar
- Ejemplo: `Biotech_ESTRUCTURA_CAPITULOS_COMPLETO.csv`
- Debe contener al menos tres columnas: `Capitulo`, `subsección`, `Contenido_Generado`

### Paso 2: Procesar Datos

- Haz clic en el botón **"🚀 Procesar y Generar"**
- La aplicación procesará los datos y mostrará:
  - Mensaje de éxito
  - Estadísticas (capítulos, insights, tendencias, scan cards)
  - Vista previa del JSON generado

### Paso 3: Descargar Resultado

- Haz clic en **"📥 Descargar JSON"**
- El archivo se descargará como `info_consolidada_ACTUALIZADO.json`
- El archivo mantendrá todos los caracteres especiales del español (tildes, ñ, etc.)

## Formato del CSV Esperado

El archivo CSV debe seguir esta estructura:

| Capitulo | subsección | Contenido_Generado |
|----------|------------|-------------------|
| Capítulo 1 | Título | Introducción al tema |
| Capítulo 1 | Subtítulo | Descripción breve |
| Capítulo 1 | Párrafo explicativo | Contenido detallado |
| Capítulo 1 | Scan Cards | Elemento1,Elemento2,Elemento3 |
| Capítulo 1 | Título Insight 1 | Título del insight |
| Capítulo 1 | Insight 1 | Contenido del insight |
| Capítulo 1 | Frase de cierre Insight 1 | Frase final |
| Capítulo 1 | Quote Insight 1 | "Texto de la cita" |
| Capítulo 1 | Autor Insight 1 | Autor, Afiliación |
| Capítulo 1 | Nombre Tendencia 1 | Nombre de la tendencia |
| Capítulo 1 | Explicación Tendencia 1 | Descripción |
| Capítulo 1 | Frase cuantitativa Tendencia 1 | Dato numérico |
| Capítulo 1 | Implicación Tendencia 1 | Impacto estratégico |

## Lógica de Mapeo

### Capítulos
- Se agrupan dinámicamente por el campo `Capitulo`
- El número se extrae automáticamente (ej: "Capítulo 1" → 1)
- Se ordenan secuencialmente (1, 2, 3, ...)

### Subsecciones Principales
- **Título** → `titulo` del capítulo
- **Subtítulo** → `subtitulo` del capítulo
- **Párrafo explicativo** → `parrafo_explicativo`
- **Scan Cards** → Array de strings (separados por comas)

### Insights (N-Insights)
- Se detectan por contener "insight" en el nombre
- El número se extrae automáticamente (ej: "Insight 12" → ID 12)
- **Título Insight N** → `titulo` del insight
- **Insight N** → `contenido` del insight
- **Frase de cierre Insight N** → `frase_cierre`
- **Quote Insight N** → `quote.texto`
- **Autor Insight N** → `quote.autor` y `quote.afiliacion` (si hay coma)

### Tendencias (N-Tendencias)
- Se detectan por contener "tendencia" en el nombre
- El número se extrae automáticamente
- **Nombre Tendencia N** → `nombre`
- **Explicación Tendencia N** → `explicacion`
- **Frase cuantitativa Tendencia N** → `frase_cuantitativa`
- **Implicación Tendencia N** → `implicacion_estrategica`

## Estructura del JSON de Salida

```json
{
  "metadata": {
    "titulo": "Informe Consolidado Biotech",
    "version": "1.0",
    "fecha_creacion": "2024-01-15",
    "autor": "Equipo de Investigación",
    "descripcion": "Análisis completo del ecosistema biotech..."
  },
  "configuracion": {
    "idioma": "es",
    "moneda": "USD",
    "region": "Global",
    "categorias": ["biotecnología", "salud digital", ...]
  },
  "autores": [
    {
      "nombre": "Dra. María González",
      "afiliacion": "Instituto de Biotecnología",
      "email": "m.gonzalez@instituto.edu",
      "rol": "Investigadora Principal"
    }
  ],
  "aprendizajes": [
    {
      "capitulo": 1,
      "titulo": "Título del capítulo",
      "subtitulo": "Subtítulo",
      "parrafo_explicativo": "Párrafo completo",
      "scan_cards": ["Elemento1", "Elemento2"],
      "insights": [
        {
          "numero": 1,
          "titulo": "Título del insight",
          "contenido": "Contenido del insight",
          "frase_cierre": "Frase de cierre",
          "quote": {
            "texto": "Texto de la cita",
            "autor": "Autor",
            "afiliacion": "Afiliación"
          }
        }
      ],
      "tendencias": [
        {
          "numero": 1,
          "nombre": "Nombre de la tendencia",
          "explicacion": "Explicación",
          "frase_cuantitativa": "Dato numérico",
          "implicacion_estrategica": "Impacto"
        }
      ]
    }
  ],
  "estadisticas": {
    "total_capitulos": 3,
    "total_insights": 6,
    "total_tendencias": 3,
    "ultima_actualizacion": "2024-01-15 10:30:00"
  },
  "tags": ["biotech", "innovación", "investigación", ...]
}
```

## Archivos Incluidos

- `app.py` - Aplicación principal Streamlit con plantilla integrada
- `info_consolidada_biotech.json` - Plantilla JSON base de ejemplo (referencia)
- `Biotech_ESTRUCTURA_CAPITULOS_COMPLETO.csv` - CSV de datos de ejemplo
- `requirements.txt` - Dependencias del proyecto
- `test_transformacion.py` - Script de prueba para verificar la lógica

## Consideraciones Técnicas

### Plantilla Integrada
- La plantilla JSON base (`PLANTILLA_BASE_JSON`) está definida como constante en `app.py`
- Contiene metadata, configuración, autores y estructura estática
- Solo se modifica la propiedad `"aprendizajes"` durante el procesamiento
- Las estadísticas se actualizan automáticamente

### Robustez en la Lectura
- Se utiliza `encoding='utf-8-sig'` para manejar BOM de Excel
- Se usa `csv.DictReader` para procesamiento seguro
- Validaciones defensivas para columnas requeridas

### Flexibilidad en el Mapeo
- Búsqueda por subcadenas en minúsculas (`.lower().strip()`)
- Expresiones regulares para extracción de números
- No se requieren coincidencias exactas rígidas

### Integridad de la Plantilla
- Solo se modifica la propiedad `"aprendizajes"`
- El resto de la estructura JSON se mantiene intacta
- Se utiliza `json.dumps(ensure_ascii=False)` para preservar caracteres UTF-8

## Solución de Problemas

### La aplicación no inicia
```bash
# Verificar instalación de Streamlit
pip show streamlit

# Reinstalar si es necesario
pip install --upgrade streamlit
```

### Error al cargar CSV
- Verificar que el archivo esté en formato CSV (delimitado por comas)
- Asegurarse de que tenga encoding UTF-8
- Confirmar que las columnas se llamen exactamente: `Capitulo`, `subsección`, `Contenido_Generado`

### Caracteres especiales no se muestran correctamente
- El archivo JSON de salida usa `ensure_ascii=False` para mantener caracteres UTF-8
- Si hay problemas, verificar que el editor de texto soporte UTF-8

### El botón de procesamiento está deshabilitado
- Asegurarse de que el archivo CSV esté cargado
- Verificar que el archivo no esté vacío

## Despliegue en la Nube

### Streamlit Cloud (Recomendado)
1. Subir el repositorio a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repositorio
4. El archivo principal debe ser `app.py`
5. El archivo de requisitos es `requirements.txt`

### Heroku
```bash
# Crear archivos adicionales necesarios
echo "web: sh run.sh" > Procfile
echo "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > run.sh
chmod +x run.sh

# Desplegar
heroku create nombre-app
git push heroku main
```

## Licencia

Este proyecto está bajo la licencia MIT.

## Contribución

Las contribuciones son bienvenidas. Por favor:
1. Haz un fork del repositorio
2. Crea una rama para tu feature
3. Envía un Pull Request

## Soporte

Para problemas o preguntas:
- Revisar la documentación de Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- Reportar issues en el repositorio de GitHub

---

**Desarrollado con ❤️ usando Python y Streamlit**