const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

const html = fs.readFileSync(studyHtml, "utf8");
const start = html.indexOf("<script>") + "<script>".length;
const end = html.indexOf("</script>", start);
const code = html.slice(start, end);

const anchors = [
  "function parseRaw",
  "const ALL = parseRaw",
  "const VOCAB_ALL",
  "const HIRA_ALL",
  "let filter = ",
  "const viewCards = ",
  "function refreshVocabSubtitle",
  "function renderVocabList",
  "function setMode",
];

for (const a of anchors) {
  const i = code.indexOf(a);
  if (i < 0) {
    console.log("missing", a);
    continue;
  }
  const tail = code.slice(i);
  try {
    new Function(tail);
    console.log("OK from", a);
  } catch (e) {
    console.log("FAIL from", a, "—", e.message);
  }
}

// strip all template literals for parse test
let stripped = code.replace(/`[^`]*`/gs, "`X`");
try {
  new Function(stripped);
  console.log("stripped templates: OK");
} catch (e) {
  console.log("stripped templates: FAIL", e.message);
  const m = e.message.match(/position (\d+)/);
  if (m) {
    const pos = +m[1];
    const line = stripped.slice(0, pos).split("\n").length;
    console.log("line", line, stripped.split("\n")[line - 1]?.slice(0, 120));
  }
}
