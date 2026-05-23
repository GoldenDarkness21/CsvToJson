"""
Motor de Inyección y Consolidación de Datos sobre un Molde Maestro Rígido
Aplicación Streamlit para procesamiento de archivos CSV/JSON y generación de reportes consolidados
"""

import streamlit as st
import json
import csv
import copy
import re
import io
from typing import Dict, List, Any, Optional

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Motor de Consolidación de Reportes Biotech",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# MOLDE MAESTRO INALTERABLE (BASE JSON)
# =============================================================================
MOLDE_MAESTRO: Dict[str, Any] = {
    "portada": {
        "titulo_principal": "Informe de Inteligencia Tecnológica: Biotecnología y Futuros Emergentes",
        "subtitulo": "Análisis de Tendencias, Escenarios Plausibles y Recomendaciones Estratégicas",
        "version": "1.0",
        "fecha_publicacion": "2024",
        "organizacion": "Centro de Estudios en Biotecnología y Futuros Estratégicos",
        "autores": [
            "Equipo de Inteligencia Tecnológica",
            "Comité de Prospectiva Biotecnológica"
        ],
        "logo_url": "https://ejemplo.org/logo-biotech.png",
        "color_corporativo": "#1a5276",
        "idioma": "es"
    },
    "tabla-contenidos": {
        "secciones": [
            {"orden": 1, "titulo": "Ficha Técnica", "pagina": 3},
            {"orden": 2, "titulo": "Resumen Ejecutivo", "pagina": 4},
            {"orden": 3, "titulo": "Introducción", "pagina": 6},
            {"orden": 4, "titulo": "Aprendizajes e Insights por Capítulos", "pagina": 8},
            {"orden": 5, "titulo": "Escenarios Plausibles", "pagina": 15},
            {"orden": 6, "titulo": "Glosario de Términos", "pagina": 25},
            {"orden": 7, "titulo": "Referencias y Scan Cards", "pagina": 28},
            {"orden": 8, "titulo": "Anexos Metodológicos", "pagina": 32}
        ]
    },
    "ficha-tecnica-1": {
        "titulo_documento": "Informe de Inteligencia Tecnológica en Biotecnología",
        "tipo_documento": "Reporte de Prospectiva Tecnológica",
        "alcance": "Global con énfasis en Latinoamérica",
        "horizonte_temporal": "2024-2035",
        "metodologia": "Análisis STEEP + prospectiva estratégica + revisión sistemática de literatura",
        "fuentes_primarias": 150,
        "fuentes_secundarias": 320,
        "expertos_consultados": 45,
        "fecha_elaboracion": "Enero - Marzo 2024",
        "palabras_clave": [
            "biotecnología",
            "futuros emergentes",
            "innovación disruptiva",
            "análisis STEEP",
            "escenarios plausibles",
            "inteligencia tecnológica"
        ]
    },
    "resumen-ejecutivo": {
        "introduccion": (
            "Este informe presenta un análisis comprehensivo de las tendencias biotecnológicas "
            "más relevantes que moldearán el panorama global en las próximas dos décadas. "
            "A través de una metodología rigurosa que combina análisis STEEP (Social, Tecnológico, "
            "Económico, Ambiental y Político) con técnicas de prospectiva estratégica, identificamos "
            "los impulsores críticos de cambio y construimos escenarios plausibles que permiten a "
            "tomadores de decisión anticipar y prepararse para futuros alternativos."
        ),
        "hallazgos_principales": [
            {
                "orden": 1,
                "hallazgo": "La convergencia entre biotecnología, inteligencia artificial y nanotecnología está acelerando la innovación a ritmos sin precedentes",
                "nivel_impacto": "Crítico",
                "horizonte": "Corto-Mediano Plazo (2024-2028)"
            },
            {
                "orden": 2,
                "hallazgo": "Las tecnologías de edición genética CRISPR y sus derivados están democratizando el acceso a modificaciones genéticas",
                "nivel_impacto": "Alto",
                "horizonte": "Mediano Plazo (2026-2030)"
            },
            {
                "orden": 3,
                "hallazgo": "La biología sintética está emergiendo como plataforma transversal para múltiples industrias",
                "nivel_impacto": "Alto",
                "horizonte": "Mediano-Largo Plazo (2028-2035)"
            },
            {
                "orden": 4,
                "hallazgo": "Los marcos regulatorios globales enfrentan desafíos significativos para mantener el ritmo de la innovación biotecnológica",
                "nivel_impacto": "Crítico",
                "horizonte": "Continuo"
            }
        ],
        "recomendaciones_estrategicas": [
            {
                "orden": 1,
                "recomendacion": "Establecer comités de vigilancia tecnológica interdisciplinarios",
                "prioridad": "Alta",
                "responsable": "Dirección de I+D+i"
            },
            {
                "orden": 2,
                "recomendacion": "Desarrollar alianzas estratégicas con centros de investigación líderes",
                "prioridad": "Alta",
                "responsable": "Dirección de Alianzas"
            },
            {
                "orden": 3,
                "recomendacion": "Invertir en capacidades internas de biología sintética y análisis de datos ómicos",
                "prioridad": "Media",
                "responsable": "Dirección de Talento"
            }
        ]
    },
    "introduccion": {
        "contexto_global": (
            "El panorama biotecnológico global experimenta una transformación acelerada impulsada "
            "por la convergencia de múltiples disciplinas científicas. La intersección entre "
            "biología, computación, ingeniería y ciencias de materiales está generando oportunidades "
            "sin precedentes para abordar desafíos en salud, agricultura, energía y sostenibilidad "
            "ambiental. Este contexto de innovación disruptiva requiere marcos analíticos robustos "
            "que permitan comprender las implicaciones estratégicas y construir capacidades de "
            "respuesta ágiles y efectivas."
        ),
        "objetivos_documento": [
            "Proporcionar un mapeo comprehensivo de las tendencias biotecnológicas emergentes",
            "Construir escenarios plausibles que ilustren futuros alternativos para el sector",
            "Identificar oportunidades y riesgos estratégicos para tomadores de decisión",
            "Establecer recomendaciones accionables para el desarrollo de capacidades organizacionales",
            "Documentar aprendizajes e insights derivados de análisis de casos y revisión de literatura"
        ],
        "alcance_limitaciones": {
            "cobertura_geografica": "Global con profundidad en Norteamérica, Europa y Asia-Pacífico",
            "sectores_incluidos": [
                "Salud y medicina personalizada",
                "Agricultura y seguridad alimentaria",
                "Bioenergía y biocombustibles",
                "Biomateriales y manufactura sostenible",
                "Bioprocesos industriales"
            ],
            "limitaciones": [
                "Rapidez del cambio tecnológico puede superar el ciclo de actualización del informe",
                "Sesgo inherente hacia tecnologías con mayor visibilidad en literatura científica",
                "Variabilidad regulatoria entre jurisdicciones dificulta generalizaciones"
            ]
        },
        "estructura_documento": (
            "El documento se organiza en siete secciones principales: (1) Ficha Técnica que "
            "describe la metodología y alcance; (2) Resumen Ejecutivo con hallazgos clave; "
            "(3) Introducción al contexto y objetivos; (4) Aprendizajes e Insights organizados "
            "por capítulos temáticos; (5) Escenarios Plausibles construidos mediante metodología "
            "STEEP; (6) Glosario de términos técnicos; y (7) Referencias y Scan Cards con "
            "fuentes documentales detalladas."
        )
    },
    "aprendizajes": [],
    "escenarios": [],
    "glosario": {
        "terminos": [
            {
                "termino": "Biotecnología",
                "definicion": "Uso de sistemas biológicos u organismos vivos para desarrollar o crear productos, a menudo combinando biología con tecnología.",
                "categoria": "General"
            },
            {
                "termino": "CRISPR-Cas9",
                "definicion": "Sistema de edición genética que permite modificar secuencias de ADN de manera precisa, eficiente y flexible.",
                "categoria": "Edición Genética"
            },
            {
                "termino": "Biología Sintética",
                "definicion": "Diseño y construcción de nuevos sistemas biológicos o rediseño de sistemas existentes para fines útiles.",
                "categoria": "Biología Sintética"
            },
            {
                "termino": "ómica",
                "definicion": "Término colectivo para campos de estudio en biología que terminan en -ómica (genómica, proteómica, metabolómica).",
                "categoria": "Análisis Molecular"
            },
            {
                "termino": "Terapia Génica",
                "definicion": "Técnica experimental que usa genes para tratar o prevenir enfermedades mediante la inserción de un gen en las células.",
                "categoria": "Medicina"
            },
            {
                "termino": "Biomarcador",
                "definicion": "Indicador biológico medible que puede ser usado para evaluar procesos biológicos, condiciones patológicas o respuestas a intervenciones.",
                "categoria": "Diagnóstico"
            },
            {
                "termino": "Microbioma",
                "definicion": "Conjunto de microorganismos (bacterias, arqueas, hongos, virus) que habitan en un ambiente particular, especialmente en el cuerpo humano.",
                "categoria": "Microbiología"
            },
            {
                "termino": "Bioinformática",
                "definicion": "Campo interdisciplinario que desarrolla métodos y herramientas de software para comprender datos biológicos, especialmente grandes conjuntos de datos.",
                "categoria": "Computación"
            },
            {
                "termino": "Fermentación de Precisión",
                "definicion": "Uso de microorganismos programados para producir compuestos específicos de manera eficiente y escalable.",
                "categoria": "Bioprocesos"
            },
            {
                "termino": "Órgano-en-un-chip",
                "definicion": "Sistema microfluídico que simula las actividades, mecánicas y respuestas fisiológicas de órganos humanos.",
                "categoria": "Modelado"
            }
        ]
    },
    "scan-cards": [],
    "anexos": {
        "metodologia_detallada": {
            "enfoque_general": (
                "La metodología empleada combina análisis STEEP estructurado con técnicas de "
                "prospectiva estratégica y revisión sistemática de literatura científica y técnica. "
                "El proceso incluyó: (1) Búsqueda y filtrado de fuentes primarias y secundarias; "
                "(2) Codificación y categorización temática; (3) Identificación de patrones y "
                "tendencias emergentes; (4) Construcción de escenarios mediante análisis de "
                "incertidumbres críticas; (5) Validación con panel de expertos."
            ),
            "criterios_inclusion": [
                "Publicaciones de los últimos 10 años (2014-2024)",
                "Fuentes revisadas por pares o informes de organizaciones reconocidas",
                "Enfoque en aplicaciones biotecnológicas con potencial de impacto significativo",
                "Disponibilidad de datos verificables y metodología transparente"
            ],
            "fuentes_datos": [
                "Bases de datos científicas (PubMed, Scopus, Web of Science)",
                "Repositorios de patentes (USPTO, EPO, WIPO)",
                "Informes de inteligencia de mercado (CB Insights, PitchBook)",
                "Publicaciones de agencias gubernamentales y organismos internacionales"
            ]
        },
        "matriz_steeP": {
            "social": {
                "descripcion": "Factores demográficos, culturales, éticos y de aceptación pública",
                "dimensiones": [
                    "Percepción pública de tecnologías biotecnológicas",
                    "Consideraciones éticas y bioéticas",
                    "Equidad en acceso a beneficios biotecnológicos",
                    "Cambios demográficos y necesidades de salud"
                ]
            },
            "tecnologico": {
                "descripcion": "Avances científicos, convergencia tecnológica y capacidades emergentes",
                "dimensiones": [
                    "Tasas de innovación y ciclos de desarrollo",
                    "Convergencia interdisciplinaria",
                    "Infraestructura de investigación y desarrollo",
                    "Madurez tecnológica (TRL) de innovaciones clave"
                ]
            },
            "economico": {
                "descripcion": "Mercados, inversiones, modelos de negocio y competitividad",
                "dimensiones": [
                    "Tamaño y crecimiento de mercados biotecnológicos",
                    "Flujos de inversión en I+D biotecnológica",
                    "Modelos de negocio emergentes",
                    "Cadenas de valor y ecosistemas de innovación"
                ]
            },
            "ambiental": {
                "descripcion": "Sostenibilidad, impacto ecológico y economía circular",
                "dimensiones": [
                    "Contribución a objetivos de sostenibilidad",
                    "Huella ambiental de procesos biotecnológicos",
                    "Aplicaciones en remediación y conservación",
                    "Economía circular y bioeconomía"
                ]
            },
            "politico": {
                "descripcion": "Marcos regulatorios, políticas públicas y gobernanza",
                "dimensiones": [
                    "Regulaciones de bioseguridad y biotecnología",
                    "Políticas de fomento a la innovación",
                    "Acuerdos internacionales y estándares",
                    "Gobernanza de tecnologías emergentes"
                ]
            }
        }
    },
    "metadata": {
        "fecha_generacion": "2024-03-15",
        "version_esquema": "2.1",
        "autor_esquema": "Centro de Estudios en Biotecnología y Futuros Estratégicos",
        "licencia": "CC BY-NC-SA 4.0",
        "contacto": "info@cebfe.org",
        "sitio_web": "https://www.cebfe.org"
    }
}


# =============================================================================
# FUNCIONES DE PROCESAMIENTO
# =============================================================================

def procesar_archivo(apoyo_archivo, tipo_archivo: str) -> Optional[Any]:
    """
    Procesa un archivo subido (CSV o JSON) y retorna su contenido estructurado.
    
    Args:
        apoyo_archivo: Objeto UploadedFile de Streamlit
        tipo_archivo: Extensión del archivo ('csv' o 'json')
    
    Returns:
        Contenido procesado del archivo o None si hay error
    """
    try:
        if tipo_archivo == 'json':
            return json.load(apoyo_archivo)
        elif tipo_archivo == 'csv':
            # Intentar detectar el delimitador
            contenido = apoyo_archivo.getvalue().decode('utf-8-sig')
            primer_linea = contenido.split('\n')[0]
            
            if ';' in primer_linea and ',' not in primer_linea:
                delimitador = ';'
            else:
                delimitador = ','
            
            reader = csv.DictReader(io.StringIO(contenido), delimiter=delimitador)
            return list(reader)
    except Exception as e:
        st.error(f"Error procesando archivo: {str(e)}")
        return None
    
    return None


def procesar_modulo_aprendizajes(datos) -> List[Dict[str, Any]]:
    """
    Procesa los datos del Módulo 1 (Aprendizajes e Insights).
    
    Si los datos son JSON, los retorna directamente.
    Si son CSV, agrupa por Capítulo y estructura jerárquicamente.
    
    Args:
        datos: Lista de registros (desde CSV) o diccionario (desde JSON)
    
    Returns:
        Lista de objetos de aprendizajes estructurados
    """
    if isinstance(datos, dict):
        # Ya viene como JSON estructurado
        return datos.get("aprendizajes", datos if isinstance(datos, list) else [datos])
    
    if not isinstance(datos, list) or len(datos) == 0:
        return []
    
    # Procesamiento de CSV - Agrupar por Capítulo
    capitulos_dict: Dict[str, Dict[str, Any]] = {}
    
    for fila in datos:
        nombre_capitulo = fila.get('Capitulo', fila.get('capitulo', 'Sin Capítulo'))
        seccion = fila.get('sección', fila.get('seccion', fila.get('Sección', 'general'))).strip().lower()
        
        if nombre_capitulo not in capitulos_dict:
            capitulos_dict[nombre_capitulo] = {
                "nombre_capitulo": nombre_capitulo,
                "insights": [],
                "tendencias": []
            }
        
        # Crear objeto de insight/tendencia basado en la sección
        item = {
            "titulo": fila.get('titulo', fila.get('Título', fila.get('Title', ''))),
            "descripcion": fila.get('descripcion', fila.get('Descripción', fila.get('Description', ''))),
            "nivel_impacto": fila.get('nivel_impacto', fila.get('Nivel_Impacto', 'Medio')),
            "horizonte_temporal": fila.get('horizonte', fila.get('Horizonte', fila.get('Horizonte_Temporal', ''))),
            "evidencia": fila.get('evidencia', fila.get('Evidencia', '')),
            "fuentes": fila.get('fuentes', fila.get('Fuentes', ''))
        }
        
        # Clasificar según la sección
        if 'insight' in seccion or seccion == 'general':
            capitulos_dict[nombre_capitulo]["insights"].append(item)
        elif 'tendencia' in seccion:
            capitulos_dict[nombre_capitulo]["tendencias"].append(item)
        else:
            # Por defecto, agregar a insights
            capitulos_dict[nombre_capitulo]["insights"].append(item)
    
    # Convertir a lista
    resultados = []
    for capitulo_data in capitulos_dict.values():
        # Filtrar listas vacías
        if capitulo_data["insights"] or capitulo_data["tendencias"]:
            resultados.append(capitulo_data)
    
    return resultados


def procesar_modulo_escenarios(datos) -> List[Dict[str, Any]]:
    """
    Procesa los datos del Módulo 2 (Escenarios Plausibles).
    
    Si los datos son JSON, los retorna directamente.
    Si son CSV, mapea columnas y parsea línea de tiempo y STEEP.
    
    Args:
        datos: Lista de registros (desde CSV) o diccionario (desde JSON)
    
    Returns:
        Lista de objetos de escenarios estructurados
    """
    if isinstance(datos, dict):
        # Ya viene como JSON estructurado
        return datos.get("escenarios", datos if isinstance(datos, list) else [datos])
    
    if not isinstance(datos, list) or len(datos) == 0:
        return []
    
    escenarios = []
    
    for fila in datos:
        escenario = {
            "titulo": fila.get('Nombre y Título Evocador', fila.get('titulo', fila.get('Título', ''))),
            "descripcion_corta": fila.get('descripcion', fila.get('Descripcion', fila.get('Descripción', ''))),
            "secciones": {},
            "linea_tiempo": {},
            "end_state": {}
        }
        
        # Mapear columnas de texto largo a secciones en snake_case
        columnas_secciones = {
            'logica_del_escenario': ['Logica_del_escenario', 'Lógica_del_escenario', 'logica_escenario', 'lógica_escenario'],
            'elementos_predeterminados': ['Elementos_predeterminados', 'Elementos_predeterminados', 'elementos_predeterminados'],
            'narrativa_experiencial': ['Narrativa_experiencial', 'Narrativa_experiencial', 'narrativa_experiencial'],
            'implicaciones_estrategicas': ['Implicaciones_estrategicas', 'Implicaciones_estratégicas', 'implicaciones_estratégicas']
        }
        
        for clave_seccion, posibles_nombres in columnas_secciones.items():
            for nombre in posibles_nombres:
                if nombre in fila and fila[nombre]:
                    escenario["secciones"][clave_seccion] = fila[nombre]
                    break
        
        # Parsear línea de tiempo
        columna_timeline = fila.get('Mapa_historia_linea_tiempo', fila.get('Línea_de_tiempo', fila.get('linea_tiempo', '')))
        if columna_timeline:
            escenario["linea_tiempo"] = parsear_linea_tiempo(columna_timeline)
        
        # Parsear estado final STEEP
        columna_end_state = fila.get('Estado_final', fila.get('End_state', fila.get('estado_final', '')))
        if columna_end_state:
            escenario["end_state"] = parsear_steep(columna_end_state)
        
        escenarios.append(escenario)
    
    return escenarios


def parsear_linea_tiempo(texto: str) -> Dict[str, str]:
    """
    Parsea el texto de línea de tiempo extrayendo rangos de años.
    
    Args:
        texto: Texto conteniendo rangos de años y descripciones
    
    Returns:
        Diccionario con rangos de años como claves
    """
    resultado = {}
    
    # Patrón para encontrar rangos de años (ej: 2026-2027, 2028-2030)
    patron_rango = r'(\d{4})\s*-\s*(\d{4})'
    # Patrón para año individual
    patron_anio = r'(\d{4})'
    
    lineas = texto.split('\n') if '\n' in texto else [texto]
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        
        # Buscar rango de años
        match_rango = re.search(patron_rango, linea)
        if match_rango:
            anio_inicio = match_rango.group(1)
            anio_fin = match_rango.group(2)
            clave = f"{anio_inicio}-{anio_fin}"
            
            # Extraer texto descriptivo (lo que no es el rango de años)
            descripcion = re.sub(patron_rango, '', linea).strip().strip(':').strip('-').strip()
            
            if clave not in resultado:
                resultado[clave] = descripcion
            else:
                resultado[clave] += " " + descripcion if descripcion else ""
            continue
        
        # Buscar año individual
        match_anio = re.search(patron_anio, linea)
        if match_anio:
            anio = match_anio.group(1)
            descripcion = re.sub(patron_anio, '', linea).strip().strip(':').strip('-').strip()
            
            if anio not in resultado:
                resultado[anio] = descripcion
            else:
                resultado[anio] += " " + descripcion if descripcion else ""
    
    # El último elemento se considera estado_final
    if resultado:
        ultima_clave = list(resultado.keys())[-1]
        resultado["estado_final"] = resultado.pop(ultima_clave) if ultima_clave != "estado_final" else resultado["estado_final"]
    
    return resultado


def parsear_steep(texto: str) -> Dict[str, str]:
    """
    Parsea el texto de estado final identificando categorías STEEP.
    
    Args:
        texto: Texto conteniendo viñetas o palabras clave STEEP
    
    Returns:
        Diccionario con categorías STEEP como claves
    """
    resultado = {}
    
    categorias_steep = {
        'social': [r'\b[Ss]ocial\b', r'\b[Ss]ociedad\b', r'\b[Dd]emográfico\b', r'\b[Cc]ultural\b', r'\b[Éé]tico\b'],
        'tecnologico': [r'\b[Tt]ecnológico\b', r'\b[Tt]ecnologia\b', r'\b[Tt]ecnología\b', r'\b[Ii]nnovación\b', r'\b[Ii]nnovacion\b'],
        'economico': [r'\b[Ee]conómico\b', r'\b[Ee]conomia\b', r'\b[Ee]conomía\b', r'\b[Mm]ercado\b', r'\b[Ii]nversión\b'],
        'ambiental': [r'\b[Aa]mbiental\b', r'\b[Ee]cológico\b', r'\b[Ee]cologico\b', r'\b[Ss]ostenible\b', r'\b[Ss]ustentable\b'],
        'politico': [r'\b[Pp]olítico\b', r'\b[Pp]olitico\b', r'\b[Rr]egulatorio\b', r'\b[Rr]egulación\b', r'\b[Gg]obernanza\b']
    }
    
    # Dividir por viñetas comunes
    separadores = ['\n', '•', '●', '○', '▪', '▸', '-', '*']
    segmentos = [texto]
    
    for sep in separadores:
        nuevos_segmentos = []
        for seg in segmentos:
            nuevos_segmentos.extend(seg.split(sep))
        segmentos = nuevos_segmentos
    
    for segmento in segmentos:
        segmento = segmento.strip()
        if not segmento:
            continue
        
        # Identificar categoría STEEP
        categoria_encontrada = None
        for categoria, patrones in categorias_steep.items():
            for patron in patrones:
                if re.search(patron, segmento):
                    categoria_encontrada = categoria
                    break
            if categoria_encontrada:
                break
        
        if categoria_encontrada:
            if categoria_encontrada not in resultado:
                resultado[categoria_encontrada] = segmento
            else:
                resultado[categoria_encontrada] += " " + segmento
        else:
            # Si no se identifica categoría, agregar a 'otros'
            if 'otros' not in resultado:
                resultado['otros'] = segmento
            else:
                resultado['otros'] += " " + segmento
    
    return resultado


def procesar_modulo_scan_cards(datos) -> List[Dict[str, Any]]:
    """
    Procesa los datos del Módulo 3 (Scan Cards / Documentos).
    
    Si los datos son JSON, los retorna directamente.
    Si son CSV, transforma cada fila en objeto plano.
    
    Args:
        datos: Lista de registros (desde CSV) o diccionario (desde JSON)
    
    Returns:
        Lista de objetos de scan cards estructurados
    """
    if isinstance(datos, dict):
        # Ya viene como JSON estructurado
        return datos.get("scan-cards", datos.get("scan_cards", datos if isinstance(datos, list) else [datos]))
    
    if not isinstance(datos, list) or len(datos) == 0:
        return []
    
    scan_cards = []
    
    # Mapeo de posibles nombres de columnas
    mapeo_columnas = {
        'id': ['ID', 'id', 'Id', 'Código', 'codigo', 'Código_ID'],
        'calidad': ['Calidad', 'calidad', 'Quality', 'quality', 'Nivel_Calidad'],
        'titulo': ['Title', 'title', 'Título', 'titulo', 'Titulo', 'Título_Documento'],
        'anio': ['Year', 'year', 'Año', 'anio', 'Año_Publicacion', 'Fecha'],
        'fuente': ['Source', 'source', 'Fuente', 'fuente', 'Origen', 'Publicacion'],
        'autores': ['Authors', 'authors', 'Autores', 'autores', 'Autor', 'Autoría'],
        'resumen': ['Abstract', 'abstract', 'Resumen', 'resumen', 'Descripción', 'descripcion']
    }
    
    for fila in datos:
        scan_card = {}
        
        for clave, posibles_nombres in mapeo_columnas.items():
            valor = None
            for nombre in posibles_nombres:
                if nombre in fila:
                    valor = fila[nombre]
                    break
            
            # Limpiar valor si existe
            if valor is not None:
                valor = str(valor).strip()
                if valor:
                    scan_card[clave] = valor
        
        # Agregar campos adicionales no mapeados
        for clave_fila, valor_fila in fila.items():
            if clave_fila not in [n for nombres in mapeo_columnas.values() for n in nombres]:
                valor = str(valor_fila).strip() if valor_fila else ''
                if valor:
                    scan_card[clave_fila] = valor
        
        scan_cards.append(scan_card)
    
    return scan_cards


# =============================================================================
# INTERFAZ DE USUARIO
# =============================================================================

st.title("🧬 Motor de Consolidación de Reportes Biotech")
st.markdown("""
Esta aplicación permite cargar archivos de datos (CSV o JSON) y consolidarlos 
en un reporte estructurado basado en una plantilla maestra institucional.
""")

st.divider()

# Crear tres columnas para los cargadores
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📚 Módulo 1: Aprendizajes")
    archivo_aprendizajes = st.file_uploader(
        "Datos de Aprendizajes e Insights",
        type=["csv", "json"],
        key="uploader_aprendizajes",
        help="Archivo CSV o JSON con datos de capítulos, insights y tendencias"
    )

with col2:
    st.subheader("🔮 Módulo 2: Escenarios")
    archivo_escenarios = st.file_uploader(
        "Datos de Escenarios Plausibles",
        type=["csv", "json"],
        key="uploader_escenarios",
        help="Archivo CSV o JSON con escenarios, líneas de tiempo y análisis STEEP"
    )

with col3:
    st.subheader("📋 Módulo 3: Referencias")
    archivo_scan_cards = st.file_uploader(
        "Datos de Documentos / Scan Cards",
        type=["csv", "json"],
        key="uploader_scan_cards",
        help="Archivo CSV o JSON con referencias documentales y fuentes"
    )

st.divider()

# Estado de sesión para almacenar resultado procesado
if 'resultado_procesado' not in st.session_state:
    st.session_state.resultado_procesado = None
if 'mensaje_error' not in st.session_state:
    st.session_state.mensaje_error = None


def procesar_todo():
    """
    Función principal de procesamiento que se ejecuta al hacer clic en el botón.
    """
    try:
        # Crear copia profunda del molde maestro
        resultado = copy.deepcopy(MOLDE_MAESTRO)
        
        # Procesar Módulo 1: Aprendizajes
        if archivo_aprendizajes is not None:
            nombre = archivo_aprendizajes.name
            tipo = nombre.split('.')[-1].lower()
            datos = procesar_archivo(archivo_aprendizajes, tipo)
            
            if datos is not None:
                aprendizajes = procesar_modulo_aprendizajes(datos)
                resultado["aprendizajes"] = aprendizajes
                st.success(f"✅ Módulo 1 procesado: {len(aprendizajes)} capítulos cargados")
            else:
                st.warning("⚠️ Módulo 1: Error al procesar archivo")
        else:
            st.info("ℹ️ Módulo 1: No se cargó archivo, se mantiene plantilla base")
        
        # Procesar Módulo 2: Escenarios
        if archivo_escenarios is not None:
            nombre = archivo_escenarios.name
            tipo = nombre.split('.')[-1].lower()
            datos = procesar_archivo(archivo_escenarios, tipo)
            
            if datos is not None:
                escenarios = procesar_modulo_escenarios(datos)
                resultado["escenarios"] = escenarios
                st.success(f"✅ Módulo 2 procesado: {len(escenarios)} escenarios cargados")
            else:
                st.warning("⚠️ Módulo 2: Error al procesar archivo")
        else:
            st.info("ℹ️ Módulo 2: No se cargó archivo, se mantiene plantilla base")
        
        # Procesar Módulo 3: Scan Cards
        if archivo_scan_cards is not None:
            nombre = archivo_scan_cards.name
            tipo = nombre.split('.')[-1].lower()
            datos = procesar_archivo(archivo_scan_cards, tipo)
            
            if datos is not None:
                scan_cards = procesar_modulo_scan_cards(datos)
                resultado["scan-cards"] = scan_cards
                st.success(f"✅ Módulo 3 procesado: {len(scan_cards)} referencias cargadas")
            else:
                st.warning("⚠️ Módulo 3: Error al procesar archivo")
        else:
            st.info("ℹ️ Módulo 3: No se cargó archivo, se mantiene plantilla base")
        
        # Actualizar metadata
        from datetime import datetime
        resultado["metadata"]["fecha_generacion"] = datetime.now().strftime("%Y-%m-%d")
        
        # Guardar en sesión
        st.session_state.resultado_procesado = resultado
        st.session_state.mensaje_error = None
        
    except Exception as e:
        st.session_state.mensaje_error = f"Error crítico en procesamiento: {str(e)}"
        st.session_state.resultado_procesado = None
        st.error(st.session_state.mensaje_error)


# Botón de procesamiento
st.subheader("⚙️ Procesamiento")
col_btn1, col_btn2 = st.columns([1, 4])

with col_btn1:
    btn_procesar = st.button(
        "Procesar y Unificar Todo",
        type="primary",
        use_container_width=True
    )

if btn_procesar:
    procesar_todo()

st.divider()

# Sección de descarga
st.subheader("📥 Descarga del Reporte")

if st.session_state.resultado_procesado is not None:
    # Convertir a JSON con ensure_ascii=False para preservar caracteres especiales
    json_output = json.dumps(
        st.session_state.resultado_procesado,
        ensure_ascii=False,
        indent=4
    )
    
    col_dl1, col_dl2 = st.columns([1, 4])
    with col_dl1:
        st.download_button(
            label="📄 Descargar JSON",
            data=json_output,
            file_name="reporte_biotech_consolidado.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.success("✅ Los archivos se procesaron y ensamblaron exitosamente.")
    
    # Mostrar resumen estadístico
    with st.expander("📊 Resumen Estadístico del Reporte"):
        resumen = {
            "Capítulos de Aprendizajes": len(st.session_state.resultado_procesado.get("aprendizajes", [])),
            "Escenarios Plausibles": len(st.session_state.resultado_procesado.get("escenarios", [])),
            "Referencias / Scan Cards": len(st.session_state.resultado_procesado.get("scan-cards", [])),
            "Términos en Glosario": len(st.session_state.resultado_procesado.get("glosario", {}).get("terminos", []))
        }
        st.json(resumen)
        
        # Vista previa de la estructura
        st.subheader("Vista Previa de Estructura")
        estructura_preview = {
            "portada": "✓ Sección completa",
            "tabla-contenidos": "✓ Sección completa",
            "ficha-tecnica-1": "✓ Sección completa",
            "resumen-ejecutivo": "✓ Sección completa",
            "introduccion": "✓ Sección completa",
            "aprendizajes": f"✓ {len(st.session_state.resultado_procesado.get('aprendizajes', []))} capítulos",
            "escenarios": f"✓ {len(st.session_state.resultado_procesado.get('escenarios', []))} escenarios",
            "glosario": f"✓ {len(st.session_state.resultado_procesado.get('glosario', {}).get('terminos', []))} términos",
            "scan-cards": f"✓ {len(st.session_state.resultado_procesado.get('scan-cards', []))} referencias",
            "anexos": "✓ Sección completa",
            "metadata": "✓ Actualizada"
        }
        for seccion, estado in estructura_preview.items():
            st.text(f"  {seccion:30s} → {estado}")

elif st.session_state.mensaje_error:
    st.error(f"❌ {st.session_state.mensaje_error}")
else:
    st.info("👆 Cargue archivos y presione 'Procesar y Unificar Todo' para comenzar.")

# =============================================================================
# PIE DE PÁGINA
# =============================================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Motor de Consolidación de Reportes Biotech v1.0</p>
    <p>Centro de Estudios en Biotecnología y Futuros Estratégicos</p>
</div>
""", unsafe_allow_html=True)