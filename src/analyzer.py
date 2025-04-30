from src.utils import guardar_corpus_json, cargar_configuracion, obtener_valor_configuracion, imprimir_top_palabras
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import spacy
from textblob import TextBlob
import gensim
from gensim import corpora

# Cargar el modelo de spaCy para NER (si es necesario)
try:
    nlp_ner = spacy.load("en_core_web_sm")
except OSError:
    print("Advertencia: No se pudo cargar el modelo 'en_core_web_sm' para NER.")
    nlp_ner = None


def calcular_frecuencia_palabras(lista_de_tokens):
    """Calcula la frecuencia de cada palabra en una lista de tokens."""
    return Counter(lista_de_tokens)


def obtener_top_n_palabras(frecuencia, n=20):
    """Obtiene las n palabras más comunes y sus frecuencias."""
    return frecuencia.most_common(n)


def crear_nube_palabras(frecuencia, max_words=100, background_color="black", colormap="autumn"):
    """Genera y muestra una nube de palabras a partir de la frecuencia."""
    wordcloud = WordCloud(width=800, height=400,
                          background_color=background_color,
                          max_words=max_words,
                          colormap=colormap,
                          stopwords=set(), # Las stopwords ya deberían estar eliminadas
                          collocations=False).generate_from_frequencies(frecuencia)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def crear_nube_palabras_redonda(frecuencias, num_palabras=20, background_color="black", colormap="autumn"):
    """Crea y muestra una nube de palabras con forma circular."""
    x, y = np.ogrid[:600, :600]
    center = (300, 300)
    radius = 280
    mask = (x - center[0])**2 + (y - center[1])**2 > radius**2
    mask = 255 * mask.astype(int)

    wordcloud = WordCloud(width=600, height=600,
                          background_color=background_color,
                          colormap=colormap,
                          max_words=num_palabras,
                          mask=mask,
                          stopwords=set(),
                          collocations=False).generate_from_frequencies(frecuencias)

    plt.figure(figsize=(6, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def analizar_sentimiento(texto):
    """Analiza el sentimiento de un texto usando TextBlob."""
    analysis = TextBlob(texto)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity


def identificar_entidades(texto):
    """Identifica entidades nombradas en un texto usando spaCy."""
    if nlp_ner is None or texto is None:
        return []
    doc = nlp_ner(texto)
    return [(ent.text, ent.label_) for ent in doc.ents]


def modelar_temas(lista_de_tokens_por_documento, num_temas=5, num_palabras_por_tema=10):
    """Modela temas usando LDA con Gensim."""
    dictionary = corpora.Dictionary(lista_de_tokens_por_documento)
    corpus_gensim = [dictionary.doc2bow(tokens) for tokens in lista_de_tokens_por_documento]
    lda_model = gensim.models.LdaModel(corpus_gensim, num_topics=num_temas, id2word=dictionary, passes=15)
    temas = lda_model.print_topics(num_words=num_palabras_por_tema)
    return temas


if __name__ == '__main__':
    tokens_ejemplo = ['ejemplo', 'texto', 'limpio', 'ejemplo', 'palabra', 'frecuencia', 'texto']
    frecuencia = calcular_frecuencia_palabras(tokens_ejemplo)
    print(f"Frecuencia de palabras: {frecuencia}")

    top_palabras = obtener_top_n_palabras(frecuencia, n=3)
    print(f"Top 3 palabras: {top_palabras}")

    texto_sentimiento = "This is a great and positive example."
    polaridad, subjetividad = analizar_sentimiento(texto_sentimiento)
    print(f"Sentimiento: Polaridad={polaridad}, Subjetividad={subjetividad}")

    texto_entidades = "Apple is a technology company based in Cupertino, California."
    entidades = identificar_entidades(texto_entidades)
    print(f"Entidades encontradas: {entidades}")

    corpus_ejemplo_tema = [['ejemplo', 'tema', 'uno'], ['segundo', 'tema', 'ejemplo']]
    temas_encontrados = modelar_temas(corpus_ejemplo_tema)
    print("Temas encontrados:")
    for tema_id, palabras in temas_encontrados:
        print(f"Tema #{tema_id+1}: {palabras}")