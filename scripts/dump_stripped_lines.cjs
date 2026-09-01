const fs = require("fs");
const { studyHtml } = require("./paths.cjs");
const html = fs.readFileSync(studyHtml, "utf8");
const s = html.indexOf("<script>") + 8;
const e = html.indexOf("</script>", s);
const code = html.slice(s, e).replace(/`[^`]*`/gs, "`X`");
const lines = code.split("\n");
for (let i = 305; i <= 325; i++) {
  console.log(String(i).padStart(4), lines[i - 1]);
}
