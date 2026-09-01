const fs = require("fs");
const { studyHtml, kanjiRaw } = require("./paths.cjs");

function esc(s) {
  return s.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
}

const lines = fs.readFileSync(kanjiRaw, "utf8").trim().split(/\r?\n/);
const rawLines = lines
  .map((line) => {
    const parts = line.split("\t");
    if (parts.length < 3) return null;
    const id = parts[0].padStart(3, "0");
    return `${id}\t${parts[1]}\t${parts.slice(2).join("\t")}`;
  })
  .filter(Boolean);

const block = `const RAW = \`${esc(rawLines.join("\n"))}\`;\n\n`;

let html = fs.readFileSync(studyHtml, "utf8");
const re = /const RAW = `[\s\S]*?function parseRaw/;
if (!re.test(html)) throw new Error("RAW block not found");
html = html.replace(re, block + "    function parseRaw");
fs.writeFileSync(studyHtml, html, { encoding: "utf8" });
console.log("injected kanji:", rawLines.length);
