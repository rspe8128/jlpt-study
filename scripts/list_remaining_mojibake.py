# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "study.html").read_text(encoding="utf-8")
out = ROOT / "reports" / "_remaining_mojibake.txt"
lines = []
for i, line in enumerate(text.splitlines(), 1):
    if "\ufffd" in line or "?/" in line:
        lines.append(f"{i}: {line[:240]}")

out.write_text("\n".join(lines[:120]), encoding="utf-8")
print(len(lines), "lines ->", out)
