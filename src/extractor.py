import requests
from bs4 import BeautifulSoup


def obtener_pagina_principal(url):
    """Descarga el contenido HTML de la página principal, asegurando que la URL tenga el esquema."""
    if not url.startswith('https://') and not url.startswith('http://'):
        url = 'https://' + url  # Añade https:// si falta
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL '{url}': {e}")
        return None

def extraer_enlaces_articulos(html_content, url_base, limite=6):
    """Extrae los enlaces a los artículos de la página principal."""
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    articulos = soup.find_all('article', class_='article-pFLe7', limit=limite)
    enlaces = []
    for articulo in articulos[1:]:  # Saltar el primer artículo (duplicado)
        enlace_tag = articulo.find('a', href=True)
        if enlace_tag and 'href' in enlace_tag.attrs:
            enlace = url_base.rstrip('/') + enlace_tag['href']
            enlaces.append(enlace)
    return enlaces

def obtener_contenido_articulo(url_articulo):
    """Descarga el contenido HTML de un artículo."""
    try:
        response = requests.get(url_articulo, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL del artículo '{url_articulo}': {e}")
        return None

def extraer_titulo_contenido(html_articulo, selector_titulo='h2', selector_contenido='p'):
    """Extrae el título y el contenido principal del HTML de un artículo."""
    if not html_articulo:
        return None, None
    soup = BeautifulSoup(html_articulo, 'html.parser')

    titulo_tag = soup.select_one(selector_titulo)
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else None

    cuerpo_articulo = soup.select_one(selector_contenido)
    contenido = ''
    
    parrafos = soup.find_all('p')
    if parrafos and len(parrafos) > 2:
        contenido = ' '.join(p.get_text(strip=True) for p in parrafos[2:])
    elif parrafos:
        contenido = ' '.join(p.get_text(strip=True) for p in parrafos)
    else:
        print(f"No se encontró el contenido principal con el selector '{selector_contenido}'.")

    return titulo, contenido

if __name__ == '__main__':
    url_principal = 'https://www.scientificamerican.com/'
    html_principal = obtener_pagina_principal(url_principal)
    if html_principal:
        enlaces = extraer_enlaces_articulos(html_principal, url_principal)
        if enlaces:
            print(f"Se encontraron {len(enlaces)} enlaces a artículos.")
            for enlace in enlaces:
                print(f"Procesando artículo: {enlace}")
                html_articulo = obtener_contenido_articulo(enlace)
                if html_articulo:
                    titulo, contenido = extraer_titulo_contenido(html_articulo)
                    if titulo and contenido:
                        print(f"  Título: {titulo[:50]}...")
                        print(f"  Contenido (primeros 100 chars): {contenido[:100]}...")
                    else:
                        print(f"  No se pudo extraer título o contenido de {enlace}")
                else:
                    print(f"  No se pudo obtener el contenido de {enlace}")
        else:
            print("No se encontraron enlaces a artículos en la página principal.")