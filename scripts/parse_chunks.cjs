const fs = require("fs");
const { studyHtml } = require("./paths.cjs");
const html = fs.readFileSync(studyHtml, "utf8");
const s = html.indexOf("<script>") + 8;
const e = html.indexOf("</script>", s);
const code = html.slice(s, e);
const lines = code.split("\n");

function tryLines(from, to) {
  const chunk = lines.slice(from - 1, to).join("\n");
  try {
    new Function(chunk);
    return "OK";
  } catch (err) {
    return err.message;
  }
}

// binary search line ranges
let lo = 1,
  hi = lines.length;
while (lo < hi - 1) {
  const mid = Math.floor((lo + hi) / 2);
  const r = tryLines(1, mid);
  if (r === "OK") lo = mid;
  else hi = mid;
}
console.log("first bad line", hi, tryLines(1, hi));
console.log("line content:", lines[hi - 1]?.slice(0, 200));
console.log("prev:", lines[hi - 2]?.slice(0, 200));

// try full
console.log("full:", tryLines(1, lines.length));
