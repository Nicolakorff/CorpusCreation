# Importaciones
from src.extractor import obtener_pagina_principal, extraer_enlaces_articulos, obtener_contenido_articulo, extraer_titulo_contenido
from src.preprocessor import limpiar_texto, procesar_texto
from src.analyzer import calcular_frecuencia_palabras, obtener_top_n_palabras, crear_nube_palabras_redonda, analizar_sentimiento, identificar_entidades, modelar_temas
from src.utils import cargar_configuracion, obtener_valor_configuracion, guardar_corpus_json, imprimir_top_palabras

# Cargar configuración
config = cargar_configuracion()

# Obtener parámetros de configuración
url_principal = obtener_valor_configuracion(config.get('extraccion', {}), 'url_principal', 'https://www.scientificamerican.com/')
limite_articulos = obtener_valor_configuracion(config.get('extraccion', {}), 'limite_articulos', 6)
selector_titulo = obtener_valor_configuracion(config.get('extraccion', {}), 'selector_titulo_articulo', 'h2')
selector_contenido = obtener_valor_configuracion(config.get('extraccion', {}), 'selector_contenido_articulo', 'p')

cargar_stopwords = obtener_valor_configuracion(config.get('preprocesamiento', {}), 'cargar_stopwords_desde_archivo', False)
ruta_archivo_stopwords = obtener_valor_configuracion(config.get('preprocesamiento', {}), 'ruta_archivo_stopwords', 'data/stopwords_personalizadas.txt')
stopwords_excluir_config = obtener_valor_configuracion(config.get('preprocesamiento', {}), 'stopwords_excluir', [])

ruta_archivo_corpus = obtener_valor_configuracion(config.get('rutas', {}), 'archivo_corpus', 'data/corpus.json')

# Extracción
html_principal = obtener_pagina_principal(url_principal)
corpus_articulos = []

if html_principal:
    enlaces = extraer_enlaces_articulos(html_principal, url_principal, limite=limite_articulos)
    for enlace in enlaces:
        html_articulo = obtener_contenido_articulo(enlace)
        if html_articulo:
            titulo, contenido = extraer_titulo_contenido(html_articulo, selector_titulo, selector_contenido)
            if titulo and contenido:
                corpus_articulos.append({'titulo': titulo, 'contenido': contenido})
            else:
                print(f"No se pudo extraer título o contenido de {enlace}")
        else:
            print(f"No se pudo obtener el contenido de {enlace}")

    guardar_corpus_json(corpus_articulos, ruta_archivo_corpus)

    # Preprocesamiento
    corpus_procesado = []
    for articulo in corpus_articulos:
        texto_limpio = limpiar_texto(articulo['contenido'])
        tokens = procesar_texto(texto_limpio,
                                stopwords_excluir=stopwords_excluir_config,
                                ruta_archivo_stopwords=ruta_archivo_stopwords,
                                cargar_stopwords_desde_archivo=cargar_stopwords)
        corpus_procesado.append(tokens)

    if corpus_procesado:
        # Análisis de frecuencia
        todas_las_palabras = [palabra for sublista in corpus_procesado for palabra in sublista]
        frecuencia_palabras = calcular_frecuencia_palabras(todas_las_palabras)
        top_n = obtener_valor_configuracion(config.get('analisis', {}).get('top_n_palabras', {}), 'n', 20)
        top_palabras = obtener_top_n_palabras(frecuencia_palabras, n=top_n)
        imprimir_top_palabras(top_palabras, n=top_n)

        # Visualización de la nube de palabras
        nube_config = config.get('analisis', {}).get('nube_palabras', {})
        num_palabras_nube = obtener_valor_configuracion(nube_config, 'num_palabras', 20)
        color_fondo_nube = obtener_valor_configuracion(nube_config, 'background_color', 'black')
        colormap_nube = obtener_valor_configuracion(nube_config, 'colormap', 'autumn')
        forma_circular_nube = obtener_valor_configuracion(nube_config, 'forma_circular', True)

        if forma_circular_nube:
            crear_nube_palabras_redonda(dict(frecuencia_palabras.most_common(num_palabras_nube)),
                                        num_palabras=num_palabras_nube,
                                        background_color=color_fondo_nube,
                                        colormap=colormap_nube)
        else:
            crear_nube_palabras(frecuencia_palabras,
                                max_words=num_palabras_nube,
                                background_color=color_fondo_nube,
                                colormap=colormap_nube)

        # Ejemplo de análisis de sentimiento (del primer artículo si existe)
        if corpus_articulos:
            polaridad, subjetividad = analizar_sentimiento(corpus_articulos[0]['contenido'])
            print(f"\nSentimiento del primer artículo: Polaridad={polaridad:.2f}, Subjetividad={subjetividad:.2f}")

        # Ejemplo de identificación de entidades (del primer artículo si existe)
        if corpus_articulos:
            entidades = identificar_entidades(corpus_articulos[0]['contenido'])
            print(f"\nEntidades encontradas en el primer artículo: {entidades}")

        # Ejemplo de modelado de temas (si el corpus procesado tiene suficientes documentos)
        num_temas_config = obtener_valor_configuracion(config.get('analisis', {}).get('modelado_temas', {}), 'num_temas', 5)
        palabras_por_tema_config = obtener_valor_configuracion(config.get('analisis', {}).get('modelado_temas', {}), 'num_palabras_por_tema', 10)
        if len(corpus_procesado) > 1:
            temas = modelar_temas(corpus_procesado, num_temas=num_temas_config, num_palabras_por_tema=palabras_por_tema_config)
            print("\nTemas encontrados en el corpus:")
            for tema_id, palabras in temas:
                print(f"Tema #{tema_id+1}: {palabras}")
        else:
            print("\nNo hay suficientes documentos para realizar el modelado de temas.")

else:
    print("No se pudo obtener el contenido de la página principal.")
