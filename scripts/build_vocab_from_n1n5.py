# -*- coding: utf-8 -*-
"""Extract N4/N5 vocabulary from N1-N5단어 정리.pdf text dump."""
from __future__ import annotations

import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SOURCES = os.path.join(DATA, "sources")
VOCAB = os.path.join(DATA, "vocab")
LINE_RE = re.compile(r"^(.+?)\s+N([1-5]),\s*(.+)$")
BRACKET_RE = re.compile(r"^(.+?)\[(.+)\]$")


def find_pdf() -> str:
    for name in os.listdir(ROOT):
        if name.lower().endswith(".pdf") and "N1" in name:
            return os.path.join(ROOT, name)
    raise FileNotFoundError("N1-N5 단어 PDF not found")


def extract_pdf_text(pdf_path: str) -> str:
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) required: pip install pymupdf")
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)


def parse_lemma(lemma: str) -> tuple[str, str]:
    lemma = lemma.strip()
    m = BRACKET_RE.match(lemma)
    if not m:
        return lemma, lemma
    reading = m.group(1).strip()
    kanji_part = m.group(2).strip()
    if re.search(r"[一-龯々〻]", kanji_part):
        word = kanji_part.split("/")[0].strip()
    else:
        word = reading
    return word, reading


def load_source_text() -> str:
    dump = os.path.join(SOURCES, "_n1n5_full.txt")
    if os.path.isfile(dump):
        with open(dump, encoding="utf-8") as f:
            return f.read()
    pdf = find_pdf()
    text = extract_pdf_text(pdf)
    with open(dump, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def collect_level(level: str, text: str) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if not m or m.group(2) != level:
            continue
        word, reading = parse_lemma(m.group(1))
        meaning = m.group(3).strip()
        key = f"{word}\t{reading}\t{meaning}"
        if key in seen:
            continue
        seen.add(key)
        rows.append({"word": word, "reading": reading, "meaning": meaning})
    return rows


def write_tsv(path: str, rows: list[dict]) -> None:
    lines = []
    for i, r in enumerate(rows, 1):
        parts = [
            str(i),
            r["word"].replace("\t", " "),
            r["reading"].replace("\t", " "),
            r["meaning"].replace("\t", " "),
        ]
        lines.append("\t".join(parts))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))


def main() -> None:
    text = load_source_text()
    n5 = collect_level("5", text)
    n4 = collect_level("4", text)
    write_tsv(os.path.join(VOCAB, "n5_vocab.tsv"), n5)
    write_tsv(os.path.join(VOCAB, "n4_vocab.tsv"), n4)
    print(f"N5: {len(n5)} entries -> n5_vocab.tsv")
    print(f"N4: {len(n4)} entries -> n4_vocab.tsv")


if __name__ == "__main__":
    main()
