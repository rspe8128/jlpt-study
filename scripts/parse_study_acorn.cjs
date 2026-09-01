const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

const html = fs.readFileSync(studyHtml, "utf8");
const s = html.indexOf("<script>") + 8;
const e = html.indexOf("</script>", s);
const code = html.slice(s, e);

try {
  require("acorn").parse(code, { ecmaVersion: 2022, sourceType: "script" });
  console.log("acorn: OK");
} catch (err) {
  console.log("acorn:", err.message);
  console.log("loc", err.loc);
  if (err.loc) {
    const lines = code.split("\n");
    const ln = err.loc.line;
    for (let i = ln - 2; i <= ln + 2 && i <= lines.length; i++) {
      if (i > 0) console.log(i, lines[i - 1].slice(0, 160));
    }
  }
}
