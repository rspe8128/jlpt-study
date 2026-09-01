const fs = require("fs");
const { studyHtml, vocab } = require("./paths.cjs");

const tsv = fs.readFileSync(vocab("n4_vocab.tsv"), "utf8");
let html = fs.readFileSync(studyHtml, "utf8");
const marker = "/*__N4_VOCAB_RAW__*/";
if (!html.includes(marker)) throw new Error("marker missing in study.html");
const escaped = tsv.trim().replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
const injection = `const N4_VOCAB_RAW = \`${escaped}\`;

    function parseN4Tsv(text) {
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

    const N4_ALL = parseN4Tsv(N4_VOCAB_RAW);
`;
html = html.replace(marker, injection);
fs.writeFileSync(studyHtml, html, "utf8");
console.log("injected n4", tsv.trim().split("\n").length);
