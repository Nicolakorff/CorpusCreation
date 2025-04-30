import re
import string
import spacy
from src.utils import cargar_configuracion, obtener_valor_configuracion
import os

# Cargar el modelo de spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Advertencia: No se pudo cargar el modelo 'en_core_web_sm'. Asegúrate de que esté descargado (python -m spacy download en_core_web_sm).")
    nlp = None

def cargar_stopwords(ruta_archivo):
    """Carga stopwords desde un archivo de texto."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f]
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo de stopwords '{ruta_archivo}'.")
        return []
    except IOError as e:
        print(f"Error al leer el archivo de stopwords '{ruta_archivo}': {e}")
        return []

def limpiar_texto(texto):
    """Limpia el texto eliminando caracteres especiales y múltiples espacios."""
    if texto is None:
        return ""
    texto = re.sub(r'[^a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def procesar_texto(texto, stopwords_excluir=None, ruta_archivo_stopwords=None, cargar_stopwords_desde_archivo=False):
    """Procesa el texto con spaCy: tokeniza, elimina stopwords y puntuación, y lematiza."""
    if nlp is None or texto is None:
        return []

    doc = nlp(texto)
    tokens = []
    if stopwords_excluir is None:
        stopwords_excluir = []

    if cargar_stopwords_desde_archivo and ruta_archivo_stopwords:
        stopwords_excluir.extend(cargar_stopwords(ruta_archivo_stopwords))

    for token in doc:
        if not token.is_stop and not token.is_punct and token.lemma_.lower() not in stopwords_excluir:
            tokens.append(token.lemma_.lower())
    return tokens

if __name__ == '__main__':
    # Ejemplo de uso (sin depender de config.json para ser ejecutable directamente)
    texto_ejemplo = "This is an example sentence with some punctuation! and stop words like is and a. Let's see the lemmas of words like running and ran."
    texto_limpio = limpiar_texto(texto_ejemplo)
    print(f"Texto limpio: {texto_limpio}")

    if nlp:
        tokens_procesados = procesar_texto(texto_limpio)
        print(f"Tokens procesados: {tokens_procesados}")

        # Para probar la carga de stopwords desde archivo, crea 'data/stopwords_personalizadas.txt'
        ruta_stopwords = 'data/stopwords_personalizadas.txt'
        os.makedirs(os.path.dirname(ruta_stopwords), exist_ok=True)
        with open(ruta_stopwords, 'w', encoding='utf-8') as f:
            f.write("example\nlet")

        tokens_con_exclusion_archivo = procesar_texto(texto_limpio,
                                                    ruta_archivo_stopwords=ruta_stopwords,
                                                    cargar_stopwords_desde_archivo=True)
        print(f"Tokens procesados (con exclusión de archivo): {tokens_con_exclusion_archivo}")