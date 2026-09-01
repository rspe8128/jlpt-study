# -*- coding: utf-8 -*-
"""Restore corrupted Korean UI in study.html."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "study.html"

R = "\ufffd"

FIXES: list[tuple[str, str]] = [
    (f"/* ?{R}\ub2e8 ??{R}\ubaa8??{R}? \ucf58\ud150{R}???{R}?{R}\ub370 \uace0\uc815",
     "/* \uc0c1\ub2e8 \ud0ed\xb7\ubaa8\ub4dc \ubc14: \ucf58\ud150\uce20 \uc0c1\ub2e8\uc5d0 \uace0\uc815"),
    (f"(\ubaa8\ub4dc ?{R}\ud658 ???{R}\ucabd?{R}\ub85c ??{R}\ubc29{R}) */",
     "(\ubaa8\ub4dc \uc804\ud658 \uc2dc \uc67c\ucabd\uc73c\ub85c \ubc00\ub9bc \ubc29\uc9c0) */"),
    ("\ub4a4\uc9d1\uae30?\xb7", "\ub4a4\uc9d1\uae30 \xb7 "),
    (f'aria-label="\ud559\uc2b5 ??{R}"', 'aria-label="\ud559\uc2b5 \uc885\ubaa9"'),
    (f'aria-label="\ub2e8\uc5b4 \ud559\uc2b5 ?{R}\ud0dc"', 'aria-label="\ub2e8\uc5b4 \ud559\uc2b5 \uc0c1\ud0dc"'),
    (f"\ud55c\uc790{R} \uc8fc\uc5b4{R}?", "\ud55c\uc790\ub97c \uc8fc\uc5b4\uc9c4 "),
    ("??\ub9de\ub294", "\uc5d0 \ub9de\ub294"),
    ("\ud558\ub098\ub97c\uace0\ub9bd\ub2c8\ub2e4", "\ud558\ub098\ub97c \uace0\ub9bd\ub2c8\ub2e4"),
    (f"\ubb38\uc81c ?{R}\uc11c? \ubcf4\uae30 ?{R}\uc11c??\uc138\ud2b8\ub9c8\ub2e4",
     "\ubb38\uc81c \uc21c\uc11c\uc640 \ubcf4\uae30 \uc21c\uc11c\ub294 \uc138\ud2b8\ub9c8\ub2e4"),
    (f"(\ubcf4\uae30 4{R})", "(\ubcf4\uae30 4\uac1c)"),
    (f"?{R}{R}{R}?", "\uadf8\ub9cc\ud558\uae30"),
    ("\uc8fc\uad00\uc2dd?\uc815", "\uc8fc\uad00\uc2dd \uc124\uc815"),
    (f"\ud55c\uc790{R} \ubcf4\uc774{R}?", "\ud55c\uc790\uac00 \ubcf4\uc774\uba74 "),
    (f"<strong>?</strong>{R}?", "<strong>\ub73b</strong>\uacfc "),
    (f"<strong>\ub73b</strong>\uacfc?{R}\uce78\uc5d0", "<strong>\ub73b</strong>\uacfc <strong>\uc74c</strong> \uce78\uc5d0"),
    (f"\ucc45\uc810</strong>?{R}\ub2c8??", "\ucc45\uc810</strong>\ud569\ub2c8\ub2e4"),
    (f"\ubb38\uc81c ?{R}\uc11c??\uc138\ud2b8\ub9c8\ub2e4", "\ubb38\uc81c \uc21c\uc11c\ub294 \uc138\ud2b8\ub9c8\ub2e4"),
    (f"(?{R}\ub2f5?{R} \ub73b\uc758 \ub73b\xb7\uc74c{R}?\ube44\uad50",
     "(\uc815\ub2f5\uc740 \ub73b\uc758 \ub73b\xb7\uc74c\uacfc \ube44\uad50"),
    (f"?{R}\ub7ec \uc12d\uae30", "\uc5ec\ub7ec \ub73b"),
    (f"??\uad6c\uac04 ???{R}\uc6a9", "\ub73b \uad6c\uac04 \xb7 | \xb7 \ud5c8\uc6a9"),
    (f"?{R}\uc791", "\uc2dc\uc791"),
    (f"??(?{R}??)", "\ub73b (\ud55c\uae00)"),
    (f"??(?{R}??)", "\uc74c (\ud6c8\ub3c5)"),
    (f'lang="ja">?{R}\u3046</div>', 'lang="ja">\u3042\u3046</div>'),
    (f"?{R}\ub7ec ?{R}\uad6d??\ub4a4 \ubcf4\uae30", "\ub204\ub7ec \ud55c\uad6d\uc5b4 \ub73b\xb7\ub4a4 \ubcf4\uae30"),
    ('aria-label="\ub2e8\uc5b4 \ud50c\ub798\uc2dc\uce74\ub4dc>', 'aria-label="\ub2e8\uc5b4 \ud50c\ub798\uc2dc\uce74\ub4dc">'),
    ('aria-label="\ub2e8\uc5b4 \uce74\ub4dc, \ub204\ub7ec \ub4a4\uc9d1\uae30?>', 'aria-label="\ub2e8\uc5b4 \uce74\ub4dc, \ub204\ub7ec \ub4a4\uc9d1\uae30">'),
    ('aria-label="\ub2e8\uc5b4 \uac1d\uad00\uc2dd?\uc988"', 'aria-label="\ub2e8\uc5b4 \uac1d\uad00\uc2dd \ud034\uc988"'),
    (f"?{R}\uc5b4 ?{R}\uc988 ?{R}\uc815", "\ub2e8\uc5b4 \ud034\uc988 \uc124\uc815"),
    (f'aria-label="\ub2e8\uc5b4 ?{R}\uc988 ?{R}\ud615"', 'aria-label="\ub2e8\uc5b4 \ud034\uc988 \uc720\ud615"'),
    (f"??(?{R}\uad6d??", "\ub73b (\ud55c\uad6d\uc5b4)"),
    (f"??(?{R}\uae30)", "\uc74c (\uc77d\uae30)"),
    (f"?{R}\ubcf8??\uc12d\uae30", "\uc77c\ubcf8\uc5b4 \uc77d\uae30"),
    (f"?{R}\uad6d??\ub73b", "\ud55c\uad6d\uc5b4 \ub73b"),
    (f"?{R}\uad6d??\ub73b</strong>\uacfc?", "\ud55c\uad6d\uc5b4 \ub73b</strong>\uc744"),
    (f"?{R}\uc7ac \uae09\uc218 \uc77d\uae30\uc640)", "\xb7 \ud604\uc7ac \uae09\uc218 \ud480 \uae30\uc900)"),
    (f"??\uc12d\uae30??\ub9de\ub294", "\uc774 \uc77d\uae30\uc5d0 \ub9de\ub294"),
    ('aria-label="\ud788\ub77c\uac00\ub098\ud559\uc2b5 ?\ud0dc"', 'aria-label="\ud788\ub77c\uac00\ub098 \ud559\uc2b5 \uc0c1\ud0dc"'),
    ('aria-label="\ud788\ub77c\uac00\ub098\ud50c\ub798\uc2dc\uce74\ub4dc>', 'aria-label="\ud788\ub77c\uac00\ub098 \ud50c\ub798\uc2dc\uce74\ub4dc">'),
    ('aria-label="\ud788\ub77c\uac00\ub098\uce74\ub4dc, \ub204\ub7ec \ub4a4\uc9d1\uae30?>', 'aria-label="\ud788\ub77c\uac00\ub098 \uce74\ub4dc, \ub204\ub7ec \ub4a4\uc9d1\uae30">'),
    ("\ud788\ub77c\uac00\ub098/span>", "\ud788\ub77c\uac00\ub098</span>"),
    (f"?{R}\uc9d1? \ub85c\ub9c8\uc790", "\ub4a4\uc9d1\uc5b4 \ub85c\ub9c8\uc790"),
    ("\uc774\ub984\uc744\ubcf4\uc785\ub2c8\ub2e4", "\uc774\ub984\uc744 \ubcf4\uc785\ub2c8\ub2e4"),
    (f"?{R}\ub7ec \uc12d\uae30\xb7???{R}\ub0b4 \ubcf4\uae30", "\ub204\ub7ec \uc77d\uae30\xb7\ud589 \uc548\ub0b4 \ubcf4\uae30"),
    ('aria-label="\ud788\ub77c\uac00\ub098????>', 'aria-label="\ud788\ub77c\uac00\ub098 \ud45c">'),
    (f"<strong>\ud788\ub77c\uac00\ub098\ub73b</strong>\uacfc?\ub9de\ub294 <strong>\ud0a4\ubcf4\ub4dc \ub85c\ub9c8\uc790/strong>{R}?",
     "<strong>\ud788\ub77c\uac00\ub098 \ud55c \uae00\uc790</strong>\uc5d0 \ub9de\ub294 <strong>\ub85c\ub9c8\uc790</strong>\ub97c"),
    ("\ud788\ub77c\uac00\ub098\ud034\uc988 \uc124\uc815", "\ud788\ub77c\uac00\ub098 \ud034\uc988 \uc124\uc815"),
    ('aria-label="\ud788\ub77c\uac00\ub098\uac1d\uad00\uc2dd>', 'aria-label="\ud788\ub77c\uac00\ub098 \uac1d\uad00\uc2dd">'),
    (f"???{R}\uc758 <strong>\ub85c\ub9c8??\uc12d\uae30</strong>{R}?",
     "\uc774 \u304b\u306a\uc758 <strong>\ub85c\ub9c8\uc790 \uc77d\uae30</strong>\ub97c"),
    ("\uc815\ub2f5\ub960?", "\uc815\ub2f5\ub960 "),
    ("\ub2e4\uc2dc \ud480\uae30/button>", "\ub2e4\uc2dc \ud480\uae30</button>"),
    (f"?{R}\ub7ec \uc12d\uae30 \ubcf4\uae30", "\ub204\ub7ec \ub4a4\uc9d1\uae30 \ubcf4\uae30"),
    (f"\u00ab\ubaa8\ub450 \uc55e\uba74\u00bb?{R}\ub85c ??? ?{R}\uc73c{R}",
     "\u00ab\ubaa8\ub450 \uc55e\uba74\u00bb\uc73c\ub85c \ub2e4\uc2dc \uc55e\uba74\uc73c\ub85c"),
    ("\ud788\ub77c\uac00\ub098\uac1d\uad00\uc2dd ?\uc5d0", "\ud788\ub77c\uac00\ub098 \uac1d\uad00\uc2dd: \u304b\u306a\uc5d0"),
    (f" \ub85c\ub9c8??{R}? \uace0\ub9bd\ub2c8\ub2e4", " \ub85c\ub9c8\uc790\ub97c \uace0\ub9bd\ub2c8\ub2e4"),
    (f"?{R}\ub294 \ud55c\uc790 ?{R}\ub4dc 1~4{R}?", " \ub610\ub294 \uc22b\uc790 \ud0a4 1~4\ub85c"),
    ("?? (${maxN}", "\uc804\ubd80 (${maxN}"),
    (f"?{R}\ubb38\ud56d??\ud559\uc2b5?{R}\ub2e4", "\ud2c0\ub9b0 \ubb38\ud56d\uc744 \ud559\uc2b5\ud588\uc2b5\ub2c8\ub2e4"),
    (f"?{R}\ub2f5(\ub85c\ub9c8?:", "\uc815\ub2f5(\ub85c\ub9c8\uc790):"),
    (f"?? \uace0\ub978 ??", "\ub0b4\uac00 \uace0\ub978 \ub2f5:"),
    (f"\ubcf4\uae30{R}?\ub9cc\ub4e4?{R}\uba74", "\ubcf4\uae30\ub97c \ub9cc\ub4e4\ub824\uba74"),
    (f"4??{R}\uc0c1 ?{R}\uc694?{R}\ub2c8??", "4\uac1c \uc774\uc0c1 \ud544\uc694\ud569\ub2c8\ub2e4"),
    (f"?{R}\uc988?{R}\uc911\ub2e8?{R}\uae4c??", "\ud034\uc988\ub97c \uc911\ub2e8\ud560\uae4c\uc694?"),
    (f"?{R}\ub2f5(\ucc38\uace0):", "\uc815\ub2f5(\ucc38\uace0):"),
    (f"\uc8fc??{R}\uc744 \uc911\ub2e8?{R}\uae4c??", "\uc8fc\uad00\uc2dd\uc744 \uc911\ub2e8\ud560\uae4c\uc694?"),
    (f"\uac1d\uad00\uc2dd \ud55c\uc790??\ub9de\ub294", "\uac1d\uad00\uc2dd: \ud55c\uc790\uc5d0 \ub9de\ub294"),
    (f"??(\ubcf4\uae30 ??", "\ub73b (\ubcf4\uae30 \ubd80\uc871)"),
    (f"?{R}\ub2f5:", "\uc815\ub2f5:"),
    (f"?{R}\ub2f5(\uc12d\uae30):", "\uc815\ub2f5(\uc77d\uae30):"),
    (f"?{R}\ub2f5(??", "\uc815\ub2f5(\ub73b:"),
    (f"?? \uc785\ub825\ud55c \ub4a4", "\ub0b4\uac00 \uc785\ub825\ud55c \ub73b:"),
    (f"?? \uc785\ub825\ud55c \ub4a4", "\ub0b4\uac00 \uc785\ub825\ud55c \uc74c:"),
    (f"\uae09\uc218??\ud55c\uc790", "\uae09\uc218\uc5d0 \ud55c\uc790\uac00"),
    (f"???{R}\uc790??\ub9de\ub294", "\uc774 \ud55c\uc790\uc5d0 \ub9de\ub294"),
    ('<span class="kanji" id="kanjiFront"></span>', '<span class="kanji" id="kanjiFront">\u4e00</span>'),
    ('id="quizKanji"></div>', 'id="quizKanji">\u4e00</motion>'),
    ('id="writtenKanji"></div>', 'id="writtenKanji">\u4e00</motion>'),
]

UNDO = [
    ("\uc77c\ubcf8\uc5b4 \uc12d\uae30", "\uc77c\ubcf8\uc5b4 \uc77d\uae30"),
    ("\ub85c\ub9c8\uc790 \uc12d\uae30", "\ub85c\ub9c8\uc790 \uc77d\uae30"),
    ("\ud55c\uad6d\uc5b4 \ub73b\xb7\uc12d\uae30 \uc804\uccb4", "\ud55c\uad6d\uc5b4 \ub73b(\uc77d\uae30 \uc804\uccb4)"),
    ("<strong>\uc12d\uae30</strong>(\ud788\ub77c\uac00\ub098", "<strong>\uc77d\uae30</strong>(\ud788\ub77c\uac00\ub098"),
    ("\uc815\ub2f5(\uc12d\uae30):", "\uc815\ub2f5(\uc77d\uae30):"),
    ("\ub2e8\uc5b4 \uac1d\uad00\uc2dd \uc12d\uae30??", "\ub2e8\uc5b4 \uac1d\uad00\uc2dd: \uc77d\uae30\uc5d0"),
]


def main() -> None:
    text = STUDY.read_text(encoding="utf-8")
    n0 = text.count("\ufffd")
    for a, b in FIXES + UNDO:
        text = text.replace(a, b)
    text = text.replace('id="quizKanji">\u4e00</motion>', 'id="quizKanji">\u4e00</div>')
    text = text.replace('id="writtenKanji">\u4e00</motion>', 'id="writtenKanji">\u4e00</div>')
    STUDY.write_text(text, encoding="utf-8", newline="\n")
    print("U+FFFD", n0, "->", text.count("\ufffd"))


if __name__ == "__main__":
    main()
