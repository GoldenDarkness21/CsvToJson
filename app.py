"""
Herramienta de Transformación de Datos (Conversor ETL) - Versión Simplificada
==============================================================================
Aplicación Streamlit para convertir archivos CSV jerárquicos a estructura JSON anidada.
La plantilla JSON base está integrada directamente en el código.

Instrucciones de uso:
1. Ejecutar: streamlit run app.py
2. Cargar el archivo CSV con los datos
3. Hacer clic en "Procesar y Generar"
4. Descargar el archivo JSON resultante

Requisitos:
- Python 3.8+
- Streamlit
"""

import streamlit as st
import json
import csv
import re
import io
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime


# ============================================================================
# CONFIGURACIÓN DE COLORES - PALETA UNIVERSIDAD ICESI
# ============================================================================

COLORES_ICESI = {
    "azul_principal": "#325BBD",
    "azul_oscuro_hover": "#23438C",
    "blanco": "#FFFFFF",
    "gris_estructura": "#8A8D8F",
    "gris_claro_fondo": "#F8F9FA",
    "verde_exito": "#28A745",
    "rojo_error": "#DC3545",
    "amarillo_info": "#FFC107"
}


# ============================================================================
# ESTILOS CSS PERSONALIZADOS CON LA PALETA ICESI
# ============================================================================

def inyectar_estilos_css():
    """Inyecta estilos CSS personalizados con la paleta de colores de la Universidad Icesi."""
    
    estilos = f"""
    <style>
    /* ========================================
       VARIABLES DE COLORES - PALETA ICESI
       ======================================== */
    :root {{
        --azul-icesi: {COLORES_ICESI['azul_principal']};
        --azul-oscuro: {COLORES_ICESI['azul_oscuro_hover']};
        --blanco: {COLORES_ICESI['blanco']};
        --gris-estructura: {COLORES_ICESI['gris_estructura']};
        --gris-claro: {COLORES_ICESI['gris_claro_fondo']};
        --verde-exito: {COLORES_ICESI['verde_exito']};
        --rojo-error: {COLORES_ICESI['rojo_error']};
        --amarillo-info: {COLORES_ICESI['amarillo_info']};
    }}
    
    /* ========================================
       ESTILOS GENERALES
       ======================================== */
    .stApp {{
        background-color: var(--blanco);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* ========================================
       ENCABEZADOS Y TÍTULOS
       ======================================== */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--azul-icesi) !important;
        font-weight: 600;
    }}
    
    .stTitle h1 {{
        color: var(--azul-icesi) !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }}
    
    /* ========================================
       BARRA LATERAL (SIDEBAR)
       ======================================== */
    .stSidebar {{
        background-color: var(--gris-claro);
        border-right: 2px solid var(--gris-estructura);
    }}
    
    .stSidebar h2, .stSidebar h3 {{
        color: var(--azul-icesi) !important;
        border-bottom: 2px solid var(--azul-icesi);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    /* ========================================
       BOTONES PERSONALIZADOS
       ======================================== */
    .stButton > button {{
        background-color: var(--azul-icesi);
        color: var(--blanco);
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(50, 91, 189, 0.2);
    }}
    
    .stButton > button:hover {{
        background-color: var(--azul-oscuro);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(35, 67, 140, 0.3);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Botón de descarga */
    .stDownloadButton > button {{
        background-color: var(--verde-exito);
        color: var(--blanco);
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(40, 167, 69, 0.2);
    }}
    
    .stDownloadButton > button:hover {{
        background-color: #218838;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(33, 136, 56, 0.3);
    }}
    
    /* ========================================
       CAMPOS DE CARGA DE ARCHIVOS
       ======================================== */
    .stFileUploader {{
        border: 2px dashed var(--gris-estructura);
        border-radius: 12px;
        padding: 2rem;
        background-color: var(--gris-claro);
        transition: all 0.3s ease;
    }}
    
    .stFileUploader:hover {{
        border-color: var(--azul-icesi);
        background-color: #F0F4FF;
    }}
    
    .stFileUploader label {{
        color: var(--azul-icesi);
        font-weight: 600;
    }}
    
    /* ========================================
       TARJETAS Y CONTENEDORES
       ======================================== */
    .css-1r6slb0 {{
        background-color: var(--blanco);
        border: 1px solid var(--gris-estructura);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(138, 141, 143, 0.15);
    }}
    
    /* ========================================
       MÉTRICAS Y ESTADÍSTICAS
       ======================================== */
    .stMetric {{
        background-color: var(--gris-claro);
        border-left: 4px solid var(--azul-icesi);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }}
    
    .stMetricLabel {{
        color: var(--gris-estructura);
        font-size: 0.9rem;
        font-weight: 600;
    }}
    
    .stMetricValue {{
        color: var(--azul-icesi);
        font-size: 2rem;
        font-weight: 700;
    }}
    
    /* ========================================
       MENSAJES DE ÉXITO Y ERROR
       ======================================== */
    .stSuccess {{
        background-color: #D4EDDA;
        border-left: 4px solid var(--verde-exito);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .stError {{
        background-color: #F8D7DA;
        border-left: 4px solid var(--rojo-error);
        color: #721C24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .stInfo {{
        background-color: #FFF3CD;
        border-left: 4px solid var(--amarillo-info);
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* ========================================
       EXPANDERS (SECCIONES DESPLEGABLES)
       ======================================== */
    .streamlit-expanderHeader {{
        background-color: var(--gris-claro);
        border: 1px solid var(--gris-estructura);
        border-radius: 8px;
        padding: 1rem;
        color: var(--azul-icesi);
        font-weight: 600;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: #E9ECEF;
    }}
    
    .streamlit-expanderContent {{
        background-color: var(--blanco);
        border: 1px solid var(--gris-estructura);
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
    }}
    
    /* ========================================
       DIVISORES
       ======================================== */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(to right, var(--azul-icesi), var(--gris-estructura));
        margin: 2rem 0;
    }}
    
    /* ========================================
       TEXTO Y PÁRRAFOS
       ======================================== */
    p, li {{
        color: #333333;
        line-height: 1.6;
    }}
    
    strong {{
        color: var(--azul-icesi);
    }}
    
    /* ========================================
       TABLAS (para visualización JSON)
       ======================================== */
    .stJson table {{
        border-collapse: collapse;
        width: 100%;
    }}
    
    .stJson th {{
        background-color: var(--azul-icesi);
        color: var(--blanco);
        padding: 12px;
        text-align: left;
        font-weight: 600;
    }}
    
    .stJson td {{
        padding: 10px 12px;
        border-bottom: 1px solid var(--gris-claro);
    }}
    
    .stJson tr:hover td {{
        background-color: var(--gris-claro);
    }}
    
    /* ========================================
       SCROLLBAR PERSONALIZADO
       ======================================== */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--gris-claro);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--gris-estructura);
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--azul-icesi);
    }}
    
    /* ========================================
       RESPONSIVE DESIGN
       ======================================== */
    @media (max-width: 768px) {{
        .stTitle h1 {{
            font-size: 2rem;
        }}
        
        .stButton > button {{
            width: 100%;
            margin-bottom: 0.5rem;
        }}
        
        .stMetric {{
            margin-bottom: 1rem;
        }}
    }}
    </style>
    """
    
    st.markdown(estilos, unsafe_allow_html=True)


# ============================================================================
# PLANTILLA BASE JSON - INTEGRADA DIRECTAMENTE EN EL CÓDIGO
# ============================================================================

PLANTILLA_BASE_JSON = {
    "metadata": {
        "titulo": "Informe Consolidado Biotech",
        "version": "1.0",
        "fecha_creacion": "2024-01-15",
        "autor": "Equipo de Investigación",
        "descripcion": "Análisis completo del ecosistema biotech con aprendizajes clave y tendencias del sector"
    },
    "configuracion": {
        "idioma": "es",
        "moneda": "USD",
        "region": "Global",
        "categorias": [
            "biotecnología",
            "salud digital",
            "medicina personalizada",
            "terapias avanzadas"
        ]
    },
    "autores": [
        {
            "nombre": "Dra. María González",
            "afiliacion": "Instituto de Biotecnología",
            "email": "m.gonzalez@instituto.edu",
            "rol": "Investigadora Principal"
        },
        {
            "nombre": "Dr. Carlos Rodríguez",
            "afiliacion": "Universidad Tecnológica",
            "email": "c.rodriguez@universidad.edu",
            "rol": "Analista Senior"
        }
    ],
    "aprendizajes": [],
    "estadisticas": {
        "total_capitulos": 0,
        "total_insights": 0,
        "total_tendencias": 0,
        "ultima_actualizacion": None
    },
    "tags": [
        "biotech",
        "innovación",
        "investigación",
        "tendencias",
        "análisis"
    ]
}


# ============================================================================
# FUNCIONES DE PROCESAMIENTO DE DATOS
# ============================================================================

def extraer_numero(texto: str) -> Optional[int]:
    """
    Extrae el primer número entero encontrado en una cadena de texto.
    
    Args:
        texto: Cadena de texto donde buscar el número
        
    Returns:
        El número entero encontrado o None si no hay número
    """
    numeros = re.findall(r'\d+', texto)
    return int(numeros[0]) if numeros else None


def clasificar_subseccion(subseccion: str) -> Tuple[str, Optional[int], str]:
    """
    Clasifica el tipo de subsección y extrae información relevante.
    
    Args:
        subseccion: Nombre de la subsección a clasificar
        
    Returns:
        Tupla con (tipo, indice, subtipo) donde:
        - tipo: 'titulo', 'subtitulo', 'parrafo', 'scan_cards', 'insight', 'tendencia', 'quote', 'autor', 'otro'
        - indice: Número asociado (para insights/tendencias) o None
        - subtipo: Detalle adicional del mapeo
    """
    subseccion_lower = subseccion.lower().strip()
    
    # Verificar si es insight (debe verificarse antes que "título" para evitar falsos positivos)
    if 'insight' in subseccion_lower:
        indice = extraer_numero(subseccion_lower)
        if 'título' in subseccion_lower or 'titulo' in subseccion_lower:
            return ('insight', indice, 'titulo')
        elif 'frase de cierre' in subseccion_lower:
            return ('insight', indice, 'frase_cierre')
        elif 'quote' in subseccion_lower:
            return ('quote', indice, 'texto')
        elif 'autor' in subseccion_lower or 'afiliación' in subseccion_lower or 'afiliacion' in subseccion_lower:
            return ('autor', indice, 'afiliacion' if 'afiliacion' in subseccion_lower or 'afiliación' in subseccion_lower else 'autor')
        else:
            return ('insight', indice, 'contenido')
    
    # Verificar si es tendencia
    if 'tendencia' in subseccion_lower:
        indice = extraer_numero(subseccion_lower)
        if 'nombre' in subseccion_lower:
            return ('tendencia', indice, 'nombre')
        elif 'explicación' in subseccion_lower or 'explicacion' in subseccion_lower:
            return ('tendencia', indice, 'explicacion')
        elif 'frase cuantitativa' in subseccion_lower:
            return ('tendencia', indice, 'frase_cuantitativa')
        elif 'implicación' in subseccion_lower or 'implicacion' in subseccion_lower:
            return ('tendencia', indice, 'implicacion_estrategica')
        else:
            return ('tendencia', indice, 'explicacion')  # Por defecto
    
    # Verificar otros tipos
    if 'título' in subseccion_lower or 'titulo' in subseccion_lower:
        return ('titulo', None, 'titulo')
    elif 'subtítulo' in subseccion_lower or 'subtitulo' in subseccion_lower:
        return ('subtitulo', None, 'subtitulo')
    elif 'párrafo explicativo' in subseccion_lower or 'parrafo explicativo' in subseccion_lower:
        return ('parrafo', None, 'parrafo_explicativo')
    elif 'scan cards' in subseccion_lower:
        return ('scan_cards', None, 'scan_cards')
    else:
        return ('otro', None, subseccion_lower)


def procesar_csv(csv_content: str) -> Dict[str, Any]:
    """
    Procesa el contenido del CSV y lo organiza en una estructura jerárquica.
    
    Args:
        csv_content: Contenido del archivo CSV como string
        
    Returns:
        Diccionario con la estructura de capítulos, insights y tendencias
    """
    # Leer CSV con encoding utf-8-sig para manejar BOM
    lector = csv.DictReader(io.StringIO(csv_content), delimiter=',')
    
    # Estructura temporal para almacenar datos
    capitulos_data = defaultdict(lambda: {
        'titulo': '',
        'subtitulo': '',
        'parrafo_explicativo': '',
        'scan_cards': [],
        'insights': defaultdict(lambda: {
            'titulo': '',
            'contenido': '',
            'frase_cierre': '',
            'quote': {'texto': '', 'autor': '', 'afiliacion': ''}
        }),
        'tendencias': defaultdict(lambda: {
            'nombre': '',
            'explicacion': '',
            'frase_cuantitativa': '',
            'implicacion_estrategica': ''
        })
    })
    
    # Procesar cada fila
    for fila in lector:
        # Validar que existan las columnas necesarias
        if 'Capitulo' not in fila or 'subsección' not in fila or 'Contenido_Generado' not in fila:
            continue
        
        nombre_capitulo = fila['Capitulo'].strip()
        subseccion = fila['subsección'].strip()
        contenido = fila['Contenido_Generado'].strip()
        
        # Extraer número del capítulo para ordenamiento
        num_capitulo = extraer_numero(nombre_capitulo)
        if num_capitulo is None:
            continue
        
        # Clasificar la subsección
        tipo, indice, subtipo = clasificar_subseccion(subseccion)
        
        # Asignar contenido según el tipo
        capitulo = capitulos_data[num_capitulo]
        capitulo['nombre_original'] = nombre_capitulo
        
        if tipo == 'titulo':
            capitulo['titulo'] = contenido
        elif tipo == 'subtitulo':
            capitulo['subtitulo'] = contenido
        elif tipo == 'parrafo':
            capitulo['parrafo_explicativo'] = contenido
        elif tipo == 'scan_cards':
            # Separar por comas y limpiar espacios
            scan_cards_lista = [item.strip() for item in contenido.split(',')]
            capitulo['scan_cards'] = scan_cards_lista
        elif tipo == 'insight' and indice is not None:
            insight = capitulo['insights'][indice]
            if subtipo == 'titulo':
                insight['titulo'] = contenido
            elif subtipo == 'contenido':
                insight['contenido'] = contenido
            elif subtipo == 'frase_cierre':
                insight['frase_cierre'] = contenido
        elif tipo == 'quote' and indice is not None:
            insight = capitulo['insights'][indice]
            insight['quote']['texto'] = contenido
        elif tipo == 'autor' and indice is not None:
            insight = capitulo['insights'][indice]
            # Separar autor y afiliación si hay coma
            if ',' in contenido:
                partes = contenido.split(',', 1)
                insight['quote']['autor'] = partes[0].strip()
                insight['quote']['afiliacion'] = partes[1].strip()
            else:
                if subtipo == 'autor':
                    insight['quote']['autor'] = contenido
                else:
                    insight['quote']['afiliacion'] = contenido
        elif tipo == 'tendencia' and indice is not None:
            tendencia = capitulo['tendencias'][indice]
            if subtipo == 'nombre':
                tendencia['nombre'] = contenido
            elif subtipo == 'explicacion':
                tendencia['explicacion'] = contenido
            elif subtipo == 'frase_cuantitativa':
                tendencia['frase_cuantitativa'] = contenido
            elif subtipo == 'implicacion_estrategica':
                tendencia['implicacion_estrategica'] = contenido
    
    return dict(capitulos_data)


def construir_estructura_aprendizajes(capitulos_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Construye la estructura final de aprendizajes lista para inyectar en el JSON.
    
    Args:
        capitulos_data: Diccionario con los datos procesados de capítulos
        
    Returns:
        Lista de objetos capítulo con su estructura completa
    """
    aprendizajes = []
    
    # Ordenar capítulos por número
    capitulos_ordenados = sorted(capitulos_data.items(), key=lambda x: x[0])
    
    for num_capitulo, datos in capitulos_ordenados:
        capitulo_obj = {
            'capitulo': num_capitulo,
            'titulo': datos.get('titulo', ''),
            'subtitulo': datos.get('subtitulo', ''),
            'parrafo_explicativo': datos.get('parrafo_explicativo', ''),
            'scan_cards': datos.get('scan_cards', [])
        }
        
        # Procesar insights
        insights_lista = []
        insights_data = datos.get('insights', {})
        if insights_data:
            # Ordenar insights por índice
            insights_ordenados = sorted(insights_data.items(), key=lambda x: x[0])
            for idx_insight, insight_datos in insights_ordenados:
                insight_obj = {
                    'numero': idx_insight,
                    'titulo': insight_datos.get('titulo', ''),
                    'contenido': insight_datos.get('contenido', ''),
                    'frase_cierre': insight_datos.get('frase_cierre', '')
                }
                
                # Agregar quote si existe información
                quote_data = insight_datos.get('quote', {})
                if quote_data and (quote_data.get('texto') or quote_data.get('autor') or quote_data.get('afiliacion')):
                    insight_obj['quote'] = {
                        'texto': quote_data.get('texto', ''),
                        'autor': quote_data.get('autor', ''),
                        'afiliacion': quote_data.get('afiliacion', '')
                    }
                
                insights_lista.append(insight_obj)
        
        capitulo_obj['insights'] = insights_lista
        
        # Procesar tendencias
        tendencias_lista = []
        tendencias_data = datos.get('tendencias', {})
        if tendencias_data:
            # Ordenar tendencias por índice
            tendencias_ordenadas = sorted(tendencias_data.items(), key=lambda x: x[0])
            for idx_tendencia, tendencia_datos in tendencias_ordenadas:
                tendencia_obj = {
                    'numero': idx_tendencia,
                    'nombre': tendencia_datos.get('nombre', ''),
                    'explicacion': tendencia_datos.get('explicacion', ''),
                    'frase_cuantitativa': tendencia_datos.get('frase_cuantitativa', ''),
                    'implicacion_estrategica': tendencia_datos.get('implicacion_estrategica', '')
                }
                tendencias_lista.append(tendencia_obj)
        
        capitulo_obj['tendencias'] = tendencias_lista
        aprendizajes.append(capitulo_obj)
    
    return aprendizajes


def inyectar_en_plantilla(plantilla_json: Dict[str, Any], aprendizajes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Inyecta la estructura de aprendizajes en la plantilla JSON base.
    
    Args:
        plantilla_json: Diccionario con la plantilla JSON base
        aprendizajes: Lista de objetos capítulo procesados
        
    Returns:
        Diccionario JSON con los aprendizajes inyectados
    """
    # Crear una copia profunda para no modificar el original
    resultado = json.loads(json.dumps(plantilla_json))
    
    # Inyectar o reemplazar únicamente la propiedad "aprendizajes"
    resultado['aprendizajes'] = aprendizajes
    
    # Actualizar estadísticas
    resultado['estadisticas']['total_capitulos'] = len(aprendizajes)
    resultado['estadisticas']['total_insights'] = sum(len(cap.get('insights', [])) for cap in aprendizajes)
    resultado['estadisticas']['total_tendencias'] = sum(len(cap.get('tendencias', [])) for cap in aprendizajes)
    resultado['estadisticas']['ultima_actualizacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return resultado


# ============================================================================
# INTERFAZ DE USUARIO STREAMLIT
# ============================================================================

def main():
    """Función principal de la aplicación Streamlit."""
    
    # Configuración de la página
    st.set_page_config(
        page_title="Conversor ETL - CSV a JSON",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inyectar estilos CSS personalizados
    inyectar_estilos_css()
    
    # Encabezado con logo (opcional - se puede agregar un logo de Icesi si existe)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #325BBD; font-size: 2.5rem; font-weight: 700;">
             Herramienta de Transformación de Datos (ETL)
        </h1>
        <p style="color: #8A8D8F; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
            Esta aplicación permite cargar un archivo CSV jerárquico y transformarlo en una estructura JSON anidada,
            utilizando una plantilla JSON base integrada directamente en el código.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra lateral con instrucciones
    with st.sidebar:
        # Mostrar logo de innlab
        try:
            st.image("innlab-logo.svg", width=400, clamp=True)
            st.markdown("<div style='text-align: center; margin-bottom: 1rem;'><p style='color: #8A8D8F; font-size: 0.85rem;'><strong>InnLab</strong> - Universidad Icesi</p></div>", unsafe_allow_html=True)
        except:
            # Si no se encuentra el logo, mostrar texto alternativo
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #325BBD; font-size: 1.5rem; font-weight: 700; margin: 0;">
                    InnLab
                </h3>
                <p style="color: #8A8D8F; font-size: 0.85rem; margin: 0.25rem 0 0 0;">
                    Universidad Icesi
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="color: #325BBD; border-bottom: 2px solid #325BBD; padding-bottom: 0.5rem;">
                 Instrucciones
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        1. **Cargar CSV**: Sube el archivo CSV con los datos a transformar.
        2. **Procesar**: Haz clic en el botón para procesar los datos.
        3. **Descargar**: Obtén el archivo JSON resultante.
        """)
        
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 style="color: #325BBD; border-bottom: 2px solid #325BBD; padding-bottom: 0.5rem;">
                ℹ️ Información
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        - **Encoding**: UTF-8 con detección de BOM
        - **Formato CSV**: Delimitado por comas
        - **Columnas requeridas**: 
          - `Capitulo`
          - `subsección`
          - `Contenido_Generado`
        """)
        
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 style="color: #325BBD; border-bottom: 2px solid #325BBD; padding-bottom: 0.5rem;">
                📄 Plantilla Integrada
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("""
        La plantilla JSON base con metadatos, configuración, autores y estructura estática 
        ya viene integrada en la aplicación. Solo necesitas proporcionar los datos dinámicos 
        a través del archivo CSV.
        """)
    
    # Cargador único de archivo CSV
    st.markdown("""
    <div style="background-color: #F8F9FA; border: 2px dashed #8A8D8F; border-radius: 12px; padding: 2rem; margin: 2rem 0;">
        <h2 style="color: #325BBD; text-align: center; margin-bottom: 1rem;">
             Cargar Archivo CSV de Datos
        </h2>
        <p style="color: #8A8D8F; text-align: center; margin-bottom: 1.5rem;">
            Arrastra o selecciona tu archivo CSV aquí
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    archivo_csv = st.file_uploader(
        "Selecciona tu archivo CSV",
        type=['csv'],
        help="Archivo CSV con la estructura de capítulos y contenidos (ej: Biotech_ESTRUCTURA_CAPITULOS_COMPLETO.csv)"
    )
    
    # Estado de sesión para almacenar resultados
    if 'resultado_transformacion' not in st.session_state:
        st.session_state.resultado_transformacion = None
    if 'json_salida' not in st.session_state:
        st.session_state.json_salida = None
    
    # Botón de procesamiento (solo habilitado si hay CSV)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        boton_procesar = st.button(
            "Procesar y Generar",
            type="primary",
            disabled=archivo_csv is None,
            use_container_width=True
        )
    
    # Procesar transformación
    if boton_procesar and archivo_csv:
        try:
            with st.spinner("Procesando datos..."):
                # Usar la plantilla base integrada
                plantilla_json = PLANTILLA_BASE_JSON
                
                # Leer CSV (primero decodificar a string)
                csv_content = archivo_csv.getvalue().decode('utf-8-sig')
                
                # Procesar CSV
                capitulos_data = procesar_csv(csv_content)
                
                # Construir estructura de aprendizajes
                aprendizajes = construir_estructura_aprendizajes(capitulos_data)
                
                # Inyectar en plantilla
                resultado = inyectar_en_plantilla(plantilla_json, aprendizajes)
                
                # Convertir a JSON string
                json_salida = json.dumps(resultado, ensure_ascii=False, indent=2)
                
                # Guardar en sesión
                st.session_state.resultado_transformacion = resultado
                st.session_state.json_salida = json_salida
                
                # Mostrar resumen
                st.success("✅ Transformación completada exitosamente!")
                
                # Mostrar estadísticas
                st.markdown("""
                <div style="margin: 2rem 0;">
                    <h3 style="color: #325BBD; text-align: center; margin-bottom: 1.5rem;">
                        Estadísticas del Procesamiento
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                col_est1, col_est2, col_est3, col_est4 = st.columns(4)
                with col_est1:
                    st.metric("Capítulos", len(aprendizajes))
                with col_est2:
                    total_insights = sum(len(cap.get('insights', [])) for cap in aprendizajes)
                    st.metric("Insights", total_insights)
                with col_est3:
                    total_tendencias = sum(len(cap.get('tendencias', [])) for cap in aprendizajes)
                    st.metric("Tendencias", total_tendencias)
                with col_est4:
                    total_scans = sum(len(cap.get('scan_cards', [])) for cap in aprendizajes)
                    st.metric("Scan Cards", total_scans)
                
        except Exception as e:
            st.error(f"❌ Error durante la transformación: {str(e)}")
            st.exception(e)
    
    # Mostrar vista previa y botón de descarga
    if st.session_state.json_salida:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Sección de descarga (ahora arriba)
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h3 style="color: #325BBD; text-align: center; margin-bottom: 1.5rem;">
                Descarga del Archivo JSON
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de descarga centrado y destacado
        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            st.download_button(
                label="📥 Descargar JSON",
                data=st.session_state.json_salida,
                file_name="info_consolidada_ACTUALIZADO.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Advertencia sobre encoding
        st.info("""
        **Nota**: El archivo se descarga con encoding UTF-8 para garantizar la correcta visualización 
        de caracteres especiales del español (tildes, ñ, etc.).
        """)
        
        # Vista previa del JSON (ahora abajo y expandida por defecto)
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h3 style="color: #325BBD; text-align: center; margin-bottom: 1.5rem;">
                Vista Previa del JSON Generado
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar JSON directamente (sin expander, siempre visible)
        st.json(st.session_state.resultado_transformacion)
        


if __name__ == "__main__":
    main()