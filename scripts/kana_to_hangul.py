# -*- coding: utf-8 -*-
"""히라가나·가타카나 → 한국어 표기 발음 (교재식, 근사 변환)."""
from __future__ import annotations

import re

_HIRA = (
    "あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてと"
    "だぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめも"
    "やゆよらりるれろわゐゑをんゔー"
)
_HANGUL = (
    "아이우에오카키쿠케코가기구게고사시스세소자지즈제조타치츠테토"
    "다지즈데도나니누네노하히후헤호바비부베보파피푸페포마미무메모"
    "야유요라리루레로와이에오느브ー"
)
_KATA = "アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヰヱヲンヴー"

_MAP: dict[str, str] = {}
for a, b in zip(_HIRA, _HANGUL):
    _MAP[a] = b
for a, b in zip(_KATA, _HANGUL):
    _MAP[a] = b

_YOON = {
    "きゃ": "캬",
    "きゅ": "큐",
    "きょ": "쿄",
    "ぎゃ": "갸",
    "ぎゅ": "규",
    "ぎょ": "교",
    "しゃ": "샤",
    "しゅ": "슈",
    "しょ": "쇼",
    "じゃ": "쟈",
    "じゅ": "주",
    "じょ": "조",
    "ちゃ": "챠",
    "ちゅ": "츄",
    "ちょ": "쵸",
    "にゃ": "냐",
    "にゅ": "뉴",
    "にょ": "뇨",
    "ひゃ": "햐",
    "ひゅ": "휴",
    "ひょ": "효",
    "びゃ": "뱌",
    "びゅ": "뷰",
    "びょ": "뵤",
    "ぴゃ": "퍄",
    "ぴゅ": "퓨",
    "ぴょ": "표",
    "みゃ": "먀",
    "みゅ": "뮤",
    "みょ": "묘",
    "りゃ": "랴",
    "りゅ": "류",
    "りょ": "료",
    "キャ": "캬",
    "キュ": "큐",
    "キョ": "쿄",
    "シャ": "샤",
    "シュ": "슈",
    "ショ": "쇼",
    "チャ": "챠",
    "チュ": "츄",
    "チョ": "쵸",
}

_GEM = {
    "か": "ㅋ",
    "き": "ㅋ",
    "く": "ㅋ",
    "け": "ㅋ",
    "こ": "ㅋ",
    "が": "ㄲ",
    "ぎ": "ㄲ",
    "ぐ": "ㄲ",
    "げ": "ㄲ",
    "ご": "ㄲ",
    "さ": "ㅅ",
    "し": "ㅅ",
    "す": "ㅅ",
    "せ": "ㅅ",
    "そ": "ㅅ",
    "た": "ㅌ",
    "ち": "ㅌ",
    "つ": "ㅌ",
    "て": "ㅌ",
    "と": "ㅌ",
    "ぱ": "ㅃ",
    "ぴ": "ㅃ",
    "ぷ": "ㅃ",
    "ぺ": "ㅃ",
    "ぽ": "ㅃ",
    "は": "ㅎ",
    "ひ": "ㅎ",
    "ふ": "ㅎ",
    "へ": "ㅎ",
    "ほ": "ㅎ",
}

_HAS_KR_PRON = re.compile(r"\([가-힣][가-힣\s]*\)")

# 짧은 읽기·교재 관용 표기
_SPECIAL: dict[str, str] = {
    "えん": "엔",
    "おん": "온",
    "いっしょ": "잇쇼",
    "いっしゅう": "잇슈",
    "がっこう": "갓코",
    "きっ": "킷",
    "ちょっと": "촛토",
}


def _to_hira(ch: str) -> str:
    o = ord(ch)
    if 0x30A1 <= o <= 0x30F6:
        return chr(o - 0x60)
    return ch


def _long(prev: str) -> str:
    if not prev:
        return "우"
    for v, vowels in (
        ("아", ("아", "카", "사", "타", "파", "하", "마", "야", "라", "와", "가", "자", "다", "바")),
        ("이", ("이", "키", "시", "치", "니", "히", "미", "리", "기", "지", "비", "피", "디")),
        ("우", ("우", "쿠", "스", "츠", "푸", "무", "루", "구", "즈", "부", "두")),
        ("에", ("에", "케", "세", "테", "헤", "메", "레", "게", "제", "베", "페", "데")),
        ("오", ("오", "코", "소", "토", "호", "모", "요", "로", "고", "조", "보", "포", "도")),
    ):
        if prev.endswith(vowels):
            return prev[:-1] + v
    return prev + "우"


def kana_to_hangul(text: str) -> str:
    if not text or not text.strip():
        return ""
    raw = text.strip()
    if raw in _SPECIAL:
        return _SPECIAL[raw]
    for key, val in _SPECIAL.items():
        if raw.startswith(key) and len(raw) > len(key):
            return val + kana_to_hangul(raw[len(key) :])
    s = "".join(_to_hira(c) for c in raw)
    out: list[str] = []
    i = 0
    while i < len(s):
        if i + 1 < len(s):
            pair = s[i : i + 2]
            if pair in _YOON:
                out.append(_YOON[pair])
                i += 2
                continue
        ch = s[i]
        if ch == "っ" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt in _GEM:
                out.append(_GEM[nxt])
            i += 1
            continue
        if ch == "ー":
            if out:
                out[-1] = _long(out[-1])
            i += 1
            continue
        if ch == "ん":
            if i + 1 < len(s) and s[i + 1] in "さしすせそざじずぜぞたちつてとだぢづでどはひふへほ":
                i += 1
                continue
            if out and out[-1].endswith("사"):
                out[-1] = out[-1][:-1] + "상"
            i += 1
            continue
        h = _MAP.get(ch) or _MAP.get(s[i])
        if h and h != "ー":
            out.append(h)
        i += 1
    result = "".join(out)
    if result.endswith("san"):
        result = result[:-3] + "상"
    # 흔한 교재 표기 보정
    fixes = (
        ("가ㅋ코", "갓코"),
        ("가ㅋ쿠", "갓쿠"),
        ("쵸ㅌ토", "촛토"),
        ("세n세", "센세"),
        ("세n", "센"),
        ("카ㅋ", "캇"),
        ("이ㅅ쇼", "잇쇼"),
        ("이ㅅ슈", "잇슈"),
        ("아사ㅌ테", "아사떼"),
        ("이라ㅅ샤", "이라샤"),
        (" (에)", " (엔)"),
    )
    for a, b in fixes:
        result = result.replace(a, b)
    return result


def japanese_reading_part(reading: str) -> str:
    t = reading.strip()
    cut = t.find(" (")
    if cut >= 0:
        return t[:cut].strip()
    return t


def add_korean_pronunciation(reading: str) -> str:
    raw = reading.strip()
    if not raw:
        return raw
    if _HAS_KR_PRON.search(raw):
        return raw
    parts = re.split(r"([/／])", raw)
    out: list[str] = []
    for p in parts:
        if p in "/／":
            out.append(p)
            continue
        seg = p.strip()
        if not seg:
            continue
        jp = japanese_reading_part(seg)
        if _HAS_KR_PRON.search(seg):
            out.append(seg)
            continue
        kr = kana_to_hangul(jp)
        if kr and re.search(r"[ぁ-んァ-ンー]", jp):
            out.append(f"{jp} ({kr})")
        else:
            out.append(seg)
    return "".join(out)
