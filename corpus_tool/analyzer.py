from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel
from textblob import TextBlob
from wordcloud import WordCloud


def top_words(token_lists, n=20):
    return Counter(t for tokens in token_lists for t in tokens).most_common(n)


def lexical_stats(token_lists):
    """Basic corpus-quality numbers: size, vocabulary and type/token ratio."""
    all_tokens = [t for tokens in token_lists for t in tokens]
    lengths = [len(t) for t in token_lists]
    return {
        "documents": len(token_lists),
        "tokens": len(all_tokens),
        "vocabulary": len(set(all_tokens)),
        "type_token_ratio": round(len(set(all_tokens)) / len(all_tokens), 4) if all_tokens else 0.0,
        "tokens_per_doc_min": min(lengths) if lengths else 0,
        "tokens_per_doc_median": sorted(lengths)[len(lengths) // 2] if lengths else 0,
        "tokens_per_doc_max": max(lengths) if lengths else 0,
    }


def sentiment(text):
    """Polarity (-1..1) and subjectivity (0..1) with TextBlob (lexicon-based, English only)."""
    s = TextBlob(text).sentiment
    return s.polarity, s.subjectivity


def entities(text, nlp, top=15):
    return Counter((e.text, e.label_) for e in nlp(text).ents).most_common(top)


def fit_lda(token_lists, num_topics, passes=10, seed=42):
    dictionary = corpora.Dictionary(token_lists)
    dictionary.filter_extremes(no_below=2, no_above=0.8)
    bow = [dictionary.doc2bow(t) for t in token_lists]
    model = LdaModel(bow, num_topics=num_topics, id2word=dictionary, passes=passes, random_state=seed)
    return model, dictionary


def coherence(model, token_lists, dictionary):
    return CoherenceModel(model=model, texts=token_lists, dictionary=dictionary, coherence="c_v").get_coherence()


def select_topics(token_lists, k_min, k_max, passes=10, seed=42):
    """Fit LDA for k in [k_min, k_max] and keep the one with the highest c_v coherence."""
    scores, best = {}, None
    for k in range(k_min, k_max + 1):
        model, dictionary = fit_lda(token_lists, k, passes, seed)
        scores[k] = round(coherence(model, token_lists, dictionary), 4)
        if best is None or scores[k] > scores[best[0]]:
            best = (k, model, dictionary)
    return best[0], best[1], scores


def topic_table(model, words_per_topic=8):
    return [(i, [w for w, _ in model.show_topic(i, words_per_topic)]) for i in range(model.num_topics)]


def save_wordcloud(frequencies, path, max_words=60, background_color="white", colormap="viridis"):
    cloud = WordCloud(width=900, height=500, background_color=background_color, colormap=colormap,
                      max_words=max_words, collocations=False).generate_from_frequencies(dict(frequencies))
    plt.figure(figsize=(9, 5))
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
