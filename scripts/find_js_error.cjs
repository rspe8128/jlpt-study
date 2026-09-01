const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

const html = fs.readFileSync(studyHtml, "utf8");
const start = html.indexOf("<script>") + "<script>".length;
const end = html.indexOf("</script>", start);
const code = html.slice(start, end);

// Binary search parse failure
function tryParse(slice) {
  try {
    new Function(slice);
    return true;
  } catch {
    return false;
  }
}

let lo = 0,
  hi = code.length;
while (lo < hi - 1) {
  const mid = (lo + hi) >> 1;
  if (tryParse(code.slice(0, mid))) lo = mid;
  else hi = mid;
}
const errPos = hi;
const line = code.slice(0, errPos).split("\n").length;
const col = errPos - code.lastIndexOf("\n", errPos - 1);
console.log("first error near byte", errPos, "line", line, "col", col);
console.log("--- context ---");
const lines = code.split("\n");
for (let i = line - 4; i <= line + 2 && i < lines.length; i++) {
  if (i >= 0) console.log(String(i + 1).padStart(5), lines[i].slice(0, 150));
}

// Find stray </ in JS outside strings (rough)
const backtickBlocks = [];
let i = 0;
while (i < code.length) {
  if (code[i] === "`") {
    const j = code.indexOf("`", i + 1);
    if (j === -1) {
      console.log("UNCLOSED backtick at", code.slice(0, i).split("\n").length);
      break;
    }
    backtickBlocks.push([i, j]);
    i = j + 1;
  } else i++;
}
console.log("backtick template blocks:", backtickBlocks.length);

// Check for </ in code between backtick blocks
let lastEnd = 0;
for (const [a, b] of backtickBlocks) {
  const between = code.slice(lastEnd, a);
  const hits = [...between.matchAll(/<\/?[a-zA-Z]/g)];
  if (hits.length) {
    const pos = lastEnd + hits[0].index;
    const ln = code.slice(0, pos).split("\n").length;
    console.log("HTML-like token between templates at line", ln, hits[0][0]);
  }
  lastEnd = b + 1;
}
