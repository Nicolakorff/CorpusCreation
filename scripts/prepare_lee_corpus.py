"""Write the Lee news corpus bundled with gensim (300 short news articles, English)
as one .txt file per document, so it can be used as a demo input.

    python scripts/prepare_lee_corpus.py   ->  data/lee_demo/*.txt  (not committed)
"""
from pathlib import Path

from gensim.test.utils import datapath

out = Path("data/lee_demo")
out.mkdir(parents=True, exist_ok=True)
with open(datapath("lee_background.cor"), encoding="latin-1") as f:
    for i, line in enumerate(f, 1):
        if line.strip():
            (out / f"article_{i:03d}.txt").write_text(line.strip(), encoding="utf-8")
print(f"Wrote {len(list(out.glob('*.txt')))} documents to {out}")
