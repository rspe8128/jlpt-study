const fs = require("fs");
const { studyHtml } = require("./paths.cjs");

let h = fs.readFileSync(studyHtml, "utf8");
h = h.replace(/aria-label="\uD559\uC2B5 [^"]+"/g, 'aria-label="\uD559\uC2B5 \uC885\uBAA9"');
h = h.replace(/<h2>\uC8FC\uAD00\uC2DD[^<]*<\/h2>/, "<h2>\uC8FC\uAD00\uC2DD \uC124\uC815</h2>");
h = h.replace(
  /<label for="writtenMean">[^<]*<\/label>/,
  '<label for="writtenMean">\uB73B (\uD55C\uAE00)</label>'
);
h = h.replace(
  /<label for="writtenRead">[^<]*<\/label>/,
  '<label for="writtenRead">\uC74C (\uD6C8\uB3C5)</label>'
);
h = h.replace(
  /(<div id="writtenSetup"[\s\S]*?<p style="margin:0 0 14px[^"]*">)[\s\S]*?(<\/p>\s*<div class="quiz-actions" style="margin-top:0;">)/,
  "$1\n        \uD55C\uC790\uAC00 \uBCF4\uC774\uBA74 <strong>\uB73B</strong>\uACFC <strong>\uC74C</strong> \uCE78\uC5D0 \uC785\uB825\uD55C \uB4A4 <strong>\uCC45\uC810</strong>\uD569\uB2C8\uB2E4.<br />\n        \uBB38\uC81C \uC21C\uC11C\uB294 \uC138\uD2B8\uB9C8\uB2E4 \uBB34\uC791\uC704\uC785\uB2C8\uB2E4. (\uC815\uB2F5\uC740 \uB73B\xb7\uC74C\uACFC \uBE44\uAD50\xb7\uC5EC\uB7EC \uB73B\xb7<code>|</code> \uD5C8\uC6A9)\n      $2"
);
h = h.replace(
  /aria-label="\uD50C\uB798\uC2DC\uCE74\uB4DC[^"]*"/g,
  'aria-label="\uD50C\uB798\uC2DC\uCE74\uB4DC, \uB204\uB7EC \uB4A4\uC9D1\uAE30"'
);
fs.writeFileSync(studyHtml, h, { encoding: "utf8" });
console.log("fffd", (h.match(/\uFFFD/g) || []).length);
