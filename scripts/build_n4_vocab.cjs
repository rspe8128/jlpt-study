const fs = require("fs");
const { sources, vocab } = require("./paths.cjs");

const files = ["_n4_noun_pdf.txt", "_n4_verb_pdf.txt", "_n4_adj_pdf.txt"];
const rows = [];
const seen = new Set();

function normDash(s) {
  return s.replace(/[―—ー＿]/g, "").trim();
}

for (const f of files) {
  const text = fs.readFileSync(sources(f), "utf8");
  for (let line of text.split(/\n/)) {
    line = line.trim();
    if (!line || line.startsWith("어휘")) continue;
    const parts = line.split("\t").map((x) => x.trim());
    if (parts.length < 3) continue;
    const reading = parts[0];
    const kanji = parts[1];
    const meaning = parts.slice(2).join(" ").trim();
    if (!/[ぁ-んァ-ン一-龯々]/.test(reading)) continue;
    if (!meaning) continue;
    const key = `${reading}\t${kanji}\t${meaning}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const kd = normDash(kanji);
    const word = kd ? kanji : reading;
    rows.push({ reading, word, meaning });
  }
}

let out = "";
rows.forEach((r, i) => {
  out += `${i + 1}\t${r.word}\t${r.reading}\t${r.meaning}\n`;
});
fs.writeFileSync(vocab("n4_vocab.tsv"), out, "utf8");
console.log("entries", rows.length);
