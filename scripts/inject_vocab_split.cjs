const fs = require("fs");
const { studyHtml, vocab } = require("./paths.cjs");

function esc(s) {
  return s.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
}

function readTsv(name) {
  const p = vocab(name);
  if (!fs.existsSync(p)) throw new Error("missing " + name);
  return fs.readFileSync(p, "utf8").trim();
}

const n5Legacy = readTsv("n5_vocab_legacy.tsv");
const n5New = readTsv("n5_vocab_new.tsv");
const n4Legacy = readTsv("n4_vocab_legacy.tsv");
const n4New = readTsv("n4_vocab_new.tsv");

let html = fs.readFileSync(studyHtml, "utf8");

const rawBlock =
  `const N5_VOCAB_LEGACY_RAW = \`${esc(n5Legacy)}\`;\n` +
  `    const N5_VOCAB_NEW_RAW = \`${esc(n5New)}\`;\n` +
  `    const N4_VOCAB_LEGACY_RAW = \`${esc(n4Legacy)}\`;\n` +
  `    const N4_VOCAB_NEW_RAW = \`${esc(n4New)}\`;\n\n`;

const rawRe =
  /const N5_VOCAB_LEGACY_RAW = `[\s\S]*?`;\s*\r?\n\s*const N5_VOCAB_NEW_RAW = `[\s\S]*?`;\s*\r?\n\s*const N4_VOCAB_LEGACY_RAW = `[\s\S]*?`;\s*\r?\n\s*const N4_VOCAB_NEW_RAW = `[\s\S]*?`;\s*\r?\n\s*/;

const parseBlock = `const N5_LEGACY = parseVocab(N5_VOCAB_LEGACY_RAW);
    const N5_NEW = parseVocab(N5_VOCAB_NEW_RAW);
    const N4_LEGACY = parseN4Tsv(N4_VOCAB_LEGACY_RAW);
    const N4_NEW = parseN4Tsv(N4_VOCAB_NEW_RAW);
`;

const parseRe =
  /const N5_LEGACY = parseVocab\(N5_VOCAB_LEGACY_RAW\);\s*\r?\n\s*const N5_NEW = parseVocab\(N5_VOCAB_NEW_RAW\);\s*\r?\n\s*const N4_LEGACY = parseN4Tsv\(N4_VOCAB_LEGACY_RAW\);\s*\r?\n\s*const N4_NEW = parseN4Tsv\(N4_VOCAB_NEW_RAW\);\s*\r?\n/;

if (rawRe.test(html)) {
  html = html.replace(rawRe, rawBlock);
} else {
  const anchor = /(const N4_VOCAB_RAW = `[\s\S]*?`;\s*\r?\n)(\s*function parseN4Tsv)/;
  if (!anchor.test(html)) throw new Error("N4_VOCAB_RAW anchor not found");
  html = html.replace(anchor, `$1\n    ${rawBlock}$2`);
}

if (parseRe.test(html)) {
  html = html.replace(parseRe, parseBlock);
} else {
  const anchor = /(const N4_ALL = parseN4Tsv\(N4_VOCAB_RAW\);\s*\r?\n)(\s*const HIRA_RAW)/;
  if (!anchor.test(html)) throw new Error("N4_ALL anchor not found");
  html = html.replace(
    anchor,
    `const VOCAB_ALL = parseVocab(VOCAB_RAW);\n    $1    ${parseBlock}\n$2`
  );
}

if (!/const VOCAB_ALL = parseVocab\(VOCAB_RAW\)/.test(html)) {
  throw new Error("VOCAB_ALL parse missing after inject");
}

fs.writeFileSync(studyHtml, html, "utf8");
console.log(
  "injected split pools N5 legacy/new:",
  n5Legacy.split("\n").length,
  n5New.split("\n").length,
  "N4:",
  n4Legacy.split("\n").length,
  n4New.split("\n").length
);
