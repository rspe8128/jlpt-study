const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

let html = fs.readFileSync(studyHtml, "utf8");

const refreshVocabSubtitle = `    function refreshVocabSubtitle() {
      if (topMode === "hira" || subjectMode !== "vocab") return;
      if (vocabStudyMode === "list") {
        appSubtitle.textContent =
          "\\uae30\\ubcf8(\\uae30\\uc874) \\ub2e8\\uc5b4 \\ubaa9\\ub85d: \\ud589\\uc744 \\ub204\\ub974\\uba74 \\uc624\\ub978\\ucabd\\uc5d0 \\uc77d\\uae30\\u00b7\\ub73b. \\u00ab\\ubaa8\\ub450 \\uc228\\uae30\\u00bb\\ub85c \\uc804\\ubd80 \\uc228\\uae41\\ub2c8\\ub2e4.";
        return;
      }
      if (vocabStudyMode === "cards") {
        appSubtitle.innerHTML =
          "\\uc55e \\uc77c\\ubcf8\\uc5b4 \\uc77d\\uae30 \\u00b7 \\ub4a4 \\ud55c\\uad6d\\uc5b4 \\ub73b(\\uc77d\\uae30 \\uc804\\uccb4) \\u00b7 <kbd>Space</kbd> \\ub4a4\\uc9d1\\uae30 \\u00b7 <kbd>\\u2190</kbd><kbd>\\u2192</kbd>";
      } else if (vocabQuizKind === "reading") {
        appSubtitle.textContent =
          "\\ub2e8\\uc5b4 \\uac1d\\uad00\\uc2dd: \\uc77d\\uae30\\uc5d0 \\ub9de\\ub294 \\uc77c\\ubcf8\\uc5b4 \\uc77d\\uae30\\ub97c \\uace0\\ub985\\ub2c8\\ub2e4. \\ud0a4\\ubcf4\\ub4dc 1~4 \\ub610\\ub294 \\uc22b\\uc790 \\ud0a4 1~4\\ub85c \\ubcf4\\uae30 \\uc120\\ud0dd";
      } else {
        appSubtitle.textContent =
          "\\ub2e8\\uc5b4 \\uac1d\\uad00\\uc2dd: \\uc77d\\uae30\\uc5d0 \\ub9de\\ub294 \\ud55c\\uad6d\\uc5b4 \\ub73b\\uc744 \\uace0\\ub985\\ub2c8\\ub2e4. \\ud0a4\\ubcf4\\ub4dc 1~4 \\ub610\\ub294 \\uc22b\\uc790 \\ud0a4 1~4\\ub85c \\ubcf4\\uae30 \\uc120\\ud0dd";
      }
    }`;

const updateVocabQuizSetupHelp = `    function updateVocabQuizSetupHelp() {
      if (!vocabQuizSetupHelp) return;
      if (vocabQuizKind === "reading") {
        vocabQuizSetupHelp.innerHTML =
          "\\uc704\\uc5d0 \\ubcf4\\uc774\\ub294 <strong>\\uc77c\\ubcf8\\uc5b4 \\uc77d\\uae30</strong>\\uc5d0 \\ub9de\\ub294 <strong>\\uc77d\\uae30</strong>(\\ud788\\ub77c\\uac00\\ub098\\u00b7\\uac00\\ud0c0\\uce74\\ub098)\\ub97c \\uace0\\ub974\\uc138\\uc694.<br />\\ubb38\\uc81c \\uc21c\\uc11c\\uc640 \\ubcf4\\uae30 \\uc21c\\uc11c\\ub294 \\uc138\\ud2b8\\ub9c8\\ub2e4 \\ubb34\\uc791\\uc704\\uc785\\ub2c8\\ub2e4. (\\ubcf4\\uae30 4\\uac1c \\u00b7 \\ud604\\uc7ac \\uae09\\uc218 \\ud480 \\uae30\\uc900)";
      } else {
        vocabQuizSetupHelp.innerHTML =
          "\\uc704\\uc5d0 \\ubcf4\\uc774\\ub294 <strong>\\uc77c\\ubcf8\\uc5b4 \\uc77d\\uae30</strong>\\uc5d0 \\ub9de\\ub294 <strong>\\ud55c\\uad6d\\uc5b4 \\ub73b</strong>\\uc744 \\uace0\\ub974\\uc138\\uc694.<br />\\ubb38\\uc81c \\uc21c\\uc11c\\uc640 \\ubcf4\\uae30 \\uc21c\\uc11c\\ub294 \\uc138\\ud2b8\\ub9c8\\ub2e4 \\ubb34\\uc791\\uc704\\uc785\\ub2c8\\ub2e4. (\\ubcf4\\uae30 4\\uac1c \\u00b7 \\ud604\\uc7ac \\uae09\\uc218 \\ud480 \\uae30\\uc900)";
      }
    }`;

const refreshHiraSubtitle = `    function refreshHiraSubtitle() {
      if (topMode !== "hira") return;
      if (hiraStudyMode === "cards") {
        appSubtitle.innerHTML =
          "\\uc55e \\u304b\\u306a \\u00b7 \\ub4a4 \\ub85c\\ub9c8\\uc790\\u00b7\\ud589(\\ub2e8) \\u00b7 <kbd>Space</kbd> \\ub4a4\\uc9d1\\uae30 \\u00b7 <kbd>\\u2190</kbd><kbd>\\u2192</kbd>";
      } else if (hiraStudyMode === "chart") {
        appSubtitle.textContent =
          "\\u4e94\\u5341\\u97f3\\u56f3: \\uce78\\uc744 \\ub204\\ub974\\uba74 \\ub4a4\\uc9d1\\uc5b4 \\ub85c\\ub9c8\\uc790\\u00b7\\ud589 \\uc774\\ub984\\uc744 \\ubcf4\\uc785\\ub2c8\\ub2e4. \\u00ab\\ubaa8\\ub450 \\uc55e\\uba74\\u00bb\\uc73c\\ub85c \\ub2e4\\uc2dc \\uc55e\\uba74\\uc73c\\ub85c \\ub3cc\\ub9bd\\ub2c8\\ub2e4.";
      } else {
        appSubtitle.textContent =
          "\\ud788\\ub77c\\uac00\\ub098 \\uac1d\\uad00\\uc2dd: \\u304b\\u306a\\uc5d0 \\ub9de\\ub294 \\ub85c\\ub9c8\\uc790\\ub97c \\uace0\\ub985\\ub2c8\\ub2e4. \\ud0a4\\ubcf4\\ub4dc 1~4 \\ub610\\ub294 \\uc22b\\uc790 \\ud0a4 1~4\\ub85c \\ubcf4\\uae30 \\uc120\\ud0dd";
      }
    }`;

function replaceFn(name, body) {
  const re = new RegExp(`function ${name}\\(\\)[\\s\\S]*?\\n    }`);
  if (!re.test(html)) throw new Error("fn not found: " + name);
  html = html.replace(re, body.trim());
}

replaceFn("refreshVocabSubtitle", refreshVocabSubtitle);
replaceFn("updateVocabQuizSetupHelp", updateVocabQuizSetupHelp);
replaceFn("refreshHiraSubtitle", refreshHiraSubtitle);

const htmlFixes = [
  ["<h2>주관식?정</h2>", "<h2>주관식 설정</h2>"],
  [
    "한자가 보이면 <strong>뜻</strong>과 <strong>음</strong>?칸에 입력한 뒤<strong>채점</strong>?니??<br />",
    "한자가 보이면 <strong>뜻</strong>과 <strong>음</strong> 칸에 입력한 뒤 <strong>채점</strong>합니다.<br />",
  ],
  [
    "문제 ?서??세트마다 무작위입니다. (?답? ?의 뜻·음?비교·여러 뜻·",
    "문제 순서는 세트마다 무작위입니다. (정답은 뜻의 뜻·음과 비교·여러 뜻·",
  ],
  ['<label for="writtenMean">??(??)</label>', '<label for="writtenMean">뜻 (한글)</label>'],
  ['<label for="writtenRead">??(??)</label>', '<label for="writtenRead">음 (훈독)</label>'],
];

for (const [a, b] of htmlFixes) {
  if (html.includes(a)) html = html.split(a).join(b);
}

html = html.replace(
  /\/\* 상단 탭·모드 바:[\s\S]*?\*\//,
  "/* 상단 탭·모드 바: 콘텐츠 상단에 고정 (모드 전환 시 왼쪽으로 밀림 방지) */"
);
html = html.replace(/aria-label="학습 [^"]*"/, 'aria-label="학습 종목"');

fs.writeFileSync(studyHtml, html, { encoding: "utf8" });
console.log("patched functions, fffd", (html.match(/\uFFFD/g) || []).length);
