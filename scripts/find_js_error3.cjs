const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

const html = fs.readFileSync(studyHtml, "utf8");
const start = html.indexOf("<script>") + "<script>".length;
const end = html.indexOf("</script>", start);
let code = html.slice(start, end).replace(/`[^`]*`/gs, "`X`");

const lines = code.split("\n");
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (/^\s*<[a-zA-Z]/.test(line)) {
    console.log("HTML line", i + 1, line.trim().slice(0, 100));
  }
}

try {
  new Function(code);
  console.log("OK");
} catch (e) {
  console.log(e.message);
  // bisect lines
  let lo = 0,
    hi = lines.length;
  while (lo < hi - 1) {
    const mid = Math.floor((lo + hi) / 2);
    const chunk = lines.slice(0, mid).join("\n");
    try {
      new Function(chunk);
      lo = mid;
    } catch {
      hi = mid;
    }
  }
  console.log("error before line", hi, lines[hi - 1]?.slice(0, 150));
  console.log("prev", lines[hi - 2]?.slice(0, 150));
}
