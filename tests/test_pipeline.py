import pytest

from corpus_tool import analyzer, extractor, preprocessor

HTML = """<html><body><h1>Title here</h1><article><p>First paragraph.</p><p>Second one.</p></article>
<a href="/a1">x</a></body></html>"""


def test_clean_text_removes_urls_and_spaces():
    assert preprocessor.clean_text("see  https://x.org/a   now") == "see now"


def test_extract_article():
    title, text = extractor.extract_article(HTML, "h1", "article p")
    assert title == "Title here" and text == "First paragraph. Second one."


def test_extract_article_missing_returns_none():
    assert extractor.extract_article("<html></html>", "h1", "p") == (None, None)


def test_extract_links_same_domain_only():
    html = '<article><a href="/a">1</a><a href="https://other.com/b">2</a></article>'
    assert extractor.extract_links(html, "https://site.com/", "article a[href]", 10) == ["https://site.com/a"]


def test_load_local_corpus(tmp_path):
    (tmp_path / "a.txt").write_text("hello world", encoding="utf-8")
    (tmp_path / "empty.txt").write_text("", encoding="utf-8")
    docs = extractor.load_local_corpus(tmp_path)
    assert [d["title"] for d in docs] == ["a"]


def test_tokenize_lemmatizes_and_filters():
    nlp = preprocessor.get_nlp()
    tokens = preprocessor.tokenize("The dogs were running quickly in 2024!", nlp)
    assert "dog" in tokens and "run" in tokens and "the" not in tokens and "2024" not in tokens


def test_lexical_stats():
    s = analyzer.lexical_stats([["a", "b", "a"], ["c"]])
    assert s["documents"] == 2 and s["tokens"] == 4 and s["vocabulary"] == 3


def test_select_topics_returns_best_k():
    docs = [["fire", "smoke", "wind", "town"], ["election", "vote", "party", "leader"]] * 10
    k, model, scores = analyzer.select_topics(docs, 2, 3, passes=2)
    assert k in (2, 3) and set(scores) == {2, 3}
