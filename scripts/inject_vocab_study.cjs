const fs = require("fs");
const { studyHtml, vocab } = require("./paths.cjs");

const n5 = fs.readFileSync(vocab("n5_vocab.tsv"), "utf8").trim();
const n4 = fs.readFileSync(vocab("n4_vocab.tsv"), "utf8").trim();

function esc(s) {
  return s.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
}

let html = fs.readFileSync(studyHtml, "utf8");

const n5Re = /const VOCAB_RAW = `[\s\S]*?`;\s*\r?\n\s*function parseVocab/;
const n4Re = /const N4_VOCAB_RAW = `[\s\S]*?`;\s*\r?\n\s*function parseN4Tsv/;

if (!n5Re.test(html) || !n4Re.test(html)) {
  throw new Error("VOCAB_RAW / N4_VOCAB_RAW blocks not found in study.html");
}

html = html.replace(
  n5Re,
  `const VOCAB_RAW = \`${esc(n5)}\`;\n\n    function parseVocab`
);
html = html.replace(
  n4Re,
  `const N4_VOCAB_RAW = \`${esc(n4)}\`;\n\n    function parseN4Tsv`
);

fs.writeFileSync(studyHtml, html, "utf8");
console.log("injected N5:", n5.split("\n").length, "N4:", n4.split("\n").length);
