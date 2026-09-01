const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

let html = fs.readFileSync(studyHtml, "utf8");
const s = html.indexOf("<script>") + 8;
const e = html.indexOf("</script>", s);
let code = html.slice(s, e);

code = code.replace(
  /out\.push\("[^"]*보기[^"]*"\);/g,
  'out.push("뜻 (보기 부족)");'
);
code = code.replace(
  /val\.textContent = value == null \|\| value === "" \? "[^"]* : String\(value\);/,
  'val.textContent = value == null || value === "" ? "—" : String(value);'
);

html = html.slice(0, s) + code + html.slice(e);
fs.writeFileSync(studyHtml, html, { encoding: "utf8" });
console.log("patched");
