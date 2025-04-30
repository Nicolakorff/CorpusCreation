import json
import os

def guardar_corpus_json(corpus, nombre_archivo='data/corpus.json'):
    """Guarda una lista de diccionarios (corpus) en un archivo JSON."""
    try:
        # Asegurarse de que el directorio exista
        os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, indent=4, ensure_ascii=False)
        print(f"Corpus guardado correctamente en '{nombre_archivo}'.")
    except IOError as e:
        print(f"Error al guardar el corpus en '{nombre_archivo}': {e}")

def cargar_configuracion(nombre_archivo='config.json'):
    """Carga la configuración desde un archivo JSON."""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Advertencia: El archivo de configuración '{nombre_archivo}' no se encontró. Usando configuración por defecto.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON '{nombre_archivo}': {e}")
        return {}

def obtener_valor_configuracion(config, clave, valor_por_defecto=None):
    """Obtiene un valor de la configuración o devuelve un valor por defecto."""
    return config.get(clave, valor_por_defecto)

def imprimir_top_palabras(top_n_palabras, n=10):
    """Imprime las n palabras más frecuentes de una lista de tuplas (palabra, frecuencia)."""
    print(f"\nTop {n} palabras más frecuentes:")
    for palabra, frecuencia in top_n_palabras[:n]:
        print(f"- '{palabra}': {frecuencia}")