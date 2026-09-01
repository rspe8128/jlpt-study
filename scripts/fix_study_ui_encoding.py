# -*- coding: utf-8 -*-
"""Restore corrupted Korean/Japanese UI strings in study.html (UTF-8 mojibake)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "study.html"

# Literal broken fragments as they appear in the file (U+FFFD shown explicitly).
R = "\ufffd"

REPLACEMENTS: list[tuple[str, str]] = [
    (f"JLPT N4·N5 ?{R}합 ?{R}습 (study)", "JLPT N4·N5 통합 학습 (study)"),
    (f"JLPT N4·N5 ?{R}습", "JLPT N4·N5 학습"),
    (f"?{R}합 ?{R}습", "통합 학습"),
    (f"?{R}습", "학습"),
    (f"?{R}합", "통합"),
    (f"카드{R}??{R}러 ?{R}·뒤{R}??{R}기?{R}요", "카드를 눌러 앞·뒤를 뒤집어요"),
    (f"<kbd>??/kbd><kbd>??/kbd>", "<kbd>←</kbd><kbd>→</kbd>"),
    (f"?{R}집{R}", "뒤집기"),
    (f"?{R}동", "이동"),
    (f"???{R}체 목차", "← 전체 목차"),
    (f"?{R}라{R}??/button>", "히라가나</button>"),
    (f"?{R}라{R}??", "히라가나"),
    (f"?{R}습 메뉴", "학습 메뉴"),
    (f"?{R}습 ??{R}", "학습 종목"),
    (f"?{R}습 모드", "학습 모드"),
    (f"?{R}습 ?{R}태", "학습 상태"),
    (f"?{R}자", "한자"),
    (f"?{R}어", "단어"),
    (f"?{R}래?{R}카??/button>", "플래시카드</button>"),
    (f"?{R}래?{R}카??", "플래시카드"),
    (f"객{R}???/button>", "객관식</button>"),
    (f"객{R}???", "객관식"),
    (f"주{R}???/button>", "주관식</button>"),
    (f"주{R}???", "주관식"),
    (f"?{R}기", "섞기"),
    (f"?{R}전", "이전"),
    (f"?{R}음", "다음"),
    (f"?{R}릭?{R}여", "눌러"),
    (f"??보기", "뒤 보기"),
    (f"?{R}즈 ?{R}정", "퀴즈 설정"),
    (f"???{R}트 문제 ??/label>", "한 세트 문제 수</label>"),
    (f"?{R}자{R} 주어{R}?", "한자를 주어진"),
    (f"?{R}·음", "뜻·음"),
    (f"?{R}나{R}?", "하나를"),
    (f"고릅?{R}다", "고릅니다"),
    (f"?{R}서?{R}", "순서와"),
    (f"??{R}트마다", "세트마다"),
    (f"무작?{R}입?{R}다", "무작위입니다"),
    (f"(보기 4{R})", "(보기 4개)"),
    (f"?{R}즈 ?{R}작", "퀴즈 시작"),
    (f"?{R}??{R}?", "그만하기"),
    (f"?{R}트 결과", "세트 결과"),
    (f"?{R}답{R}", "정답률"),
    (f"?{R}?문제", "틀린 문제"),
    (f"?{R}시 ?{R}?", "다시 풀기"),
    (f"?{R}정?{R}로", "설정으로"),
    (f"주{R}????{R}정", "주관식 설정"),
    (f"?{R}자{R} 보이{R}", "한자가 보이면"),
    (f"??/strong>?", "뜻</strong>과"),
    (f"<strong>??/strong>??", "<strong>음</strong>을"),
    (f"?{R}력????", "입력한 뒤"),
    (f"?{R}답?{R}", "정답은"),
    (f"?{R}의 ?{R}·음{R}?", "뜻의 뜻·음과"),
    (f"?{R}러 ?{R}기", "여러 뜻"),
    (f"??(?{R}국??", "뜻 (한국어)"),
    (f"??(?{R}기)", "음 (읽기)"),
    (f"?{R}본???{R}기", "일본어 읽기"),
    (f"?{R}국????", "한국어 뜻"),
    (f"?{R}체", "전체"),
    (f"?{R}규", "신규"),
    (f"?{R}에 보이??", "위에 보이는"),
    (f"??기{R}?", "읽기와"),
    (f"??기{R}", "읽기"),
    (f"??기??", "읽기를"),
    (f"??기??", "읽기를"),
    (f"?{R}재 급수 ??기{R}", "현재 급수 풀 기준"),
    (f"?{R}보??1~4", "키보드 1~4"),
    (f"?{R}자 ?{R}드 1~4{R}?", "숫자 키 1~4로"),
    (f"보기 ?{R}택", "보기 선택"),
    (f"清音 46??", "清音 46자"),
    (f"五十?{R}図", "五十音図"),
    (f"칸을 ?{R}르{R}", "칸을 누르면"),
    (f"?{R}집?{R}", "뒤집어"),
    (f"로마?{R}·행", "로마자·행"),
    (f"?{R}름??", "이름을"),
    (f"보입?{R}다", "보입니다"),
    (f"모두 ?{R}면", "모두 앞면"),
    (f"?{R}러 ?{R}기·???{R}내", "눌러 읽기·행 안내"),
    (f"?? ?{R}기·?{R}본???{R}기", "앞 일본어 읽기 · 뒤 한국어 뜻"),
    (f"?? ?{R}국????", "뒤 한국어 뜻"),
    (f"????· ?? 로마?{R}·행(? ·", "앞 かな · 뒤 로마자·행(段) ·"),
    (f"?{R}라{R}??객{R}???", "히라가나 객관식"),
    (f"?{R}라{R}????", "히라가나 한 글자"),
    (f"?{R}보??로마??", "키보드 로마자"),
    (f"?{R}서 무작??", "순서 무작위)"),
    (f"???의", "이 かな의"),
    (f"로마???{R}기", "로마자 읽기"),
    (f"?{R}과 ?{R}을 ?{R}력?{R}세??", "뜻과 음을 입력하세요"),
    (f"??(?{R}미)", "뜻 (한글)"),
    (f"??(?{R}독)", "음 (훈독)"),
    (f"?{R}·음???{R}력????", "뜻·음을 입력한 뒤"),
    (f"채점?{R}니??", "채점합니다"),
    (f"Enter: 채점 ???{R}음", "Enter: 채점 → 다음"),
    (f"???{R}자??", "이 한자에"),
    (f"고르?{R}요", "고르세요"),
    (f"??/button>", "표</button>"),
    (f"??/span>", "あ</span>"),
    (f"<span class=\"kanji\" id=\"kanjiFront\">?/span>", '<span class="kanji" id="kanjiFront">一</span>'),
    (f"<motion>", "<motion>"),  # noop if any
    (f"/* ?{R}단 ??{R}모??{R}? 콘텐{R}???{R}?{R}데 고정 (모드 ?{R}환 ???{R}쪽?{R}로 ?방{R}) */",
     "/* 상단 탭·모드 바: 콘텐츠 상단에 고정 (모드 전환 시 왼쪽으로 밀림 방지) */"),
    (f'appH.textContent = "JLPT · ?{R}라{R}??;', 'appH.textContent = "JLPT · 히라가나";'),
    (f'?{R}어" : "JLPT N4 · ?{R}어"', '단어" : "JLPT N4 · 단어"'),
    (f'"JLPT N5 · ?{R}어"', '"JLPT N5 · 단어"'),
    (f'?{R}자"', '한자"'),
    (f' · ?{R}규"', ' · 신규"'),
    (f' + " ?{R}어"', ' + " 단어"'),
    (f'"?? ?{R}기·?{R}본???{R}기 · ?? ?{R}국???? · ?{R}기 ?{R}체) · <kbd>Space</kbd> ?{R}집{R}· <kbd>??/kbd><kbd>??/kbd>"',
     '"앞 일본어 읽기 · 뒤 한국어 뜻(읽기 전체) · <kbd>Space</kbd> 뒤집기 · <kbd>←</kbd><kbd>→</kbd>"'),
    (f"?{R}어 객{R}???", "단어 객관식"),
    (f"?{R}기??", "읽기를"),
    (f"?{R}본???{R}기", "일본어 읽기"),
    (f"?{R}국???{R}", "한국어 뜻을"),
    (f"?{R}보??1~4 ?{R}는 ?{R}자 ?{R}드 1~4{R}?", "키보드 1~4 또는 숫자 키 1~4로"),
    (f'headLabel.textContent = "??;', 'headLabel.textContent = "段";'),
    (f'for (const col of ["??, "??, "??, "??, "??])', 'for (const col of ["あ", "い", "う", "え", "お"])'),
    (f"?{R}라{R}??객{R}??? ?{R}??", "히라가나 객관식 한 글자"),
    (f"«모두 ?{R}면»?{R}로 ?{R}?? ?{R}으{R}", "«모두 앞면»으로 다시 앞면으로"),
    (f"?{R}립?{R}다", "돌립니다"),
]

# Fix broken closing tags: `?/button>` -> missing `<` before /
BROKEN_TAG = re.compile(
    r"(?<=[가-힣a-zA-Z0-9\u3040-\u30ff\u4e00-\u9fff·\s])\?/(\w+>)"
)


def main() -> None:
    text = STUDY.read_text(encoding="utf-8")
    before_fffd = text.count("\ufffd")
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
    text = BROKEN_TAG.sub(r"</\1", text)
    # Remaining ?/button> patterns
    text = text.replace("?/button>", "</button>")
    text = text.replace("?/label>", "</label>")
    text = text.replace("?/span>", "</span>")
    text = text.replace("?/strong>", "</strong>")
    text = text.replace("?/div>", "</div>")
    text = text.replace("?/option>", "</option>")
    after_fffd = text.count("\ufffd")
    STUDY.write_text(text, encoding="utf-8", newline="\n")
    print(f"U+FFFD: {before_fffd} -> {after_fffd}")
    if after_fffd:
        print("warning: replacement chars remain — check study.html manually")


if __name__ == "__main__":
    main()
