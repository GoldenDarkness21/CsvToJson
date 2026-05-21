"""
Script de prueba para verificar la lógica de transformación sin Streamlit.
Este script permite testear las funciones principales de procesamiento.
"""

import json
import csv
import re
import io
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


def extraer_numero(texto: str) -> Optional[int]:
    """Extrae el primer número entero encontrado en una cadena de texto."""
    numeros = re.findall(r'\d+', texto)
    return int(numeros[0]) if numeros else None


def clasificar_subseccion(subseccion: str) -> Tuple[str, Optional[int], str]:
    """Clasifica el tipo de subsección y extrae información relevante."""
    subseccion_lower = subseccion.lower().strip()
    
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
            return ('tendencia', indice, 'explicacion')
    
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
    """Procesa el contenido del CSV y lo organiza en una estructura jerárquica."""
    lector = csv.DictReader(io.StringIO(csv_content), delimiter=',')
    
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
    
    for fila in lector:
        if 'Capitulo' not in fila or 'subsección' not in fila or 'Contenido_Generado' not in fila:
            continue
        
        nombre_capitulo = fila['Capitulo'].strip()
        subseccion = fila['subsección'].strip()
        contenido = fila['Contenido_Generado'].strip()
        
        num_capitulo = extraer_numero(nombre_capitulo)
        if num_capitulo is None:
            continue
        
        tipo, indice, subtipo = clasificar_subseccion(subseccion)
        
        capitulo = capitulos_data[num_capitulo]
        capitulo['nombre_original'] = nombre_capitulo
        
        if tipo == 'titulo':
            capitulo['titulo'] = contenido
        elif tipo == 'subtitulo':
            capitulo['subtitulo'] = contenido
        elif tipo == 'parrafo':
            capitulo['parrafo_explicativo'] = contenido
        elif tipo == 'scan_cards':
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
    """Construye la estructura final de aprendizajes lista para inyectar en el JSON."""
    aprendizajes = []
    
    capitulos_ordenados = sorted(capitulos_data.items(), key=lambda x: x[0])
    
    for num_capitulo, datos in capitulos_ordenados:
        capitulo_obj = {
            'capitulo': num_capitulo,
            'titulo': datos.get('titulo', ''),
            'subtitulo': datos.get('subtitulo', ''),
            'parrafo_explicativo': datos.get('parrafo_explicativo', ''),
            'scan_cards': datos.get('scan_cards', [])
        }
        
        insights_lista = []
        insights_data = datos.get('insights', {})
        if insights_data:
            insights_ordenados = sorted(insights_data.items(), key=lambda x: x[0])
            for idx_insight, insight_datos in insights_ordenados:
                insight_obj = {
                    'numero': idx_insight,
                    'titulo': insight_datos.get('titulo', ''),
                    'contenido': insight_datos.get('contenido', ''),
                    'frase_cierre': insight_datos.get('frase_cierre', '')
                }
                
                quote_data = insight_datos.get('quote', {})
                if quote_data and (quote_data.get('texto') or quote_data.get('autor') or quote_data.get('afiliacion')):
                    insight_obj['quote'] = {
                        'texto': quote_data.get('texto', ''),
                        'autor': quote_data.get('autor', ''),
                        'afiliacion': quote_data.get('afiliacion', '')
                    }
                
                insights_lista.append(insight_obj)
        
        capitulo_obj['insights'] = insights_lista
        
        tendencias_lista = []
        tendencias_data = datos.get('tendencias', {})
        if tendencias_data:
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
    """Inyecta la estructura de aprendizajes en la plantilla JSON base."""
    resultado = json.loads(json.dumps(plantilla_json))
    resultado['aprendizajes'] = aprendizajes
    return resultado


def test_transformacion():
    """Función de prueba que carga los archivos de ejemplo y ejecuta la transformación."""
    print("=" * 80)
    print("TEST DE TRANSFORMACIÓN CSV A JSON")
    print("=" * 80)
    
    try:
        # Cargar CSV de ejemplo
        print("\n📄 Cargando archivo CSV de ejemplo...")
        with open('Biotech_ESTRUCTURA_CAPITULOS_COMPLETO.csv', 'r', encoding='utf-8-sig') as f:
            csv_content = f.read()
        print("✅ CSV cargado exitosamente")
        
        # Procesar CSV
        print("\n🔄 Procesando datos del CSV...")
        capitulos_data = procesar_csv(csv_content)
        print(f"✅ Se procesaron {len(capitulos_data)} capítulos")
        
        # Construir estructura de aprendizajes
        print("\n🏗️ Construyendo estructura de aprendizajes...")
        aprendizajes = construir_estructura_aprendizajes(capitulos_data)
        print(f"✅ Se construyeron {len(aprendizajes)} capítulos con estructura completa")
        
        # Mostrar estadísticas
        total_insights = sum(len(cap.get('insights', [])) for cap in aprendizajes)
        total_tendencias = sum(len(cap.get('tendencias', [])) for cap in aprendizajes)
        total_scans = sum(len(cap.get('scan_cards', [])) for cap in aprendizajes)
        
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   • Capítulos: {len(aprendizajes)}")
        print(f"   • Insights: {total_insights}")
        print(f"   • Tendencias: {total_tendencias}")
        print(f"   • Scan Cards: {total_scans}")
        
        # Cargar plantilla JSON
        print("\n📄 Cargando plantilla JSON base...")
        with open('info_consolidada_biotech.json', 'r', encoding='utf-8') as f:
            plantilla_json = json.load(f)
        print("✅ Plantilla JSON cargada exitosamente")
        
        # Inyectar aprendizajes
        print("\n💉 Inyectando estructura en la plantilla...")
        resultado = inyectar_en_plantilla(plantilla_json, aprendizajes)
        print("✅ Inyección completada")
        
        # Verificar que otras propiedades se mantengan
        print("\n🔍 Verificando integridad de la plantilla...")
        propiedades_esperadas = ['metadata', 'configuracion', 'autores', 'estadisticas', 'tags']
        for prop in propiedades_esperadas:
            if prop in resultado:
                print(f"   ✅ Propiedad '{prop}' se mantiene intacta")
            else:
                print(f"   ❌ Propiedad '{prop}' falta en el resultado")
        
        # Convertir a JSON string
        json_salida = json.dumps(resultado, ensure_ascii=False, indent=2)
        
        # Guardar resultado
        print("\n💾 Guardando archivo JSON de salida...")
        with open('info_consolidada_ACTUALIZADO.json', 'w', encoding='utf-8') as f:
            f.write(json_salida)
        print("✅ Archivo 'info_consolidada_ACTUALIZADO.json' guardado exitosamente")
        
        # Mostrar vista previa del primer capítulo
        print("\n👁️ VISTA PREVIA DEL PRIMER CAPÍTULO:")
        print("-" * 80)
        if aprendizajes and len(aprendizajes) > 0:
            primer_cap = aprendizajes[0]
            print(f"Capítulo {primer_cap['capitulo']}: {primer_cap['titulo']}")
            print(f"Subtítulo: {primer_cap['subtitulo']}")
            print(f"Insights: {len(primer_cap['insights'])}")
            if primer_cap['insights']:
                print(f"  • Primer insight: {primer_cap['insights'][0]['titulo']}")
            print(f"Tendencias: {len(primer_cap['tendencias'])}")
            if primer_cap['tendencias']:
                print(f"  • Primera tendencia: {primer_cap['tendencias'][0]['nombre']}")
            print(f"Scan Cards: {len(primer_cap['scan_cards'])}")
            if primer_cap['scan_cards']:
                print(f"  • Primeras cards: {', '.join(primer_cap['scan_cards'][:3])}")
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print("\n📁 Archivos generados:")
        print("   • info_consolidada_ACTUALIZADO.json")
        print("\n🚀 Para ejecutar la aplicación web completa:")
        print("   streamlit run app.py")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Archivo no encontrado - {e}")
        print("   Asegúrate de que los archivos de ejemplo estén en el mismo directorio.")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__} - {e}")
        return False


if __name__ == "__main__":
    exit(0 if test_transformacion() else 1)