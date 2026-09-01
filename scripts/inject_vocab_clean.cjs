const fs = require("fs");
const { studyHtml, vocab } = require("./paths.cjs");

function esc(s) {
  return s.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
}

function readTsv(name) {
  return fs.readFileSync(vocab(name), "utf8").trim();
}

const n5 = readTsv("n5_vocab.tsv");
const n4 = readTsv("n4_vocab.tsv");
const n5Legacy = readTsv("n5_vocab_legacy.tsv");
const n5New = readTsv("n5_vocab_new.tsv");
const n4Legacy = readTsv("n4_vocab_legacy.tsv");
const n4New = readTsv("n4_vocab_new.tsv");

const block = `const VOCAB_RAW = \`${esc(n5)}\`;

    function parseVocab(text) {
      const rows = [];
      for (const line of text.trim().split("\\n")) {
        const parts = line.split("\\t");
        if (parts.length < 4) continue;
        rows.push({
          no: parseInt(parts[0], 10),
          word: parts[1],
          reading: parts[2],
          meaning: parts[3],
        });
      }
      return rows;
    }

    const N5_VOCAB_LEGACY_RAW = \`${esc(n5Legacy)}\`;
    const N5_VOCAB_NEW_RAW = \`${esc(n5New)}\`;
    const N4_VOCAB_RAW = \`${esc(n4)}\`;
    const N4_VOCAB_LEGACY_RAW = \`${esc(n4Legacy)}\`;
    const N4_VOCAB_NEW_RAW = \`${esc(n4New)}\`;

    function parseN4Tsv(text) {
      return parseVocab(text);
    }

    const VOCAB_ALL = parseVocab(VOCAB_RAW);
    const N4_ALL = parseN4Tsv(N4_VOCAB_RAW);
    const N5_LEGACY = parseVocab(N5_VOCAB_LEGACY_RAW);
    const N5_NEW = parseVocab(N5_VOCAB_NEW_RAW);
    const N4_LEGACY = parseN4Tsv(N4_VOCAB_LEGACY_RAW);
    const N4_NEW = parseN4Tsv(N4_VOCAB_NEW_RAW);

`;

let html = fs.readFileSync(studyHtml, "utf8");
const re = /const VOCAB_RAW = `[\s\S]*?(?=\s*const HIRA_RAW = `)/;
if (!re.test(html)) throw new Error("VOCAB_RAW..HIRA_RAW span not found");
html = html.replace(re, block);
fs.writeFileSync(studyHtml, html, { encoding: "utf8" });
console.log("vocab clean inject ok");
