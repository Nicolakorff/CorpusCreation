"""Run the pipeline:  python main.py --config config.json"""
import argparse
import csv
import json
from pathlib import Path

from corpus_tool import analyzer, config as cfg, extractor, preprocessor


def run(config):
    src, prep, ana = config["source"], config["preprocessing"], config["analysis"]
    out = Path(config["output_dir"])
    out.mkdir(parents=True, exist_ok=True)

    docs = extractor.load_local_corpus(src["path"]) if src["type"] == "dir" else extractor.scrape_corpus(src)
    if not docs:
        raise SystemExit("No documents found.")

    nlp = preprocessor.get_nlp(prep["spacy_model"])
    stop = set(w.lower() for w in prep["extra_stopwords"]) | preprocessor.load_stopwords(prep["stopwords_file"])
    kept, tokens, dropped = [], [], []
    for d in docs:
        t = preprocessor.tokenize(d["text"], nlp, stop, prep["min_token_length"])
        (kept if len(t) >= prep["min_doc_tokens"] else dropped).append(d)
        if len(t) >= prep["min_doc_tokens"]:
            tokens.append(t)

    report = {"documents_found": len(docs), "documents_dropped_too_short": len(dropped),
              **analyzer.lexical_stats(tokens)}
    freqs = analyzer.top_words(tokens, ana["top_n_words"])
    with open(out / "top_words.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([("word", "count")] + freqs)
    analyzer.save_wordcloud(analyzer.top_words(tokens, 500)[: ana["wordcloud"]["max_words"]], out / "wordcloud.png",
                            **ana["wordcloud"])

    sent = [analyzer.sentiment(d["text"]) for d in kept]
    report["mean_polarity"] = round(sum(p for p, _ in sent) / len(sent), 3)
    report["mean_subjectivity"] = round(sum(s for _, s in sent) / len(sent), 3)
    report["top_entities"] = [f"{e[0]} ({e[1]}): {c}" for e, c in analyzer.entities(" ".join(d["text"] for d in kept[:20]), nlp)]

    tp = ana["topics"]
    if len(tokens) >= 10:
        k, model, scores = analyzer.select_topics(tokens, tp["min"], tp["max"], tp["passes"], tp["seed"])
        report["topic_coherence_c_v"] = scores
        report["selected_topics"] = k
        with open(out / "topics.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["topic", "words"])
            for i, words in analyzer.topic_table(model, tp["words_per_topic"]):
                w.writerow([i + 1, " ".join(words)])
    else:
        report["topic_modelling"] = "skipped: fewer than 10 usable documents"

    if config["save_corpus_text"]:
        with open(out / "corpus.jsonl", "w", encoding="utf-8") as f:
            for d in kept:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(out / "report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=None, help="JSON config (merged over defaults)")
    run(cfg.load_config(ap.parse_args().config))
