import json
from copy import deepcopy

DEFAULTS = {
    "source": {
        "type": "dir",                 # "dir" (local .txt files) or "web"
        "path": "data/sample",         # used when type == "dir"
        "url": "",                     # used when type == "web"
        "article_link_selector": "article a[href]",
        "title_selector": "h1",
        "content_selector": "article p",
        "max_articles": 50,
        "delay_seconds": 1.0,
        "user_agent": "CorpusCreation/1.0 (research; contact: see repository)",
    },
    "preprocessing": {
        "spacy_model": "en_core_web_sm",
        "min_token_length": 3,
        "extra_stopwords": [],
        "stopwords_file": None,
        "min_doc_tokens": 50,
    },
    "analysis": {
        "top_n_words": 20,
        "topics": {"min": 2, "max": 8, "words_per_topic": 8, "passes": 10, "seed": 42},
        "wordcloud": {"max_words": 60, "background_color": "white", "colormap": "viridis"},
    },
    "output_dir": "outputs",
    "save_corpus_text": False,
}


def _merge(base, override):
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v
    return base


def load_config(path=None):
    """Load a JSON config and merge it over the defaults."""
    config = deepcopy(DEFAULTS)
    if path:
        with open(path, encoding="utf-8") as f:
            _merge(config, json.load(f))
    return config
