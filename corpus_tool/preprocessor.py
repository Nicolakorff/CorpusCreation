import re

import spacy

_NLP = {}


def get_nlp(model="en_core_web_sm"):
    if model not in _NLP:
        try:
            _NLP[model] = spacy.load(model, disable=["parser"])
        except OSError as error:
            raise SystemExit(f"spaCy model '{model}' not found. Run: python -m spacy download {model}") from error
    return _NLP[model]


def clean_text(text):
    """Collapse whitespace and remove URLs."""
    text = re.sub(r"https?://\S+", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def load_stopwords(path):
    if not path:
        return set()
    with open(path, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip() and not line.startswith("#")}


def tokenize(text, nlp, extra_stopwords=frozenset(), min_len=3):
    """Lemmatize, keep alphabetic non-stopword tokens (nouns, verbs, adjectives, adverbs)."""
    keep = {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}
    tokens = []
    for tok in nlp(clean_text(text)):
        lemma = tok.lemma_.lower()
        if tok.is_alpha and not tok.is_stop and tok.pos_ in keep and len(lemma) >= min_len and lemma not in extra_stopwords:
            tokens.append(lemma)
    return tokens
