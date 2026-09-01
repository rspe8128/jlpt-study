const fs = require("fs");
const { studyHtml, DATA } = require("./paths.cjs");
const path = require("path");

function esc(s) {
  return s.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$/g, "\\$");
}

const tsv = fs.readFileSync(path.join(DATA, "hiragana.tsv"), "utf8").trim();
const hiraRaw = `const HIRA_RAW = \`${esc(tsv)}\`;\n\n`;

const chartRows = `const HIRA_CHART_ROWS = [
      { label: "あ", cells: ["あ", "い", "う", "え", "お"] },
      { label: "K", cells: ["か", "き", "く", "け", "こ"] },
      { label: "S", cells: ["さ", "し", "す", "せ", "そ"] },
      { label: "T", cells: ["た", "ち", "つ", "て", "と"] },
      { label: "N", cells: ["な", "に", "ぬ", "ね", "の"] },
      { label: "H", cells: ["は", "ひ", "ふ", "へ", "ほ"] },
      { label: "M", cells: ["ま", "み", "む", "め", "も"] },
      { label: "Y", cells: ["や", null, "ゆ", null, "よ"] },
      { label: "R", cells: ["ら", "り", "る", "れ", "ろ"] },
      { label: "W", cells: ["わ", "を", "ん", null, null] },
    ];
`;

let html = fs.readFileSync(studyHtml, "utf8");

const rawRe = /const HIRA_RAW = [\s\S]*?function parseHiraTsv/;
if (!rawRe.test(html)) throw new Error("HIRA_RAW block not found");
html = html.replace(rawRe, hiraRaw + "    function parseHiraTsv");

const chartRe = /const HIRA_CHART_ROWS = \[[\s\S]*?\];\s*\n/;
if (!chartRe.test(html)) throw new Error("HIRA_CHART_ROWS not found");
html = html.replace(chartRe, chartRows + "\n");

fs.writeFileSync(studyHtml, html, { encoding: "utf8" });
console.log("injected hiragana:", tsv.split("\n").length);
