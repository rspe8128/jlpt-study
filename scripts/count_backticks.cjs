const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

const html = fs.readFileSync(studyHtml, "utf8");
const s = html.indexOf("<script>") + 8;
const e = html.indexOf("</script>", s);
const code = html.slice(s, e);
const BT = String.fromCharCode(96);
let count = 0;
for (let i = 0; i < code.length; i++) {
  if (code[i] === BT) {
    count++;
    const line = code.slice(0, i).split("\n").length;
    if (count <= 30 || count > count - 5) {
      console.log(count, "line", line, JSON.stringify(code.slice(i, i + 40)));
    }
  }
}
console.log("total", count);
