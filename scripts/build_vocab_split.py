# -*- coding: utf-8 -*-
"""Split N4/N5 vocab into legacy (4 PDF) vs new (N1–N5 통합 추가분) pools."""
from __future__ import annotations

import os
import re

from build_vocab_from_n1n5 import collect_level, load_source_text
from kana_to_hangul import add_korean_pronunciation, japanese_reading_part

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SOURCES = os.path.join(DATA, "sources")
VOCAB = os.path.join(DATA, "vocab")
BASELINES = os.path.join(DATA, "baselines")


def norm_dash(s: str) -> str:
    return re.sub(r"[―—ー＿]", "", s.strip())


def vocab_key(word: str, reading: str) -> str:
    return f"{word.strip()}\t{japanese_reading_part(reading).strip()}"


def parse_tsv(path: str) -> list[dict]:
    rows = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        rows.append(
            {
                "word": parts[1],
                "reading": parts[2],
                "meaning": "\t".join(parts[3:]),
            }
        )
    return rows


def write_tsv(path: str, rows: list[dict]) -> None:
    lines = []
    for i, r in enumerate(rows, 1):
        lines.append(
            "\t".join(
                [
                    str(i),
                    r["word"].replace("\t", " "),
                    r["reading"].replace("\t", " "),
                    r["meaning"].replace("\t", " "),
                ]
            )
        )
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))


def write_keys(path: str, keys: list[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(keys) + ("\n" if keys else ""))


def finalize_legacy_row(row: dict) -> dict:
    """PDF 원문 읽기 + 한국어 발음 괄호."""
    r = dict(row)
    r["reading"] = add_korean_pronunciation(japanese_reading_part(r["reading"]))
    return r


def load_n4_pdf_rows() -> list[dict]:
    """기존 N4 = PDF 3종(명사·동사·형용사·부사·기타)."""
    rows: list[dict] = []
    seen: set[str] = set()
    for fname in ("_n4_noun_pdf.txt", "_n4_verb_pdf.txt", "_n4_adj_pdf.txt"):
        path = os.path.join(SOURCES, fname)
        if not os.path.isfile(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("어휘"):
                continue
            parts = [p.strip() for p in re.split(r"\t+", line)]
            if len(parts) < 3:
                parts = [p.strip() for p in line.split()]
                if len(parts) < 3:
                    continue
            reading, kanji = parts[0], parts[1]
            meaning = " ".join(parts[2:]).strip()
            if not re.search(r"[ぁ-んァ-ン一-龯々]", reading) or not meaning:
                continue
            kd = norm_dash(kanji)
            word = kanji if kd else reading
            dedupe = f"{reading}\t{kanji}\t{meaning}"
            if dedupe in seen:
                continue
            seen.add(dedupe)
            rows.append({"word": word, "reading": reading, "meaning": meaning})
    return rows


def load_n5_pdf_by_key() -> dict[str, dict]:
    """4번째 PDF(N1–N5 통합)에서 N5 항목."""
    text = load_source_text()
    by_key: dict[str, dict] = {}
    for row in collect_level("5", text):
        by_key[vocab_key(row["word"], row["reading"])] = row
    return by_key


def load_n5_legacy_key_order() -> list[str]:
    """기존 N5 100어 순서(間 제외, n5_vocab.tsv 선두와 동일)."""
    order_path = os.path.join(BASELINES, "n5_legacy_order.tsv")
    if os.path.isfile(order_path):
        return [line.strip() for line in open(order_path, encoding="utf-8") if line.strip()]

    n5_full = parse_tsv(os.path.join(VOCAB, "n5_vocab.tsv"))
    start = 1 if n5_full and n5_full[0]["word"] == "間" else 0
    keys = [vocab_key(r["word"], r["reading"]) for r in n5_full[start : start + 100]]
    os.makedirs(BASELINES, exist_ok=True)
    write_keys(order_path, keys)
    return keys


def build_n4_legacy(pdf_rows: list[dict]) -> list[dict]:
    """PDF 3종 내용만 사용, 일·한 발음 포함."""
    legacy: list[dict] = []
    seen: set[str] = set()
    for row in pdf_rows:
        key = vocab_key(row["word"], row["reading"])
        if key in seen:
            continue
        seen.add(key)
        legacy.append(finalize_legacy_row(row))
    return legacy


def build_n5_legacy(pdf_by_key: dict[str, dict], key_order: list[str]) -> list[dict]:
    """N1–N5 PDF(4번째)에서 기존 N5 키만, PDF 순서 유지."""
    legacy: list[dict] = []
    for key in key_order:
        row = pdf_by_key.get(key)
        if not row:
            continue
        legacy.append(finalize_legacy_row(row))
    return legacy


def norm_word(word: str) -> str:
    w = re.sub(r"[―—ー＿\s()（）\[\]]", "", word.strip())
    return w.replace("答(え)", "答え")


def meaning_tokens(m: str) -> set[str]:
    return set(re.findall(r"[가-힣]{2,}", m))


def meaning_overlap(a: str, b: str) -> bool:
    def norm(s: str) -> str:
        s = re.sub(r"\s+", "", s.strip())
        return s[:12]

    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    return na in nb or nb in na or na[:4] == nb[:4]


def has_meaning_signal(anchor: dict, full_row: dict) -> bool:
    if norm_word(anchor["word"]) == norm_word(full_row["word"]):
        return True
    if meaning_overlap(anchor["meaning"], full_row["meaning"]):
        return True
    return bool(meaning_tokens(anchor["meaning"]) & meaning_tokens(full_row["meaning"]))


def match_score(anchor: dict, full_row: dict) -> int:
    ar = japanese_reading_part(anchor["reading"])
    fr = japanese_reading_part(full_row["reading"])
    if ar != fr:
        return 0
    if vocab_key(anchor["word"], anchor["reading"]) == vocab_key(
        full_row["word"], full_row["reading"]
    ):
        return 100

    score = 0
    if norm_word(anchor["word"]) == norm_word(full_row["word"]):
        score += 80
    if meaning_overlap(anchor["meaning"], full_row["meaning"]):
        score += 60
    shared = meaning_tokens(anchor["meaning"]) & meaning_tokens(full_row["meaning"])
    if shared:
        score += 35 + len(shared) * 8
    if (
        re.search(r"[一-龯々〻]", anchor["word"])
        and ar == full_row["word"] == fr
        and anchor["word"] != anchor["reading"]
    ):
        score += 28
    return score


MATCH_EXCLUDE = 35


def row_matches_legacy(full_row: dict, legacy_anchors: list[dict]) -> bool:
    for leg in legacy_anchors:
        score = match_score(leg, full_row)
        if score >= 100:
            return True
        if score >= MATCH_EXCLUDE and has_meaning_signal(leg, full_row):
            return True
    return False


def main() -> None:
    n5_full = parse_tsv(os.path.join(VOCAB, "n5_vocab.tsv"))
    n4_full = parse_tsv(os.path.join(VOCAB, "n4_vocab.tsv"))

    n4_pdf_rows = load_n4_pdf_rows()
    n5_pdf_by_key = load_n5_pdf_by_key()
    n5_key_order = load_n5_legacy_key_order()

    n4_legacy = build_n4_legacy(n4_pdf_rows)
    n5_legacy = build_n5_legacy(n5_pdf_by_key, n5_key_order)

    n5_legacy_keys = {vocab_key(r["word"], r["reading"]) for r in n5_legacy}
    n5_new = [r for r in n5_full if vocab_key(r["word"], r["reading"]) not in n5_legacy_keys]
    n4_new = [r for r in n4_full if not row_matches_legacy(r, n4_pdf_rows)]

    write_tsv(os.path.join(VOCAB, "n5_vocab_legacy.tsv"), n5_legacy)
    write_tsv(os.path.join(VOCAB, "n5_vocab_new.tsv"), n5_new)
    write_tsv(os.path.join(VOCAB, "n4_vocab_legacy.tsv"), n4_legacy)
    write_tsv(os.path.join(VOCAB, "n4_vocab_new.tsv"), n4_new)

    missing_kr = sum(
        1
        for r in n5_legacy + n4_legacy
        if not re.search(r"\([가-힣]", r["reading"])
    )
    print(f"N5: legacy {len(n5_legacy)}, new {len(n5_new)}, total {len(n5_full)}")
    print(f"N4: legacy {len(n4_legacy)}, new {len(n4_new)}, total {len(n4_full)}")
    if missing_kr:
        print(f"warning: legacy rows without Korean pron: {missing_kr}")


if __name__ == "__main__":
    main()
