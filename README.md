# Corpus Creator and Analyzer

This project automates the process of extracting articles from a specified website, preprocessing the text content, and performing basic analysis such as generating a word cloud of the most frequent terms, perform sentiment analysis and topic modeling. It serves as a practical introduction to web scraping, natural language processing (NLP), and data visualization using Python.

<img width="753" alt="Captura de pantalla 2025-04-30 a las 22 37 44" src="https://github.com/user-attachments/assets/4ac298c6-594b-4eb4-abe1-bbdd21dbae95" />
<img width="582" alt="Captura de pantalla 2025-04-30 a las 22 52 03" src="https://github.com/user-attachments/assets/994519f3-70ba-4c99-9da7-32d8a3f25ad7" />
<img width="1196" alt="Captura de pantalla 2025-04-30 a las 22 37 28" src="https://github.com/user-attachments/assets/8e6ec73b-3510-4a2f-9ea3-8982c78f34f9" />
<img width="986" alt="Captura de pantalla 2025-04-29 a las 23 13 55" src="https://github.com/user-attachments/assets/345cfc72-410f-4db2-b5f1-1a6666310d2a" />

## Setup and Installation

Follow these steps to set up and run the project on your local machine:

1.  **Clone the repository (if it's public):**
    ```bash
    git clone [repository_url]
    cd [repository_name]
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv        # For macOS/Linux
    source venv/bin/activate   # For macOS/Linux

    python -m venv venv        # For Windows
    .\venv\Scripts\activate.bat # For Windows
    ```
    or using conda:
    ```bash
    conda create -n myenv python=3.x  # Replace 3.x with your Python version
    conda activate myenv
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    or if using conda:
    ```bash
    conda install --file requirements.txt
    ```

4.  **Download the spaCy English language model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Configuration

The project's behavior is controlled by the `config.json` file located in the `data/` directory. You can modify parameters such as the target website URL, the number of articles to extract, CSS selectors for titles and content, stopwords to exclude, and the appearance of the generated word cloud.

```json
{
  "extraccion": {
    "url_principal": "[https://www.scientificamerican.com/](https://www.scientificamerican.com/)",
    "limite_articulos": 6,
    "selector_titulo_articulo": "h2",
    "selector_contenido_articulo": ".article-body"
  },
  "preprocesamiento": {
    "stopwords_excluir": ["example", "another", "scientific", "american"],
    "cargar_stopwords_desde_archivo": false,
    "ruta_archivo_stopwords": "data/stopwords_personalizadas.txt"
  },
  "analisis": {
    "nube_palabras": {
      "num_palabras": 20,
      "background_color": "black",
      "colormap": "autumn",
      "forma_circular": true
    },
    "top_n_palabras": {
      "n": 20
    },
    "modelado_temas": {
      "num_temas": 5,
      "num_palabras_por_tema": 10
    }
  },
  "rutas": {
    "archivo_corpus": "data/corpus.json"
  }
}
```


## Usage

To run the main script, execute the main.ipynb notebook (or main.py script) in your activated environment. This script will:

Extract news articles from the specified URL.
Preprocess the text content (cleaning, tokenization, stopword removal, lemmatization).
Analyze the frequency of words in the extracted articles.
Generate and display a word cloud of the most frequent words.
Perform sentiment analysis and topic modeling.

## Running the Notebook:
```
jupyter notebook main.ipynb
```

## Runnin the main_script.py:
```
python main._script.py
```

## Exploring the Code

The project is organized into several modules within the src/ directory:

**- extractor.py:** Contains functions for web scraping, including downloading page content and extracting article links, titles, and content.
**- preprocessor.py:** Includes functions for cleaning and processing text data, such as removing special characters, handling stopwords, and lemmatization using spaCy.
**- analyzer.py:** Houses functions for performing text analysis, such as calculating word frequencies, generating word clouds, and (optionally) other analyses like sentiment analysis or topic modeling.
**-utils.py:** Provides utility functions for tasks like loading configuration from JSON, saving the corpus, and printing formatted output.

## Contributing

Contributions to this project are welcome. If you have ideas for improving the application or have found a bug, please feel free to open an issue or submit a pull request.

## Author

Nicola Korff [My Github](https://github.com/Nicolakorff/)

## License

MIT License
